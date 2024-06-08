# ------------------------------------------------------------------------------
# -- Xango --
# ------------------------------------------------------------------------------

from .database import Database as db, Collection, CollectionItem, ActiveCollectionItem, GraphEdgeCollection, GraphEdgeCollectionItem, GraphEdgeCollectionNode
from .lib_xql import xql_to_aql
from .lib_xsql import parse as parse_xsql
from .lib_xgraphql import parse as parse_xgraphql, resolve as resolve_xgraphql
from .dict_mutator import mutate as parse_dict_mutations
from .lib import gen_xid
from . import exceptions
from arango.exceptions import ArangoError
