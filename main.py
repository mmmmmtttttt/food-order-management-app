# Import to sqlite3
import sqlite3
from datetime import datetime

class Foot_Order:
    def __init__(self):
        try:
            # Create Databace and Conection
            self.conn = sqlite3.connect("D:/GitHub/foot-order-management-app/foot_orders.db")
            self.cr = self.conn.cursor()
            # Create Table On Database
            self.cr.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT, age INTEGER, gander TEXT)")
            self.cr.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, class TEXT, price INTEGER)")
            self.cr.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer TEXT, class TEXT, quantity TEXT, price INTEGER, total INTEGER)")
            # Create file
            self.file_orders = open(r"D:/GitHub/foot-order-management-app/foot_orders.txt", "a")
            self.dt = datetime.now()
        except ConnectionError as co:
            print(f"Error: Conection => {co}")
        except sqlite3.OperationalError as o:
            print(f"Error: Operation => {o}")
        except FileNotFoundError as f:
            print(f"Error: File => {f}")

    def view_menu(self): # Function For Show All M
        print("Show All Items")
        self.cr.execute("SELECT * FROM items")
        self.items = self.cr.fetchall()
        if self.items:
            print('''
                            |  ID  |       Items       |   Price   |
                            ----------------------------------------
                    ''')
            for clas in self.items:
                print(f"""
                            |   {clas[0]}  |       {clas[1]}      |   {clas[2]} SR   |
                    """)
        else:
            print("No Items")
        
    def add_items(self): # Function Add Items
        print("Add New Items")
        self.count = int(input("Type count the add items: ").strip())
        self.i = 0
        while self.i < self.count:
            self.clas = input("Type New Item: ").strip().capitalize()
            self.prc = int(input("Type Price of the Item: ").strip())
            self.cr.execute("SELECT class FROM items")
            self.classes = self.cr.fetchall()
            if self.clas in self.classes:
                print("This item already exists")
            else:
                self.cr.execute("INSERT INTO items (class, price) VALUES (?, ?)", (self.clas, self.prc))
                self.conn.commit()
                print(f"New item '{self.clas}' added successfully")
        else:
            print("All items added successfully")
    
    def add_orders(self): # Function add orders
        print("Add New Order")
        self.cust = input("Type your name: ").strip().capitalize()
        self.clas = input("Type Item: ").strip().capitalize()
        self.qua = int(input("Type Quantity: ").strip())
        self.cr.execute("SELECT class, price FROM items")
        self.data = self.cr.fetchall()
        for data in self.data:
            if self.clas == data[0]:
                self.price = data[1]
                self.total = self.price * self.qua
                with open(r"D:/GitHub/foot-order-management-app/foot_orders.txt", "a") as file_orders:
                    self.file_orders.write(f"Foot Orders\n")
                    self.file_orders.write(f"Invoice" + "\n")
                    self.file_orders.write(f"Custmer: {self.cust}" + "\n")
                    self.file_orders.write(f"Item: {self.clas} - Quantity: {self.qua} - Price: {self.price} - Total: {self.total}" + "\n")
                    self.file_orders.write("=" * 30 + "\n")
                self.cr.execute("INSERT INTO orders (customer, class, quantity, price, total) VALUES (?, ?, ?, ?, ?)",
                                (self.cust, self.clas, self.qua, self.price, self.total))
                self.conn.commit()
        print(f"""
                        Invoice

                |       Items       |   Price   |
                ---------------------------------
                |   {self.clas}          |     {self.price}    |

                |   Totel           |    {self.total}    |
                """)

    def view_all_orders(self): # Function show orders
        print("Show All Orders")
        self.cr.execute("SELECT * FROM orders")
        self.orders = self.cr.fetchall()
        for order in self.orders:
            print(f"{order[0]}- customer: {order[1]} - Item: {order[2]} - Quantity: {order[3]} - Price: {order[4]} - Total: {order[5]}")
        print("This is All Orders")

    def search_order(self): # function search order
        print("Searching Order")
        self.cust = input("Type name customer return ordear: ").strip().capitalize()
        self.cr.execute("SELECT * FROM orders")
        self.orders = self.cr.fetchall()
        for order in self.orders:
            if self.cust == order[1]:
                print(f"{order[0]} - customer: {order[1]} - Item: {order[2]} - Quantity: {order[3]} - Price: {order[4]} - Total: {order[5]}")
        print(f"This is all orders of the customer: {self.cust}")

    def add_username(self): # function add username
        print("Add new username")
        self.name = input("Type your name: ").strip().capitalize()
        self.email = input("Type your email: ").strip().capitalize()
        self.password = input("Type Create password: ").strip().capitalize()
        self.age = int(input("Type your age: ").strip())
        self.gander = input("Type your gander: ").strip().capitalize()
        self.cr.execute("SELECT username FROM users")
        self.users = self.cr.fetchall()
        if self.name in self.users:
            print("This name already exists")
        else:
            self.cr.execute("INSERT INTO users (username, email, password, age, gander) VALUES (?, ?, ?, ?, ?)",
                            (self.name, self.email, self.password, self.age, self.gander))
            self.conn.commit()
            print("New user is Added successfully")
    
    def start_app(self): # Function start application
        print("Welcome to Fast food restaurant")
        print("""
                        Are you:

                1- customer
                2- user

                3- Exit

                """)
        self.choice = int(input("Type choice from (1-3): ").strip())
        if self.choice == 1:
            self.app_customer()
        elif self.choice == 2:
            self.sign_in()
        elif self.choice == 3:
            self.quit()
            return

    def sign_in(self): # Function sign in
        print("Sign in by username and password")
        self.username = input("Type your username: ").strip().capitalize()
        self.password = input("Type your password: ").strip().capitalize()
        self.cr.execute("SELECT username, password FROM users")
        self.users = self.cr.fetchall()
        for user in self.users:
            if self.username == user[0] and self.password == user[1]:
                self.app_user()

    def app_user(self): # Function app user
        print(f"Welcome '{self.username}' to Fast food restaurant")
        print(self.dt)
        while True:
            print("""
                            1- View Menu
                            2- Add User
                            3- Add Item
                            4- Add Nwe Order
                            5- View All Orders
                            6- Search Order By Customer
                            7- Sign Out
                """)
            self.choice = int(input("Type choice from (1-7): "))
            if self.choice == 1:
                self.view_menu()
            elif self.choice == 2:
                self.add_username()
            elif self.choice == 3:
                self.add_items()
            elif self.choice == 4:
                self.add_orders()
            elif self.choice == 5:
                self.view_all_orders()
            elif self.choice == 6:
                self.search_order()
            elif self.choice == 7:
                self.start_app()
            else:
                print("Pleas choice of (1-7)")

    def app_customer(self): # function app costomer
        print(f"Welcome to Fast food restaurant")
        print(self.dt)
        while True:
            print("""
                            1- View Menu
                            2- Add Nwe Order

                            3- Exit
                """)
            self.choice = int(input("Type choice from (1-2): "))
            if self.choice == 1:
                self.view_menu()
            elif self.choice == 2:
                self.add_orders()
            elif self.choice == 3:
                self.start_app()
            else:
                print("Pleas choice of (1-2)")

    def quit(self): # Function exit
        self.conn.commit()
        self.cr.close()
        self.conn.close()
        self.file_orders.close()
        print("The App is Closed")

# if __name__ == "__main__":

#     start = Foot_Order()
#     start.start_app()

start = Foot_Order()
start.start_app()