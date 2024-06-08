#-----------------------------
# -- Xango --
#-----------------------------

import copy 
from typing import Any, List
from arango import ArangoClient
from arango.collection import StandardCollection
from arango.exceptions import ArangoError, DocumentUpdateError, DocumentRevisionError
from contextlib import contextmanager
from . import lib, lib_xql, dict_mutator, dict_query, lib_dict

# Protected (one underscore _*) and Private (two underscores __*)
SPECIAL_KEYS = ["_id", "_key", "_rev", "_from", "_to", "__ttl", "__collection", "__properties", "_created_at", "_modified_at", "__subcollections"]

DEFAULT_INDEXES = [
    {
        "type": "persistent",
        "fields": ["_created_at"],
        "name": "idx00__created_at"
    },
    
    {
        "type": "persistent",
        "fields": ["_modified_at"],
        "name": "idx00__modified_at"
    },
    {
        "type": "persistent",
        "fields": ["__collection"],
        "name": "idx00__collection"
    },
    {
        "type": "ttl",
        "fields": ["__ttl"],
        "name": "idx00__ttl",
        "expireAfter": 0
    }
]

DEFAULT_EDGE_INDEXES = [
    {
        "type": "persistent",
        "fields": ["_created_at"],
        "name": "idx00__created_at"
    },
    {
        "type": "persistent",
        "fields": ["_modified_at"],
        "name": "idx00__modified_at"
    },
    {
        "type": "persistent",
        "fields": ["_kind"],
        "name": "idx00__kind"
    },
    {
        "type": "persistent",
        "fields": ["_rbac"],
        "name": "idx00__rbac"
    }
]

#------------------------------------------------------------------------------
# Exception
class XangoError(Exception): pass
class AdapterError(XangoError): pass
class CollectionNotFoundError(XangoError): pass
class CollectionExistsError(XangoError): pass
class ItemNotFoundError(XangoError):pass
class ItemExistsError(XangoError):pass
class NoResultsError(XangoError): pass
class ConstraintError(XangoError): pass
class UndeletableError(XangoError): pass
class MissingCommitterCallbackError(XangoError): pass
class MissingItemKeyError(XangoError): pass
class InvalidItemPathError(XangoError): pass 

#------------------------------------------------------------------------------

class ActiveCollectionItem(object):
    """
    ActiveCollectionItem

    An abstraction class to use as an active record on the items

    Usage:

      class User(ActiveCollectionItem):
        def full_name(self):
            return "%s %s" % (self.get("first_name), self.get("last_name"))
            
      coll = #db.select_collection(..., item_class=User)

      if item := coll.get(_key):
        print(item.full_name())

    """
    _item = None

    def __init__(self, _item, *a, **kw):
        self._item = _item


    def __call__(self, _item=None, *a, **kw):
        i = copy.deepcopy(self)
        i._item = _item
        return i

    def __getattr__(self, __name: str, *a, **kw):
      return self._item.__getattribute__(__name, *a, **kw)

#------------------------------------------------------------------------------

class _QueryResultIterator(object):
    results:list = []
    pagination:dict = {}
    cursor:list = []
    count:int = 0
    size:int = 0

    def __init__(self, cursor, pager, data_mapper=None):
        self.cursor = cursor
        stats = cursor.statistics()
        self.count = self.cursor.count() # current count
        self.size = stats["fullCount"] # total count
        self.pagination = lib.gen_pagination(
                                            size=self.size,
                                            count=self.count,
                                            page=pager[0],
                                            per_page=pager[1])

        def _default_data_mapper_cb(item): return item 
    
        _data_mapper = _default_data_mapper_cb if not data_mapper else data_mapper

        self.results = [_data_mapper(item) for item in self.cursor]

    def __iter__(self):
        """
        Iterate over the results
        """
        yield from self.results

    def __len__(self):
        """
        Get the total results 
        """
        return self.size

class _ItemMixin(dict):
    """
    !ALL THE METHODS MODIFIERS ARE DEPRECTATED AS OF JAN 21 2024
    ! ONLY USER $update() for 
    """
    NAMESPACE = None
 
    def _make_path(self, path):
        # if self.NAMESPACE:
        #     return "%s.%s" % (self.NAMESPACE, path)
        return path

    def _update(self, data):
        raise NotImplementedError()

    def update(self, data: dict) -> "Self":
        """
        UPDATE: Update the active CollectionItem

        Returns:
            CollectionItem

        Example:
            #item.update({k/v...})
            #item.commit()

            or 
            #item.update({k/v...}).commit()
        """
        self._update(data)
        return self


    #! BELOW DEPRECATED

    def get(self, path: str, default: Any = None) -> Any:
        """
        GET: Return a property by key/DotNotation

        ie: 
            #get("key.deep1.deep2.deep3")

        Params:
            path:str - the dotnotation path
            default:Any - default value 

        Returns:
            Any
        """
        path = self._make_path(path)
        return lib.dict_get(obj=dict(self), path=path, default=default)

    def set(self, path: str, value: Any):
        """
        SET: Set a property by key/DotNotation

        Params:
            path:str - the dotnotation path
            value:Any - The value

        Returns:
            Void
        """

        path = self._make_path(path)
        self._update({path: value})
        return self

    def len(self, path: str):
        """
        Get the length of the items in a str/list/dict
        Params:
            path:str - the dotnotation path
        Returns:
            data that was removed
        """
        path = self._make_path(path)
        v = self.get(path)
        return len(v) if v else 0

    def incr(self, path: str, incr=1):
        """
        INCR: increment a value by 1
        Args
            path:str - path
            incr:1 - value to inc by
        Returns:    
            int - the value that was incremented
        """
        op = "%s:$incr" % self._make_path(path)        
        oplog = self._update({op: incr})
        return oplog.get(op)

    def decr(self, path: str, decr=1):
        """
        DECR: decrement a value by 1
        Args
            path:str - path
            decr:1 - value to dec by
        Returns:    
            int - the value that was decremented
        """
        op = "%s:$decr" % self._make_path(path)

        oplog = self._update({op: decr})
        return oplog.get(op)

    def unset(self, path: str):
        """ 
        UNSET: Remove a property by key/DotNotation and return the value

        Params:
            path:str

        Returns:
            Any: the value that was removed
        """
        path = self._make_path(path)
        self._update({"%s:$unset" % path: True})

    def rename(self, path: str, value:str):
        """ 
        RENAME: Rename a property by key/DotNotation and return the value

        Params:
            path:str - The source
            value:str - the target value

        Returns:
            Any: the value that was removed
        """
        path = self._make_path(path)
        self._update({"%s:$rename" % path: value})

    def copy(self, path: str, value:str):
        """ 
        COPY: Copy a property by key/DotNotation and return the value

        Params:
            path:str - The source
            value:str - the target value
        """
        path = self._make_path(path)
        self._update({"%s:$copy" % path: value})

    def xadd(self, path: str, values):
        """
        XADD: Add *values if they don't exist yet

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xadd" % self._make_path(path)
        self._update({op: values})

    def xadd_many(self, path: str, *values: List[Any]):
        """
        XADD: Add *values if they don't exist yet

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xadd_many" % self._make_path(path)
        self._update({op: values})

    def xrem(self, path: str, values):
        """
        XREM: Remove items from a list

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xrem" % self._make_path(path)
        oplog = self._update({op: values})
        return oplog.get(op)

    def xrem_many(self, path: str, *values: List[Any]):
        """
        XREM: Remove items from a list

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xrem_many" % self._make_path(path)
        oplog = self._update({op: values})
        return oplog.get(op)

    def xpush(self, path: str, values: Any):
        """
        XPUSH: push item to the right of list. 

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xpush" % self._make_path(path)
        self._update({op: values})

    def xpush_many(self, path: str, *values: List[Any]):
        """
        XPUSH_MANY: push item to the right of list. 

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xpush_many" % self._make_path(path)
        self._update({op: values})

    def xpushl(self, path: str, values: Any):
        """
        XPUSHL: push item to the right of list. 

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xpushl" % self._make_path(path)
        self._update({op: values})

    def xpushl_many(self, path: str, *values: List[Any]):
        """
        LPUSH: push item to the right of list. 

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xpush_many" % self._make_path(path)
        self._update({op: values})

    def xpop(self, path: str):
        """
        Remove value at the end an array/list
        Params:
            path:str - the dotnotation path
        Returns:
            data that was removed

        """
        op = "%s:$xpop" % self._make_path(path)
        oplog = self._update({op: True})
        return oplog.get(op)

    def xpopl(self, path: str):
        """
        Remove value at the beginning an array/list
        Params:
            path:str - the dotnotation path
        Returns:
            data that was removed        
        """
        op = "%s:$xpopl" % self._make_path(path)
        oplog = self._update({op: True})
        return oplog.get(op)

    def timestamp(self, path:str, value:Any=True):
        op = "%s:$datetime" % self._make_path(path)
        oplog = self._update({op: value})
        return oplog.get(op)   

    def template(self, path:str, value:str):
        op = "%s:$template" % self._make_path(path)
        oplog = self._update({op: value})
        return oplog.get(op)

    def uuid4(self, path:str):
        op = "%s:$uuid4" % self._make_path(path)
        oplog = self._update({op: True})
        return oplog.get(op)



