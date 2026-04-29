import psycopg2
import json
import csv
import os
from connect import get_connection

# Absolute paths to SQL and data resources
SCHEMA_PATH = r"C:\Users\tamer\OneDrive\Documents\PP2\TSIS\TSIS1\schema.sql"
PROCEDURES_PATH = r"C:\Users\tamer\OneDrive\Documents\PP2\TSIS\TSIS1\procedures.sql"
CSV_PATH = r"C:\Users\tamer\OneDrive\Documents\PP2\TSIS\TSIS1\contact.csv"

def init_db():
    """Initializes the database schema and stored procedures from SQL files"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        for path in [SCHEMA_PATH, PROCEDURES_PATH]:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    cur.execute(f.read())
                    print(f"Migration successful: {os.path.basename(path)}")
        conn.commit()
    except Exception as e:
        print(f"Migration Failed: {e}")
        conn.rollback()
    finally:
        cur.close(); conn.close()

def search_interface():
    """Advanced search across name, email, and multiple phone numbers"""
    term = input("Search term (name/email/phone): ")
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (term,))
    results = cur.fetchall()
    for r in results:
        print(f"User: {r[0]} | Email: {r[1]} | Birthday: {r[2]} | Group: {r[3]} | Phones: {r[4]}")
    cur.close(); conn.close()

def paginate_contacts():
    """Navigation through contact list using LIMIT and OFFSET"""
    conn = get_connection(); cur = conn.cursor()
    limit, offset = 3, 0
    while True:
        cur.execute("SELECT name, email FROM contacts ORDER BY name LIMIT %s OFFSET %s", (limit, offset))
        rows = cur.fetchall()
        print("\n--- Current Page ---")
        for r in rows:
            print(f"Name: {r[0]} | Email: {r[1]}")
        cmd = input("\n[n]ext, [p]rev, [q]uit: ").lower()
        if cmd == 'n': offset += limit
        elif cmd == 'p': offset = max(0, offset - limit)
        else: break
    cur.close(); conn.close()

def export_to_json():
    """Saves database state to a JSON file"""
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts('')")
    rows = cur.fetchall()
    data = [{"name": r[0], "email": r[1], "birthday": str(r[2]), "group": r[3], "phones": r[4]} for r in rows]
    with open("contacts_export.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Exported to contacts_export.json")
    cur.close(); conn.close()

def import_from_json():
    """Imports data from JSON with duplicate check (Overwrite logic)"""
    filename = "contacts_export.json"
    if not os.path.exists(filename):
        print("JSON file not found. Run Export first.")
        return
    with open(filename, "r") as f:
        data = json.load(f)
    
    conn = get_connection(); cur = conn.cursor()
    for item in data:
        # Check if contact exists to handle overwrite logic
        cur.execute("SELECT id FROM contacts WHERE name = %s", (item['name'],))
        if cur.fetchone():
            confirm = input(f"Contact '{item['name']}' exists. Overwrite? (y/n): ")
            if confirm.lower() != 'y': continue
            cur.execute("DELETE FROM contacts WHERE name = %s", (item['name'],))
        
        # Insert using procedures
        cur.execute("CALL move_to_group(%s, %s)", (item['name'], item['group']))
        cur.execute("UPDATE contacts SET email=%s, birthday=%s WHERE name=%s", 
                    (item['email'], item['birthday'], item['name']))
        # Logic to parse phone strings back to calls would go here if needed
    conn.commit(); cur.close(); conn.close()
    print("JSON Import finished.")

def import_csv_data():
    """Imports enriched data from CSV file"""
    if not os.path.exists(CSV_PATH):
        print("CSV file not found.")
        return
    conn = get_connection(); cur = conn.cursor()
    with open(CSV_PATH, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("CALL move_to_group(%s, %s)", (row['name'], row['group']))
            cur.execute("UPDATE contacts SET email=%s, birthday=%s WHERE name=%s", 
                        (row['email'], row['birthday'], row['name']))
            cur.execute("CALL add_phone(%s, %s, %s)", (row['name'], row['phone'], row['type']))
    conn.commit(); cur.close(); conn.close()
    print("CSV Import complete.")

def main():
    while True:
        print("\n--- PHONEBOOK CONSOLE ---")
        print("1. Search           | 5. Paginated List")
        print("2. Add Phone        | 6. Export JSON")
        print("3. Move to Group    | 7. Import JSON")
        print("4. Filter by Group  | 8. Import CSV")
        print("9. RESET DATABASE   | 0. EXIT")
        choice = input("Select: ")

        if choice == "1": search_interface()
        elif choice == "2":
            n, p, t = input("Name: "), input("Num: "), input("Type: ")
            conn = get_connection(); cur = conn.cursor(); cur.execute("CALL add_phone(%s,%s,%s)", (n,p,t))
            conn.commit(); cur.close(); conn.close()
        elif choice == "3":
            n, g = input("Name: "), input("Group: ")
            conn = get_connection(); cur = conn.cursor(); cur.execute("CALL move_to_group(%s,%s)", (n,g))
            conn.commit(); cur.close(); conn.close()
        elif choice == "4":
            g = input("Group: ")
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT * FROM search_contacts('') WHERE g_name ILIKE %s", (g,))
            for r in cur.fetchall(): print(r)
            cur.close(); conn.close()
        elif choice == "5": paginate_contacts()
        elif choice == "6": export_to_json()
        elif choice == "7": import_from_json()
        elif choice == "8": import_csv_data()
        elif choice == "9": init_db()
        elif choice == "0": break

if __name__ == "__main__":
    main()