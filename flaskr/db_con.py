# Copyright (c) 2025 Claus Ilginnis
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mysql.connector
from mysql.connector import pooling
import configparser

configFile = 'flaskr/secret_mysql_con.conf'



def create_pool():
    config = configparser.ConfigParser()
    config.read(configFile)
    connectionSectionName = config['DEFAULT']['connection']
    connectionSectionName = connectionSectionName.replace('"', "")
    print(f"Using connection section: {connectionSectionName}")
    db_config = config[connectionSectionName]
    try:
        pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="ToolToucan_WebUI_Pool",
            pool_size=32,
            pool_reset_session=True,
            host=db_config['host'].replace('"', ""),
            user=db_config['user'].replace('"', ""),
            password=db_config['password'].replace('"', ""),
            database=db_config['database'].replace('"', "")
        )
        return pool
    except mysql.connector.Error as err:
        print(f"Error creating connection pool: {err}")
        return None
    
cnxpool = create_pool()

def get_db():
    return cnxpool.get_connection()

###
# def connect_to_database():
    error=""
    config = configparser.ConfigParser()
    config.read(configFile)
    connectionSectionName = config['DEFAULT']['connection']
    connectionSectionName = connectionSectionName.replace('"', "")
    print(f"Using connection section: {connectionSectionName}")
    db_config = config[connectionSectionName]
    try:
        connection = mysql.connector.connect(
            host=db_config['host'].replace('"', ""),
            user=db_config['user'].replace('"', ""),
            password=db_config['password'].replace('"', ""),
            database=db_config['database'].replace('"', "")
        )
        
        return (True,error,connection)
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            error = "Something is wrong with your user name or password"
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            error = "Database does not exist"
        else:
            error = err.msg
        
    return (False,error,None)
###