class CollectionItem(_ItemMixin):
    """
    CollectionItem

    Every row is a document 
    """

    # item _key
    _key = None

    # item _id 
    _id = None 

    # items subcollections
    _subcollections = {}
    
    # immutable keys
    _immut_keys = []

    # _read_only. When read_only, it can update 
    _read_only = False

    # A flag to indicate to use replace when updating
    _commit_replace = False

    @classmethod
    def new(cls, data:dict, immut_keys:list=[], db=None, collection=None, commiter=None, custom_ops:dict={}, read_only:bool=False):
        data = _create_document_item(data)
        data, _, __ = dict_mutator.mutate(mutations=data,  immuts=immut_keys, custom_ops=custom_ops)
        return cls(data=data, db=db, collection=collection, immut_keys=immut_keys, commiter=commiter, custom_ops=custom_ops, read_only=read_only)

    def __init__(self, data: dict, db=None, collection=None, immut_keys:list=[], load_parser=None, commiter=None, custom_ops:dict={}, read_only:bool=False):
        
        if "_key" not in data:
            raise MissingItemKeyError()
        
        self._db = db
        self._collection = collection
        self._load_parser = load_parser
        self._commiter = commiter
        self._immut_keys = immut_keys
        self._cx = False
        self._custom_ops = custom_ops
        self._read_only = read_only
          
        self._load(data)

    def to_dict(self):
        data = dict(self)
        if self._subcollections:
            data["__subcollections"] = self._subcollections
        return copy.deepcopy(data)

    def set_immut_keys(self, immut_keys:list=[]):
        self._immut_keys = immut_keys

    @contextmanager
    def context(self):
        """
        *ContextManager for CollectionItem

        Do transactional mutation and commit the changes upon exit

        Yield:
            CollectionItem

        Example:
            with item.context() as ctx:
                ctx.update({"name": "Y"})

        """
        yield self 
        self.commit()

    @contextmanager
    def context_subcollection(self, name: str, constraints: list = None):
        """
        *Context Manager for Subcollection

        Do transactional mutation on subcollection and commit the changes upon exit

        Yield:
          SubCollection

        Example:

        with item.context_subcollection('name') as sc:
            sc.insert()
        
        """
        sc = SubCollection(item=self, name=name, custom_ops=self._custom_ops, constraints=constraints)
        yield sc
        self.commit()

    def select_subcollection(self, name: str, constraints: list = None):
        """

        Select a subcollection. When making changes, must use `commit` on parent

        Retuns:
          SubCollection

        Example:
            sc = item.select_subcollection(name)
            sc.insert({...})
            sc.insert({...})
            item.commit()

            -- or with #context
            with item.context() as ictx:
                sc = item.select_subcollection(name)
                sc.insert({...})
                sc.insert({...})
            
            or refer to #context_subscollection

        """
        return SubCollection(item=self, name=name, custom_ops=self._custom_ops, constraints=constraints)

    def get_item(self, path:str) -> "_SubCollectionItem":
        """
        To get a subcollection item via path

        Path: [SUB_COLLECTION_NAME/DOCUMENT_KEY] -> articles/1234568

        Params:
            path:str - str of [sub_collection_name/document_key]
        Return:
            collection.item

        Example:
            db.get_item("collection/_key").get_item("sub_collection/_key")
        
        Returns:
            _SubCollectionItem

        """
        
        paths = path.split("/")
        if len(paths) != 2:
            raise InvalidItemPathError()

        return self.select_subcollection(paths[0]).get(paths[1])        

    @property
    def subcollections(self) -> list:
        """ List all collections """
        return list(self._subcollections.keys())

    def drop_subcollection(self, name: str):
        try:
            if name in self._subcollections:
                del self._subcollections[name]
        except KeyError as _:
            pass
        return True

    def _set_subcollection(self, name:str, data:Any):
        self._subcollections[name] = data

    def commit(self) -> "Self":
        """ To save """

        if self._read_only:
            return self
        
        if not self._commiter:
            raise MissingCommitterCallbackError()
        
        if data := self._commiter(item=self, replace_document=self._commit_replace):
            self._commit_replace = False
            self._load(data)
        return self
        
    def _update(self, mutations: dict):
        """
        Return oplog
        """
        
        if self._read_only:
            return self
        
        data = copy.deepcopy(dict(self))
        doc, oplog, _commit_replace = dict_mutator.mutate(mutations=mutations, init_data=data, immuts=self._immut_keys, custom_ops=self._custom_ops)
        if _commit_replace:
            self._commit_replace = True
        self._load(doc)
        return oplog

    def _load(self, item: dict):
        """
        load the content into the document

        Params:
            row: dict
        """
        self._clear_self()
        
        if self._load_parser:
          item = self._load_parser(item)

        #self._subcollections = {}
        if "__subcollections" in item:
            self._subcollections = item.pop("__subcollections") or {}

        if "_key" in item:
            self._key = item.get("_key")

        if "_id" not in item:
            self._id = "%s/%s" % (self._collection.name, item.get("_key"))
        else:
            self._id = item.get("_id")

        super().__init__(item)

    def _clear_self(self):
        """ clearout all properties """
        for _ in list(self.keys()):
            if _ in self:
                del self[_]

    def set_ttl(self, nattime:str) -> "Self":
        """
        To set a time to live on an item
        ie: 
            item.set_ttl("2days")

            to reset the ttl
                item.set_ttl(False)

        Params:
            - nattime:str - Natural time - ie 1hour, 60seconds

        Returns:
            self
        """
        if isinstance(nattime, str):
            self.update({"__ttl:$datetime": nattime})
        elif nattime is False:
            self.update({"__ttl": None})
        return self

    def delete(self) -> bool:
        """
        To delete an item
        Todo: deleted links/edges
        """
        self._collection.delete(self._key)
        return True

    def use_graph_edge(self, name: str, use_prefix=True):
        """
            item:CollectionItem
            ge = item.use_edge_collection()
            ge.link(other_item, kind="users:orgs")
            ge.traverse(traversals=[ge.traversals()])
        """
        if isinstance(name, GraphEdgeCollection):
            name = name.collection_name
            use_prefix = False 

        return GraphEdgeCollectionItem(name=name, item=self, use_prefix=use_prefix)

    def get_sizeof(self) -> int:
        """
        !@deprecated
        @use get_document_size
        """
        return self.get_document_size()

    def get_document_size(self, include_subcollections=False) -> int:
        """
        Get the size of the document

        Params:
            include_subscollections:bool - To also include the subcollections

        Returns: int
        """
        d = self.to_dict() if include_subcollections else dict(self)
        return lib.get_sizeof(d)

    def get_document_keys_depth(self, include_subcollections=False) -> int:
        """
        Get max max nested depth (max nested level)

        Params:
            include_subscollections:bool - To also include the subcollections

        Returns: int
        """
        d = self.to_dict() if include_subcollections else dict(self)
        return lib_dict.get_keys_depth(d)

    def get_document_keys_count(self, deep=False, include_subcollections=False) -> int:
        """
        Get the total of keys in a document

        Params:
            deep: bool - By default it will get the 1st level of keys
            include_subscollections:bool - To also include the subcollections
        Returns: int
        """

        d = self.to_dict() if include_subcollections else dict(self)
        return lib_dict.get_keys_count(d, deep=deep)
 
