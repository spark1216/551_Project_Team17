import pymysql
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd

#Set Up
df = pd.read_csv('/Users/soniapark/Documents/USC_Courses/DSCI551/Project/airbnb_ds_clean.csv')
df0 = df[df['room_type'] == 'Entire home/apt']
df1 = df[df['room_type'] != 'Entire home/apt']
property0 = df0[['property_id', 'name', 'room_type', 'price','minimum_nights', 'availability_365','available_since_date']].drop_duplicates()
property1 = df1[['property_id', 'name', 'room_type', 'price','minimum_nights', 'availability_365','available_since_date']].drop_duplicates()
host0 = df0[['host_id', 'host_name']].drop_duplicates()
host1 = df1[['host_id', 'host_name']].drop_duplicates()
hostby0 = df0[['property_id','host_id']].drop_duplicates()
hostby1 = df1[['property_id','host_id']].drop_duplicates()
location0 = df0[['location_id', 'neighbourhood_group','neighbourhood', 'latitude', 'longitude']].drop_duplicates()
location1 = df1[['location_id', 'neighbourhood_group','neighbourhood', 'latitude', 'longitude']].drop_duplicates()
locatein0 = df0[['property_id','location_id']].drop_duplicates()
locatein1 = df1[['property_id','location_id']].drop_duplicates()
# Establish connection
connection = pymysql.connect(host='localhost', user='root', password='dsci551')
cursor = connection.cursor()
#Airbnb0
new_database_name = 'airbnb0'
cursor.execute(f"CREATE DATABASE {new_database_name}")
engine = create_engine('mysql+pymysql://root:dsci551@localhost/airbnb0', pool_pre_ping=True)
connection=engine.connect()

#property
create_table_query = """
CREATE TABLE IF NOT EXISTS property (
    property_id	BIGINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    price INT NOT NULL,
    minimum_nights INT,
    availability_365 INT,
    available_since_date DATE
);
"""
connection.execute(text(create_table_query))
connection.commit()
table_name = 'property'
property0.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

#host
create_table_query = """
CREATE TABLE IF NOT EXISTS host (
    host_id BIGINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
)
"""
connection.execute(text(create_table_query))
connection.commit()
table_name = 'host'
host0.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
#Need to create index for hostby to not get foreign key error
connection.execute(text("CREATE INDEX idx_property_id ON property(property_id);"))
connection.execute(text("CREATE INDEX idx_host_id ON host(host_id);"))
#hostby
create_table_query = """
CREATE TABLE IF NOT EXISTS hostby (
    property_id BIGINT,
    host_id BIGINT,
    PRIMARY KEY (property_id, host_id),
    FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (host_id) REFERENCES host(host_id) ON DELETE CASCADE ON UPDATE CASCADE);
"""
connection.execute(text(create_table_query))
connection.commit()
table_name = 'hostby'
hostby0.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
#location
create_table_query = """
CREATE TABLE IF NOT EXISTS location (
    location_id INT PRIMARY KEY,
    neighbourhood_group VARCHAR(50),
    neighbourhood VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT
);
"""
connection.execute(text(create_table_query))
connection.commit()
table_name = 'location'
location0.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
#To avoid error
connection.execute(text("CREATE INDEX idx_location_id ON location(location_id);"))
#locatein
create_table_query = """
CREATE TABLE IF NOT EXISTS locatein (
    property_id BIGINT,
    location_id BIGINT,
    PRIMARY KEY (property_id, location_id),
    FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location(location_id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""
connection.execute(text(create_table_query))
connection.commit()
table_name = 'locatein'
locatein0.to_sql(name=table_name, con=engine, if_exists='replace', index=False)


#Airbnb1
new_database_name = 'airbnb1'
cursor.execute(f"CREATE DATABASE {new_database_name}")
engine = create_engine('mysql+pymysql://root:dsci551@localhost/airbnb1', pool_pre_ping=True)
connection=engine.connect()
connection.commit()
#property
create_table_query = """
CREATE TABLE IF NOT EXISTS property (
    property_id	BIGINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    price INT NOT NULL,
    minimum_nights INT,
    availability_365 INT,
    available_since_date DATE
);
"""
connection.execute(text(create_table_query))
connection.commit()
table_name = 'property'
property1.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

#host
create_table_query = """
CREATE TABLE IF NOT EXISTS host (
    host_id BIGINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
)
"""
connection.execute(text(create_table_query))
connection.commit()
table_name = 'host'
host1.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
#Need to create index for hostby to not get foreign key error
connection.execute(text("CREATE INDEX idx_property_id ON property(property_id);"))
connection.execute(text("CREATE INDEX idx_host_id ON host(host_id);"))
#hostby
create_table_query = """
CREATE TABLE IF NOT EXISTS hostby (
    property_id BIGINT,
    host_id BIGINT,
    PRIMARY KEY (property_id, host_id),
    FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (host_id) REFERENCES host(host_id) ON DELETE CASCADE ON UPDATE CASCADE);
"""
connection.execute(text(create_table_query))
connection.commit()
table_name = 'hostby'
hostby1.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
#location
create_table_query = """
CREATE TABLE IF NOT EXISTS location (
    location_id INT PRIMARY KEY,
    neighbourhood_group VARCHAR(50),
    neighbourhood VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT
);
"""
connection.execute(text(create_table_query))
connection.commit()
table_name = 'location'
location1.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
#To avoid error
connection.execute(text("CREATE INDEX idx_location_id ON location(location_id);"))
#locatein
create_table_query = """
CREATE TABLE IF NOT EXISTS locatein (
    property_id BIGINT,
    location_id BIGINT,
    PRIMARY KEY (property_id, location_id),
    FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location(location_id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""
connection.execute(text(create_table_query))
connection.commit()
table_name = 'locatein'
locatein1.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

# Query 1: Show tables
result=connection.execute(text("SHOW TABLES;"))
tables = [row[0] for row in result.fetchall()]
print(tables)

#Query 2: Insert some values in the host table

def room_type_hash(room_type):
    if room_type == 'Entire home/apt':
        database = 0
    else:
        database = 1
    return database

def insert_record(record):
    room_type = record['room_type']
    database = 'airbnb' + str(room_type_hash(room_type))
    return database
record = {
    'property_id': 1,
    'name': 'Example Property',
    'room_type': 'Entire home/apt',
    'price': 100,
    'minimum_nights': 2,
    'availability_365': 300,
    'available_since_date': '2019-05-19'
}
database=insert_record(record)
engine = create_engine(f'mysql+pymysql://root:dsci551@localhost/{database}')
connection = engine.connect()
insert_query = f"""
    INSERT INTO property (property_id, name, room_type, price, minimum_nights, availability_365, available_since_date)
    VALUES ({record['property_id']}, '{record['name']}', '{record['room_type']}', {record['price']}, {record['minimum_nights']}, {record['availability_365']}, {record['available_since_date']} )
    """
connection.execute(text(insert_query))
connection.commit()


#cursor.close()
#connection.close()