# -----------------------------
# -- Xango --
# -----------------------------

import re
from slugify import slugify
from . import lib



# -----------------------------------------------------------------------------
# === MACROS ------------------------------------------------------------------

def _re_match(pattern, value) -> re:
    return re.match(pattern, value, flags=re.IGNORECASE)

def _macro_now(re_match:re):
    """
    This macro eval the NOW|DATETIME in the query
    
    :Params:
        :re_match: regexp match the 

    Regex: 


    Example:
        {
            "_created_at:$gt": "[[@NOW:-3hh]]",
        }

    Format: [[@MACRO:NOW, shifter, format]]
    Regex: "^\[\[\@MACRO:NOW\s*,?\s*(.*)]]$",
        re_match[1]
    """

    dt_format = "ISO_DATETIME"
    shifter = re_match[1]
    if ";" in shifter:
        shifter, dt_format = shifter.split(";", 1)
        shifter = shifter.strip()
        dt_format = dt_format.strip()

    now = lib.get_datetime()
    if shifter:
        now = lib.arrow_date_shifter(now, shifter)
    return now.format(lib.DATES_FORMAT.get(dt_format) if dt_format in lib.DATES_FORMAT else dt_format)

MACROS_DEFS = [
    {   
        # TIME
        # [[@T:]]
        # [[@T:+2d;]]
        # [[@T:+2d; YYYY-MM-DD HH:mm:ss]]
        "name": "TIME",
        "pattern": "^\[\[\@T:\s*(.*)]]$",
        "func": _macro_now
    },
    {
        # NOW 
        # [[@NOW:]]
        # [[@NOW:+2d;]]
        # [[@NOW:+2d; YYYY-MM-DD HH:mm:ss]]
        "name": "NOW_ALIAS_T",
        "pattern": "^\[\[\@NOW:\s*(.*)]]$",
        "func": _macro_now
    },
]


def eval_macros(value):
    for item in MACROS_DEFS:
        if isinstance(value, str) and (m := _re_match(item.get("pattern"), value)):
            return item.get("func")(m)
        elif isinstance(value, list):
            return [eval_macros(v) for v in value]
    return value


# -----------------------------------------------------------------------------
# === QUERY OPERATORS ---------------------------------------------------------

AQL_FILTER_LOGIC = {
    "$AND": " AND ",
    "$OR": " OR ",
    "$NOT": " NOT ",
    "$NOR": " NOR "
}

# AQL UTILITIES
AQL_FILTER_OPERATORS = {
    "_": None, # Not an operator

    "$EQ": "==",  # equal
    "$NE": "!=",  # not equal
    "$GT": ">",  # greater than
    "$GTE": ">=",  # greater than or equal
    "$LT": "<",  # lesser than
    "$LTE": "<=",  # lesser than or equal
    #?$BETWEEN: LOGIC IMPLEMENTED IN CODE


    # INCLUDES + XINCLUDES
    # Test if data in RIGHT(string|int) is in data in LEFT(array)
    # ie: "__subcollections.something[*].value:$INCLUDES": "my-value"
    # --> "my-value" IN __subcollections.something[*].value 
    "$INCLUDES": "IN",
    "$XINCLUDES": "NOT IN",

    # IN + NIN
    # reverse the order of INCLUDES
    # To test if data in (LEFT:str|int) is in the (RIGHT:array)
    # ie "city:$IN": ["charlotte", "atlanta"]
    # --> u.city IN ["charlotte", "atlanta"]
    "$IN": "IN",
    "$XIN": "NOT IN",


    # LIKE + NOTLIKE
    # right hand in left hand array -> values IN [field.value]
    "$LIKE": "LIKE",  # search
    "$NLIKE": "NOT LIKE",  # 

    # "$CONTAINS": "" # will turn into 
    # must return a tuple of [statement:str, dict:{value, ...}]
    "$CONTAINS": lambda odict: ("{propkey}.{key} LIKE @{ukey}", {**odict, "value": "%{value}%".format(value=odict.get("value"))}),
    "$XCONTAINS": lambda odict: ("{propkey}.{key} NOT LIKE @{ukey}", {**odict, "value": "%{value}%".format(value=odict.get("value"))}),

    #TODO:
    # == for case insensitive ==
    # "$ILIKE": "",
    # "$NILIKE": ""
}
# reverse operator, where the right hand will point to left hand
# ie: cities:$INCLUDES: 'charlotte' -> 'charlotte' IN cities
_rev_ops_order = ['$INCLUDES', '$XINCLUDES']