class _SubCollectionItem(_ItemMixin):
    _key = None 

    def __init__(self, subCollection: "SubCollection", data):
        self._subcollection = subCollection
        self._load(data)

    @property
    def parent(self):
        """
        Holds parent data
        """
        return self._subcollection._item

    def to_dict(self):
        data = dict(self)
        return copy.deepcopy(data)
    
    def _update(self, mutations):
        data = self.to_dict()
        doc, oplog, _commit_replace = dict_mutator.mutate(mutations=mutations, init_data=data, immuts=self.parent._immut_keys, custom_ops=self._subcollection._custom_ops)
        self._subcollection._save(self._key, doc)
        self._load(doc)
        return oplog

    def _load(self, data):
        self._key = data.get("_key")
        super().__init__(data)

    def delete(self):
        self._subcollection.delete({"_key": self._key})
        return True

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

class Database(object):
    """
    Xango Database
    """
    SYSTEM_DB = "_system"

    def __init__(self,
                 hosts:str=None,
                 username:str="root",
                 password:str=None, 
                 dbname: str = SYSTEM_DB, 
                 client:"Database"= None, 
                 default_indexes:list=[],
                 query_max_limit=100,
                 collection_prefix:str=None,
                 custom_ops:dict={}):
        """
        
        Params:
            host:str|list
            username:str
            password
            dbname
            client:Database
            default_indexes:list
            query_max_limit
            collection_prefix:str|function - a prefix to add in all collection name
            custom_ops:dict - 
        
        """

        self.client = client
        self.username = username
        self.password = password
        self.db = None
        self.dbname = dbname or self.SYSTEM_DB # fallback to _system_db
        self.default_indexes = default_indexes
        self.query_max_limit = query_max_limit
        self._custom_ops = custom_ops
        self._collection_prefix = collection_prefix

        if not self.client:
            self.client = ArangoClient(hosts=hosts, serializer=lib.json_ext.dumps, deserializer=lib.json_ext.loads)

        if self.dbname:
            self.db = self.client.db(name=self.dbname, username=self.username, password=self.password)



    @property
    def aql(self):
        return self.db.aql

    def prefix_collection_name(self, collection_name:str) -> str:
        if self._collection_prefix:
            if isinstance(self._collection_prefix, str):
                collection_name = "%s%s" % (self._collection_prefix, collection_name)
            elif callable(self._collection_prefix):
                collection_name = self._collection_prefix(collection_name)
        return collection_name

    def unprefix_collection_name(self, collection_name:str) -> str:
        if self._collection_prefix:
            return collection_name.replace(self._collection_prefix, "")
        return collection_name
        
    def has_db(self, dbname:str=None) -> bool:
        """
        Check if the system has a database

        Params:
            dbname:str|None - The dbname to check or the current self.dbname

        Returns: 
            bool
        """
        _dbname = dbname or self.dbname
        sys_db = self.select_db("_system")
        return sys_db.db.has_database(_dbname)

    def create_db(self, dbname:str=None) -> "Database":
        """
        Create a database if doesn't exists
        Params:
            dbname:str|None - The dbname to check or the current self.dbname

        Returns:
            Database
        """
        _dbname = dbname or self.dbname
        sys_db = self.select_db("_system")
        if not sys_db.db.has_database(_dbname):
            sys_db.db.create_database(_dbname)
        return self.select_db(_dbname)

    def delete_db(self, dbname:str) -> bool:
        """
        To delete a database 

        """
        sys_db = self.select_db("_system")
        if sys_db.db.has_database(dbname):
            return sys_db.db.delete_database(name=dbname, ignore_missing=True)
        return False

    def select_db(self, dbname:str, collection_prefix:str=None, default_indexes:dict=None) -> "Database":
        """
        Select a different DB using the same connection

        Params:
            dbname:str - The dbname to check
            collection_prefix
            default_indexes
        Returns: 
            Database
        """
        return Database(client=self.client, 
                        dbname=dbname, 
                        username=self.username, 
                        password=self.password, 
                        collection_prefix=collection_prefix or self._collection_prefix, 
                        custom_ops=self._custom_ops, 
                        default_indexes=default_indexes or self.default_indexes,
                        query_max_limit=self.query_max_limit)

    def has_collection(self, collection_name, use_prefix=True) -> bool:
        """
        Test if collection exists in the current db. 

        Params:
            collection_name:str - the collection name 

        Returns:
            bool
        """
        if use_prefix:
            collection_name = self.prefix_collection_name(collection_name)
        return self.db.has_collection(collection_name)

    def create_collection(self, collection_name:str, indexes:list=[], use_prefix=True) -> bool:
        """
        Create a collection if not exists
        Returns: bool
        """
        if not self.has_collection(collection_name):
            if use_prefix:
                collection_name = self.prefix_collection_name(collection_name)
            col = self.db.create_collection(collection_name)

            # indexes
            if _indexes := {l.get("name"):l for l in [*DEFAULT_INDEXES, *(self.default_indexes or []), *(indexes or [])]}.values():
                for index in _indexes:
                    col._add_index(index) 
                    
            return True 
        return False

    def select_collection(self, collection_name:str, indexes:list=[], immut_keys:list=[], item_class=None, auto_create:bool=True, use_prefix=True) -> "Collection":
        """
        To select a collection

        Params:
            collection_name:str - collectioin name 
            indexes:List[dict] - the indexes to use
            immut_keys:list - immutable keys. Keys that can't be updated once created
            auto_create:bool - To auto create the collection if doesn't exist
            use_prefix:bool - To use the prefix or not
        Return: Collection

        """

        if self.has_collection(collection_name):
            if use_prefix:
                collection_name = self.prefix_collection_name(collection_name)
            col = self.db.collection(collection_name)
        elif auto_create is True:
            self.create_collection(collection_name=collection_name, indexes=indexes)
            if use_prefix:
                collection_name = self.prefix_collection_name(collection_name)
            col = self.db.collection(collection_name)
        else:
            raise CollectionNotFoundError()

        return Collection(db=self, collection=col, immut_keys=immut_keys, custom_ops=self._custom_ops, item_class=item_class)

    def select_edge_collection(self, edge_collection:str, use_prefix=True, indexes:list=[]):
        collection_name = edge_collection
        if self.db.has_collection(collection_name):
            if use_prefix:
                collection_name = self.prefix_collection_name(collection_name)
            return self.db.collection(collection_name)
        else:
            if use_prefix:
                collection_name = self.prefix_collection_name(collection_name)
            col = self.db.create_collection(name=collection_name, edge=True)

            # indexes
            if _indexes := {l.get("name"):l for l in [*DEFAULT_EDGE_INDEXES, *(self.default_indexes or []), *(indexes or [])]}.values():
                for index in _indexes:
                    col._add_index(index) 

            return col

    def get_item(self, path:str) -> CollectionItem:
        """
        To get an item via path.

        - Item Path: [COLLECTION_NAME/KEY] -> articles/1234568
        - Item's Subcollection path: [COLLECTION/_KEY/SUBCOLLECTION] -> articles/1234/comments
        - Item's Subcollection sub Item path: [COLLECTION/_KEY/SUBCOLLECTION/_SUB_KEY] -> articles/1234/comments/73992

        Params:
            path:str - str of [collection_name/document_key]
        Return:
            collection.item

        Example:
            db.get_item("articles/somethingf")
        
        Returns:
            CollectionItem

        """

        paths = path.split("/")
        len_paths = len(paths)
        if len_paths < 2 or len_paths > 4:
            raise InvalidItemPathError()

        try:
            if len_paths == 2: # item -> [coll/key]
                return self.select_collection(self.prefix_collection_name(paths[0])).get(paths[1])
            elif len_paths == 3: # item's subcolelction -> [coll/key/subcoll]
                return self.select_collection(self.prefix_collection_name(paths[0])).get(paths[1]).select_subcollection(paths[2])
            elif len_paths == 4: # item's subcollection items -> [coll/key/subcoll/subkey]
                return self.select_collection(self.prefix_collection_name(paths[0]))\
                    .get(paths[1])\
                    .select_subcollection(paths[2])\
                    .get(paths[3])
        except Exception as e:
            return None

    def execute_aql(self, query:str, bind_vars:dict={}, *a, **kw):
        """ 
        Execute AQL 
        Params:
            query:str - the AQL to execute 
            bind_vars: dict - the variables to pass in the query
        Return aql cursor
        """
        return self.aql.execute(query=query, bind_vars=bind_vars, *a, **kw)

    def query(self, xql:lib_xql.XQLDEFINITION, data:dict={}, parser=None, data_mapper=None) -> _QueryResultIterator:
        """
        XQL query  a collection based on filters

        It will return the cursor:ArangoCursor and a pagination for the current state
        
        Params:
            xql:lib_xql.XQLDEFINITION
            data:dict
            data_mapper:function - a callback function
        Returns
            _QueryResultIterator
        """

        aql, bind_vars, pager = self.build_query(xql=xql, data=data, parser=parser)
        cursor = self.execute_aql(aql, bind_vars=bind_vars, count=True, full_count=True)            
        return _QueryResultIterator(cursor=cursor, pager=pager, data_mapper=data_mapper)

    def build_query(self, xql:lib_xql.XQLDEFINITION, data:dict={}, parser=None):
        """
        Build a query from XQL

        Return tuple:
            - aql:str
            - bind_vars:dict
            - pagination:tuple 
                -> tuple(page, per_page)
        """        
        xql = lib_xql.prepare_xql(xql)

        # pagination
        if "page" in data:
            xql["PAGE"] = data.get("page") or 1
            del data["page"]
        if "limit" in data:
            xql["LIMIT"] = data.get("limit") or 100
            del data["limit"]

        max_limit = xql.get("LIMIT") or self.query_max_limit

        _per_page, _, _page = lib_xql.xql_take_skip_page(xql=xql, max_limit=max_limit)
        aql, bind_vars = lib_xql.xql_to_aql(xql, vars=data, parser=parser, max_limit=max_limit)
        bind_vars.update(data)
        return aql, bind_vars, (_page, _per_page)

    def return_count(self, xql:lib_xql.XQLDEFINITION, data:dict={}) -> int:
        """
        From a query, it returns the count 

        Params:
            xql:lib_xql.XQLDEFINITION
            data:dict
        Returns
            Interger
        """
        xql["RETURN_COUNT"] = True
        aql, bind_vars, pager = self.build_query(xql=xql, data=data)
        cursor = self.execute_aql(aql, bind_vars=bind_vars, count=True, full_count=True) 
        return cursor.batch()[0] if cursor.count() else 0

    def collections(self) -> list:
        """
        All collections in the db

        Returns:
            list
        """
        return self.db.collections()
    
    def rename_collection(self, collection_name:str, new_name:str, use_prefix=True):
        """
        Rename collection
        """
        if self.has(collection_name, use_prefix=use_prefix) and not self.has(new_name, use_prefix=use_prefix):
            if use_prefix:
                collection_name = self.prefix_collection_name(collection_name)
            if use_prefix:
                new_name = self.prefix_collection_name(new_name)
            coll = self.select_collection(collection_name, use_prefix=use_prefix)
            coll.collection.rename(new_name)
            return self.select_collection(new_name, use_prefix=use_prefix)
    
    def delete_collection(self, collection_name:str, use_prefix=True):
        if self.has_collection(collection_name, use_prefix=use_prefix):
            if use_prefix:
                collection_name = self.prefix_collection_name(collection_name)
            self.db.delete_collection(collection_name)

    def truncate_collection(self, collection_name:str, use_prefix=True):
        if self.has_collection(collection_name, use_prefix=use_prefix):
            if use_prefix:
                collection_name = self.prefix_collection_name(collection_name)
            coll = self.select_collection(collection_name, use_prefix=use_prefix)
            coll.collection.truncate()

    def add_index(self, collection_name, data:dict):
        """
        Args:
            - collection, the collection name
            - data: dict of 
                    {
                        "type": "persistent",
                        "fields": [] # list of fields
                        "unique": False # bool - Whether the index is unique
                        "sparse": False # bool,
                        "name": "" # str - Optional name for the index
                        "inBackground": False # bool - Do not hold the collection lock
                    }
        """
        collection_name = self.prefix_collection_name(collection_name)
        col = self.db.collection(collection_name)
        col._add_index(data)
      
    def delete_index(self, collection_name:str, id):
        """
        Delete Index

        Args:
            - collection, the collection name
            - id: the index id
        """
        collection_name = self.prefix_collection_name(collection_name)
        col = self.db.collection(collection_name)
        col.delete_index(id, ignore_missing=True)

    def get_collection_stats(self, collection_name:str, use_prefix=True) -> dict:
        coll = self.select_collection(collection_name=collection_name, use_prefix=use_prefix)
        koll = coll.collection
        count = koll.count()
        statistics = koll.statistics() or {"documents_size": 0, "indexes": {"count": 0, "size": 0}}
        return {
            "documents_count": count, 
            "documents_size": statistics.get("documents_size"),
            "indexes_count": statistics.get("indexes").get("count"),
            "indexes_size": statistics.get("indexes").get("size"),
        }

    def _load_item(self, data:dict) -> "CollectionItem":
        if "_id" in data:
            collection_name, _key = data.get("_id").split("/")
            collection_name = self.prefix_collection_name(collection_name)
            col = self.db.collection(collection_name)
            return Collection(db=self, collection=col, custom_ops=self._custom_ops).item(data)
        else:
            raise Exception("INVALID_ITEM__MUST_HAVE_ID")

    def use_graph_edge(self, name: str, use_prefix=True) -> "GraphEdgeCollection":
        """
            item:CollectionItem
            ge = item.use_edge_collection()
            ge.link(other_item, kind="users:orgs")

            ge.traverse(traversals=[ge.traversals()])
        """

        if isinstance(name, GraphEdgeCollection):
            name = name.collection_name
            use_prefix = False 

        return GraphEdgeCollection(db=self, name=name, use_prefix=use_prefix)

