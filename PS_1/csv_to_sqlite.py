import csv
import sqlite3
import os

CSV_FILE_PATH = "data/users.csv"
DB_FILE_PATH = "db/users.db"


def create_database():

    os.makedirs("db", exist_ok=True)

    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)

    conn.commit()
    conn.close()


def read_csv():

    users = []

    with open(CSV_FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row.get("name")
            email = row.get("email")

            if not name or not email:
                continue

            users.append((name.strip(), email.strip()))

    return users


def insert_users(users):

    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()

    cursor.executemany(
        "INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
        users
    )

    conn.commit()
    conn.close()


def display_users():

    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, email FROM users")
    rows = cursor.fetchall()

    conn.close()

    print("\nStored Users:\n")
    for name, email in rows:
        print(f"Name: {name} | Email: {email}")


def main():
    create_database()
    users = read_csv()

    if users:
        insert_users(users)
    else:
        print("No valid users found in CSV")

    display_users()


if __name__ == "__main__":
    main()