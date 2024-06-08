"""
=== XGraphQL ===

A Graphql interface to resolve data into resolved graphql

It contains one type `query`, which accepts a statement that can be used in an external engine

Type:
    - query

Methods:
    - parse(query:str):dict
    - resolve(query:str, data:[dict|list], variables:dict={}, resolver:BaseResolver_=None):dict


Usage:

    0. Receive the query and the variable
    query = `
        {
            articles: query(select * from article where _key=$_key) {
                title
                description
                url
                image_url
            }
        }
    `
    # note: the vars is the XSQL vars
    vars = {
        _key: "124"
    }
    
    1. Parse the query, to extract relevant data
        parsedql:dict = lib_xgraphql.parse(query=query)

    1.1 Retrieve the `statement` and make the query to get the results data, which can be a dict for single entry, list of multi entries
        statement:str = parsedql.get("statement")
        results_data:[dict|list] = some_function(statement, vars=vars)

    2. Resolve the Graphql
        data = lib_xgraphql.resolve(query=parsedql.get("query"), data:[dict|list]=results_data)
        print(data)


"""
import re
import json
import copy
import random
import string
import pydash
import graphql
from . import lib
from typing import cast


class BaseQueryResolver_(object):
    """
    A generic resolver to help parse the data
    """

    TYPE = """ 
        type Query {           
            query: RootType
        }
    """

    def __init__(self, data):
        self.data = data

    def query(self, _info):
        return self.data


class QueryResolverList(BaseQueryResolver_):
    """
    A query Resolver to resolve List data
    """

    TYPE = """ 
        type Query {           
            query: [RootType]
        }
    """


class QueryResolverDict(BaseQueryResolver_):
    """
    A query Resolver to resolve single Dict data
    """

    TYPE = """ 
        type Query {           
            query: RootType
        }
    """


def parse(query: str):
    """
    To parse a xgraphql query to dict that contains data to use in `resolve`

    {
        articles: query(select * from articles where id=1 limit=1) {
            _key,
            title,
            something:alias
        }
    }

    Returns: dict

    """
    #regex = "\s*((getOne|getMany|getByKey|search|query)\s*\((.*?)\))\s*"
    # regex = "\s*((getOne|getMany|getByKey|search|data|query)\s*)\s*"
    regex = "\s*((query)\s*\((.*?)\))\s*"

    m = re.findall(regex, query)
    if not m:
        raise Exception("Invalid XGRAPHQL Query")

    stmt_, method_, statement = m[0]
    query = query.replace(stmt_, method_)

    d = graphql.parse(query)
    def0 = d.definitions[0]
    sel0 = def0.selection_set.selections[0]
    return {
        "query": query,  # the new graphql query
        "query_statement": statement, # the statement that will be used for the query
        "type": def0.operation.value,
        "method": sel0.name.value,
        "alias": sel0.alias.value if sel0.alias else None,
        "args": [_parse_query_get_arg_value(a) for a in sel0.arguments],
    }


def resolve(query: str, data: dict, variables: dict = {}, resolver=None):
    """
    To resolve a GraphQL query leveraging data

    If data is dict, assuming it's a single object, it will resolve a QueryResolverDict
    if data is list, assuming it's multiple entries, it will resolve QueryResolverList

    Params:
        @query:str - the graphql string
        @data:[dict|list] - the data that will resolve to graphql
        @variables:dict - variables that will work with the query
        @resolver:class - A resolver class
    """
    
    # select the resolve based on the data type
    if not resolver:
        if isinstance(data, list):
            data = [remove_underscore_properties(d) for d in data]
            resolver = QueryResolverList
        elif isinstance(data, dict):
            data = remove_underscore_properties(data)
            resolver = QueryResolverDict

    if resolver:
        model = _build_document_model(data)
        types, _  = define_types(model, "RootType")
        schema = graphql.build_schema(types + resolver.TYPE)
        return _execute(schema=schema,
                        source=query,
                        root_value=resolver(data),
                        variable_values=variables)
    return None

def _build_document_model(data) -> dict:
    """
    Build a document model, to help generate the schema for GQL
    """
    #!todo when list, create a document model with fields from all docs
    if isinstance(data, list):
        return data[0]
        data = lib.dict_merge(*data)
    return data


#------------------------

def _execute(schema, source, root_value, variable_values):
    """
    Execute a GraphQL operation synchronously
    This methods omits the validations as the data can be loose

    # ref: https://github.com/graphql-python/graphql-core/blob/main/src/graphql/graphql.py 

    :arg schema:
        The GraphQL type system to use when validating and executing a query.
    :arg source:
        A GraphQL language formatted string representing the requested operation.
    :arg root_value:
        The value provided as the first argument to resolver functions on the top level
        type (e.g. the query object type).
    :arg variable_values:
        A mapping of variable name to runtime value to use for all variables defined
        in the request string.

    """

    schema_validation_errors = graphql.type.validate_schema(schema)
    if schema_validation_errors:
        return graphql.execution.ExecutionResult(data=None, errors=schema_validation_errors)

    # Parse
    try:
        document = graphql.language.parse(source)
    except graphql.error.GraphQLError as error:
        return graphql.execution.ExecutionResult(data=None, errors=[error])

    # Execute
    result = graphql.execution.execute(
        schema=schema,
        document=document,
        root_value=root_value,
        variable_values=variable_values
    )

    return cast(graphql.execution.ExecutionResult, result)


