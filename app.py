import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

# Database initialization
def init_db():
    conn = sqlite3.connect("ice_cream.db")
    cursor = conn.cursor()

    # Create tables for seasonal flavors and customer cart
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS seasonal_flavors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY,
        flavor_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (flavor_id) REFERENCES seasonal_flavors(id)
    )
    ''')

    conn.commit()
    conn.close()


# Add flavor to the database
def add_flavor(name, description):
    conn = sqlite3.connect("ice_cream.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO seasonal_flavors (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()


# Add to Cart
def add_to_cart(flavor_id, quantity):
    conn = sqlite3.connect("ice_cream.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (flavor_id, quantity) VALUES (?, ?)", (flavor_id, quantity))
    conn.commit()
    conn.close()


# View all flavors
def get_all_flavors(exclude=None):
    conn = sqlite3.connect("ice_cream.db")
    cursor = conn.cursor()
    if exclude:
        cursor.execute("SELECT * FROM seasonal_flavors WHERE name NOT LIKE ?", ('%' + exclude + '%',))
    else:
        cursor.execute("SELECT * FROM seasonal_flavors")
    flavors = cursor.fetchall()
    conn.close()
    return flavors


# View cart
def get_cart():
    conn = sqlite3.connect("ice_cream.db")
    cursor = conn.cursor()
    cursor.execute('''
    SELECT sf.name, c.quantity
    FROM cart c
    JOIN seasonal_flavors sf ON c.flavor_id = sf.id
    ''')
    cart_items = cursor.fetchall()
    conn.close()
    return cart_items


# Initialize the database and populate it with 10 sample flavors
init_db()
sample_flavors = [
    ("Vanilla", "Classic vanilla ice cream"),
    ("Chocolate", "Rich chocolate flavor"),
    ("Strawberry", "Fresh strawberry delight"),
    ("Mango", "Tropical mango flavor"),
    ("Blueberry", "Tangy blueberry treat"),
    ("Pistachio", "Nutty pistachio delight"),
    ("Butterscotch", "Caramel and butterscotch blend"),
    ("Coffee", "Creamy coffee flavor"),
    ("Mint", "Refreshing mint with chocolate chips"),
    ("Cookie Dough", "Loaded with cookie dough pieces")
]
for name, desc in sample_flavors:
    add_flavor(name, desc)


# Frontend with Tkinter
class IceCreamParlorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Frosty Delights")
        self.root.geometry("500x600")

        self.allergen = None  # To store allergen information
        self.create_welcome_screen()

    def create_welcome_screen(self):
        tk.Label(self.root, text="Welcome to Frosty Delights", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Button(self.root, text="Enter the Parlor", command=self.create_main_screen, font=("Arial", 14)).pack(pady=50)

    def create_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Available Flavors", font=("Arial", 16)).pack(pady=10)
        self.flavor_listbox = tk.Listbox(self.root, width=50, height=10)
        self.flavor_listbox.pack()

        self.refresh_flavors()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="View Cart", command=self.view_cart, width=15).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Add to Cart", command=self.add_to_cart_page, width=15).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Add Allergy", command=self.add_allergy, width=15).grid(row=0, column=2, padx=10)

    def refresh_flavors(self):
        self.flavor_listbox.delete(0, tk.END)
        flavors = get_all_flavors(self.allergen)
        for flavor in flavors:
            self.flavor_listbox.insert(tk.END, f"{flavor[1]} - {flavor[2]}")

    def add_to_cart_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Select a Flavor to Add to Cart", font=("Arial", 16)).pack(pady=10)
        self.cart_flavor_listbox = tk.Listbox(self.root, width=50, height=10)
        self.cart_flavor_listbox.pack()

        self.refresh_flavors_for_cart()

        tk.Button(self.root, text="Add to Cart", command=self.add_to_cart_action, width=15).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_screen, width=15).pack()

    def refresh_flavors_for_cart(self):
        self.cart_flavor_listbox.delete(0, tk.END)
        flavors = get_all_flavors(self.allergen)
        for flavor in flavors:
            self.cart_flavor_listbox.insert(tk.END, f"{flavor[1]} - {flavor[2]}")

    def add_to_cart_action(self):
        selected_index = self.cart_flavor_listbox.curselection()
        if selected_index:
            flavor_id = selected_index[0] + 1
            add_to_cart(flavor_id, 1)
            messagebox.showinfo("Success", "Flavor added to cart!")
        else:
            messagebox.showwarning("Selection Error", "Please select a flavor!")

    def view_cart(self):
        cart_items = get_cart()
        if cart_items:
            cart_info = "\n".join([f"{item[0]} - Quantity: {item[1]}" for item in cart_items])
            messagebox.showinfo("Your Cart", cart_info)
        else:
            messagebox.showinfo("Your Cart", "Your cart is empty!")

    def add_allergy(self):
        allergen = simpledialog.askstring("Allergy Input", "Enter an allergen (e.g., Mango):")
        if allergen:
            self.allergen = allergen
            self.refresh_flavors()
            messagebox.showinfo("Allergy Set", f"Flavors containing '{allergen}' are hidden.")


# Create the root window and run the Tkinter app
root = tk.Tk()
app = IceCreamParlorApp(root)
root.mainloop()
