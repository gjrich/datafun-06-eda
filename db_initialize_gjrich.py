# creates a .db file from a #CSV file

import sqlite3
import pathlib


# Import from external packages
import pandas as pd
import os
from datetime import datetime

# Define paths using joinpath
db_file_path = pathlib.Path("project.db")
data_folder_path = pathlib.Path("data")

def verify_and_create_folders(paths):
    """Verify and create folders if they don't exist."""
    for path in paths:
        folder = path.parent
        if not folder.exists():
            print(f"Creating folder: {folder}")
            folder.mkdir(parents=True, exist_ok=True)
        else:
            print(f"Folder already exists: {folder}")
            

def create_database(db_path):
    """Create a new SQLite database file if it doesn't exist."""
    try:
        conn = sqlite3.connect(db_path)
        conn.close()
        print("Database created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating the database: {e}")

def generate_create_table_sql(table_name, df):
    """Generate a CREATE TABLE SQL statement based on the DataFrame structure."""
    columns = []
    for column in df.columns:
        # Inferring column data types (you can refine this if needed)
        if pd.api.types.is_integer_dtype(df[column]):
            col_type = "INTEGER"
        elif pd.api.types.is_float_dtype(df[column]):
            col_type = "REAL"
        else:
            col_type = "TEXT"
        columns.append(f"{column.replace(' ', '_')} {col_type}")

    # Create table with id as the primary key
    columns_sql = ",\n    ".join(columns)
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {columns_sql}
    );
    """
    return create_table_sql

def insert_data_from_csv(db_path, csv_file_path):
    """Read data from CSV files and insert the records into their respective tables."""
    try:
        table_name = csv_file_path.stem  # Use the CSV filename (without extension) as table name
        df = pd.read_csv(csv_file_path)

        # Generate and execute the CREATE TABLE statement
        create_table_sql = generate_create_table_sql(table_name, df)

        with sqlite3.connect(db_path) as conn:
            conn.execute(create_table_sql)
            df.to_sql(table_name, conn, if_exists="append", index=False)
            print(f"Data from {csv_file_path} inserted successfully into {table_name}.")

    except (sqlite3.Error, pd.errors.EmptyDataError, FileNotFoundError) as e:
        print(f"Error inserting data from {csv_file_path}: {e}")

def get_recent_csv_files(directory, limit=10):
    """Get a list of recently modified CSV files in the 'data' directory."""
    csv_files = list(directory.glob("*.csv"))
    csv_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)  # Sort by modification time
    return csv_files[:limit]

def prompt_for_manual_selection(csv_files, max_selections=10):
    """Prompt the user to select CSV files manually for import."""
    selected_files = []
    print("Select up to 10 CSV files to import (enter the number):")
    for i, csv_file in enumerate(csv_files):
        print(f"{i + 1}: {csv_file.name} (Last modified: {datetime.fromtimestamp(csv_file.stat().st_mtime)})")

    while len(selected_files) < max_selections:
        choice = input(f"Enter the number of the file to import (or press enter to stop): ")
        if not choice:
            break
        try:
            selected_file = csv_files[int(choice) - 1]
            selected_files.append(selected_file)
            print(f"Selected: {selected_file.name}")
        except (IndexError, ValueError):
            print("Invalid choice. Please enter a valid number.")

    return selected_files

def main():
    # Ensure that the data folder exists
    verify_and_create_folders([data_folder_path])

    # Create the database
    create_database(db_file_path)

    # Prompt user for import option
    import_option = input("Enter 'a' for automatic import or 'm' for manual import: ").lower()

    if import_option == 'a':
        # Automatic import: Use the 10 most recently modified CSV files in the 'data' directory
        csv_files = get_recent_csv_files(data_folder_path, limit=10)
        print("Automatically importing the following files:")
        for csv_file in csv_files:
            print(f"  - {csv_file.name}")
            insert_data_from_csv(db_file_path, csv_file)
    elif import_option == 'm':
        # Manual import: Prompt the user to select CSV files to import
        csv_files = get_recent_csv_files(data_folder_path, limit=50)
        selected_files = prompt_for_manual_selection(csv_files, max_selections=10)
        for csv_file in selected_files:
            insert_data_from_csv(db_file_path, csv_file)
    else:
        print("Invalid option selected. Please run the script again and choose 'a' or 'm'.")

if __name__ == "__main__":
    main()