def keys_(obj):
    return pydash.objects.keys(obj)


def pascal_case_(value):
    return pydash.strings.pascal_case(value)


def set_(o, p, v):
    return pydash.objects.set_(o, p, v)


def gen_number(length: int = 4) -> int:
    """
    Generate random number
    """
    return ''.join(random.choice(string.digits) for _ in range(length))


def transform_primitive(value: str) -> str:
    if isinstance(value, int):
        return "Int"
    elif isinstance(value, float):
        return "Float"
    elif isinstance(value, bool):
        return "Boolean"
    return "String"


def clean_name(name: str) -> str:
    return re.sub(r"[\W]+", "", str(name))


def make_type_name(types: list, name: str, randomize: bool = False) -> str:
    """
    To help making sure types have unique name
    """
    nname = name
    if randomize:
        nname += gen_number(4)
    if nname in types:
        return make_type_name(types, name, True)
    types.append(nname)
    return "%sType" % nname


def dict_to_schema(djson: dict) -> dict:
    """
    Create the schema
    """
    result = {}
    cache = []
    stack = [(djson, "", "")]
    while(len(stack)):
        obj, path, cleaned_path = stack.pop()

        for k in keys_(obj):
            v = obj[k]
            if not isinstance(v, (list, dict)):
                nov = transform_primitive(v)
                novp = ("%s." % cleaned_path) if cleaned_path else ""
                novpk = "%s%s" % (novp, clean_name(k))
                if str(k).isdigit():
                    novpk = "%s[0]" % novp
                set_(result, novpk, nov)
                continue

            if v in cache:
                continue

            cache.append(v)

            path_prefix = ("%s." % path) if path else ""
            new_path = "%s%s" % (path_prefix, k)
            cleaned_path_prefix = "%s" % cleaned_path if cleaned_path else ""
            if str(k).isdigit():
                new_cleaned_path = "%s[%s]" % (cleaned_path_prefix, k)
            else:
                new_cleaned_path = "%s.%s" % (
                    cleaned_path_prefix, clean_name(k))

            if isinstance(v, list) and len(v):
                v = [v[0]]
            stack.append((v, new_path, new_cleaned_path))

    cache = cache[0: len(cache) * -1]
    return result


def schema_to_string(schema: dict, type_name: str = "RootType", prefix: str = "", types: list = []) -> tuple:
    s = ""
    for k in keys_(schema):
        if isinstance(schema[k], list):
            v = schema[k][0]
            if len(v) == 1:
                n = "%s%s" % (prefix, pascal_case_(k))
                return "%s: [%s]" % (n, v)
            if isinstance(v, (list, dict)):
                ntype_name = make_type_name(
                    types=types, name="%s%s" % (prefix, pascal_case_(k)))
                s += schema_to_string(v, ntype_name, prefix, types)[0]
                #print("-1-SXSXS", v, ntype_name, "->>", schema_to_string(v,  ntype_name, prefix, types), "->", s)

                schema[k][0] = ntype_name
            continue
            # return ""
        elif isinstance(schema[k], dict):
            v = schema[k]
            ntype_name = make_type_name(
                types=types, name="%s%s" % (prefix, pascal_case_(k)))
            r = schema_to_string(v,  ntype_name, prefix, types)
            s += r[0]
            # print("-2-SXSXS", v, ntype_name, "->>", r[0], r[0] == "A", "->", s)
            schema[k] = ntype_name
            continue
    obj_str = json.dumps(schema)
    o = "%stype %s %s" % (s, type_name, re.sub(r"/'/g", "", obj_str))
    o = re.sub(r"\[\n", "[", o)
    o = re.sub(r"\[\s+", "[", o)
    o = re.sub(r"\n\s+\]", "]", o)
    o = re.sub(r",", "", o)
    o = re.sub(r" {3,}", "  ", o)
    o = re.sub(r"\"", "", o)
    return o, ["%sType" % t for t in types]


def _parse_query_get_arg_value(a) -> tuple:
    value = a.value
    if isinstance(value, graphql.language.ast.VariableNode):
        value = "$" + a.value.name.value
    elif isinstance(value, graphql.language.ast.StringValueNode):
        value = a.value.value
    elif isinstance(value, graphql.language.ast.IntValueNode):
        value = int(a.value.value)
    elif isinstance(value, graphql.language.ast.FloatValueNode):
        value = float(a.value.value)
    else:
        value = a.value.value

    return a.name.value, value


def define_types(data, main_type_name: str = "RootType") -> tuple:
    schema = dict_to_schema(data)
    return schema_to_string(schema, main_type_name)


def remove_underscore_properties(data:dict):
    data = copy.deepcopy(data)
    for key in list(data.keys()):
        if key.startswith('__'):
            del data[key]
        elif isinstance(data[key], dict):
            data[key] = remove_underscore_properties(data[key])
    return data