import sqlite3
import sys
import os

def inspect_database(db_path):
    if not os.path.exists(db_path):
        print(f"Error: File '{db_path}' not found.")
        return

    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print("No tables found in the database.")
            return

        for table_tuple in tables:
            table_name = table_tuple[0]
            print(f"\n{1}", '='*50)
            print(f"TABLE: {table_name}")
            print('='*50)

            # 2. Get Column names, types, and constraints
            print("\n[Column Schema]")
            # pragma_table_info returns: (id, name, type, notnull, default_value, pk)
            cursor.execute(f"PRAGMA table_info('{table_name}');")
            columns = cursor.fetchall()
            
            print(f"{'ID':<3} {'Name':<20} {'Type':<20} {'NotNull':<8} {'PK':<3}")
            print("-" * 50)
            for col in columns:
                print(f"{col[0]:<3} {col[1]:<20} {col[2]:<20} {col[3]:<8} {col[5]:<3}")

            # 3. Dump most recent 20 records
            # Note: This assumes there is an auto-increment ID or RowID
            print(f"\n[Most Recent 20 Records]")
            try:
                cursor.execute(f"SELECT * FROM '{table_name}' ORDER BY ROWID DESC LIMIT 20;")
                rows = cursor.fetchall()
                
                if not rows:
                    print("Table is empty.")
                else:
                    # Print headers for the data dump
                    headers = [col[1] for col in columns]
                    print(" | ".join(headers))
                    print("-" * 50)
                    for row in rows:
                        print(row)
            except sqlite3.Error as e:
                print(f"Could not retrieve records: {e}")

        conn.close()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 inspect_db.py <path_to_db_file>")
    else:
        inspect_database(sys.argv[1])


