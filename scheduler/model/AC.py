import sys
sys.path.append("../db/*")
from db.ConnectionManager import ConnectionManager
import pymysql


class AC:
    def __init__(self, brand, quantity):
        self.brand = brand
        self.quantity = quantity

    def get(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        get_AC = "SELECT Brand, Quantity FROM AC WHERE Brand = %s"
        try:
            cursor.execute(get_AC, self.brand)
            for row in cursor:
                self.quantity = row[1]
                return self
        except pymysql.Error:
            print("Error occurred when getting AC")
            raise
        finally:
            cm.close_connection()
        return None

    def get_AC_brand(self):
        return self.brand

    def get_available_quantity(self):
        return self.quantity

    def save_to_db(self):
        if self.quantity is None or self.quantity <= 0:
            raise ValueError("Argument cannot be negative!")

        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_quantity = "INSERT INTO AC VALUES (%s, %s)"
        try:
            cursor.execute(add_quantity, (self.brand, self.quantity))
            conn.commit()
        except pymysql.Error:
            print("Error occurred when insert AC")
            raise
        finally:
            cm.close_connection()

    # Increment the available quantity
    def increase_available_quantity(self, num):
        if num <= 0:
            raise ValueError("Argument cannot be negative!")
        self.quantity += num

        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        update_AC_availability = "UPDATE AC SET Quantity = %s WHERE Brand = %s"
        try:
            cursor.execute(update_AC_availability, (self.quantity, self.brand))
            conn.commit()
        except pymysql.Error:
            print("Error occurred when updating AC availability")
            raise
        finally:
            cm.close_connection()

    # Decrement the available quantity 
    def decrease_available_quantity(self, num):
        if self.quantity - num < 0:
            ValueError("Not enough available quantity!")
        self.quantity -= num

        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        update_AC_availability = "UPDATE AC SET Quantity = %s WHERE Brand = %s"
        try:
            cursor.execute(update_AC_availability, (self.quantity, self.brand))
            conn.commit()
        except pymysql.Error:
            print("Error occurred when updating AC availability")
            raise
        finally:
            cm.close_connection()

    def __str__(self):
        return f"(AC Brand: {self.brand}, Available Quantity: {self.quantity})"
