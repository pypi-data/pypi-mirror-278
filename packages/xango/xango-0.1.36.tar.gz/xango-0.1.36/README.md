# Xango

**Xango**

## API

- `db` 
- `xql_to_aql`
- `parse_xsql`
- `parse_xgraphql`
- `resolve_xgraphql`
- `parse_dict_mutations`
- `gen_xid`
- `Collection` 
- `CollectionItem`
- `CollectionActiveRecordMixin`
  

## Connection

```
import xango

#--- connect
db = xango.db(hosts="http://host:8529", username="root", password:str)

#--- select collection
coll = db.select_collection('test')

#--- insert item
coll.insert({k:v, ...})

#--- insert item with custom _key
coll.insert({k:v,...}, _key='awesome')


```

### Query 



```
  {
    "_modified_at:$datetime": "+2hh"
  }
```

Format:

```
YYYY: Year
MM: Month
DD: Date
HH: Hour
mm: Min
ss: seconds

ISODATE: YYYY-MM-DDTHH:mm:ss

```


### $AND and $OR

```
filters = {

  "$or": [
    { // query between dates
      "_created_at:$lt": "@@CURRDATE() -2days",
      "_created_at:$gt": "@@CURRDATE() +2days"
    }
  ]
}
```



