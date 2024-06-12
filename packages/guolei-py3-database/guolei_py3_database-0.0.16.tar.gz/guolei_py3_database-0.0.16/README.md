# guolei_py3_database

## introduce

**guolei python3 database library**



## software architecture

~python 3.*

## installation tutorial

```shell
pip install guolei_py3_database
```

## catalog description
### pymysql example

```python
# import module
from guolei_py3_database import pymysql as gl_pymysql

# connect config
cfg = {
    "host": "<HOST>",
    "port": "<PORT>",
    "user": "<USER>",
    "password": "<PASSWORD>",
    "database": "<DATABASE>",
}

# open connect
connect = gl_pymysql.open_connect(**cfg)

# execute
state, rowcount, lastrowid = gl_pymysql.execute(connect=connect, query="sql", args={})

# executemany
state, rowcount = gl_pymysql.executemany(connect=connect, query="sql", args={})

# execute_transaction
state, rowcount = gl_pymysql.execute_transaction(connect=connect, query="sql", args={})

# fetchone
state, dict = gl_pymysql.fetchone(connect=connect, query="sql", args={})

# fetchone
state, list[{}] = gl_pymysql.fetchone(connect=connect, query="sql", args={})

# close connect
gl_pymysql.close_connect(connect=connect)


```

### sqlite3 example
```python
# import module
from guolei_py3_database import pymysql as gl_sqlite3

# connect config
cfg = {
    "host": "<HOST>",
    "port": "<PORT>",
    "user": "<USER>",
    "password": "<PASSWORD>",
    "database": "<DATABASE>",
}

# open connect
connect = gl_sqlite3.open_connect(**cfg)

# execute
state, rowcount, lastrowid = gl_sqlite3.execute(connect=connect, query="sql", args={})

# executemany
state, rowcount = gl_sqlite3.executemany(connect=connect, query="sql", args={})

# execute_transaction
state, rowcount = gl_sqlite3.execute_transaction(connect=connect, query="sql", args={})

# fetchone
state, dict = gl_sqlite3.fetchone(connect=connect, query="sql", args={})

# fetchone
state, list[{}] = gl_sqlite3.fetchone(connect=connect, query="sql", args={})

# close connect
gl_sqlite3.close_connect(connect=connect)

```
### strictredis example

```python
from guolei_py3_database import strictredis as gl_strictredis

# connect config
cfg = {
    # StrictRedis 
}
# open connect
connect = gl_strictredis.open_connect(**cfg)

# execute
gl_strictredis.execute(connect=connect, method="keys", pattern="*")

# close connect
gl_strictredis.close_connect(connect=connect)
```




