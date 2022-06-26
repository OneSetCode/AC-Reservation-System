from model.AC import AC
from model.Technician import Technician
from model.Customer import Customer
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymysql
import datetime

'''
objects to keep track of the currently logged-in user
It is always true that at most one of currentTechnician and currentCustomer is not null 
since only one user can be logged-in at a time
'''
current_customer = None

current_technician = None

def create_customer(tokens):
    username = tokens[0]
    password = tokens[1]

    if len(username) < 3:
        return("Invalid username, try again!")
    if len(password) < 5:
        return("Invalid password, try again!")

    if username_exists_customer(username):
        return("Username taken, try again!")
    
    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    customer = Customer(username, salt=salt, hash=hash)

    try:
        customer.save_to_db()
    except pymysql.Error as e:
        return("Failed to create user.")
        #print("Db-Error:", e)
        quit()
    except Exception as e:
        return("Failed to create user.")
        #print(e)
        return
    return("Created user: " + username)


def create_technician(tokens):
    username = tokens[0]
    password = tokens[1]

    if len(username) < 3:
        return("Invalid username, try again!")
    if len(password) < 5:
        return("Invalid password, try again!")
    # check 2: check if the username has been taken already
    if username_exists_technician(username):
        return("Username taken, try again!")
        
    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the technician
    technician = Technician(username, salt=salt, hash=hash)

    # save to technician information to our database
    try:
        technician.save_to_db()
    except pymysql.Error as e:
        return("Failed to create user.")
        quit()
    except Exception as e:
        return("Failed to create user.")
    return("Created user: " + username)


def username_exists_technician(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Technicians WHERE Username = %s"
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(select_username, username)
        # returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymysql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def username_exists_customer(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Customers WHERE Username = %s"
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(select_username, username)
        for row in cursor:
            return row['Username'] is not None
    except pymysql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_customer(tokens):
    global current_customer
    if current_technician is not None or current_customer is not None:
        return("User already logged in.")

    username = tokens[0]
    password = tokens[1]

    customer = None
    try:
        customer = Customer(username, password=password).get()
    except pymysql.Error as e:
        return("Login failed.")
        quit()
    except Exception as e:
        return("Login failed.")

    if customer is None:
        return("Login failed.")
    else:
        current_customer = customer
        return("Logged in as: " + username)  


def login_technician(tokens):
    # check 1: if someone's already logged-in, they need to log out first
    global current_technician
    if current_technician is not None or current_customer is not None:
        return("User already logged in.")

    username = tokens[0]
    password = tokens[1]

    technician = None
    try:
        technician = Technician(username, password=password).get()
    except pymysql.Error as e:
        return("Login failed.")
        quit()
    except Exception as e:
        return("Login failed.")

    # check if the login was successful
    if technician is None:
        return("Login failed.")
    else:
        current_technician = technician
        return("Logged in as: " + username)


def search_technician_schedule(tokens):
    # Check if an user has loged in
    global current_technician, current_customer
    if current_technician is None and current_customer is None:
        return("Please login first!")
    # read the date 
    date = tokens
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    get_avaiable_technician = "SELECT Username FROM Availabilities WHERE Time = %s"
    get_AC = "SELECT Brand, Quantity FROM AC"

    result = ''

    try:
        d = datetime.datetime(year, month, day)
        cursor.execute(get_avaiable_technician, d)
        result += "Available Technicians: "
        for row in cursor:
            result += str(row['Username']) + ' '
        result += '\n'
        result += "Remaining AC: "
        cursor.execute(get_AC)
        for row in cursor:
           result += str(row['Brand']) + ' ' + str(row['Quantity']) + ' '
        return (result)
    except pymysql.Error:
        return("Please try again!")
        quit()
    except ValueError:
        return("Please try again!")
    except Exception:
        return("Please try again!")
    finally:
        cm.close_connection()


def reserve(tokens):
    # check if a customer has loged in 
    global current_technician, current_customer
    if current_technician is None and current_customer is None:
        return("Please login first!")
    if current_customer is None:
        return("Please login as a customer!")
    
    date = tokens[0]
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])

    ac = tokens[1]

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    get_technician = "SELECT Username FROM Availabilities WHERE Time = %s LIMIT 1"
    get_quantity = "SELECT Quantity FROM AC WHERE Brand = %s"
    check_current = "SELECT COUNT(*) AS Count FROM Appointment WHERE Customer = %s AND Time = %s"
    make_appointment = "INSERT INTO Appointment VALUES (null, %s, %s, %s, %s)"
    update_availability = "DELETE FROM Availabilities WHERE Time = %s AND Username = %s"
    update_quantity = "UPDATE AC SET Quantity = %s WHERE Brand = %s"
    appointment_id = "SELECT AppID FROM Appointment WHERE Time = %s AND Customer = %s"
    try:
        d = datetime.datetime(year, month, day)
        cursor.execute(check_current, (current_customer.get_username(), d))
        for row in cursor:
            check = row['Count']
        if check != 0:
            return("Sorry, user already has an appointment that day!")
        cursor.execute(get_technician, d)
        for row in cursor:
            technician = row["Username"]
        if not technician:
            return("No technician is available!")
        cursor.execute(get_quantity, ac)
        for row in cursor:
            quantity = row["Quantity"] 
        if quantity == 0:
            return("Not enough available quantity!")
        cursor.execute(make_appointment, (current_customer.get_username(), d, ac, technician))
        cursor.execute(update_quantity, (quantity - 1, ac))
        cursor.execute(appointment_id, (d, current_customer.get_username()))
        for row in cursor:
            appid = row["AppID"]
        cursor.execute(update_availability, (d, technician))
        conn.commit()
        return ("Appointment ID: " + str(appid) + '\n' + "Technician username: "+ technician)
    except pymysql.Error:
        return("Please try again!")
        quit()
    except ValueError:
        return("Please try again!")
    except Exception:
        return("Please try again!")
    finally:
        cm.close_connection()


