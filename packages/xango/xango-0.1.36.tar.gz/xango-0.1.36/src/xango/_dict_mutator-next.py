#-----------------------------
# -- Xango --
#-----------------------------

import re
import copy
import arrow
import uuid
from . import lib, lib_dict, exceptions
from functools import reduce
# ----

# Operators that work with list
LISTTYPES_OPERATORS = ["xadd", "xadd_many", "xrem", "xrem_many", "xpush", "xpush_many", "xpushl", "xpushl_many", "xpop", "xpopl", "xset"]


# _FlattenDictType - Data Type flatten_dict
class _FlattenDictType(dict): pass

# To unset a value from being updated
class _UnOperableValue(object): pass

# ListMut is object a list mutations
class ListMut(dict):
    def add(self, key, value):
        self[key] = value

    def unflatten(self):
        return lib_dict.unflatten(dict(self))

def mutate(mutations: dict, init_data: dict = {}, immuts:list=[], custom_ops:dict={}):
    """
    mutate

    Args:
        mutations:dict - data contains operators to update
        init_data:dict - initial data 
        immuts: list - list of keys to not mutate
        custom_ops: dict - dict of custom operations

    Returns:
        tuple(updated_data:dict, oplog)

    """

    init_data = lib_dict.flatten(lib.deepcopy(init_data))
    flatten_data = lib_dict.flatten(lib.deepcopy(mutations))
    d, _ = _mutate(flatten_data=flatten_data, init_data=init_data, immuts=immuts, custom_ops=custom_ops)

    return lib_dict.unflatten(d), _