class Collection(object):

    def __init__(self, db:Database, collection,  immut_keys:list=[], custom_ops:dict={}, item_class=None):
        self.db = db
        self.collection = collection
        self._immut_keys = immut_keys
        self._custom_ops = custom_ops
        self.collection_name = self.collection.name
        self.item_class = item_class

    def _commit(self, item:CollectionItem, replace_document=False, merge_objects=True, upsert=True, persist=True):
        """
        To commit/save changes

        Params:
            item:CollectionItem
            replace_document:bool - To replace instead of updating. Replace will not merge the data.
            merge_objects:bool - when a key is present in both src and dest document, 
                it will merge if True, otherwise new object will replace    
            upsert:bool - to insert when update fail  
            persist:bool - By default, it will save. When False it will not save the data but return it       
        """
        if not item._key:
            raise MissingItemKeyError()

        try:
            if not replace_document:
                item.timestamp("_modified_at")

            item_ = item.to_dict()

            for _ in ["_id", "_rev"]:
                if _ in item_:
                    item_.pop(_, None)

            if persist is False:
                return item_
            
            # ensure documents have valid keys before inserting/updating
            lib.dict_inspect_valid_keyname(item_)

            #-> collection.update|collection.replace
            if replace_document:
                return self.collection.replace(item_, return_new=True)["new"]
            else:
                return self.collection.update(item_, merge=merge_objects, return_new=True)["new"]

        except DocumentUpdateError as due:
            if persist is False:
                item.update({"_modified_at": None})
                # ensure documents have valid keys before inserting/updating
                lib.dict_inspect_valid_keyname(item_)
                return item.to_dict()
            
            if upsert:
                item.update({"_modified_at": None})
                item_ = item.to_dict()

                # ensure documents have valid keys before inserting/updating
                lib.dict_inspect_valid_keyname(item_)
                return self.collection.insert(item_, return_new=True)["new"]
            return None 
        
    def __iter__(self):
        return self.find(filters={})

    def load(self, data:dict, read_only:bool=False) -> CollectionItem:
        """
        Load data as item

        Returns:
            CollectionItem
        """
        item = None
        if not isinstance(data, CollectionItem) and "_key" not in data:
            item = CollectionItem.new(data, db=self.db, collection=self.collection, commiter=self._commit, immut_keys=self._immut_keys, custom_ops=self._custom_ops)               
        else:
            item = CollectionItem(data, db=self.db, collection=self.collection, commiter=self._commit, immut_keys=self._immut_keys, custom_ops=self._custom_ops, read_only=read_only)

        return self.item_class(item) if item and self.item_class else item

    def item(self, data:dict, read_only:bool=False) -> CollectionItem:
        """
        Deprecated
        Use #.load 
        Return CollectionItem
        """
        return self.load(data=data, read_only=read_only)
    
    def has(self, _key) -> bool: 
        """
        Check if a collection has _key

        Args:
            _key:str

        Returns: 
            Bool
        """
        return self.collection.has(_key)

    def get(self, _key) -> CollectionItem:
        """ 
        Get a document from the collection and returns a collectionItem
        Returns:
            CollectionItem
        """

        if data := self.collection.get(_key):
            return self.item(data)
        return None

    def create(self, data:dict={}) -> CollectionItem:
        """
        To create a new Item without inserting in the collection

        Requires #commit() to save data

        Returns:
            CollectionItem

        Example:
            item = coll.create({...})
            item.commit()
        """
        item = CollectionItem.new(data, db=self.db, collection=self.collection, commiter=self._commit, custom_ops=self._custom_ops)
        return self.item(item)
    
    def insert(self, data:dict, _key=None, return_object=True) -> CollectionItem:
        """
        To insert a new Item and commit in the collection

        Returns:
            CollectionItem

        Example
            item = coll.insert(...)
        """
        if _key or "_key" in data:
            _key = _key or data["_key"]
            if self.has(_key):
                raise ItemExistsError()
            data["_key"] = _key

        item = data
        if not isinstance(data, CollectionItem):
            item = CollectionItem.new(data, db=self.db, collection=self.collection, custom_ops=self._custom_ops)

        self.collection.insert(item.to_dict(), silent=True)

        if return_object:
            return self.get(item._key) 
        return None 

    def update(self, _key:str, data:dict, replace_document=False, merge_objects=True, upsert=True, refetch_data=True) -> CollectionItem:
        """
        To update and item. Can also replace the item

        Params:
            _key:str - document key 
            data:dict - data to update
            replace_document:bool - If true will replace the document and not merge
            merge_objects:bool - when a key is present in both src and dest document, 
                it will merge if True, otherwise new object will replace 
            upsert:bool - to insert data if it doesnt exist
            refetch_data:bool - To prevent making a 2nd round to fetch the data. Will retun 
                from the commit 
        Returns
            CollectionItem
        """
        item = self.item({**data, "_key": _key})
        upd = self._commit(item, replace_document=replace_document, merge_objects=merge_objects, upsert=upsert)  
        if refetch_data:
            return self.get(item._key) 
        return upd

    def upsert(self, data:dict) -> CollectionItem:
        """
        To update or insert data.

        Args:
            data:dict

        Return:
            CollectionItem
        """

        if "_key" in data:
            if self.has(data["_key"]):
                _key = data.pop("_key")
                return self.update(_key=_key, data=data)
        return self.insert(data)

    def delete(self, _key):
        """
        Delete a document by _key
        """
        self.collection.delete(_key)

    def find(self, filters:dict={}, offset=None, limit=100, sort=None, page=None, aggregations:dict=None, collects=None, skip_limit=False, xql:dict=None):
        """
        Perform a find in the collections

        Returns
            Generator[CollectionItem]
        """

        # page + limit take precedence
        if (page and limit) or (page and offset is None):
            offset = lib.calc_pagination_offset_from_page(page=page, limit=limit)
        elif page is None and offset:
            page = lib.calc_pagination_page_from_offset(offset=offset, limit=limit)

        read_only = False
        _xql = {
            "FROM": self.collection_name, 
            "FILTERS": filters,
            "OFFSET": offset,
            "LIMIT": limit,
            "SORT": sort,
            "PAGE": page,
            "AGGREGATIONS": aggregations,
            "COLLECTS": collects,
            "SKIP_LIMIT": skip_limit
        }

        # Extended XQL
        if xql:
            _xql.update(xql)
            if "JOIN" in _xql:
                read_only = True

        def data_mapper(item): return self.item(item, read_only=read_only)
        return self.db.query(_xql, data_mapper=data_mapper)

    def return_count(self, filters:dict={}) -> int:
        """
        Return the total count of documents from query

        Returns
            Int
        """
        
        _xql = {
            "FROM": self.collection_name, 
            "FILTERS": filters
        }
        return self.db.return_count(xql=_xql)

    def find_one(self, filters:dict, sort=None):
        """
        Retrieve one item based on the criteria

        Returns
            CollectionItem
        """
        if data := list(self.find(filters=filters, limit=1, sort=sort)):
            return data[0]
        return None

