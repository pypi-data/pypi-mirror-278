
#### 安装python环境
```shell
sudo yum install gcc gcc-c++ libffi-devel python-devel python-pip python-wheel openssl-devel cyrus-sasl-devel openldap-devel

```

#### 安装superset
```shell
cd /data
mkdir superset
cd superset
python3 -m venv venv
source venv/bin/activate
export FLASK_APP=superset
export PYTHONPATH=$HOME/.superset:$PYTHONPATH
pip install smart-superset --constraint "constraints3.9.txt"  -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### config
```shell
vim $PYTHONPATH/superset_config.py
```
```shell
# Superset specific config
ROW_LIMIT = 5000
SUPERSET_WEBSERVER_PORT = 8088
APPKEY = 'smartchart'

# Flask App Builder configuration
# You can generate a strong key using `openssl rand -base64 42`
SECRET_KEY = 'YOUR_OWN_RANDOM_GENERATED_SECRET_KEY'
# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
SQLALCHEMY_DATABASE_URI = 'sqlite:////path/to/superset.db'
SQLALCHEMY_DATABASE_URI = 'mysql://<UserName>:<DBPassword>@<Database Host>/<Database Name>'
SQLALCHEMY_DATABASE_URI = 'postgresql://<UserName>:<DBPassword>@<Database Host>/<Database Name>'

# Flask-WTF flag for CSRF
# WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
# WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
# WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

# Set this API key to enable Mapbox visualizations
# MAPBOX_API_KEY = ''

import redis

CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/3',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'SUPERSET_VIEW'
}

DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/3',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'SUPERSET_DATA'
}

EXPLORE_FORM_DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/3',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'SUPERSET_E'
}

FILTER_STATE_CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/3',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'SUPERSET_F'
}

```


#### Create an admin user in your metadata database
```shell
superset db upgrade
superset fab create-admin
```



#### Load some data to play with(option)
```shell
superset load_examples

```

#### Create default roles and permissions
```shell
superset init
```

#### start a development web server on port 8088, use -p to bind to another port
```shell
superset run -p 8088 -h0.0.0.0 --with-threads --reload --debugger
```

#### 生产环境启动
```shell
gunicorn -w 5 \
-k gevent \
--worker-connections 1000 \
--timeout 120 \
-b  0.0.0.0:8088 \
--limit-request-line 0 \
--limit-request-field_size 0 \
"superset.app:create_app()"

```

#### 生产启动
```shell
ps -ef|grep superset|grep -v grep|awk '{print "kill -9 "$2}'|sh
nohup gunicorn -w 5 -k gevent --worker-connections 1000 --timeout 120 -b  0.0.0.0:8088 --limit-request-line 0 --limit-request-field_size 0 "superset.app:create_app()" &
```
