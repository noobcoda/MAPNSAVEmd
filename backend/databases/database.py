import sqlite3

conn = sqlite3.connect("database3.db")
c=conn.cursor()
conn.commit()
conn.close()

def create_all_tables():
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()

    #log table
    c.execute("CREATE TABLE IF NOT EXISTS Log"
              "("
              "LogID INTEGER PRIMARY KEY AUTOINCREMENT,"
              "Email VARCHAR(255),"
              "Username VARCHAR(50),"
              "Salt INTEGER NOT NULL)")

    #store table
    c.execute("CREATE TABLE IF NOT EXISTS Store"
                        "("
                        "StoreID INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "sLat DECIMAL(65,30),"
                        "sLong DECIMAL(65,30),"
                        "storeName VARCHAR(255))")

    #product table
    c.execute("CREATE TABLE IF NOT EXISTS Product"
                        "("
                        "ProductID INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "StoID INTEGER NOT NULL,"
                        "productName VARCHAR(255),"
                        "productPrice DECIMAL(65,30),"
                        "FOREIGN KEY(StoID) REFERENCES Store(StoreID))")

    #user table
    c.execute("CREATE TABLE IF NOT EXISTS User"
                        "("
                        "UserID INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "UID INTEGER NOT NULL,"
                        "SID INTEGER NOT NULL,"
                        "uLat DECIMAL(65,30),"
                        "uLong DECIMAL(65,30),"
                        "ProductSearch VARCHAR(255),"
                        "Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,"
                        "FOREIGN KEY(UID) REFERENCES Log(LogID)"
                        "FOREIGN KEY(SID) REFERENCES Store(StoreID))")

    conn.commit()
    conn.close()

def see_all_tables():
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()

    return c.execute("SELECT * FROM Log").fetchall(),c.execute("SELECT * FROM User").fetchall(),c.execute("SELECT * FROM Store").fetchall(),c.execute("SELECT * FROM Product").fetchall()

def reset():
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS Product")
    c.execute("DROP TABLE IF EXISTS Store")
    c.execute("DROP TABLE IF EXISTS Log")
    c.execute("DROP TABLE IF EXISTS User")
    create_all_tables()

def insert_into_log_table(email,username,salt):
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()

    c.execute("INSERT INTO Log(Email,Username,Salt) VALUES(?,?,?)",(email,username,salt))
    c.execute("SELECT * FROM Log")

    conn.commit()
    conn.close()

def get_person_ID(email,username):
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()
    return int(c.execute("SELECT LogID FROM Log WHERE Email=? AND Username=? LIMIT 1",(email,username)).fetchone()[0])

def get_salt(email):
    conn=sqlite3.connect("database3.db")
    c = conn.cursor()

    salt = c.execute("SELECT Salt FROM Log WHERE Email=?",(email,)).fetchone()[0]

    return salt

def check_already_exists(email,username_ask):
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()

    username = c.execute("SELECT Username FROM Log WHERE Email=?",(email,)).fetchall()

    if len(username) ==0:
        return 1
    if username_ask != username[0] and username_ask != '[]':
        return 2
    if username_ask == username[0]:
        return True

def insert_user_table(logID,stoID,uLat,uLon,product):
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()

    c.execute("INSERT INTO User(UID,SID,uLat,uLong,ProductSearch) VALUES(?,?,?,?,?)",(str(logID),str(stoID),uLat,uLon,product))

    conn.commit()
    conn.close()

def insert_to_store(lat,long,name):
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()

    c.execute("INSERT INTO Store(sLat,sLong,storeName) VALUES(?,?,?)", (lat,long,name))

    conn.commit()
    conn.close()

def is_store(sLat,sLng,storeName):
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()
    if len(c.execute("SELECT StoreID FROM Store WHERE Store.sLat=? AND Store.sLong=? AND Store.storeName=?",(sLat,sLng,storeName)).fetchall()) == 0:
        return False
    else:
        return True

def get_store_ID(sLat,sLng,storeName):
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()
    return int(c.execute("SELECT StoreID FROM Store WHERE Store.sLat=? AND Store.sLong=? AND Store.storeName=?",(sLat,sLng,storeName)).fetchone()[0])

def insert_to_product(storeID,product_name,product_price):
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()

    c.execute("INSERT INTO Product(StoID,productName,productPrice) VALUES(?,?,?)",(str(storeID),product_name,product_price))

    conn.commit()
    conn.close()

def get_possible_store_locations(storeName):
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()

    return c.execute("SELECT Store.sLat,Store.sLong FROM Store WHERE Store.storeName =?",(storeName, )).fetchall()

def get_all_locations(logID):
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()

    return c.execute("SELECT User.uLat,User.uLong,Store.sLat,Store.sLong "
                    "FROM ((Log "
                    "INNER JOIN User ON Log.LogID = User.UID)"
                    "INNER JOIN Store ON User.SID = Store.StoreID)"
                    "WHERE Log.LogID=?"
                    "ORDER BY Time DESC "
                    "LIMIT 1",(str(logID), )).fetchall()

def show_user_history(logID):
    conn = sqlite3.connect("database3.db")
    c = conn.cursor()

    return c.execute("SELECT distinct User.Time,Store.storeName,Product.productName,Product.productPrice "
                     "FROM (((Log "
                     "INNER JOIN User ON Log.LogID = User.UID)"
                     "INNER JOIN Store ON User.SID = Store.StoreID)"
                     "INNER JOIN Product ON Product.StoID = Store.StoreID)"
                     "WHERE Log.LogID=? "
                     "ORDER BY Time DESC",(str(logID), )).fetchall()

create_all_tables()