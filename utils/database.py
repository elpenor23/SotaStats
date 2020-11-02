#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode

def connect_to_db():
    """ connects to the db """
    try:
        db = mysql.connector.connect(user='user',
                                password='*****',
                                host='localhost',
                                database='sota_stats')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return db

def add_activation_record(activation_date, 
                        activation_callsign,
                        summit_association_code,
                        summit_region_code,
                        summit_code, 
                        summit_name, 
                        summit_points, 
                        activation_number_of_qso):
    """ Adds record to the DB """

    query = ("INSERT INTO raw_activator_data "
            "(activation_date, activation_callsign, summit_association_code, summit_region_code, summit_code, summit_name, summit_points, activation_number_of_qso) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

    data = (activation_date, activation_callsign, summit_association_code, summit_region_code, summit_code, summit_name, summit_points, activation_number_of_qso)

    db = connect_to_db()
    cursor = db.cursor()

    try:
        cursor.execute(query, data)
        db.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        print("Query: " + query)
        print("Data: " + str(data))

    cursor.close()
    db.close()
