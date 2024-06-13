import os
from copy import copy, deepcopy
import uuid
import time
import jwt
from typing import List, Union, Optional
from dateutil import parser as dt_parser
import datetime as dt
import base64
from pydantic import BaseModel, ConfigDict
import json
import hashlib
import itertools
from enum import Enum
from typing import Dict, Any

from octostar.utils.workspace import read_file, upsert_entities, write_file
from octostar.utils.ontology import fetch_ontology_data
from octostar.utils.workspace.permissions import get_permissions, PermissionLevel
from octostar.client import AuthenticatedClient, check_required_env_vars

METADATA_FIELD_NAME = 'os_item_content'
RELATIONSHIP_ENTITY_NAME = 'os_workspace_relationship'
FILE_ENTITY_NAME = 'os_file'
GENERIC_RELATIONSHIP_NAME = 'related_to'
FILE_RELATIONSHIP_NAME = 'generator_of'
TAG_RELATIONSHIP_NAME = 'has_tag'
TAG_ENTITY_NAME = 'os_tag'

class NifiEntityModel(BaseModel):
    class RequestModel(BaseModel):
        class OntologyInfoModel(BaseModel):
            parents: List[str]
            relationships: List[str]
        jwt: str
        ontology_name: str
        ontology_info: OntologyInfoModel
        sync_params: dict = {}
        nifi_attributes: dict = {}
        config: dict = {}
        is_temporary: bool = False
        exception: dict = {}
        last_processor_name: Optional[str] = None
        fallback_os_workspace: Optional[str] = None
    class RecordModel(BaseModel):
        model_config = ConfigDict(extra='allow')
        entity_id: str
        os_entity_uid: str
        entity_type: str
        os_concept: str
        os_workspace: Optional[str] = None
        entity_label: Optional[str] = None
    request: RequestModel
    record: RecordModel
    metadata: dict = {}
    children: List[Union[str, 'NifiEntityModel']] = []
    contents: Optional[bytes] = None

class NifiEntityProxy(object):
    def __init__(self, context, uid, output_as_child, output_as_independent, proxy=None):
        self.context = context
        self.uid = uid
        self.output_as_child = output_as_child
        self.output_as_independent = output_as_independent
        self._proxy = proxy
    
    def __eq__(self, other):
        if isinstance(other, NifiEntity):
            return self.uid == other.record['entity_id']
        elif isinstance(other, NifiEntityProxy):
            return self.uid == other.uid
        else:
            return False
    
    def fetch_proxy(self):
        def _flatten_entities(entity):
            entities = []
            entities.append(entity)
            for child_entity in entity['children']:
                if not child_entity._proxy:
                    child_entity.fetch_proxy()
                entities.extend(_flatten_entities(child_entity._proxy))
            return entities
        if not self._proxy:
            main_entities = itertools.chain(*[b.entities for b in self.context.in_batches])
            main_entities = {e.record['entity_id']: e for e in main_entities}
            if main_entities.get(self.uid):
                self._proxy = main_entities.get(self.uid)
                return self._proxy
            else:
                all_entities = itertools.chain(*[_flatten_entities(entity) for entity in main_entities])
                if all_entities.get(self.uid):
                    self._proxy = all_entities.get(self.uid)
                    return self._proxy
                else:
                    ## TODO: Try to get the entity from the database with query_ontology()
                    raise AttributeError(f"Cannot find children with UUID {self.uid}! It may exist in the database (search not implemented yet!)")
    
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            if not self._proxy:
               self.fetch_proxy()
            return getattr(self._proxy, name)

    def __setattr__(self, name, value):
        if name in ('context', 'uid', 'output_as_child', 'output_as_independent', '_proxy'):
            super().__setattr__(name, value)
        else:
            if not self._proxy:
                self.fetch_proxy()
            setattr(self._proxy, name, value)