AQL_AGGREGATE_OPERATORS = {
    "$LENGTH": "LENGTH",
    "$SIZE": "LENGTH",
    "$SUM": "SUM",
    "$MAX": "MAX",
    "$MIN": "MIN"
}


MAX_LIMIT = 1000

# UNSET_KEYS
DEFAULT_UNSET_KEYS = ['_rev', '_old_rev']

# -----------------------------------------------------------------------------
# === XQLDEFINITION -----------------------------------------------------------

class XQLDEFINITION:
    """
    XQL Schema Definition:

        :param FROM: str = the collection name
        :param ALIAS: str = alias
        :param AS: str = alias
        :param FILTERS: dict = filters
        :param SORT: list/str = sort 
        :param OFFSET: int = the offset of the limit, default=0
        :param LIMIT: int = the limit of result, default=10
        :param PAGE: int = help calculate the skip by using a page number. 
        :param JOIN: list[XQL]
        :param AGGREGATIONS: dict = aggregations
        :param COLLECT: ? [NOT YET IMPLEMETED]
        :param RETURN_COUNT: bool =  Will return a count of all matched documents
        :param RETURN: str = string representation
        :param MERGE: str = on JOIN, to merge the data.
            ie: MERGE: "{__profile: profile}" 
            Can be done manually with RETURN MERGE(doc, {data})
        :param RETURN_PARTIAL_QUERY: bool 
            To return the query without final the return. By this can help with SELECT to INSERT

    """
    FROM: str = None
    ALIAS: str = None
    AS: str = None
    FILTERS: dict = {}
    SORT: list = []
    OFFSET: int = 0
    LIMIT: int = MAX_LIMIT
    PAGE: int = 1
    JOIN: list = []
    RETURN_COUNT: str = None
    RETURN: str = None
    MERGE: str = None
    RETURN_PARTIAL_QUERY: bool = False


def filter_builder(filters: dict, propkey: str) -> tuple:
    """
    Create a FILTERS clause

    Params:
        filter: dict
            {
                'name': 'something',
                'age:$gt': 18,
                'cities:$in': ['charlotte', 'Concord'],
                'date:$between:["[[@MACRO:NOW, -2Days]]", "[[@MACRO:NOW, -1Days]]"],
                
                # Logical Operators 
                == as a dict, it will make the comparison between the values, by turning it into dict
                '$or': {
                    key1: v1,
                    key2: v2
                }, #-> [{key1: v1}, {key2: v2}]

                == as list, it will group all the dict with AND and create OR between
                '$or': [
                    {
                       "cities:$in": [],
                       "_perms.read:$in":[] 
                    }, 
                    {
                        "k2": v2,
                        "k3": v3
                    }
                 ]
                ]
            }
        propkey:str
            the property key from the parent query

    Returns
        tuple(aql:str, params:dict)

    """
    logical_keys = AQL_FILTER_LOGIC.keys()
    params = {}
    aql = ""
    for k in filters:

        #* LOGICAL OPERATION
        if k.startswith("$"):
            k_ = k.upper()
            # operation
            if k_ in logical_keys and isinstance(filters[k], (dict, list)):
                fk = filters[k]
                _logic_op = AQL_FILTER_LOGIC[k_]
                _and_op = AQL_FILTER_LOGIC["$AND"]
                
                # A flat dict will turn into a list dict to apply OR on all 
                if isinstance(fk, dict):
                    fk = [{_1:_2} for _1, _2 in fk.items()]
                
                logic_aql = []
                for k0 in fk:
                    tmp_aql = []
                    for k2 in k0:
                        _aql, _params = _parse_filter_row(k2, k0[k2], propkey)
                        tmp_aql.append(_aql)
                        params.update(_params)
                    logic_aql.append("\n(%s)" % _and_op.join(tmp_aql))
                aql += "FILTER (%s)\n" % _logic_op.join(logic_aql)
            else:
                raise Exception("INVALID_LOGIC_OPERATOR: %s" % k)
        
        else:
            _aql, _params = _parse_filter_row(k, filters[k], propkey)
            aql += "FILTER (%s)\n" % _aql
            params.update(_params)
    return aql, params