def _mutate(flatten_data:_FlattenDictType, init_data:_FlattenDictType={}, immuts:list=[], custom_ops:dict={}):
    """
    Mutation operations

    Args:
        flatten_data:dict - data contains operators to update
        init_data:dict - initial data 
        immuts: list - list of keys to not mutate
        custom_ops: dict - dict of custom operations

    Returns:
        tuple(updated_data:_FlattenDictType, oplog)

    Operators:
        $set - to set a literal k/v
        $incr - to increase an INT value
        $decr - to decrease an INT value
        $unset - To remove a property
        $rename - To rename a property
        $copy - To copy the value of property to another one
        $datetime - gen the current datetime. Can manipulate time
        $template - Evalute the string as template
        $uuid4 - gen a UUID4 string, with the dashes


        $xadd - add item if doesn't exist
        $xadd_many - add many items in the list if not already in the list
        $xrem - remove item
        $xrem_many - remove many items in a list
        $xpush - push item on the right
        $xpush_many - push many items in a list on the right
        $xpushl - push item on the left
        $xpushl_many - push many items in a list on the left
        $xpop - pop an item from a list on the right 
        $xpopl - pop an item from a list on the left
        $xlen - calculate the length of an object
        

        
    Example
        {
           "key:$incr": True|1|Num,
           "key:$decr": True|1|Num,
           "some.key:$unset": True,
           "old.key:$rename: "@new_path",
           "some.key:$copy: "@new_path",
           "some.datetimefield:$datetime": True,             
           "some.datetimefield:$datetime": "+1Day +2Hours 5Minutes",
           "some.key:$template": "Hello {{ name }}!",
           "some.random.id:$uuid4": True,

           "some.list:$xadd": Any,
           "some.list:$xadd_many": [Any, Any, Any, ...],
           "some.list:$xrem": Any,
           "some.list:$xrem_many": [Any, Any, Any, ...],     
           "some.list:$xpush": Any,
           "some.list:$xpush_many": [Any, Any, Any, ...],   
           "some.list:$xpushl": Any,
           "some.list:$xpushl_many": [Any, Any, Any, ...],    
           "some.list:$xpop": True,
           "some.list:$xpopl: False,
           "some.value:$xlen": "@some.data.path",
        }

    Custom operations
        Extends the dict mutator with custom operations 

        It's K/V pair with key being the name of the operation and value a callable with
            def name(data, path, value)
        

        ie:
            def _new_uuid4(data, path, value):
                return str(uuid.uuid4()).replace("-")

            custom_ops = { 
                "new_uuid4": _new_uuid4
            }

            ops = {
                "new_uid:$new_uuid4": True
            }    
    """
    data = init_data
    oplog = {}
    postproc = {}
    listops = {}

    # disabled immuts
    immuts = []
    
    # flat operation
    for path, value in flatten_data.items():

        # -- skip
        if immuts and path in immuts:
            continue 

        if ":$" in path:
            oppath = path
            oplog_path = path
            path, op = path.split(":$")

            # -- skip
            if immuts and path in immuts:
                continue 

            # listops, list
            if "." in op:
                opl, rest_ = op.split(".", 1)
                new_path = ".".join([path, rest_])
                oppp = "%s:$%s" % (path, opl)
                if opl in LISTTYPES_OPERATORS:
                    if oppp not in listops:
                        listops[oppp] = ListMut()
                    listops[oppp].add(rest_, value)
                continue

            
            if op in LISTTYPES_OPERATORS:
                listops[oppath] = value
                continue

            # post-process data. To be parsed later
            if op in ["template", "xlen", "rename", "copy"]:
                postproc[oppath] = value 
                continue 

            # $set. literal assigment, leave as is 
            elif op == "set":

                # potential list
                if "." in path and path[-1].isdigit():
                    index_ = int(path[-1])
                    s_l = path.split(".")
                    kp_ = ".".join(s_l[:-1])
                    lib_dict.dict_get(data, kp_)[index_] = value
                    continue

            # $incr
            elif op == "incr":
                value = _get_int_data(data, path) + \
                    (value if isinstance(value, int) else 1)
                oplog[oplog_path] = value

            # $decr
            elif op == "decr":
                _ = (value if isinstance(value, int) else 1) * -1
                value = _get_int_data(data, path) + _
                oplog[oplog_path] = value

            # $unset
            elif op == "unset":
                v = _pop(data, path)
                oplog[oplog_path] = v
                value = _UnOperableValue()


            # $datetime 
            elif op in ["datetime", "timestamp", "currdate"]:
                
                dt = _get_datetime()
                if value is True:
                    value = dt
                else:
                    try:
                        if isinstance(value, str):
                            value = _arrow_date_shifter(dt=dt, stmt=value)
                        else:
                            value = _UnOperableValue()
                    except:
                        value = _UnOperableValue()

            # $uuid4
            elif op == "uuid4":
                value = str(uuid.uuid4()) #.replace("-", "")


            # $$custom_ops, add to post process
            elif op in custom_ops:
                postproc[oppath] = value 
                continue 

            # _UnOperableValue
            else:
                value = _UnOperableValue()


        if not isinstance(value, _UnOperableValue):
            data[path] = value

    # listops
    # List operations work on list items to add, remove etc
    if listops:
        for path, value in listops.items():
            if isinstance(value, ListMut):
                value = value.unflatten()

            oppath = path
            oplog_path = path
            path, op = path.split(":$")

            if op in ( "xadd", "xadd_many", "xrem", "xrem_many", "xpush", "xpush_many", "xpushl", "xpushl_many"):
                values = _values_to_mlist(value, many=op.endswith("_many"))
                v = _get_list_data(data, path)
                
                # $xadd|$xadd_many
                if op.startswith("xadd"):
                    for val in values:
                        if val not in v:
                            v.append(val)
                    value = v

                # $xrem|$xrem_many
                elif op.startswith("xrem"):
                    _removed = False
                    for val in values:
                        if val in v:
                            _removed = True
                            v.remove(val)
                    value = v
                    if not _removed:
                        value = _UnOperableValue()

                # $xpush|$xpush_many
                elif op in ("xpush", "xpush_many"):
                    v.extend(values)
                    value = v

                # $xpushl|$xpushl_many
                elif op in ("xpushl", "xpushl_many"):
                    v2 = list(values)
                    v2.extend(v)
                    value = v2

            elif op == "xset":
                index_ = int(path[-1])
                s_l = path.split(".")
                kp_ = ".".join(s_l[:-1])
                lib_dict.dict_get(data, kp_)[index_] = value
                continue

            # $xpop
            elif op == "xpop":
                v = _get_list_data(data, path)
                if len(v):
                    value = v[:-1]
                    oplog[oplog_path] = v[-1]

            # $xpopl
            elif op == "xpopl":
                v = _get_list_data(data, path)
                if len(v):
                    value = v[1:]
                    oplog[oplog_path] = v[0]

            # _UnOperableValue
            else:
                value = _UnOperableValue()

            if not isinstance(value, _UnOperableValue):
                data[path] = value


    # Post process
    # final process 
    if postproc:
        for path, value in postproc.items():            
            try:
                if ":" in path:
                    # -- skip
                    if ":$" not in path:
                        continue

                    path, op = path.split(":$")

                    # -- skip
                    if path in immuts:
                        continue 

                    # $template
                    if op == "template": 
                        _tpl_data =  {
                            **data,
                            "TIMESTAMP": _j2_currdate,
                            "DATETIME": _j2_currdate
                        }              
                        data[path] = lib.render_template(source=value, data=_tpl_data, is_data_flatten=True)
                    
                    # $xlen, requires @ref
                    elif op == "xlen" and _is_value_at_ref(value):
                        value = _clean_value_ref(value)
                        try:
                            v = _lookup_flat_data(data, value)
                            data[path] = len(v) if v else 0
                        except:
                            data[path] = 0

                    # $rename, requires @ref
                    elif op == "rename" and _is_value_at_ref(value):
                        value = _clean_value_ref(value)
                        data[value] = _pop(data, path)

                    # $copy, requires @ref
                    elif op == "copy" and _is_value_at_ref(value):
                        value = _clean_value_ref(value)
                        data[value] = _get(data, path)

                    # custom ops
                    elif op in custom_ops:
                        data[path] = custom_ops[op](data, path, value)

            except:
                pass

    return data, oplog