def upload_availability(tokens):
    #  upload_availability <date>
    #  check if the current logged-in user is a technician
    global current_technician
    if current_technician is None:
        return("Please login as a technician first!")

    date = tokens
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_technician.upload_availability(d)
    except pymysql.Error as e:
        return("Upload Availability Failed")
    except ValueError:
        return("Please enter a valid date!")
    except Exception as e:
        return("Error occurred when uploading availability")
    return("Availability uploaded!")


def cancel(tokens):
    # Check if an user has loged in
    global current_technician, current_customer
    if current_technician is None and current_customer is None:
        return("Please login first!")
    
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    appid = tokens
    search_appointment = "SELECT * FROM Appointment WHERE AppID = %s"
    get_quantity = "SELECT Quantity FROM AC WHERE Brand = %s"
    cancel_appointment = "DELETE FROM Appointment WHERE AppID = %s"
    update_availability = "INSERT INTO Availabilities VALUES (%s, %s)"
    update_quantity = "UPDATE AC SET Quantity = %s WHERE Brand = %s"

    try:
        cursor.execute(search_appointment, appid)
        if current_customer is not None: 
            for row in cursor:
                if row["Customer"] != current_customer.get_username():
                    return("The appointment ID does not match your name!")
                else:
                    technician = row["Technician"]
                    time = row["Time"]
                    AC = row["AC"]
            cursor.execute(cancel_appointment, appid)
            cursor.execute(get_quantity, AC)
            for row in cursor:
                quantity = row["Quantity"]
            cursor.execute(update_quantity, (quantity + 1, AC))
            cursor.execute(update_availability, (time, technician))
            conn.commit()
            return("You have successfully canceled your service by " + str(technician))
        else:
            for row in cursor:
                if row["Technician"] != current_technician.get_username():
                    return("The appointment ID does not match your name!")
                else:
                    customer = row["Customer"]
                    time = row["Time"]
            cursor.execute(cancel_appointment, appid)
            cursor.execute(update_availability, (time, current_customer.get_username()))
            conn.commit()
            return("You have successfully canceled your service for " + str(customer))
    except pymysql.Error:
        return("Please try again!")
        quit()
    except ValueError:
        return("Please try again!")
    except Exception:
        return("Please try again!")
    finally:
        cm.close_connection()

def add_quantity(tokens):
    #  add_quantity <AC> <number>
    #  check if the current logged-in user is a technician
    global current_technician
    if current_technician is None:
        return("Please login as a technician first!")

    brand = tokens[0]
    quantity = int(tokens[1])
    ac = None
    try:
        ac = AC(brand, quantity).get()
    except pymysql.Error as e:
        return("Error occurred when adding quantity")
    except Exception as e:
        return("Error occurred when adding quantity")

    # if the AC is not found in the database, add a new (AC, quantity) entry.
    # else, update the existing entry by adding the new quantity
    if ac is None:
        ac = AC(brand, quantity)
        try:
            ac.save_to_db()
        except pymysql.Error as e:
            return("Error occurred when adding quantity")
        except Exception as e:
            return("Error occurred when adding quantity")
    else:
        # if the AC is not null, meaning that the AC already exists in our table 
        try:
            ac.increase_available_quantity(quantity) 
        except pymysql.Error as e:
            return("Error occurred when adding quantity")
        except Exception as e:
            return("Error occurred when adding quantity")
    return("Quantity updated!")


def show_appointments():
    # Check if an user has loged in
    global current_technician, current_customer
    if current_technician is None and current_customer is None:
        return("Please login first!")

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    technician_app = "SELECT AppID, AC, Time, Customer FROM Appointment WHERE \
        Technician = %s ORDER BY AppID"
    customer_app = "SELECT AppID, AC, Time, Technician FROM Appointment WHERE \
        Customer = %s ORDER BY AppID"
    
    result = ''
    try:
        if current_technician is not None:
            cursor.execute(technician_app, current_technician.get_username())
            for row in cursor:
                result += "ID: " + str(row["AppID"]) + '\n' + "AC Brand: " + str(row["AC"]) + '\n' + \
                    "Date: " + str(row["Time"]) + '\n' + "Customer: " + str(row["Customer"]) + '\n' + '\n'
        if current_customer is not None:
            cursor.execute(customer_app, current_customer.get_username())
            for row in cursor:
                result += "ID: " + str(row["AppID"]) + '\n' + "AC Brand: " + str(row["AC"]) + '\n' + \
                    "Date: " + str(row["Time"]) + '\n' + "Technician: " + str(row["Technician"]) + '\n' + '\n'
        return result
    except pymysql.Error:
        return("Please try again!")
        quit()
    except ValueError:
        return("Please try again!")
    except Exception:
        return("Please try again!")
    finally:
        cm.close_connection()


def logout():
    global current_customer, current_technician
    if current_technician is None and current_customer is None:
        return("Please login first.")

    try:
        current_customer = None
        current_technician = None
    except Exception as e:
            return("Please try again!")
    return("Successfully logged out!")