def as_nifi_fragments(fragments, fragmenter_keylist):
    count = len(fragments)
    identifier = str(uuid.uuid4())
    for i, entity in enumerate(fragments):
        pointer = entity.request['nifi_attributes']
        for k in fragmenter_keylist.split("."):
            if not pointer.get(k):
                pointer[k] = dict()
            pointer = pointer[k]
        pointer['fragment'] = {
            'identifier': identifier,
            'count': count,
            'index': i
        }
        if 'fragment' not in entity.request['config']:
            entity.request['config']['fragment'] = {}
        if 'fragments_stack' not in entity.request['config']['fragment']:
            entity.request['config']['fragment']['fragments_stack'] = []
        entity.request['config']['fragment']['fragments_stack'].insert(0, fragmenter_keylist)
        entity.request['nifi_attributes']['fragments_stack'] = entity.request['config']['fragment']['fragments_stack']
        pointer = entity.request['config']['fragment']
        for k in fragmenter_keylist.split("."):
            if not pointer.get(k):
                pointer[k] = dict()
            pointer = pointer[k]
        pointer['fragment'] = {
            'identifier': identifier,
            'count': count,
            'index': i
        }

def push_defragment_strategy(fragment, defragmenter_config):
    pointer = fragment.request['config']
    last_fragmenter_keylist = fragment.request['config']['fragment']['fragments_stack'][0]
    for k in ("fragment." + last_fragmenter_keylist).split("."):
        if not pointer.get(k):
            pointer[k] = {}
        pointer = pointer[k]
    pointer['merge_params'] = _update_dict(pointer.get('merge_params') or {}, defragmenter_config, lambda _, v2: v2)

class NifiEntityBatch(object):
    def __init__(self, entities, config, config_key):
        self.config = config
        self.entities = entities
        self.config_key = config_key