def _parse_filter_row(k, value, propkey) -> tuple:
    operator = "$EQ"  # default operator
    # extract the key and the operator
    # ie -> "name:$eq" or "city:$in"

    # "x:$in": "@policy._key"

    # link#, especially in join: "'name': '#parent.key'"

    if ":" in k:
        k, operator = k.split(":", 2)
        operator = operator.upper()

    # literal values starts with `#`
    # it indicates the value should not be converted, but rather return as is without `#`
    # ie:
    # - {k: "@parent.key"} -> k == parent.key
    # - {k: "#parent.key"} -> k == parent.key
    # - {k: '#@params_value'} -> k == @params_value
    #
    dlit = isinstance(value, str) and value.startswith("#")

    # gen a unique number to make sure values generated are unique
    num_ = lib.gen_number(6)
    ukey = slugify("%s_%s" % (k, num_), separator="_")
    stmt = ""
    params = {}
    value = eval_macros(value=value)

    if dlit:
        if value.startswith("@"):
            value = value.replace("@", "")
        elif value.startswith("#@"):
            value = value.replace("#@", "@")
        elif value.startswith("#"):
            value = value.replace("#", "")

        if operator in _rev_ops_order:  # reverse order
            stmt = " {value} {operator} {propkey}.{key}"
        else:
            stmt = " {propkey}.{key} {operator} {value}"
    
    # between -> $gte and $lte
    elif operator == "$BETWEEN":
        if not isinstance(value, list) or len(value) != 2:
            raise Exception("INVALID_DATA_TYPE_FOR_BETWEEN")
        gte = slugify("%s_gte_%s" % (k, num_), separator="_")
        lte = slugify("%s_lte_%s" % (k, num_), separator="_")
        stmt = " {propkey}.{key} >= @%s AND <= @%s" % (gte, lte)
        operator = "_" 
        params = {
            gte: value[0],
            lte: value[1],
        }

    else:
        params = {
            ukey: value
        }
        if operator in _rev_ops_order:  # reverse order
            stmt = " @{ukey} {operator} {propkey}.{key}"
            
        elif callable(AQL_FILTER_OPERATORS.get(operator)):
            """
            An operator can be callable function that accepts a DICT of data as first arg
            and must return a 
                -> tuple(stmt:str, data:dict)

            ie:
                "$CONTAINS": lambda odict: ("{propkey}.{key} LIKE @{ukey}", {**odict, "value": "%{value}%".format(value=odict.get("value"))})
            
            """
            stmt, odict = AQL_FILTER_OPERATORS.get(operator)({"value": value})
            params = {
                ukey: odict.get("value")
            }
            operator = "_"
        else:
            stmt = " {propkey}.{key} {operator} @{ukey}"

    aql = stmt.format(
        value=value,
        propkey=propkey,
        key=k,
        operator=AQL_FILTER_OPERATORS[operator],
        ukey=ukey)

    return aql, params


def sort_builder(sorts: list, propkey: str) -> str:
    """
    Create a SORT clause

    Params
        sorts: list
            formats:
                - ["name DESC"]
                - ["name:ASC]
                - ["some.deep.path DESC"]
                - ["some.deep.path:DESC"]

            *alternative to list, it can be string
                - "name desc"
                - "name:desc"
                - "name" // will be ASC by default

        propkey:str
            the property key from the parent query
    Returns
        str
    """
    if not sorts:
        return ""

    # you can pass it as string
    # sorts: "name"
    if isinstance(sorts, str):
        sorts = [sorts]

    # @deprecated
    # make compatible with previous implementations.
    # sorts must now be a list, not dict.
    elif isinstance(sorts, dict):
        sorts = ["%s:%s" % (k, v) for k, v in sorts.items()]

    aql = []
    for s in sorts:
        s = lib.remove_extra_spaces(s)
        if not s:
            continue 
        
        if ":" in s:
            xs = s.split(':')
            aql.append("%s.%s %s" % (propkey, xs[0], xs[1].upper()))

        elif " " in s:
            xs = s.split(' ')
            if len(xs) == 2:
                aql.append("%s.%s %s" % (propkey, xs[0], xs[1].upper()))
            else:
                aql.append("%s.%s %s" % (propkey, xs[0], "ASC"))
        else:
            aql.append("%s.%s %s" % (propkey, s, "ASC"))

    if aql:
        return " SORT " + ", ".join(aql) + " "
    
    return ""


