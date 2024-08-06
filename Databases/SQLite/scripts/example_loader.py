import sqlite3
import random
from Databases.SQLite.scripts.sqlite_connect import connect_to_sqlite

# List of sample menu items
menu_items_list = [
    'Beans', 'TV', 'Shirts', 'Shoes', 'Books', 'Laptops', 'Phones', 'Headphones', 
    'Watches', 'Bags', 'Sunglasses', 'Chairs', 'Tables', 'Notebooks', 'Pens', 
    'Backpacks', 'Coffee Makers', 'Microwaves', 'Blenders', 'Toasters', 'Fridges', 
    'Washing Machines', 'Dryers', 'Vacuum Cleaners', 'Air Conditioners', 'Fans', 
    'Heaters', 'Kettles', 'Cookers', 'Ovens', 'Cameras', 'Printers', 'Monitors', 
    'Keyboards', 'Mice', 'Mouse Pads', 'Speakers', 'Microphones', 'Webcams', 
    'Smartphones', 'Tablets', 'Game Consoles', 'Games', 'DVD Players', 'Blu-ray Players', 
    'Projectors', 'Home Theaters', 'Wireless Chargers', 'Power Banks', 'Cases', 
    'Cables', 'Adapters', 'External Hard Drives', 'USB Flash Drives', 'Memory Cards'
]

def create_table(conn):

    cursor = conn.cursor()

    cursor.execute('''DROP TABLE IF EXISTS menu_items''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        SOURCE_SYSTEM TEXT DEFAULT 'TEST_DATA',
        CREATED_DATETIME TEXT DEFAULT (datetime('now')),
        MENU_ITEM_NAME TEXT NOT NULL,
        OPERATION_ID INTEGER
    )
    ''')

def insert_record(conn, menu_item_name):
    # insert a record with a random OPERATION_ID
    cursor = conn.cursor()

    random_operation_id = random.randint(1, 1000)  # Random integer between 1 and 1000
    try:
        cursor.execute('''
        INSERT INTO menu_items (MENU_ITEM_NAME, OPERATION_ID)
        VALUES (?, ?)
        ''', (menu_item_name, random_operation_id))
        conn.commit()
    except sqlite3.IntegrityError:
        # Record already exists, so we skip insertion
        pass

def run_script():
    conn = connect_to_sqlite()
    create_table(conn)
    for _ in range(50):
        menu_item_name = random.choice(menu_items_list)  # Randomly select an item from the list
        insert_record(conn, menu_item_name)
    conn.close()

if __name__ == "__main__":
    run_script()