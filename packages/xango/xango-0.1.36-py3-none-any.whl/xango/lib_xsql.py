"""
=== DQL ===
Document Query Language

- SELECT:

    (1 = default

        SELECT [*, field, field as alias, $var, ...] 
        FROM [collection:str]
        WHERE [$where:dict, a=b, ...] 
        ORDER BY [$sort_by, column (ASC|DESC)] 
        OFFSET [$offset:number]
        LIMIT [$limit:number]
        LIMIT [$limit:number, $offset:number]

    (2 = short syntax
        SELECT FROM [collection:str]

- INSERT

    (1 = regular sql insert

        INSERT INTO $collection:str 
        VALUES $data:[dict|list(dict)]

    (2 = fluent insert

        INSERT $data:[dict|list(dict)]
        IN $collection:str


    (3 = Insert conditionally

        INSERT $data
        IN $collection
        ?WHEN [$when:dict, a=b, a!=b]


- UPDATE
        UPDATE $collection:str 
        SET $data:dict 
        WHERE [$where:dict, a=b, ...]
        LIMIT [$limit, NUMBER...] [$offset, NUMBER]

- UPSERT 
        UPDATE $collection:str
        SET $data:dict
        WHERE [$where]
        ELSE INSERT [$data2]

- DELETE
        DELETE $collection:str 
        WHERE [$where:dict, a=b, ...]
        LIMIT [$limit, NUMBER...] [$offset, NUMBER]

- COUNT
        COUNT $collection
        WHERE [$where:dict, a=b, ...]

- SEARCH 
        SEARCH $collection
        WHERE query=[$query]
        ORDER BY [$sort_by, column (ASC|DESC)] 
        OFFSET [$offset:number]
        LIMIT [$limit:number]
        LIMIT [$limit:number, $offset:number]
      
"""

import re
import decimal
from sqlglot import parse_one, exp

VERSION = "1.2.0"
READ_ENGINE = "mysql"

VAR_TOKEN = "$"

WHERES_OPS_MAP = {
    "eq": "eq",
    "neq": "ne",
    "in": "in",
    "gt": "gt",
    "gte": "gte",
    "lt": "lt",
    "lte": "lte",
    "like": "like",
    "ilike": "ilike"
    
}

# DEFAULT 
COLLECTION_SELECT = "collection.fetch"
COLLECTION_INSERT = "collection.insert"
COLLECTION_UPDATE = "collection.update"
COLLECTION_UPSERT = "collection.upsert"
COLLECTION_DELETE = "collection.delete"
COLLECTION_COUNT = "collection.count"

COLLECTION_SEARCH = "collection.search"
COLLECTION_FIND = "collection.find"


class XSQL_ERROR(Exception):
    pass

def is_number(n) -> bool:
    try:
        num = float(n)
        return num == num
    except ValueError:
        pass
    return False

def cast_value(value:str):
    """
    Having a string as an input, it will cast the value to [str|int|decimal|or the type it is
    Return: Any
    """
    if isinstance(value, str):
        if is_number(value):
            if value.isdigit():
                return int(value)
            elif "." in value:
                return decimal.Decimal(value)
    return value

def parse_query(sql) -> exp.Expression:
    return parse_one(sql=sql, read=READ_ENGINE)