def aggregations_builder(aggregates:dict, propkey:str) -> tuple:
    """
    Create aggregates builder
    
    OPS: LENGTH, SUM, MAX, MIN 

    aggregates = {
        "total_objects:$LENGTH": True,
        "total_zsize:$SUM": "total_zsize",
        "total_zsize:$MAX": "total_zsize",
        "total_zsize:$MIN": "total_zsize",
    }
    Turn into:
        total_objects = LENGTH(1),
        total_objects_filesize = SUM(doc.total_objects_filesize),
        max_objects_filesize = MAX(doc.total_objects_filesize),
        min_objects_filesize = MIN(doc.total_objects_filesize),
    """
    aql = None 
    return_keys = None
    if aggregates:
        stmts = []
        keys = []
        for k in aggregates:
            if ":" in k:
                _k, operator = k.split(":", 2)
                keys.append(_k)
                operator = operator.upper()
                val = aggregates[k]

                # length needs to be LENGTH(1)
                if operator in ['$LENGTH']:
                    val = "1"
                    _s = "{_k} = {operator}({val})"
                else:
                    _s = "{_k} = {operator}({propkey}.{val})"
                _s = _s.format(_k=_k, propkey=propkey, val=val, key=k,operator=AQL_AGGREGATE_OPERATORS[operator])
                stmts.append(_s)
        if stmts:
            aql = ', '.join(stmts)
            return_keys = ", ".join(keys)
    return aql, return_keys

def collects_builder(collects: list, propkey: str) -> str:
    if not collects:
        return None
    # TODO
    return ""


def prepare_xql(xql: dict) -> dict:
    _defaults = {

        "FETCH": None, # alias to FROM
        "AS": None, # alias to ALIAS
        "SUBQUERIES": None, # alias to JOIN

        "FROM": None,
        "ALIAS": "doc",
        "FILTERS": {},
        "SORT": None,
        "OFFSET": None,
        "RETURN_COUNT": False,
        "LIMIT": 10,
        "PAGE": 1,
        "JOIN": [],
        "AGGREGATIONS": {},
        "RETURN": None,
        "RETURN_WITH": None,
        "RETURN_PARTIAL_QUERY": False,
        "UNSET_KEYS": [],
        **xql
    }
    

    r = {k.upper(): v for k, v in _defaults.items()}
    if r.get("FETCH"):
        r["FROM"] = r.get("FETCH")
    if r.get("AS") :
        r["ALIAS"] = r.get("AS")
    if r.get("SUBQUERIES"):
        r["JOIN"] = r.get("SUBQUERIES")

    if r["RETURN"] is None:
        r["RETURN"] = r["ALIAS"]
    return r


def xql_take_skip_page(xql: dict, max_limit=MAX_LIMIT) -> tuple:
    """
    Returns:
        type: tuple(LIMIT:int, OFFSET:int, PAGE:1)
            - LIMIT: limit/per_page
            - OFFSET: offset
            - PAGE: page #
    """
    xql = prepare_xql(xql)
    OFFSET = xql.get("OFFSET")
    LIMIT = xql.get("LIMIT") or 10
    PAGE = xql.get("PAGE") or 1

    if OFFSET is None:
        page = PAGE or 1
        per_page = LIMIT
        if per_page > max_limit:
            per_page = max_limit
        OFFSET = lib.calc_pagination_offset_from_page(page=page, limit=per_page)
        LIMIT = per_page
    if LIMIT > max_limit:
        LIMIT = max_limit

    return LIMIT, OFFSET, PAGE


