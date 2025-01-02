from sqlite3 import connect

def runQuery(
    query: str, data: tuple = None, receive: bool = False, db_name: str = "sau-plants.db"
):
    CONNECTION = connect(db_name)
    CURSOR = CONNECTION.cursor()

    if data:
        CURSOR.execute(query, data)
    else:
        CURSOR.execute(query)

    if receive:
        return CURSOR.fetchall()
    else:
        CONNECTION.commit()

    CONNECTION.close()

def addPlantToDB(uuid:str, eng_name: str, local_name: str, sci_name: str, family: str, category: str, image_path: str):
    query = "INSERT INTO plants ('uuid', 'english-name', 'local-name', 'scientific-name', 'family', 'category', 'image-path') VALUES (?, ?, ?, ?, ?, ?, ?)"
    runQuery(query, (uuid, eng_name, local_name, sci_name, family, category, image_path))

def searchPlants(search_term: str):
    query = "SELECT * FROM plants WHERE 'english-name' LIKE ? OR 'local-name' LIKE ? OR 'scientific-name' LIKE ? OR 'family' LIKE ? 'category' LIKE ?"
    return runQuery(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"), True)

def showNewPlants():
    query = "SELECT * FROM plants"
    return runQuery(query, receive=True)

def showPlant(uuid: str):
    query = "SELECT * FROM plants WHERE uuid = ?"
    return runQuery(query, (uuid,), True)