def parse(query: str, variables: dict = {}):
    """
    Parse the XSQL to XQL
    Params:
      - query: str 
      - variables: dict
    Returns 
        dict
    """

    # VARS
    # rename all the keys to add [$]key, ie: {name: 'Soma'} -> {"$name": 'Soma'}
    variables = {"$%s" % k: v for k, v in variables.items()}

    #!== CUSTOM QUERY SYNTAX
    insert_when_query = None
    insert_data = None
    as_count_query = False
    as_search_query = False
    _custom_parse = False # wheneven custom query was passed, set as true, to prevent subsequent query

    #? UPSERT:
    #? [UPDATE $collection SET $data WHERE $where ELSE INSERT $data2 ]
    #  Upsert starts by making sure a WHERE gets executed
    # With the present of WHEN, it will create an extra expression to parse the WHEN as WHERE
    # WHEN must resolve to TRUE to insert, otherwise it will UPDATE based on that criteria
    # 
    # Example
    # 
    # UPDATE collection SET {name: name, value: value, code:123} WHERE {'code:$ne': 123} ELSE INSERT {zone: 1}
    SQLPATH_UPSERT = "^UPDATE\s+(.*)\s+SET\s+(.*)\s+WHERE\s+(.*)\s+(ELSE\s+INSERT)\s+(.*)"
    if not _custom_parse and (_upsert := re.findall(SQLPATH_UPSERT, query, re.IGNORECASE)):
        _custom_parse = True
        tablename, upd_data, where, _, insert_data  = _upsert[0]

        insert_data = variables.get(insert_data.strip())
        if not insert_data or not isinstance(insert_data, dict):
            raise XSQL_ERROR("UPSERT_STMT__INVALID_DATA")

        # Rebuild the query to parse it properly
        query = "UPDATE {tablename} SET {upd_data} WHERE {where}".format(tablename=tablename, upd_data=upd_data, where=where)
        
    #? INSERT IN | UPDATE IN ... WHEN
    #? [INSERT $data IN $collection]
    #? [UPDATE $data IN $collection]
    #? [INSERT $data IN $collection WHEN $when]
    #? [UPDATE $data IN $collection WHERE $when]
    # Will turn into INSERT INTO $collection VALUES $value
    # If there is a WHEN, it will create an extra expression to parse the WHEN as WHERE
    # WHEN must resolve to TRUE to insert
    # 
    #:Example
    # 1) INSERT data INTO collection
    #
    # 2) INSERT {name: name, value: value, code:123} INTO collection WHEN {'code:$ne': 123}
    # Will insert data if `code` does not equal to 123

    SQLPAT_INSERT_INTO = "^(INSERT|UPDATE)\s+(.*)\s+IN\s+(\w+)\s?(.*)"
    if not _custom_parse and (_insert_into := re.findall(SQLPAT_INSERT_INTO, query, re.IGNORECASE)):
        _custom_parse = True
        _q, values, tablename, when = _insert_into[0]
        # if WHEN condition exists, it will extract it 
        if when and when.strip():
            if _when := re.findall("WHEN\s+(.*)", when.strip(), re.IGNORECASE):
                insert_when_query = parse_query("SELECT a FROM b WHERE %s" % _when[0].strip())

        # Rebuild the query to parse it properly
        if _q.upper() == "INSERT":
            query = "INSERT INTO {tablename} VALUES {values}".format(tablename=tablename, values=values)
        elif _q.upper() == "UPDATE":
            insert_when_query = None
            query = "UPDATE {tablename} SET {values} {rest}".format(tablename=tablename, values=values, rest=when)

    #? SEARCH:
    #? [SEARCH $collection WHERE query='' [ORDER BY... LIMIT ...]]
    # Inially the search will be [SEARCH $query FROM $collection]
    # Then will turn into a full SELECT statement to extract some other values
    # Then will return a SEARCH action
    SQLPAT_SEARCH = "^SEARCH\s+(.*)\s+WHERE\s+(.*)"
    if not _custom_parse and (_search := re.findall(SQLPAT_SEARCH, query, re.IGNORECASE)):
        _custom_parse = True
        as_search_query = True
        tablename, where  = _search[0]
        query = "SELECT FROM {tablename} WHERE {where}".format(tablename=tablename, where=where)


    #? COUNT:
    #? [COUNT $collection [WHERE... ORDER BY... LIMIT ...]]
    # Inially the search will be [SEARCH $query FROM $collection]
    # Then will turn into a full SELECT statement to extract some other values
    # Then will return a SEARCH action
    SQLPAT_COUNT = "^COUNT\s+(.*)\s?(.*)?"
    if not _custom_parse and (_count := re.findall(SQLPAT_COUNT, query, re.IGNORECASE)):
        _custom_parse = True
        as_count_query = True
        tablename, rest = _count[0]
        query = "SELECT * FROM {tablename} {rest}".format(tablename=tablename, rest=rest)

    e = parse_query(query)

    table_name = _parse_table(e, variables=variables)
    if not table_name:
        raise XSQL_ERROR("SYNTAX_ERROR__MISSING_COLLECTION_NAME")

    # == SEARCH
    if as_search_query:
        return _do_collection_search(e, variables=variables)

    # == INSERT
    elif isinstance(e, exp.Insert):
        return _do_collection_insert(e, variables=variables, when_exp=insert_when_query)

    # == SELECT
    elif isinstance(e, exp.Select):
        return _do_collection_select(e, variables=variables, as_count_query=as_count_query)

    # == DELETE
    elif isinstance(e, exp.Delete):
        return _do_collection_delete(e=e, variables=variables)

    # == UPDATE
    elif isinstance(e, exp.Update):
        return _do_collection_update(e=e, variables=variables, insert_data=insert_data)


