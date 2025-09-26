import pytest
from flaskr import db_con

connection=None

def test_connect_to_database():
    global connection
    success, error, connection = db_con.connect_to_database()
    if success==False:
        print(f"Database connection failed with error: {error}")
    assert success is True
    assert error == ""
    assert connection is not None
    
test_connect_to_database()
connection.close()
print("Database connection test passed.")
    