class SubCollection(object):
    _data = []
    _constraints = []
    _item = None
    _name = None 
    _commit_replace = False

    def __init__(self, item: CollectionItem, name: str, constraints:list=None, custom_ops:dict={}):
        self._item = item
        self._name = name
        self._constraints = constraints
        self._load()
        self._custom_ops = custom_ops

    def _load(self):
        self._data = self._item._subcollections.get(self._name) or []

    def _commit(self):
        if self._commit_replace:
            self._item._commit_replace = True
            self._commit_replace = False
        self._item._set_subcollection(self._name, self._data)
        
    def _save(self, _key, data):
        _data = self._normalize_data()
        _data[_key] = data
        self._data = self._denormalize_data(_data)
        self._commit()        

    def _normalize_data(self) -> dict:
        return { d.get("_key"): d for d in self._data}

    def _denormalize_data(self, data:dict) -> list:
        return list(data.values())

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self.find())

    @property
    def items(self):
        """ 
        Returns an iterator of all documents

        Returns:
            Iterator
        """
        return self.find()

    def has(self, _key):
        return bool(self.find_one({"_key": _key}))

    def insert(self, data: dict, _key:str=None):
        """
        Insert document

        Params:
            data:dict
            _key: to insert with a _key
        """

        data = _create_subdocument_item(data)
        data, _, __ = dict_mutator.mutate(mutations=data.copy(), immuts=self._item._immut_keys, custom_ops=self._custom_ops)

        if self._constraints:
            for c in  self._constraints:
                if c in data:
                    if self.find_one({c: data[c]}):
                        raise ConstraintError("Key: %s" % c)

        if _key or "_key" in data:
            _key = _key or data["_key"]
            if self.has(_key):
                raise ItemExistsError()
            data["_key"] = _key

        self._data.append(data)
        self._commit()
        return _SubCollectionItem(self, data)

    def update(self, filters:dict, mutations: dict, upsert:bool=False):
        """
        Update by filter

        Params:
            filter:dict - filter document criteria
            mutations:dict - changes on the found documents
        """
        _data = self._normalize_data()
        res = self.find(filters=filters, limit=1000)
        if res:
            for item in res:
                ts = lib.get_timestamp()
                _key = item.get("_key")
                _default = {  # ensuring we do some data can't be overwritten
                    "_key": _key,
                    # "_created_at": ts
                }
                upd, _, _commit_replace = dict_mutator.mutate(mutations=mutations, init_data=copy.deepcopy(item), immuts=self._item._immut_keys, custom_ops=self._custom_ops)
                
                if _commit_replace:
                    self._commit_replace = True
                _data[_key] = {**upd, **_default}
            self._data = self._denormalize_data(_data)
            self._commit()

        elif upsert:
            self.insert(mutations)
  

    def delete(self, filters: dict):
        """
        Delete documents based on filters

        Params:
            filters:dict
        """
        _data = self._normalize_data()
        for item in self.find(filters):
            del _data[item.get("_key")]
        self._data = self._denormalize_data(_data)
        self._commit()

    def get(self, _key:str) -> "_SubCollectionItem":
        """
        Return a document from subcollection by id 

        Returns: _SubCollectionItem
        """
        return self.find_one({"_key": _key})

    def find_one(self, filters:dict={}) -> "_SubCollectionItem":
        """
        Return only one item by criteria

        Return:
            dict
        """
        if res := self.find(filters=filters, limit=1):
            return list(res)[0]
        return None 

    def find(self, filters: dict = {}, sort: dict = {}, limit: int = 1000,  offset:int=0, page=None) -> dict_query.Cursor:
        """
        Perform a query

        Params:
            filters:
            sort:
            limit:
            offset:
        """

        if offset is None and page:
            offset = lib.calc_pagination_offset_from_page(page=page, limit=limit)

        sort = _parse_sort_dict(sort, False)
        data = [_SubCollectionItem(self, d) for d in dict_query.query(data=self._data, filters=filters)]
        return dict_query.Cursor(data, sort=sort, limit=limit, offset=offset)

    def filter(self, filters: dict = {}) -> dict_query.Cursor:
        """
        Alias to find() but makes it seems fluenty
        
        Returns:
            dict_query:Cursor
        """
        data = dict_query.query(data=self._data, filters=filters)
        return dict_query.Cursor([_SubCollectionItem(self, d) for d in data])