def _is_list_of_dict(data: list) -> bool:
    return isinstance(data, list) and all(isinstance(d, dict) for d in data)


def _parse_table(e: exp.Expression, variables: dict = {}) -> str:
    table_name = e.find(exp.Table).name
    if not table_name:
        raise XSQL_ERROR("INVALID_NAME")
    return table_name


def _parse_where(e: exp.Expression, variables: dict = {}) -> dict:
    wheres = {}
    if where := e.find(exp.Where):
        for y in where.flatten():
            if isinstance(y, (exp.And, exp.Or)):
              for x in y.flatten():
                wheres.update(_parse_wheres__(e=x, variables=variables))
            else:
              wheres.update(_parse_wheres__(e=y, variables=variables))
    return wheres

def _parse_wheres__(e: exp.Expression, variables:dict):
    wheres = {}
    if isinstance(e, exp.Column):
        name = str(e.this)
        if name.startswith(VAR_TOKEN):
            val = variables.get(name)
            if val and isinstance(val, dict):
                wheres.update(val)
    elif isinstance(e, (exp.EQ, exp.GT, exp.GTE, exp.LT, exp.LTE, exp.In, exp.Not, exp.NEQ, exp.Like, exp.ILike)):
        key = e.key
        if key in WHERES_OPS_MAP:
            key = WHERES_OPS_MAP.get(key)
        name = e.this.name

        if isinstance(e, exp.Not):
            name = str(e.this.this)
            val = str(e.this.args.get("field"))
            if isinstance(e.this, exp.In):
                key = "nin"
                val = str(e.this.args.get("field"))
            elif isinstance(e.this, (exp.Like, exp.ILike)):
                key = "nlike" if isinstance(e.this, (exp.Like)) else "nilike"
                exp_ = e.this.expression
                val = str(exp_)
                if isinstance(exp_, exp.Literal):
                    val = str(exp_.this)
                elif isinstance(exp_, exp.Column):
                    val = str(exp_.this.this)
        else:
            if e.args.get("field"):
                val = str(e.args.get("field"))
            else:
                val = e.expression.this
                if hasattr(val, "this"):
                    val = str(val.this)

        if isinstance(val, str) and val.startswith(VAR_TOKEN):
            val = variables.get(val)
        if val is not None:
            _k = name if key == "eq" else "%s:$%s" % (name, key)
            wheres[_k] = val

    return wheres


def _pop_wheres_key(wheres: dict):
    """
    To pop the _key out of the wheres
    Returns: Tuple (wheres:dict, key|None)
    """
    nwheres = {}
    _key = None
    for k, v in wheres.copy().items():
        if k == "_key" or k.startswith("_key:"):
            _key = wheres.get("_key")
        else:
            nwheres[k] = v
    return nwheres, _key


def _parse_columns(e: exp.Expression, variables: dict = {}) -> list:
    _ = [False, False]
    columns = []
    if isinstance(e, exp.Select):
        select_stmt = e.sql().split("FROM")[0]
        for x in parse_query(select_stmt).expressions:
            if isinstance(x, exp.Star):
                break  # no need to continue
            elif isinstance(x, (exp.Column, exp.Literal)):
                val = str(x.this)
                # vars
                if val.startswith(VAR_TOKEN):
                    _[0] = True
                    val = variables.get(val)
                else:
                    _[1] = True
                columns.append(val)
            elif isinstance(x, exp.Alias):
                val = str(x.this.this)
                alias = str(x.alias)
                columns.append("%s:%s" % (alias, val))
    else:
        pass
    return columns


def _parse_sort(e: exp.Expression, variables: dict = {}) -> list:
    sort = []
    if sort_by := e.find(exp.Order) or e.find(exp.Sort):
        for x in sort_by.expressions:
            val = str(x.this.name)
            args = sort_by.expressions[0].args
            if isinstance(x, exp.Ordered):
                if val.startswith(VAR_TOKEN):
                    val = variables.get(val)
                elif ":" in val:
                    val = val
                else:
                    dir_ = "DESC" if args.get("desc") is True else "ASC"
                    val = "%s:%s" % (val, dir_)
                sort.append(val)
    return sort


def _parse_limit(e: exp.Expression, variables: dict = {}) -> int:
    if limit := e.find(exp.Limit):
        val = str(limit.expression.this)
        if val.startswith(VAR_TOKEN):
          return int(variables.get(val))
        else:
          return int(val)
    return None


def _parse_offset(e: exp.Expression, variables: dict = {}) -> int:
    if offset := e.find(exp.Offset):
        return int(offset.expression.this)
    return None


