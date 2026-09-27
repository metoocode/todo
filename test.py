import mysql.connector
import pandas as pd
from tabulate import tabulate
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

# Database connection details
HOST = "localhost"
USER = "amit"
PASSWORD = "password"
DATABASE = "enrollmentfile"

# Data type mapping for user input
data_types = {
    "int": "INT",
    "varchar": "VARCHAR",
    "text": "TEXT",
    "date": "DATE",
}

def connect_db():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
def save_table_with_counts_per_column(table_name, file_name, heading="Table Data"):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        if headers[0].strip() == '':
            headers[0] = "ID"
        df = pd.DataFrame(rows, columns=headers)
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Deleted existing file: {file_name}")
        df.to_excel(file_name, index=False, startrow=2)
        wb = load_workbook(file_name)
        ws = wb.active
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
        heading_cell = ws.cell(row=1, column=1)
        heading_cell.value = heading
        heading_cell.font = Font(bold=True, size=16)
        heading_cell.alignment = Alignment(horizontal='center', vertical='center')
        thick_border = Border(bottom=Side(style='thick'))
        for col in range(1, len(headers) + 1):
            ws.cell(row=1, column=col).border = thick_border
        thick_border = Border(
            left=Side(style='thick'), 
            right=Side(style='thick'), 
            top=Side(style='thick'), 
            bottom=Side(style='thick')
        )
        header_font = Font(bold=True, size=12)
        center_alignment = Alignment(horizontal='center', vertical='center')
        for col_num, column_title in enumerate(headers, start=1):
            max_length = max(len(str(column_title)), max(len(str(row[col_num - 1])) for row in rows))
            column_letter = get_column_letter(col_num)
            ws.column_dimensions[column_letter].width = max_length + 2
            cell = ws.cell(row=3, column=col_num)
            cell.font = header_font
            cell.alignment = center_alignment
            cell.border = thick_border
        for row_num, row_data in enumerate(rows, start=4):
            for col_num, value in enumerate(row_data, start=1):
                cell = ws.cell(row=row_num, column=col_num)
                cell.value = value
                cell.alignment = center_alignment
                cell.border = thick_border
        summary_start_row = len(rows) + 4
        summary_start_col = 2
        for idx, header in enumerate(headers):
            total_count = len(df[header])
            similar_counts = df[header].value_counts()
            similar_counts = similar_counts[similar_counts > 1]
            similar_counts.font = Font(bold=True)
            count_cell = ws.cell(row=summary_start_row, column=summary_start_col)
            count_cell.value = f"{header} contains {total_count}"
            count_cell.font = Font(bold=True)
            count_cell.alignment = Alignment(horizontal='left', vertical='center')
            
            summary_row = summary_start_row + 1
            for name, count in similar_counts.items():
                similar_name_cell = ws.cell(row=summary_row, column=summary_start_col + 1)
                similar_name_cell.value = f"{name} = {count} similar"
                similar_name_cell.alignment = Alignment(horizontal='center', vertical='center')
                
                summary_row += 1
                  
            summary_start_row = summary_row + 0
        wb.save(file_name)
        print(f"Data with counts saved to {file_name}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
def create_database():
    try:
        conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
        cursor = conn.cursor()
        database_name = input("Enter the name of the new database: ")
        if not database_name.isalnum():
            print("Invalid database name.")
            return
        cursor.execute(f"CREATE DATABASE {database_name};")
        print(f"Database '{database_name}' created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def create_table():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        table_name = input("Enter the name of the new table: ")
        columns = []
        num_columns = int(input("Enter the number of columns: "))
        primary_key_column = None 
        for i in range(num_columns):
            column_name = input(f"Enter the name of column {i+1}: ")
            column_type = input(f"Enter the data type for '{column_name}': ")
            mysql_type = data_types.get(column_type.lower())
            if mysql_type is None:
                print("Invalid data type.")
                return
            if mysql_type == "VARCHAR":
                column_length = input(f"Enter the maximum length for '{column_name}' (VARCHAR): ")
                mysql_type = f"VARCHAR({column_length})"  # Add length to VARCHAR
            is_primary_key = input(f"Is '{column_name}' a primary key? (yes/no): ").lower()
            if is_primary_key == 'yes':
                if primary_key_column is not None:
                    print("Error: Only one column can be a primary key.")
                    return
                primary_key_column = column_name 
                columns.append(f"{column_name} {mysql_type} PRIMARY KEY")
            else:
                columns.append(f"{column_name} {mysql_type}")
        columns_definition = ", ".join(columns)
        cursor.execute(f"CREATE TABLE {table_name} ({columns_definition});")
        conn.commit()
        print(f"Table '{table_name}' created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
def insert_data(table_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [col[0] for col in cursor.fetchall()]
        print(f"Columns in '{table_name}': {', '.join(columns)}")
        num_rows = int(input("\nEnter the number of rows you want to insert: "))
        for row in range(num_rows):
            print(f"\nInserting row {row + 1}...")
            values = [input(f"Enter the value for '{col}': ") for col in columns]
            placeholders = ", ".join(["%s"] * len(columns))
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(insert_query, tuple(values))
        conn.commit()
        print(f"\n{num_rows} rows inserted successfully into table '{table_name}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def update_data(table_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        identifier_input = input("Enter the person's name or roll number: ")
        try:
            identifier_value = int(identifier_input)
            condition = "roll = %s"
        except ValueError:
            condition = "name = %s"
            identifier_value = identifier_input
        column_to_update = input("Enter the column name to update: ")
        new_value = input(f"Enter the new value for '{column_to_update}': ")
        update_query = f"UPDATE {table_name} SET {column_to_update} = %s WHERE {condition}"
        cursor.execute(update_query, (new_value, identifier_value))
        conn.commit()
        print(f"Data updated successfully in table '{table_name}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def show_tables():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if tables:
            print("\nTables in the database:")
            for table in tables:
                print(table[0])
                
        else:
            print("No tables found in the database.")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def show_data(table_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        df = pd.DataFrame(result, columns=columns)
        print(tabulate(df, headers='keys', tablefmt='grid'))
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def add_column(table_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        column_name = input("Enter the new column name: ")
        column_type = input("Enter the data type for the new column: ")
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
        conn.commit()
        print(f"Column '{column_name}' added to table '{table_name}' successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def delete_column(table_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        column_name = input("Enter the column name to delete: ")
        cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")
        conn.commit()
        print(f"Column '{column_name}' deleted from table '{table_name}' successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def delete_row(table_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        condition_column = input("Enter the column to use for the deletion condition: ")
        condition_value = input(f"Enter the value for '{condition_column}' to identify the row(s) to delete: ")
        cursor.execute(f"DELETE FROM {table_name} WHERE {condition_column} = %s", (condition_value,))
        conn.commit()
        deleted_rows = cursor.rowcount
        print(f"{deleted_rows} row(s) deleted from table '{table_name}' successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def delete_value(table_name):
    conn = connect_db()
    if conn is None:
        return  # Exit if connection failed
    
    try:
        cursor = conn.cursor()
        column_name = input("Enter the column name to set to NULL: ")
        
        # Check if the user wants to delete all rows (no condition).
        if input("Delete all rows (y/n)? ").lower() == 'y':
            cursor.execute(f"UPDATE {table_name} SET {column_name} = NULL")
        else:
           # Prompt for the column name for updating rows if condition is needed
            condition_column = input("Enter the column to use for the condition (leave blank if no condition is needed): ")
            if condition_column:  # Check if condition column was entered
              condition_value = input(f"Enter the value for '{condition_column}': ")
              cursor.execute(f"UPDATE {table_name} SET {column_name} = NULL WHERE {condition_column} = %s", (condition_value,))
            else:
                print("No condition specified. Updating all rows in the column.")
                cursor.execute(f"UPDATE {table_name} SET {column_name} = NULL")
                
        conn.commit()
        if input("Delete all rows (y/n)? ") == 'y':
            print(f"All values in column '{column_name}' set to NULL.")
        else:
            print(f"Value(s) in column '{column_name}' set to NULL.")


    except mysql.connector.Error as err:
        print(f"Error updating database: {err}")
        try:
            conn.rollback()
            print("Transaction rolled back.")
        except Exception as e:
            print(f"Error rolling back transaction: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

import mysql.connector

def connect_db():
    # Function to establish database connection
    return mysql.connector.connect(
        host="localhost",  # Update with your DB host
        user="amit",  # Update with your DB user
        password="password",  # Update with your DB password
        database="enrollmentfile"  # Update with your DB name
    )
def save_table_with_counts_per_column(table_name, file_name, heading="Table Data"):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        if headers[0].strip() == '':
            headers[0] = "ID"
        df = pd.DataFrame(rows, columns=headers)
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Deleted existing file: {file_name}")
        df.to_excel(file_name, index=False, startrow=2)
        wb = load_workbook(file_name)
        ws = wb.active
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
        heading_cell = ws.cell(row=1, column=1)
        heading_cell.value = heading
        heading_cell.font = Font(bold=True, size=16)
        heading_cell.alignment = Alignment(horizontal='center', vertical='center')
        thick_border = Border(bottom=Side(style='thick'))
        for col in range(1, len(headers) + 1):
            ws.cell(row=1, column=col).border = thick_border
        thick_border = Border(
            left=Side(style='thick'), 
            right=Side(style='thick'), 
            top=Side(style='thick'), 
            bottom=Side(style='thick')
        )
        header_font = Font(bold=True, size=12)
        center_alignment = Alignment(horizontal='center', vertical='center')
        for col_num, column_title in enumerate(headers, start=1):
            max_length = max(len(str(column_title)), max(len(str(row[col_num - 1])) for row in rows))
            column_letter = get_column_letter(col_num)
            ws.column_dimensions[column_letter].width = max_length + 2
            cell = ws.cell(row=3, column=col_num)
            cell.font = header_font
            cell.alignment = center_alignment
            cell.border = thick_border
        for row_num, row_data in enumerate(rows, start=4):
            for col_num, value in enumerate(row_data, start=1):
                cell = ws.cell(row=row_num, column=col_num)
                cell.value = value
                cell.alignment = center_alignment
                cell.border = thick_border
        summary_start_row = len(rows) + 4
        summary_start_col = 2
        for idx, header in enumerate(headers):
            total_count = len(df[header])
            similar_counts = df[header].value_counts()
            similar_counts = similar_counts[similar_counts > 1]
            similar_counts.font = Font(bold=True)
            count_cell = ws.cell(row=summary_start_row, column=summary_start_col)
            count_cell.value = f"{header} contains {total_count}"
            count_cell.font = Font(bold=True)
            count_cell.alignment = Alignment(horizontal='left', vertical='center')
            
            summary_row = summary_start_row + 1
            for name, count in similar_counts.items():
                similar_name_cell = ws.cell(row=summary_row, column=summary_start_col + 1)
                similar_name_cell.value = f"{name} = {count} similar"
                similar_name_cell.alignment = Alignment(horizontal='center', vertical='center')
                
                summary_row += 1
                  
            summary_start_row = summary_row + 0
        wb.save(file_name)
        print(f"Data with counts saved to {file_name}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
def manage_class_data( admin_name ): 
    db = connect_db()
    cursor = db.cursor()

    # Ensure the `granted` table exists
    table_name = "granted"
    check_table_query = f"""
    SELECT COUNT(*)
    FROM information_schema.tables
    WHERE table_schema = DATABASE() AND table_name = '{table_name}';
    """
    cursor.execute(check_table_query)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        # Create the table
        create_table_query = f"""
        CREATE TABLE {table_name} (
            admin VARCHAR(222),
            class VARCHAR(223)
        );
        """
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created.")

        # Insert default row
        insert_default_query = f"INSERT INTO {table_name} (admin, class) VALUES (%s, %s);"
        cursor.execute(insert_default_query, ("amit", "22"))
        db.commit()
        print("Default row ('amit', '22') inserted into 'granted' table.")
    else:
        print(f"Table '{table_name}' already exists.")
    # Ask for admin username (no password)
    

    # Query to check if the admin exists and fetch granted classes
    
    query = "SELECT class FROM granted WHERE admin = %s"
    cursor.execute(query, (admin_name,))

    # Fetch the result
    result = cursor.fetchall()

    if result:
        granted_classes = [row[0] for row in result]  # Fetch all granted classes for this admin
        print(f"Admin '{admin_name}' has access to the following classes: {', '.join(map(str, granted_classes))}")

        # List all tables in the database
        cursor.execute("SHOW TABLES;")
        tables = [table[0] for table in cursor.fetchall()]

        # Filter the tables that match the granted classes (e.g., class_2, class_3, amit1)
        accessible_tables = [table for table in tables if table in granted_classes]

        if not accessible_tables:
         print(f"No tables available for admin '{admin_name}'.")
        else:
    # Print all available tables for the admin
         print(f"Available tables in the database for admin '{admin_name}':")
         for table in accessible_tables:
          print(f"- {table}")
            
        
        # Print only the accessible tables based on granted classes
        print(f"\nTables available for {admin_name} to manage:")
        print(f"{', '.join(accessible_tables)}")

        table_name = input("Enter the table you want to manage: ")

        if table_name not in accessible_tables:
            print("Invalid table selection. You don't have access to this table.")
            return

        # Check if the table exists in the database
        cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
        if cursor.fetchone() is None:
            print("Table does not exist.")
            return
        else:
            print(f"Managing table: {table_name}")
            while True:
                print("\nDatabase Operations:")
                print("1. Create Database")
                print("2. Create Table")
                print("3. Insert Data")
                print("4. Update Data")
                print("5. Show Data from Table")
                print("6. Show Tables")
                print("q. Quit")

                command = input("Enter your choice: ")

                if command == "1":
                    print("Creating a database...")
                    create_database()
                    # create_database() - already defined elsewhere
                elif command == "2":
                    print("Creating a table...")
                    show_tables()
                    create_table()
                    # create_table() - already defined elsewhere
                elif command == "3":
                    
                    show_data(table_name)
                    insert_data(table_name)
                    
                elif command == "4":
                    
                    what_todo = input("""
                                      1. Add column
                                     2. Delete row
                                     3. Delete column
                                     4. Delete value
                                    5. Update data
                                    """)
                    if what_todo == "1":
                        add_column(table_name)
                        show_data(table_name)
                    elif what_todo == "2":
                        delete_row(table_name)
                        show_data(table_name)
                    elif what_todo == "3":
                         delete_column(table_name)
                         show_data(table_name)
                    elif what_todo == "4":
                       delete_value(table_name)
                       show_data(table_name)
                    elif what_todo == "5":
                        update_data(table_name)
                        show_data(table_name)
                elif command == "5":
                    
                    show_data(table_name)
                elif command == "6":
                   show_tables()
                elif command.lower() == "q":
                     file_name = input("Enter the file name: ") + ".xlsx"
                
                     save_table_with_counts_per_column(table_name, file_name)
                     os.startfile(file_name)
                     break
                else:
                     print("Invalid command. Please try again.")
                file_name = input("Enter the file name: ") + ".xlsx"
                
                save_table_with_counts_per_column(table_name, file_name)
                os.startfile(file_name) 
    else:
        print(f"Admin '{admin_name}' does not exist in the granted table.")

        # Optionally: Create new admin
        insert_query = "INSERT INTO granted (admin, class) VALUES (%s, %s)"
        cursor.execute(insert_query, (admin_name, ''))  # Create with empty allowed classes
        db.commit()
        print("New admin account created.")
               
    # Close the connection
    cursor.close()
    db.close()
def view_only_access():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # List available tables
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print("\nAvailable tables (View-Only):")
        for i, table in enumerate(tables, start=1):
            print(f"{i}. {table}")
        
        # Allow user to choose a table
        table_index = int(input("\nEnter the number corresponding to the table you want to view: ")) - 1
        if table_index < 0 or table_index >= len(tables):
            print("Invalid selection. Exiting...")
            return
        selected_table = tables[table_index]
        print(f"\nYou selected: {selected_table}")

        # View-only data display
        print("\nDisplaying data in the selected table:")
        show_data(selected_table)

        print("\nYou have view-only access. No modifications allowed.")
        input("Press Enter to return to the main menu...")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
def por():
             table_name1 = ("granted", "user1")
             try:
                 r = int(input("Enter 1 for table 'granted' and 2 for 'user1': ")) - 1  # Convert input to 0-based index
                 if r < 0 or r >= len(table_name1):
                     raise ValueError
                 table_name = table_name1[r]
                 print(f"You selected: {table_name}")
             except (ValueError, IndexError):
               print(f"Invalid choice. Please choose from {', '.join(table_name1)}.")


             while True:
                print("\nDatabase Operations:")
                print("1. Create Database")
                print("2. Create Table")
                print("3. Insert Data")
                print("4. Update Data")
                print("5. Show Data from Table")
                print("6. Show Tables")
                print("q. Quit")
                command = input("Enter your choice: ")
                if command == "1":
                      print("Creating a database...")
                      create_database()
                # create_database() - already defined elsewhere
                elif command == "2":

                    print("Creating a table...")
                    show_tables()
                    create_table()
                # create_table() - already defined elsewhere

                elif command == "3":
                   show_data(table_name)
                   insert_data(table_name)
                elif command == "4":
                    what_todo = input("""
                                     1. Add column
                                      2. Delete row
                                     3. Delete column
                                        4. Delete value
                                     5. Update data
                                           """)
                    if what_todo == "1":
                          add_column(table_name)
                          show_data(table_name)
                    elif what_todo == "2":
                         delete_row(table_name)
                         show_data(table_name)
                    elif what_todo == "3":
                          delete_column(table_name)
                          show_data(table_name)
                    elif what_todo == "4":
                          delete_value(table_name)
                          show_data(table_name)
                    elif what_todo == "5":
                        update_data(table_name)
                        show_data(table_name)
                elif command == "5":
                      show_data(table_name)
                elif command == "6":
                      show_tables()
                elif command.lower() == "q":
                     break
                else:
   
                     print("Invalid command. Please try again.")         
def check10():
             db = connect_db()
             cursor = db.cursor()
             table_name = "user1"
             check_table_query = f"""
             SELECT COUNT(*)
             FROM information_schema.tables
             WHERE table_schema = DATABASE() AND table_name = '{table_name}';
             """
             cursor.execute(check_table_query)
             table_exists = cursor.fetchone()[0]

             if not table_exists:
                 # Create the table
                 create_table_query = f"""
                 CREATE TABLE {table_name} (
                     admin VARCHAR(222),
                     adminpass VARCHAR(223)
                 );
                 """
                 cursor.execute(create_table_query)
                 print(f"Table '{table_name}' created.")
         
                 # Insert default row
                 insert_default_query = f"INSERT INTO {table_name} (admin, class) VALUES (%s, %s);"
                 cursor.execute(insert_default_query, ("amit", "22"))
                 db.commit()
                 print("Default row ('amit', '3739') inserted into 'granted' table.")
                 
             else:
                  print(f"Table '{table_name}' already exists.") 
                  
                  
        

             # Ensure the `granted` table exists
             table_name = "granted"
             check_table_query = f"""
             SELECT COUNT(*)
             FROM information_schema.tables
             WHERE table_schema = DATABASE() AND table_name = '{table_name}';
             """
             cursor.execute(check_table_query)
             table_exists = cursor.fetchone()[0]

             if not table_exists:
                 # Create the table
                 create_table_query = f"""
                 CREATE TABLE {table_name} (
                     admin VARCHAR(222),
                     class VARCHAR(223)
                 );
                 """
                 cursor.execute(create_table_query)
                 print(f"Table '{table_name}' created.")
         
                 # Insert default row
                 insert_default_query = f"INSERT INTO {table_name} (admin, class) VALUES (%s, %s);"
                 cursor.execute(insert_default_query, ("amit", "22"))
                 db.commit()
                 print("Default row ('amit', '22') inserted into 'granted' table.")
                 por()
             else:
                  print(f"Table '{table_name}' already exists.") 
                  por()
                  return
             cursor.close()                        
def login():
    aaab= input("enter you role\n")
    if aaab =="teacher":
        ask= input ("your want to change  the data\n")
        if ask =="yes":
            import mysql.connector

# Establish connection to MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="amit",
                password="password",
                database="enrollmentfile"
                
            )
            db = connect_db()
            cursor = db.cursor()
            table_name = "user1"
            check_table_query = f"""
             SELECT COUNT(*)
             FROM information_schema.tables
             WHERE table_schema = DATABASE() AND table_name = '{table_name}';
             """
            cursor.execute(check_table_query)
            table_exists = cursor.fetchone()[0]

            if not table_exists:
                 # Create the table
                 create_table_query = f"""
                 CREATE TABLE {table_name} (
                     admin VARCHAR(222),
                     adminpass VARCHAR(223)
                 );
                 """
                 cursor.execute(create_table_query)
                 print(f"Table '{table_name}' created.")
         
                 # Insert default row
                 insert_default_query = f"INSERT INTO {table_name} (admin, class) VALUES (%s, %s);"
                 cursor.execute(insert_default_query, ("amit", "22"))
                 db.commit()
                 print("Default row ('amit', '3739') inserted into 'granted' table.")
                 
            else:
                  print(f"Table '{table_name}' already exists.")     
            cursor = db.cursor()
            global admin_name  
# Ask for admin credentials from the user
            admin_name = input("Enter admin username: ..\n")
            
            admin_password = input("Enter admin password:..\n ")

# Query to check if the admin exists
            query = "SELECT * FROM user1"
            cursor.execute(query)
            
# Fetch all results
            results = cursor.fetchall()

# Flag to track if admin exists and password is correct
            admin_found = False

# Iterate through all rows and check admin credentials
            for row in results:
                admin = row[0]  # First column: admin (username)
                admipass = row[1]  # Second column: adminpass (password)

                if admin_name == admin:
                    admin_found = True
                    if admin_password == admipass:
                        print("Admin credentials are correct.")
                        manage_class_data(admin_name)
                        return
                    else:
                        print("Incorrect password.")
                        break

# If admin doesn't exist, prompt to create a new admin
            if not admin_found:
                print("Admin does not exist. Creating a new admin account...")
    
    # Query to create a new admin
                insert_query = "INSERT INTO user1 (admin, adminpass) VALUES (%s, %s)"
                cursor.execute(insert_query, (admin_name, admin_password))
                db.commit()
                print("New admin account created.")

# Close the connection
            cursor.close()
            db.close()
        else:
            view_only_access()
    elif aaab =="noname":
        print ("password")
        dd=input("Enter the password: ")
        pasx="aj+123098"
        if dd == pasx:
            c=r"C:\Users\91935\Documents\c++\python\lib\__phello__\ham\__pycache__\photo_2025-03-11_17-54-36.jpg"
            os.startfile(c)
        else:     
            print("password is incorrect")
            return   
    elif aaab =="manager":  
        passcode = input("Enter the passcode: ")
        if passcode == "admin123":      
             check10()
    else:
        print("you are not a teacher")
        return        
login()            