def xql_to_aql(xql: dict, vars: dict = {}, max_limit=MAX_LIMIT, parser=None):
    """
    XQL:=
    Xtensible Query Language to query data in ArangoDB 

    Params:
        xql: 
            type: dict = the XQL schema
        max_limit:
            type: int = a max number
        parser:
            type: function
        vars:
            type: dict - Variables for FILTERS and FILTER_WHEN

    Returns:
        tuple(AQL:string, BIND_VARS:dict)

    ===
    XQL Schema Definition:
        FROM: str = the collection name
        ALIAS: str = alias
        FILTERS: dict = filters
        SORT: list/str = sort 
        OFFSET: int = the offset of the limit, default=0
        LIMIT: int = the limit of result, default=10
        PAGE: int = help calculate the offset by using a page number. 
        JOIN: list[XQL]
        AGGREGATIONS: dict = aggregates
        COLLECTS: ?
        RETURN: str = string representation
        MERGE: str = on JOIN, to merge the data.
            ie: MERGE: "{__profile: profile}" 
            Can be done manually with RETURN MERGE(doc, {data})
        RETURN_COUNT: str =  To count all the document, and return the value. Alias to `COLLECT WITH COUNT INTO`
        RETURN_PARTIAL_QUERY: bool - To return the query without final the return. By this can help with SELECT to INSERT
        SKIP_LIMIT: bool - to skip the limit clause
        UNSET_KEYS: list of keys to remove

        # TODO
        - WHEN: ? = a conditional to evaluate before running
        - FILTER_WHEN: add additional filters when a condition is true
        

    === 
    schema example:
        FROM: collection
        ALIAS: alias1
        FILTERS:
            x:y
            "z:$gt": 5
        SORT: name:desc
        JOIN:
            FROM: collection2
            ALIAS: c2
            FILTERS:
                d: "#alias1.d"
            LIMIT: 5
            PAGE: 2
            RETURN: c2
        LIMIT: 10
        OFFSET: 2
        RETURN 
            d
            c2


        === code example
        q = {
            "FROM": "job_posts",
            "ALIAS": "post",
            "FILTERS": {
                "a": "b",
                "c:$gt": 5
            },
            "SORT": ["id:desc"],
            "LIMIT": 10,
            "OFFSET": 47,
            "JOIN": [
                {
                    "ALIAS": "app",
                    "FROM": "application",
                    "FILTERS": {
                        "a": "b",
                        "c": "d",
                        "d": "#job.v_d"
                    },
                    "JOIN": [        {
                        "ALIAS": "J_loco",
                        "FROM": "bam",
                        "FILTERS": {
                            "a": "b",
                            "c": "d",
                            "d": "#app.v_d"
                        }
                    }]
                },
                {
                    "FROM": "loco",
                    "ALIAS": "bam",
                    "FILTERS": {
                        "a": "b",
                        "c": "d",
                        "d": "#app.v_d"
                    }
                }
            ],
            "RETURN": "MERGE(post, {__account: loco})"
    """

    xql = prepare_xql(xql)

    if not xql.get("ALIAS"):
        xql["ALIAS"] = "doc"

    ALIAS = xql.get("ALIAS") or "doc"

    if parser:
        xql = parser(xql)

    COLLECTION = xql.get("FROM")
    FILTERS = xql.get("FILTERS") or {}
    SORTS = xql.get("SORT")
    OFFSET = xql.get("OFFSET")
    LIMIT = xql.get("LIMIT") or MAX_LIMIT
    PAGE = xql.get("PAGE") or 1
    JOINS = xql.get("JOIN") or []
    COLLECTS = xql.get("COLLECT") or []
    AGGREGATIONS = xql.get("AGGREGATIONS") or {}
    RETURN = xql.get("RETURN") or ALIAS
    SKIP_LIMIT = xql.get("SKIP_LIMIT") or False
    UNSET_KEYS = xql.get("UNSET_KEYS") or []

    RETURN_COUNT = xql.get("RETURN_COUNT")
    RETURN_PARTIAL_QUERY = xql.get("RETURN_PARTIAL_QUERY")

    # work with take/skip
    if OFFSET is None:
        page = PAGE or 1
        per_page = max_limit if LIMIT > max_limit else LIMIT
        OFFSET = lib.calc_pagination_offset_from_page(page=page, limit=per_page)
        LIMIT = per_page
    if LIMIT > max_limit:
        LIMIT = max_limit


    # unique num to give each field to prevent name collision
    num_ = lib.gen_number(6)
    aql_filter, filter_vars = filter_builder(FILTERS, propkey=ALIAS)
    aql_sorting = sort_builder(SORTS, propkey=ALIAS)
    aql_collects = collects_builder(COLLECTS, propkey=ALIAS)
    aql_aggregates, aggregates_return = aggregations_builder(AGGREGATIONS, propkey=ALIAS)
    
    bind_vars = {}

    # SUBQUERY/JOINS
    subquery = ""
    for xql2 in JOINS:
        xql2 = prepare_xql(xql2)
        X = xql_to_aql(xql=xql2, parser=parser, max_limit=max_limit)
        subquery += "\nLET %s = (%s) \n" % (xql2.get("ALIAS"), X[0])
        bind_vars.update(X[1])

    # Query
    query = "FOR {alias} IN @@collection_{num_} ".format(alias=ALIAS, num_=num_)
    query += aql_filter
    query += subquery

    # --
    # == Aggregation: COLLECTION AGGREGATE
    aggregation = None 

    # collects
    if aql_collects:
        if not aggregation:
            aggregation = ""

        pass
        #query += aql_collects

    # aggregates
    if aql_aggregates:
        if not aggregation:
            aggregation = ""

        if not aql_collects:
            aggregation += " COLLECT "
        aggregation += " AGGREGATE %s " % aql_aggregates

    # --
    # --

    # SORTING
    query += aql_sorting

    # with RETURN_COUNT, we don't need to set limit
    if not RETURN_COUNT and not SKIP_LIMIT:
        query += " LIMIT @offset_%s, @limit_%s " % (num_, num_)
        bind_vars.update({
            "offset_%s" % num_: OFFSET,
            "limit_%s" % num_: LIMIT
        })

    # partial query doesn't have the final return
    if not RETURN_PARTIAL_QUERY and not aggregation:
        _unset_keys = DEFAULT_UNSET_KEYS
        if UNSET_KEYS:
            _unset_keys = _unset_keys + UNSET_KEYS
        _unset_keys = ', '.join(["'%s'" % k for k in _unset_keys])
        query += "RETURN UNSET_RECURSIVE(%s, [%s])" % (RETURN, _unset_keys)

    if RETURN_COUNT:
        query = "RETURN LENGTH(%s)" % query

    # AGGREGATE RETURN
    if not RETURN_COUNT and aggregation and aggregates_return:
        query = "%s %s RETURN { %s } " % (query, aggregation, aggregates_return)

    bind_vars.update({
        **filter_vars,
        "@collection_%s" % num_: COLLECTION
    })

    return query, bind_vars