def _parse_to_action(action: str, e: exp.Expression, variables: dict = {}):
    table_name = _parse_table(e, variables=variables)
    wheres = _parse_where(e, variables=variables)
    sort = _parse_sort(e, variables=variables)
    limit = _parse_limit(e, variables=variables)
    offset = _parse_offset(e, variables=variables)

    return {
        "action": action,
        "collection": table_name,
        "filters": wheres,
        "sort": sort,
        "offset": offset,
        "limit": limit,
    }


def _do_collection_insert(e: exp.Expression, variables: dict = {}, when_exp=None) -> dict:
    """
    Create collection entry

      > INSERT INTO $collection:str VALUES $data:dict

      > INSERT $data:dict IN $collection:str

      #conditional
      > INSERT $data:dict IN $collection:str WHEN $when
    """
    table_name = _parse_table(e, variables=variables)
    if values := e.find(exp.Values):
        val = ""
        try:
            val = str(values.expressions[0].expressions[0].name)
        except:
            pass
        if not val.startswith(VAR_TOKEN):
            raise XSQL_ERROR("INSERT_STMT__MISSING_VALUES")

        data = variables.get(val)

        # must be list or dict
        if not isinstance(data, (list, dict)):
            raise XSQL_ERROR("INSERT_STMT__INVALID_VALUES_DATA_TYPE")

        # all elements must be dict
        if isinstance(data, list) and not _is_list_of_dict(data):
            raise XSQL_ERROR("INSERT_STMT__MISMATCHED_DATA_TYPE")

        when = {}
        if when_exp:
            when = _parse_where(when_exp, variables=variables)
        action = {
            "action": COLLECTION_INSERT,
            "collection": table_name,
            "data": data,
            "when": when,
            
        }

        return action 
    raise XSQL_ERROR("INSERT_STMT__MISSING_VALUES")


def _do_collection_select(e: exp.Expression, variables: dict = {}, as_count_query=False):
    """
    Select entries
      > SELECT * FROM $collection:str WHERE $where:dict ORDER BY $order_by:[str|list] LIMIT $limit, $offset

    Or count 
        COUNT collection_name WHERE *
    """
    action = _parse_to_action(COLLECTION_SELECT, e=e, variables=variables)
    
    if not action.get("filters"):
        action["filters"] = {"**": True}

    if as_count_query:
        action["action"] = COLLECTION_COUNT

    # regular select
    # @fields will be 
    if action.get("action") == COLLECTION_SELECT:
        action["fields"] = _parse_columns(e, variables=variables)
        
    return action

def _do_collection_delete(e: exp.Expression, variables: dict = {}):
    """
    Delete entries 

      > DELETE $collection:str WHERE $where:dict [SORT, LIMIT]
    """

    return _parse_to_action(COLLECTION_DELETE, e=e, variables=variables)


def _do_collection_update(e: exp.Expression, variables: dict = {}, insert_data: str = None) -> dict:
    """
    Collection Update

      > UPDATE $collection:str SET $data:dict WHERE $where:dict

      # with UPSERT
      > UPDATE $collection:str SET $data:[dict|list] WHERE $where:dict ELSE INSERT $insert_data:dict

    """
    wheres = _parse_where(e, variables=variables)
    dataset = {}
    skip_dataset_check = False

    x = e.expressions[0]
    var = str(x.this) if len(e.expressions) else None
    if var:
        if isinstance(x, exp.Column) and var.startswith(VAR_TOKEN):
            dataset = variables.get(var)

    if not dataset or not isinstance(dataset, dict):
        raise XSQL_ERROR("UPDATE_STMT__INVALID_SET")

    if not wheres:
        raise XSQL_ERROR("UPDATE_STMT__INVALID_WHERE")

    # upsert
    if isinstance(insert_data, dict):
        action = _parse_to_action(COLLECTION_UPSERT, e=e, variables=variables)
        action.update({
            "update": dataset,
            "insert": insert_data,
        })

    else:
        action = _parse_to_action(COLLECTION_UPDATE, e=e, variables=variables)
        action["data"] = dataset

    return action

def _do_collection_search(e: exp.Expression, variables: dict = {}):
    """
    SEARCH
    > SEARCH $collection_name WHERE query=$query
    !@query is required
    """

    action = _parse_to_action(COLLECTION_SEARCH, e=e, variables=variables)
    if query := action.get("filters").pop("query", None):
        action["filters"] = {
            "query": query
        }
        return action
    raise XSQL_ERROR("SEARCH_STMT__INVALID_QUERY")

