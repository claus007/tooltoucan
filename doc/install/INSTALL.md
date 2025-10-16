# Installation

## Linux (Ubuntu)

### Prerquisites

1. Mysql

2. git


### The files

Look for a place, where to store the application.
In my case it is the `/opt` directory.
If you choose another location, please replace the `/opt` with you choice.
The `sudo` and `chown` are only necessary if you choose a directory outside of your home dirrectory.

```
cd /opt
```

**Klone the repository:**
```
sudo git clone https://github.com/claus007/tooltoucan.git
sudo chown -R  <yoour user name>:root tooltoucan
cd tooltoucan
```

**Create a new file `secret_mysql_con.conf` with your mysql credentials...:**

```
nano flaskr/secret_mysql_con.conf
```

**... of the following form:**
The redirection by `connection` may usefull if you have multiple database instances or users.

```
[DEFAULT]
connection = "mysql_con2"

[mysql_con1]
host = "<host>"
user = "root"
password = "<mysql-password>"
database = "<Toultoucan-Db-Name>"

[mysql_con2]
host = "<host>"
user = "toucan_user"
password = "<mysql-password>"
database = "<Toultoucan-Db-Name>"
```

###  The Virtual Environment
Mentioned here because it is the most effective way of getting things running.

Create the environment
```
python -m venv
```

Activate it
```
source venv/bin/activate
```

Install all necessary pakets
```
pip install -r doc/install/01_pip_freeze.list
```

Do a test run (optional)
```
python -m flask --app flaskr run --port=6000
```

