from codeflex.url import connect 
 
API_URL = "https://api.codeflex.com.co/mysql_connector"

HEADERS = {
    "Content-Type": "application/json"
}
 
def createdb(username, database):
    jsonData = {
        "action": "CREATEDB",
        "username": username,
        "database": database
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err
     

def deletedb(username, database):
    jsonData = {
        "action": "DELETEDB",
        "username": username,
        "database": database
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err


def dbquery(username, password):
    jsonData = {
        "action": "DBQUERY",
        "username": username,
        "pass": password
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err
     

def createtable(username, password, database, tablename):
    jsonData = {
        "action": "CREATETABLE",
        "username": username,
        "pass": password,
        "database": database,
        "tablename": tablename
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err


def createtable_custom(username, password, database, sql):
    jsonData = {
        "action": "CREATETABLE_CUSTOM",
        "username": username,
        "pass": password,
        "database": database,
        "sql": sql
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err
    

def tablequery(username, password, database, tablename):
    jsonData = {
        "action": "TABLEQUERY",
        "username": username,
        "pass": password,
        "database": database,
        "tablename": tablename
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err
    

def tablequery_custom(username, password, database, sql):
    jsonData = {
        "action": "TABLEQUERY_CUSTOM",
        "username": username,
        "pass": password,
        "database": database,
        "sql": sql
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err
    

def tableinsert_custom(username, password, database, sql):
    jsonData = {
        "action": "TABLEINSERT_CUSTOM",
        "username": username,
        "pass": password,
        "database": database,
        "sql": sql
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err
    

def deletetable(username, password, database, tablename):
    jsonData = {
        "action": "DELETETABLE",
        "username": username,
        "pass": password,
        "database": database,
        "tablename": tablename
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err
    

def deletetable_custom(username, password, database, sql):
    jsonData = {
        "action": "DELETETABLE_CUSTOM",
        "username": username,
        "pass": password,
        "database": database,
        "sql": sql
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err
    

def updatetable_custom(username, password, database, sql):
    jsonData = {
        "action": "UPDATETABLE_CUSTOM",
        "username": username,
        "pass": password,
        "database": database,
        "sql": sql
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err


def connector(username, password, database, sql):
    jsonData = {
        "action": "CONNECTOR",
        "username": username,
        "password": password,
        "database": database,
        "sql": sql
    }
    try:
        response = connect.post(API_URL, json=jsonData, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except connect.HTTPError as http_err:
        return http_err
    except Exception as err:
        return err
 