#:: GRAPH

class GraphEdgeCollection(object):
    """
    
    Graph Usage example

        *New: Can traverse from kind - Jan 1 2024
        for node in collection:GraphEdgeCollection(kind="orgs:projects"):
            item = node.item
            _from = node._from
            edge = node.edge

            # in joins
            for k in node.group_by_kind('...'):
                ...

            for k in node.group_by_collection():
                ...




        *New Join is written with dict
        joins = [
            {kind:..., edge_collection:..., joins:[{ dict }]},

        ]                


        -- old: Jan 1 2024

        item:CollectionItem
        ge = item.use_graph_edge(edge_collection_name)
        

        # === traverse the kind
        for node in ge.traverse(kind="users:orgs"):
            item = node.item # CollectionItem
        
        # === with joins
            joins = [
                ge.join(kind="orgs:projects")
            ]
            
            for node in ge.traverse(kind="users:orgs", joins=joins):
                item = node.item # CollectionItem
                edge = node.edge # dict

                for k in node.get_kind("orgs:projects"):
                    item_ = k.item # CollectionItem
                    edge_ = k.edge  

      
    """

    def __init__(self, db:Database, name:str, use_prefix=True, indexes=[]):
        """
        GRAPH
        """
        self._db = db
        self._collection = self._db.select_edge_collection(edge_collection=name, use_prefix=use_prefix, indexes=indexes)
        self.collection_name = self._collection.name
        self._cache = {}

    def _make_from_to_from_items(self, from_item:"CollectionItem", to_item:"CollectionItem") -> tuple:
        return from_item._id, to_item._id



    def link(self, from_item:"CollectionItem", to_item:"CollectionItem", kind:str, data:dict={}):
        """
        Create a bi-directional edge between 2 two items.
        It will assure only this edge exists bi-directionally
        _from:_to <-> _to:_from

        Params:
            - from_item:CollectionItem
            - to_item:CollectionItem
            - kind:str
            - data:dict
        """

        # ensuring some props can't be set
        if data:
            for k in ["_id", "_key", "_from", "_to"]:
                if k in data:
                    data.pop(k)

        if edge := self.get(from_item=from_item, to_item=to_item):
            _d = {
                **data,
                "_modified_at": lib.get_datetime(),
                "_id": edge["_id"]
            }
            return self._collection.update(_d)
        else:
            _from, _to = self._make_from_to_from_items(from_item=from_item, to_item=to_item)
            if not _from or not _to:
                raise Exception("MISSING _from or _to for edege collection")
            
            doc = {
                "_rbac": None,
                **data,
                "_key": lib.gen_xid(),
                "_from": _from,
                "_to": _to,
                "_kind": kind,
                "_created_at": lib.get_datetime(),
                "_modified_at": None,
            }          
            return self._collection.insert(doc)

    def unlink(self, from_item:"CollectionItem", to_item:"CollectionItem"):
        """
        Remove edge directional
        """
        if edge := self.get(from_item=from_item, to_item=to_item):
            _id = edge.get("_id")
            self._collection.delete({"_id": _id})

    def get(self, from_item:"CollectionItem", to_item:"CollectionItem", strict=False) -> bool:
        """
        Get edge bi directional. This guarantee the uniqueness of it

        Args:
            - from_item
            - to_item
            - strict:bool - By default it will to get bi-directional, when strict=True, it will respect the edge
        """
        _from, _to = self._make_from_to_from_items(from_item=from_item, to_item=to_item)

        if strict:
            aql = """
                FOR d in @@collection 
                FILTER (d._from == @_from and d._to == @_to)
                LIMIT 1
                RETURN d
            """
        else:
            aql = """
                FOR d in @@collection 
                FILTER ((d._from == @_from and d._to == @_to) OR (d._from == @_to and d._to == @_from))
                LIMIT 1
                RETURN d
            """
        bind_vars = {
            "@collection": self.collection_name,
            "_from": _from, 
            "_to": _to
        }
        cursor = self._db.execute_aql(aql, bind_vars=bind_vars)
        edges = list(cursor)
        return edges[0] if len(edges) else None

    def update(self, from_item:"CollectionItem", to_item:"CollectionItem", data:dict={}):
        """
        Update the edge if exists
        """
        # ensuring some props can't be set
        if data:
            for k in ["_id", "_key", "_from", "_to", "_kind"]:
                if k in data:
                    data.pop(k)  

        if edge := self.get(from_item=from_item, to_item=to_item):
            _d = {
                **data,
                "_modified_at": lib.get_datetime(),
                "_id": edge["_id"]
            }
            return self._collection.update(_d)
        return None

    def exists(self, from_item:"CollectionItem", to_item:"CollectionItem", strict=False) -> bool:
        """
        Check the existence of an edge bi-directional
        """
        return self.get(from_item=from_item, to_item=to_item, strict=strict) is not None 

    def has_relationship(self, from_item:"CollectionItem", to_item:"CollectionItem") -> bool:
        """
        Check if there is any two ways relationship between items
        (this_item <-> to_item)        
        """
        return self.exists(from_item=from_item, to_item=to_item)

    def traverse(self, kind:str, from_item:"CollectionItem"=None, direction="ANY", depth:int=1, edge_filters:dict={}, node_filters:dict={}, limit:int=100, offset:int=0, joins:list=[]) -> list:
        """
        To do a graph traversal query

        For any direction, use `direction=ANY`

        """
        _joins = [self.join(**j) for j in joins]
        xql = self.join(from_item=from_item, 
                        kind=kind, 
                        direction=direction, 
                        depth=depth, 
                        edge_filters=edge_filters, 
                        node_filters=node_filters, 
                        limit=limit, 
                        offset=offset, 
                        joins=_joins)
        
        return self._exec_traverse(xql=xql, kind=kind)

    def join(self, edge_collection=None, from_item:"CollectionItem"=None, kind:str=None, direction="ANY", depth:int=1, edge_filters:dict={}, node_filters:dict={}, limit:int=100, offset:int=0, joins:list=[], *a, **kw) -> list:
        """
        To do a graph traversal query

        For any direction, use `direction=ANY`
        """
        
        return self._make_graph_query(
            edge_collection=edge_collection or self.collection_name,
            kind=kind,
            start_vertex=from_item._id if from_item else None,
            direction=direction,
            edge_filters=edge_filters,
            node_filters=node_filters,
            joins=joins,
            depth=depth,
            limit=limit,
            offset=offset
        )

    def traverse_one(self, from_item:"CollectionItem", kind:str, direction="ANY", depth=1, edge_filters:dict={}, node_filters:dict={}, joins:list=[]) -> "GraphEdgeCollectionNode":
        if res := self.traverse(from_item=from_item, kind=kind, direction=direction, depth=depth, edge_filters=edge_filters, node_filters=node_filters, limit=1, joins=joins):
            return res[0]
        return None 

    def _make_graph_query(self, edge_collection:str, kind:str, start_vertex:str=None, direction:str="OUTBOUND", depth:int=1,  edge_filters:dict={}, node_filters:dict={}, joins:list=[], limit:int=100, offset:int=0) -> dict:
        """
        Create a traversal graph query

        Return object

            EDGE_COLLECTION
            START_VERTEX:str|None =  # if None, it will try to use the parent's edge {e._to} with the parent_idx
            DIRECTION: OUTBOUND|INBOUND|ANY
            DEPTH: list[start:int, end:int] | int
            EDGE_FILTERS: dict
            NODE_FILTERS: dict
            OFFSET:int
            LIMIT:int
            JOINS:[
                GRAPH_XQL_DEFINITION,
                ...
            ]

        """

        if isinstance(edge_collection, (GraphEdgeCollection, GraphEdgeCollectionItem)):
            edge_collection = edge_collection.collection_name

        if kind:
            edge_filters["_kind"] = kind

        return {
            "EDGE_COLLECTION": edge_collection,
            "START_VERTEX": start_vertex,
            "DIRECTION": direction.upper(),
            "DEPTH": depth,
            "EDGE_FILTERS": edge_filters,
            "NODE_FILTERS": node_filters,
            "LIMIT": limit,
            "OFFSET": offset,
            "JOINS": joins
        }

    def _exec_traverse(self, xql:dict, parent_idx=None, idx=None, kind=None) -> list:
        aql = graph_traversal_query_builder(xql=xql, parent_idx=parent_idx, idx=idx, kind=kind)
        cursor = self._db.execute_aql(query=aql.get("query"), bind_vars=aql.get("params"))
        return [self._parse_row(row) for row in cursor]

    def _parse_row(self, row):
        item = self._load_item(row.get("@item"))
        edge = row.get("@edge")
        paths = row.get("@paths")
        kinds = {} # group by kind
        group_collections = {} # group by collection name
        if rnodes := row.get("@kinds"):
            for k, rrows in rnodes.items():
                if k and rrows:
                    kinds[k] = [self._parse_row(rrow) for rrow in rrows]
  
        if paths and "vertices" in paths and paths.get("vertices"):
            for row_ in paths.get("vertices"):
                if row_:
                    collection_name, _ = row_.get("_id").split("/")
                    if collection_name not in group_collections:
                        group_collections[collection_name] = []
                    group_collections[collection_name].append(row_)


        return GraphEdgeCollectionNode(item=item, edge=edge, kinds=kinds, paths=paths, group_collections=group_collections)
    
    
    def _load_item(self, data:dict) -> "CollectionItem":
        if data and "_id" in data:
            collection_name, _ = data.get("_id").split("/")
            if not (col := self._cache.get(collection_name)):
                _col = self._db.db.collection(collection_name)
                col = Collection(db=self._db, collection=_col, custom_ops=self._db._custom_ops)
                self._cache[collection_name] = col
            if col:
                return col.item(data)
        return None 

    def _get_collection_name(self, collection):
        if isinstance(collection, list):
            return [self._get_collection_name(c) for c in collection]
        if isinstance(collection, GraphEdgeCollection):
            return collection.collection_name         
        elif isinstance(collection, Collection):
            return collection.collection_name
        elif isinstance(collection, StandardCollection):
            return collection.name  
        return collection
    
