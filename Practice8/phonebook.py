from connect import get_connection

conn = get_connection()  # connect to PostgreSQL
cursor = conn.cursor()   # cursor for SQL queries

while True:
    print("\nPHONEBOOK MENU")
    print("1 - Search contacts")
    print("2 - Add or update user")
    print("3 - Insert many users")
    print("4 - Show contacts (pagination)")
    print("5 - Delete contact")
    print("0 - Exit")

    choice = input("Choose: ")

    # SEARCH
    if choice == "1":
        pattern = input("Enter search pattern: ")

        cursor.execute("SELECT * FROM search_contacts(%s)", (pattern,))
        rows = cursor.fetchall()

        for r in rows:
            print(r)

    # UPSERT USER
    elif choice == "2":
        name = input("Name: ")
        phone = input("Phone: ")

        # phone validation
        if not phone.isdigit():
            print("Incorrect number. Only digits allowed.")
            continue

        cursor.execute("CALL upsert_user(%s,%s)", (name, phone))
        conn.commit()

        print("User inserted/updated")

    # INSERT MANY USERS
    elif choice == "3":
        n = int(input("How many users: "))

        names = []
        phones = []

        for i in range(n):
            name = input("Name: ")
            phone = input("Phone: ")

            # phone validation
            if not phone.isdigit():
                print("Incorrect number.")
                continue

            names.append(name)
            phones.append(phone)

        if len(names) > 0:
            cursor.execute("CALL insert_many(%s,%s)", (names, phones))
            conn.commit()
            print("Users inserted")
        else:
            print("No valid users to insert")

    # PAGINATION
    elif choice == "4":
        limit = int(input("Limit: "))
        offset = int(input("Offset: "))

        cursor.execute("SELECT * FROM get_contacts_paginated(%s,%s)", (limit, offset))
        rows = cursor.fetchall()

        for r in rows:
            print(r)

    # DELETE
    elif choice == "5":
        value = input("Enter name or phone to delete: ")

        cursor.execute("CALL delete_contact(%s)", (value,))
        conn.commit()

        print("Deleted")

    # EXIT
    elif choice == "0":
        break


cursor.close()
conn.close()