def xql_extract_collections(xql: dict) -> list:
    """
    Extract all the collection names. 
    This can help with testing collection name

    Args:
        xql: dict

    Returns: 
        dict
    """
    xql = prepare_xql(xql)
    JOINS = xql.get("JOIN") or []
    collections = []
    for xql2 in JOINS:
        collections.extend(xql_extract_collections(xql2))
    collections.append(xql.get("FROM"))
    return list(set(collections))


def aql_detect_modifier_operations(aql: str) -> bool:
    """
    Detect if an AQL has retricted modifier operators.
    Use if we expect AQL to Query and not modify entries

    Params:
      @aql:
          type:str

    Returns
      bool

    """
    operators = ["REMOVE", "UPDATE", "REPLACE", "INSERT", "UPSERT"]
    return len([r for r in aql.split() if r.upper() in operators]) > 0


def aql_get_filter_keys(filters: dict) -> list:
    """
    Return all keys that are used for the filters
    """
    keys = set()
    for k in filters:
        if k.startswith("$"):
            k_ = k.upper()
            # operation
            if k_ in AQL_FILTER_LOGIC.keys() and isinstance(filters[k], (dict, list)):
                fk = filters[k]
                if isinstance(fk, dict):
                    fk = [fk]
                for k0 in fk:
                    for k2 in k0:
                        if ":" in k2:
                            _ = k2.split(":", 2)
                            keys.add(_[0])
                        else:
                            keys.add(k2)
            else:
                raise Exception("Invalid logic: %s" % k)
        else:
            if ":" in k:
                _ = k.split(":", 2)
                keys.add(_[0])
            else:
                keys.add(k)
    return list(keys)