class GraphEdgeCollectionItem(object):

    def __init__(self, name: str, item: CollectionItem, use_prefix=True):
        self.item = item
        self._id = self.item._id
        self._db = item._db
        self._use_prefix = use_prefix
        self.edge_collection = GraphEdgeCollection(db=self._db, name=name, use_prefix=use_prefix)
        self.collection_name = self.edge_collection.collection_name

        # alias
        self._make_graph_query = self.edge_collection._make_graph_query

    def link(self, to_item: CollectionItem, kind:str, data:dict={}):
        """
        To create an edge between two items (vertex)
        """
        return self.edge_collection.link(from_item=self.item, to_item=to_item, kind=kind, data=data)

    def unlink(self, item:Collection):
        return self.edge_collection.unlink(from_item=self.item, to_item=item)

    def update(self, to_item:CollectionItem, data:dict):
        """
        To update the edge
        """
        return self.edge_collection.update(from_item=self.item, to_item=to_item, data=data)

    def exists(self, to_item:CollectionItem) -> bool:
        return self.edge_collection.exists(from_item=self.item, to_item=to_item)

    def belongs_to(self, from_item:CollectionItem):
        """
        revese the _from, _to
        Check if this item item belongs to another item
        (from_item -> this_item)
        """
        return self.edge_collection.exists(from_item=from_item, to_item=self.item, strict=True)
    
    def owns(self, to_item:CollectionItem):
        """
        Alias to exists.
        Check if this item owns the to_item
        (this_item -> to_item)
        """
        return self.edge_collection.exists(from_item=self.item, to_item=to_item, strict=True)

    def has_relationship(self, to_item:CollectionItem) -> bool:
        """
        Check if there is any two ways relationship between items
        (this_item <-> to_item)
        """
        return self.edge_collection.has_relationship(from_item=self.item, to_item=to_item)

    def traverse(self, kind:str, direction="OUTBOUND", depth:int=1, edge_filters:dict={}, node_filters:dict={}, limit:int=100, offset:int=0, joins:list=[]):
        
        return self.edge_collection.traverse(from_item=self.item,
                                             kind=kind,
                                             direction=direction,
                                             depth=depth,
                                             edge_filters=edge_filters,
                                             node_filters=node_filters,
                                             limit=limit,
                                             offset=offset,
                                             joins=joins)