class NifiContextManager(object):
    class SyncFlag(Enum):
        UPSERT_ENTITY_ALL = 0
        UPSERT_ENTITY_SPECIFIC_FIELDS = 1
        UPSERT_ENTITY_METADATA = 2
        WRITE_CONTENTS = 10
        FETCH_RELATIONSHIPS = 20
    
    def __init__(self, json_data, lazy_sync=True):
        self.permissions = {}
        self.in_batches = None
        self.out_entities = None
        self.nonlazy_sync_ids = set()
        self.lazy_sync = lazy_sync
        self.client, self.ontology_name = self.get_client(json_data)
        self.ontology = fetch_ontology_data.sync(client=self.client)

    def _config_hash(config):
        def _make_hash(o):
            if isinstance(o, (set, tuple)):
                return hash(tuple([_make_hash(e) for e in sorted(o)]))
            elif isinstance(o, list):
                return hash(tuple([_make_hash(e) for e in o]))
            elif isinstance(o, dict):
                new_o = {k: _make_hash(v) for k, v in sorted(o.items())}
                return hash(tuple(frozenset(new_o.items())))
            else:
                return hash(o)
        dict_str = json.dumps(config, sort_keys=True, default=_make_hash)
        return hashlib.md5(dict_str.encode()).hexdigest()
    
    def _config_get(entity, keylist=None):
        config = entity.request['config']
        if not keylist:
            return config
        keylist = keylist.split(".")
        pointer = config
        for k in keylist:
            pointer = pointer.get(k)
            if not isinstance(pointer, (dict, list, tuple)):
                return {}
        if not isinstance(pointer, dict):
            return {}
        return pointer
    
    def get_client(self, json_data):
        all_entities = copy(json_data)
        all_jwts = [e['request'].get('jwt') for e in all_entities]
        all_jwts = [j for j in all_jwts if j]
        assert(len(set(all_jwts)) == 1) # jwt must be unique
        all_ontology_names = [e['request'].get('ontology_name') for e in all_entities]
        all_ontology_names = [j for j in all_ontology_names if j]
        assert(len(set(all_ontology_names)) == 1) # ontology name must be unique
        curr_user_jwt = all_jwts[0]
        curr_user_ontology = all_ontology_names[0]
        ancestor = os.environ.get("OS_ANCESTOR")
        current_pod_name = os.environ.get("OS_CURRENT_POD_NAME")
        if not ancestor and current_pod_name:
            ancestor = current_pod_name[:-6]
        if not ancestor:
            ancestor = "local-dev"
        check_required_env_vars(["OS_API_ENDPOINT"])
        client = AuthenticatedClient(
            fixed_token = curr_user_jwt,
            timeout = 90,
            base_url = os.environ.get("OS_API_ENDPOINT"),
            headers = {
                "x-ontology": curr_user_ontology,
                "x-app-name": os.environ.get("OS_APP_NAME", "unknown-local-app"),
                "x-ancestor": ancestor,
            },
            follow_redirects = True,
            verify_ssl = True,
            raise_on_unexpected_status = False,
        )
        return client, curr_user_ontology
    
    def receive_input(self, json_data, config_key=None) -> List["NifiEntity"]:
        def _safe_decode(contents):
            return base64.b64decode(contents) if contents else None
        entities = []
        all_independent_uids = [e['record']['entity_id'] for e in json_data]
        for elem in json_data:
            entities.append(NifiEntity(self,
                elem['request'],
                elem['record'],
                all_independent_uids,
                elem['metadata'],
                elem['children'],
                _safe_decode(elem.get('contents'))))
        entities = sorted(entities, key=lambda x: dt_parser.parse(x.record.get('os_last_updated_at') or dt.datetime.fromtimestamp(0, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
        entities = list({e.record['entity_id']: e for e in entities}.values())
        entities = [(NifiContextManager._config_hash(NifiContextManager._config_get(entity, config_key)), entity) for entity in entities]
        entities = sorted(entities, key=lambda x: x[0])
        grouped_entities = []
        for _, group in itertools.groupby(entities, key=lambda x: x[0]):
            group = [e[1] for e in group]
            grouped_entities.append(NifiEntityBatch(group, NifiContextManager._config_get(group[0], config_key), config_key))
        self.in_batches = grouped_entities
        return self.in_batches

    def __enter__(self):
        return self
    
    def get_workspaces_permissions(self, workspace_ids):
        permissions_to_fetch = list(set(workspace_ids).difference(set(list(self.permissions.keys()))))
        if permissions_to_fetch:
            permissions = get_permissions.sync(permissions_to_fetch, client=self.client)
            self.permissions.update(permissions)
        permissions = {}
        for k in workspace_ids:
            permissions[k] = self.permissions.get(k, PermissionLevel.NONE)
        return permissions
        
    def request_entity_sync(self, entity, parametrized_flags: Dict[SyncFlag, Any], merge_method=lambda _, v2: v2, now=False):
        entity.sync_params = _update_dict(entity.request.get('sync_params') or {}, parametrized_flags, merge_method)
        if now:
            self.nonlazy_sync_ids.add(entity.request['entity_id'])
    
    def send_output(self, entity_batches, processor_name):
        def _flatten_entities(entity):
            entities = []
            entity.request['last_processor_name'] = processor_name
            entities.append(entity)
            for child_entity in entity.children:
                if not child_entity.drop_on_output:
                    if child_entity.output_as_independent or child_entity.output_as_child:
                        child_entity.request['last_processor_name'] = processor_name
                    if child_entity.output_as_independent:
                        if not child_entity._proxy:
                            child_entity.fetch_proxy()
                        entities.extend(_flatten_entities(child_entity._proxy))
            return entities
        entities = itertools.chain(*[b.entities for b in entity_batches])
        all_entities = []
        for entity in entities:
            all_entities.extend(_flatten_entities(entity))
        all_entities = sorted(all_entities, key=lambda x: dt_parser.parse(x.record.get('os_last_updated_at') or dt.datetime.fromtimestamp(0, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
        self.out_entities = list({e.record['entity_id']: e for e in all_entities}.values())
        self.sync_entities()
        return self.out_entities
    
    def sync_entities(self):
        if not self.lazy_sync:
            entities = self.out_entities
        else:
            entities = [e for e in self.out_entities if e.record['entity_id'] in self.nonlazy_sync_ids]    
        if not entities:
            return
        reserved_fields = ['os_entity_uid', 'entity_id', 'entity_type', 'os_concept', 'entity_label', 'os_created_at', 'os_created_by', 'os_last_updated_at', 'os_last_updated_by']
        entities_to_upsert = []
        files_to_write = []
        fetch_relationships_entities = {}
        for entity in entities:
            fields = set()
            if entity.sync_params.get(NifiContextManager.SyncFlag.UPSERT_ENTITY_ALL) or entity.request['is_temporary']:
                fields = fields.union(set(list(entity.record.keys())))
            if entity.sync_params.get(NifiContextManager.SyncFlag.UPSERT_ENTITY_SPECIFIC_FIELDS):
                fields = fields.union(set(entity.sync_params.get(NifiContextManager.SyncFlag.UPSERT_ENTITY_SPECIFIC_FIELDS, {}).get('fields') or []))
            if entity.sync_params.get(NifiContextManager.SyncFlag.UPSERT_ENTITY_METADATA):
                fields.add(METADATA_FIELD_NAME)
            if fields:
                entities_to_upsert.append((
                    entity,
                    [f for f in list(fields) if f not in reserved_fields]
                ))
        for entity in entities:
            if entity.is_child_concept('os_file') and entity.sync_params.get(NifiContextManager.SyncFlag.WRITE_CONTENTS):
                files_to_write.append(entity)
        if entities_to_upsert:
            new_entities = upsert_entities.sync([entity.write_os_workspace for entity, _ in entities_to_upsert],
                [{
                    'entity_type': entity.record['os_concept'],
                    'os_entity_uid': entity.record['os_entity_uid'],
                    'fields': {k: entity.record.get(k) for k in fields}
                } for entity, fields in entities_to_upsert], client=self.client)
            new_entities = {e['os_entity_uid']: e for e in new_entities}
            for entity, _ in entities_to_upsert:
                ## HOTFIX
                entity.record = {**entity.record, **new_entities[entity.record['os_entity_uid']], 'os_item_content': entity.record['os_item_content']}
                entity.record['entity_id'] = entity.record['os_entity_uid']
                entity.record['entity_type'] = entity.record['os_concept']
                entity.record['entity_label'] = entity.label
                entity.request['is_temporary'] = False
        for file in files_to_write:
            new_file_record = write_file.sync(file.write_os_workspace,
                                              file.filepath, file.record['os_item_content_type'],
                                              file.contents, file.record['os_entity_uid'],
                                              client=self.client)
            ## HOTFIX
            file.record = {**file.record, **new_file_record, 'os_item_content': file.record['os_item_content']}
            file.record['entity_id'] = file.record['os_entity_uid']
            file.record['entity_type'] = file.record['os_concept']
            file.record['entity_label'] = file.label
            file.request['is_temporary'] = False
        for entity in entities:
            if entity.sync_params.get(NifiContextManager.SyncFlag.FETCH_RELATIONSHIPS):
                rels_to_fetch = entity.sync_params.get(NifiContextManager.SyncFlag.FETCH_RELATIONSHIPS)
                for rel in rels_to_fetch:
                    fetch_relationships_entities[rel] = fetch_relationships_entities.get(rel, []).append(entity)
        ## TODO: Add relationships based on the above fetch_relationships_entities
        for entity in entities:
            entity.sync_params = {}
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            return False
        if self.out_entities is None:
            raise AssertionError("Entities must be returned to the nifi context!")
    
    def jsonify(self, entities):
        def _recursive_collect_proxies(entities):
            children = []
            for entity in entities:
                children.extend(entity.children)
                children.extend(_recursive_collect_proxies(entity.children))
            return children
        all_proxies = _recursive_collect_proxies(entities)
        banned_entities = [e for e in all_proxies if not e.output_as_independent]
        entities = [e for e in entities if e not in banned_entities]
        return {
            'content': [e for e in [entity.to_json() for entity in entities] if e],
            'media_type': 'application/json'
        }
            
class NifiEntity(object):
    def __init__(self, context, request, record, all_independent_uids, metadata={}, children=[], contents=None):
        self.context = context
        self.request = request
        self.request['nifi_attributes'] = {}
        self.record = record
        if metadata:
            self.metadata = metadata
        assert(self.record.get('os_entity_uid') and self.record.get('entity_id'))
        assert(self.record.get('os_workspace') or self.request.get('fallback_os_workspace'))
        assert(self.record.get('os_concept') and self.record.get('entity_type'))
        if 'entity_label' not in self.record:
            self.record['entity_label'] = self.label
        children = [c for c in children if isinstance(c, (str, dict))]
        output_as_child = [not isinstance(c, str) for c in children]
        child_uids = [c if isinstance(c, str) else c['record']['entity_id'] for c in children]
        output_as_independent = [uid in all_independent_uids for uid in child_uids]
        child_proxies = [None if isinstance(c, str) else c for c in children]
        self.children = [NifiEntityProxy(
            self.context,
            child_uids[i],
            output_as_child[i],
            output_as_independent[i],
            child_proxies[i]) for i in range(len(children))]
        self._contents = contents
        self.drop_on_output = False
    def __eq__(self, other):
        if isinstance(other, NifiEntity):
            return self.record['entity_id'] == other.record['entity_id']
        elif isinstance(other, NifiEntityProxy):
            return self.record['entity_id'] == other.uid
        else:
            return False
    @property
    def sync_params(self):
        return {NifiContextManager.SyncFlag[k]: v for k, v in (self.request.get('sync_params') or {}).items()}
    @sync_params.setter
    def sync_params(self, new_params):
        self.request['sync_params'] = {(k.name if isinstance(k, NifiContextManager.SyncFlag) else k): v for k, v in new_params.items()}
    @property
    def metadata(self):
        return self.record.get(METADATA_FIELD_NAME) or {}
    @metadata.setter
    def metadata(self, new_metadata):
        self.record[METADATA_FIELD_NAME] = new_metadata       
    @property
    def contents(self):
        if not self._contents:
            self._contents = read_file.sync(self.record['os_workspace'], self.record['os_entity_uid'], False,
                                            client=self.context.client)
        return self._contents
    @contents.setter
    def contents(self, new_contents):
        self._contents = new_contents
    @property
    def relationships(self):
        return list(filter(lambda x: RELATIONSHIP_ENTITY_NAME == x['entity_type'], self.children))
    @property
    def write_os_workspace(self):
        permissions = self.context.get_workspaces_permissions([e for e in [self.record.get('os_workspace'), self.request.get('fallback_os_workspace')] if e])
        if self.record.get('os_workspace') and (permissions.get(self.record.get('os_workspace')) or PermissionLevel.NONE) >= PermissionLevel.WRITE:
            return self.record['os_workspace']
        elif self.request.get('fallback_os_workspace') and (permissions.get(self.request.get('fallback_os_workspace')) or PermissionLevel.NONE) >= PermissionLevel.WRITE:
            return self.request['fallback_os_workspace']
        else:
            return None
    @property
    def label(self):
        if not self.context.ontology:
            return None
        label_fields = self.context.ontology['concepts'][self.record.get('os_concept') or self.record.get('entity_type')]['labelKeys']
        label_fields = [field for field in label_fields if field]
        label = " ".join([(self.record.get(field) or "") for field in label_fields]).strip()
        if not label:
            label = None
        return label
    @property
    def filepath(self):
        return self.record.get('#path') or self.label
    @property
    def jwt_data(self):
        return jwt.decode(
            self.request['jwt'],
            algorithms=["ES256"],
            options={'verify_signature': False}
        )
    def update_last_timestamp(self):
        self.record['os_last_updated_at'] = dt.datetime.fromtimestamp(time.time(), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.context.request_entity_sync(self, {
            NifiContextManager.SyncFlag.UPSERT_ENTITY_SPECIFIC_FIELDS: {'fields': ['os_last_updated_at']}
        }, merge_method=lambda v1, v2: (v1 or []) + v2)
    def is_child_concept(self, type):
        return self.record['entity_type'] == type or type in self.request['ontology_info']['parents']
    def to_json(self):
        def _safe_encode(contents):
            return base64.b64encode(contents) if contents else None
        if self.drop_on_output:
            return
        children = []
        [c.fetch_proxy() for c in self.children if (c.output_as_child or c.output_as_independent) and not c.drop_on_output]
        children = [c for c in self.children if not c.drop_on_output]
        children = [(c.uid if not c.output_as_child else c.to_json()) for c in children]
        children = [c for c in children if c]
        virtual_children = list(set([c for c in children if isinstance(c, str)]))
        physical_children = sorted([c for c in children if not isinstance(c, str)], key=lambda x: dt_parser.parse(x.record.get('os_last_updated_at') or dt.datetime.fromtimestamp(0, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
        physical_children = list({c.uid: c for c in physical_children}.values())
        children = physical_children + virtual_children
        if not self.metadata:
            self.metadata = None
        return {
            'request': self.request,
            'record': self.record,
            'metadata': self.metadata,
            'children': children,
            'contents': _safe_encode(self._contents)
        }
    def _add_entity(self, os_workspace, entity_type, fields):
        now_time = dt.datetime.fromtimestamp(time.time(), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        random_id = str(uuid.uuid4())
        username = self.jwt_data['username']
        child_request = {
            'jwt': self.request['jwt'],
            'ontology_name': self.request['ontology_name'],
            'ontology_info': {
                'parents': self.context.ontology['concepts'][entity_type]['parents'],
                'relationships': self.context.ontology['concepts'][entity_type]['relationships']
            },
            'sync_params': {},
            'nifi_attributes': {},
            'config': deepcopy(self.request['config']),
            'fallback_os_workspace': self.request['fallback_os_workspace'],
            'is_temporary': True
        }
        child_entity = NifiEntity(self.context, child_request, {
            **fields,
            'os_workspace': os_workspace,
            'os_concept': entity_type,
            'entity_type': entity_type,
            'os_entity_uid': random_id,
            'entity_id': random_id,
            'os_created_at': now_time,
            'os_created_by': username,
            'os_last_updated_at': now_time,
            'os_last_updated_by': username
        }, [])
        child_entity.record['entity_label'] = child_entity.label
        child_entity_proxy = NifiEntityProxy(self.context, child_entity.record['entity_id'], True, False, child_entity)
        self.children.append(child_entity_proxy)
        return child_entity_proxy
    def add_relationship(self, os_entity_uid_from, entity_type_from, os_entity_uid_to, entity_type_to,
                         os_relationship_name, os_relationship_workspace, relationship_fields):
        return self._add_entity(
            os_relationship_workspace, RELATIONSHIP_ENTITY_NAME,
            {
                **relationship_fields,
                'os_entity_uid_from': os_entity_uid_from,
                'os_entity_type_from': entity_type_from,
                'os_entity_uid_to': os_entity_uid_to,
                'os_entity_type_to': entity_type_to,
                'os_relationship_name': os_relationship_name,
            }
        )
    def add_child_entity(self, os_workspace, entity_type, fields, os_relationship_name=GENERIC_RELATIONSHIP_NAME):
        child_entity = self._add_entity(os_workspace, entity_type, fields)
        child_rel = self.add_relationship(self.record['os_entity_uid'], self.record['os_concept'],
                              child_entity.record['os_entity_uid'], child_entity.record['os_concept'],
                              os_relationship_name, os_workspace, {})
        return child_entity, child_rel
    def add_child_file(self, os_workspace, full_filename, filetype, file, os_relationship_name=FILE_RELATIONSHIP_NAME):
        child_entity, child_rel = self.add_child_entity(os_workspace, FILE_ENTITY_NAME,
            {
                'os_item_name': full_filename.rsplit("/", 1)[-1],
                'os_item_content_type': filetype,
                '#path': full_filename,
            }, os_relationship_name
        )
        child_entity._contents = file
        return child_entity, child_rel
    def add_tag(self, os_workspace, name, group, order, color):
        return self.add_child_entity(
            os_workspace, 'os_tag',
            {
                'name': name,
                'group': group,
                'order': order,
                'color': color
            }, TAG_RELATIONSHIP_NAME
        )
    def add_metadata(self, json, recurse: Union[bool, int]=False, merge_method=lambda _, v2: v2):
        self.metadata = _update_dict(self.metadata, json, merge_method, recurse)
        self.context.request_entity_sync(self, {NifiContextManager.SyncFlag.UPSERT_ENTITY_METADATA: True})
    def propagate_metadata(self, to_entity, fields=None, merge_method=lambda _, v2: v2):
        metadata_to_propagate = deepcopy(self.metadata)
        if fields:
            metadata_to_propagate = {k:v for k, v in self.metadata if k in fields}
        to_entity.metadata = _update_dict(to_entity.metadata, metadata_to_propagate, merge_method)
        to_entity.context.request_entity_sync(self, {NifiContextManager.SyncFlag.UPSERT_ENTITY_METADATA: True})

def more_recent_than(record_a, record_b):
    date_a = dt_parser.parse(record_a.get('os_last_updated_at') or dt.datetime.fromtimestamp(0, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    date_b = dt_parser.parse(record_b.get('os_last_updated_at') or dt.datetime.fromtimestamp(0, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    return date_a >= date_b

def _update_dict(d1, d2, op, recurse=True):
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        return op(d1, d2)
    for k2, v2 in d2.items():
        if isinstance(v2, dict):
            v1 = d1.get(k2, {})
            if isinstance(v1, dict):
                if recurse:
                    if isinstance(recurse, int):
                        recurse -= 1
                    d1[k2] = _update_dict(v1, v2, op, recurse)
                else:
                    d1[k2] = op(v1, v2)
            else:
                if k2 in d1:
                    d1[k2] = op(v1, v2)
                else:
                    d1[k2] = v2
        else:
            if k2 in d1:
                d1[k2] = op(d1[k2], v2)
            else:
                d1[k2] = v2
    return d1