# Installation

## Linux (Ubuntu)

### Prerquisites

1. Mysql

2. git


### The files

Look for a place, where to store the application.
In my case it is the `/opt` directory.
If you choose another location, please replace the `/opt` with you choice.
The `sudo` and `chown` are only nesescary if you choose a directory outside of you home dirrectory.

```
cd /opt
```

Klone the repository:
```
sudo git clone https://github.com/claus007/tooltoucan.git
sudo chown -R  <yoour user name>:root tooltoucan
cd tooltoucan
```

Create a new file `secret_mysql_con.conf` with your mysql credentials...:

```
nano flaskr/secret_mysql_con.conf
```

... of the following form:

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
