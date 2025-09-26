import mysql.connector
import configparser

configFile = 'flaskr/secret_mysql_con.conf'

def connect_to_database():
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