_arrow_date_shifter = lib.arrow_date_shifter

def _get(data:dict, path):
    """
    _get: Alias to get data from a path
    """
    return lib_dict.dict_get(obj=data, path=path)

def _set(data:dict, path, value):
    """
    _set: Alias to set value in data
    """
    lib_dict.dict_set(data, path, value)
    return data

def _pop(data, path):
    """
    _pop: Alias to remove object from data
    """
    if path in data:
        return data.pop(path)
    return None 

def _get_int_data(data: dict, path: str) -> int:
    """
    _get_int_data: Returns INT for number type operations
    """
    v = _get(data, path)
    if v is None:
        v = 0
    if not isinstance(v, int):
        raise TypeError("Invalid data type for '%s'. Must be 'int' " % path)
    return v

def _get_list_data(data: dict, path: str) -> list:
    """
    _get_list_data: Returns a data LIST, for list types operations
    """
    v = _get(data, path)
    if v is None:
        return []
    if not isinstance(v, list):
        raise exceptions.MutationTypeError("Invalid data type for '%s'. Must be 'list' " % path)
    return v

def _values_to_mlist(value, many=False) -> list:
    """
    _values_to_mlist: Convert data multiple list items
    """
    return [value] if many is False else value if isinstance(value, (list, tuple)) else [value]

def _get_datetime() -> arrow.Arrow:
    """
    Generates the current UTC datetime with Arrow date

    ISO FORMAT
    Date    2022-08-13
    Date and time in UTC : 2022-08-13T22:45:03+00:00

    Returns:
      Arrow UTC Now
    """
    return arrow.utcnow()

def _j2_currdate(format_="ISO_DATETIME", shifter=None):
    dt = _get_datetime()
    if shifter:
        dt = _arrow_date_shifter(dt=dt, stmt=shifter)
    return lib.arrow_date_format(dt, format_)

def _lookup_flat_data(d_flatten, key):
    return lib.dict_get(obj=lib_dict.unflatten(d_flatten), path=key)

def _is_value_at_ref(value) -> bool:
    return value and isinstance(value, str) and value.startswith("@")

def _clean_value_ref(value) -> str:
    return value.replace("@", "")

