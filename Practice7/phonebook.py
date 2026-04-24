import csv
from connect import get_connection #connect function for connection data base 
def create_table():# create table  phonebook in database phonebook
    conn = get_connection()
    cursor = conn.cursor() # create a cursor for Sql commandes
    cursor.execute(
    """CREATE TABLE IF NOT EXISTS phonebook(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        UNIQUE(name, phone)
    );
    """
    )
    conn.commit()
    cursor.close()
    conn.close()
def import_csv(filename='C:/Users/tamer/OneDrive/Documents/PP2/Practice7/contacts.csv'):
    conn = get_connection()
    cursor = conn.cursor()

    with open(filename, 'r', encoding='utf-8') as f:  # open csv file
        reader = csv.DictReader(f)  # read csv as dictionary

        for row in reader:
            name = row.get('name')
            phone = row.get('phone')

            if name and phone:  # check data exists
                cursor.execute(
                    "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
                    (name, phone)
                )

    conn.commit()
    cursor.close()
    conn.close()
def add_contact():
    name = input("Enter name:")
    phone = input("Enter phone: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s);", #add name and phone 
        (name, phone)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Contact {name} added!")
def delete_contact():
    name = input("Enter name for delete: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM phonebook WHERE name = %s;",#delete contact with name
        (name,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Contact {name} deleted!")
def show_contacts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM phonebook;")
    rows = cursor.fetchall() #get result list of tuples
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    cursor.close()
    conn.close()
def update_contacts():
    name = input("Enter name for update: ")  
    new_phone = input("Enter new phone: ")  

    conn = get_connection() 
    cursor = conn.cursor()  

    cursor.execute(
        "UPDATE phonebook SET phone = %s WHERE name = %s;",
        (new_phone, name)
    )

    conn.commit()
    if cursor.rowcount == 0:
        print("Contact not found")
    else:
        print(f"Contact {name} updated!") 
    cursor.close()
    conn.close() 
def search_contact():
    name = input("Enter name to search: ")

    conn = get_connection()
    cursor = conn.cursor() 

    cursor.execute(
        "SELECT id, name, phone FROM phonebook WHERE name = %s;", 
        (name,)
        )
    rows = cursor.fetchall()

    if rows:  
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("Contact not found")

    cursor.close()
    conn.close()
if __name__ == "__main__":
    create_table() 
    import_csv() 
    show_contacts()
    while True:
        print("\nMenu: 1-Add, 2-Delete, 3-Show all contacts, 4-Update contact,5-Search contact,6-exit")
        choice = input("select an action: ")
        if choice == "1":
            add_contact()
        elif choice == "2":
            delete_contact()
        elif choice == "3":
            show_contacts()
        elif choice == "4":
            update_contacts()
        elif choice == "5":
            search_contact()
        elif choice == "6":
            break
        else:
            print("Error")