class GraphEdgeCollectionNode(object):
    def __init__(self, item:CollectionItem, db=None, edge:dict=None, paths:dict=None, kinds:dict={}, group_collections:dict={}):
        self._db = db
        self.item = item
        self.edge = edge
        self._from = paths.get("vertices")[0] if paths and paths.get("vertices") else None
        self.root = self._from 
        self.kinds = kinds or {}
        self.group_collections = group_collections or {}


    def get_kind(self, name) -> list:
        return self.kinds.get(name) or []

    def get_collection(self, name) -> list:
        return self.group_collections.get(name) or []


    def _split_doc_id(self, _id) -> tuple:
        return _id.split("/")
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

def _create_document_item(data:dict={}) -> dict:
    _key = data["_key"] if "_key" in data else lib.gen_xid()

    return {
        "_key": _key,
        "_created_at:$datetime": True,
        "_modified_at": None,
        "__ttl": None,
        **data,
    }

def _create_subdocument_item(data:dict={}) -> dict:
    _key = data["_key"] if "_key" in data else lib.gen_xid()

    return {
        "_key": _key,
        "_created_at:$datetime": True,
        "_modified_at": None,
        **data,
    }

def _ascdesc(v, as_str=True):
    if as_str:
        if isinstance(v, int):
            return "DESC" if v == -1 else "ASC"
    else:
        if isinstance(v, str):
            return -1 if v.upper() == "DESC" else 1
    return v

def _parse_sort_dict(sort: dict, as_str=True):
    return [(k, _ascdesc(v, as_str)) for k, v in sort.items()]

def _is_iter(v) -> bool:
    return isinstance(v, (list, set, tuple))

def _is_list(v) -> bool:
    return isinstance(v, list)

def graph_traversal_query_builder(xql:dict, idx=None, parent_idx=None, edge_coll=None, kind=None) -> dict:
    """
    To create a simple graph edge traversal aql

    Return dict:
        - query:str
        - params:dict
        - idx:str

    [GRAPH_XQL_DEFINITION]:
        EDGE_COLLECTION # if None, and #edge_coll, it will use the parent's
        START_VERTEX:str|None =  # if None, it will try to use the parent's edge {e._to} with the parent_idx
        DIRECTION: OUTBOUND|INBOUND|ANY
        DEPTH: list[start:int, end:int] | int
        EDGE_FILTERS: dict
        NODE_FILTERS: dict
        OFFSET:int
        LIMIT:int
        JOINS:[
            GRAPH_XQL_DEFINITION,
            ...
        ]

    """

    aql = ""
    params = {}

    if not idx:
        idx = lib.gen_number(6)
    edge_collection = xql.get("EDGE_COLLECTION") or edge_coll
    start_vertex = None
    if start_vertex_ := xql.get("START_VERTEX"):
        start_vertex = "@start_vertex_%s" % idx
        params["start_vertex_%s" % idx] = start_vertex_
    elif not start_vertex and parent_idx:
        start_vertex = "e_%s._to" % parent_idx
    else:
        # With kind when start_vertex is None, we can start a broard traversal
        if kind:
            start_vertex = "xe_._from"
            params["xe_kind_%s" % idx] = kind
            aql = f"""
                FOR xe_ in {edge_collection}
                FILTER xe_._kind == @xe_kind_{idx}
            """
            
        else:
            raise Exception("INVALID_START_VERTEX")
        
    depth = xql.get("DEPTH") or [0, 1]
    depth_start, depth_end = depth if _is_iter(depth) and len(depth) == 2 else [depth, depth]
    direction = xql.get("DIRECTION") or "OUTBOUND"

    # filters
    filter_stmt = ""
    if edge_filters := xql.get("EDGE_FILTERS"):
        r = lib_xql.filter_builder(edge_filters, propkey="e_%s" % idx)
        filter_stmt += r[0]
        params.update(r[1])
    if node_filters := xql.get("NODE_FILTERS"):
        r = lib_xql.filter_builder(node_filters, propkey="v_%s" % idx)
        filter_stmt += r[0]
        params.update(r[1])

    # join
    joins_stmt = f"""LET rel_{idx} = null"""
    joins_return_stmt = f""" {{[rel_{idx}[0]["@edge"]._kind]: rel_{idx}}} """
    i = 0
    if joins := xql.get("JOINS"):
        joins_stmt = ""
        joins_return_stmt = ""
        if not _is_list(joins):
            joins = [joins]
        for i, join_xql in enumerate(joins):
            r = graph_traversal_query_builder(join_xql, parent_idx=idx, edge_coll=edge_collection)
            idx_2 = "%s_%s" % (idx, i)
            joins_stmt += " LET rel_%s = (%s) \n" % (idx_2, r.get("query"))
            joins_return_stmt += '{ [rel_%s[0]["@edge"]._kind]: rel_%s },' % (idx_2, idx_2)
            params.update(r.get("params"))

    limit_stmt = ""
    limit = xql.get("LIMIT") or 10
    offset = xql.get("OFFSET") or 0
    params.update({
        "limit_%s" % idx: limit,
        "offset_%s" % idx: offset
    })
    limit_stmt = " LIMIT @offset_%s, @limit_%s " % (idx, idx)

    aql += f"""
        FOR v_{idx}, e_{idx}, p_{idx} 
        IN {depth_start}..{depth_end}
        {direction} {start_vertex} {edge_collection}
        {filter_stmt}
        {joins_stmt}
        {limit_stmt}
        RETURN {{ "@item": v_{idx}, "@edge": e_{idx}, "@paths": p_{idx}, "@kinds":{joins_return_stmt} }}
    """

    return {
        "idx": idx,
        "query": aql,
        "params": params
    }

