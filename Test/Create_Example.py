import sqlite3

# Function to initialize SQLite3 database and create tables
def initialize_database():
    connection = sqlite3.connect('MailDB.db')
    cursor = connection.cursor()

    # Create 'cadets' table
    cursor.execute('''
        CREATE TABLE cadets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            graduation_date DATE,
            box_number INTEGER
        )
    ''')
    
    # Create 'packages' table
    cursor.execute('''
        CREATE TABLE packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_number INTEGER,
            adressee TEXT,
            received DATE,
            picked_up DATE
        )
    ''')

    connection.commit()
    connection.close()

# Function to insert entries into 'cadets' table
def insert_cadet_entries():
    connection = sqlite3.connect('MailDB.db')
    cursor = connection.cursor()

    cadet_entries = [
        ('Cadet1', 'cadet1@example.com', 'May 1, 2024', 101),
        ('Cadet2', 'cadet2@example.com', 'June 15, 2024', 102),
        ('Cadet3', 'cadet3@example.com', 'July 20, 2024', 103),
        ('Cadet4', 'cadet4@example.com', 'August 10, 2024', 104),
        ('Cadet5', 'cadet5@example.com', 'September 5, 2024', 105),
        ('Cadet6', 'cadet6@example.com', 'October 1, 2024', 106),
        ('Cadet7', 'cadet7@example.com', 'November 15, 2024', 107),
        ('Cadet8', 'cadet8@example.com', 'December 20, 2024', 108),
        ('Cadet9', 'cadet9@example.com', 'January 10, 2025', 109),
        ('Cadet10', 'cadet10@example.com', 'February 5, 2025', 110),
        ('Cadet11', 'cadet11@example.com', 'March 1, 2025', 111),
        ('Cadet12', 'cadet12@example.com', 'April 15, 2025', 112),
        ('Cadet13', 'cadet13@example.com', 'May 20, 2025', 113),
        ('Cadet14', 'cadet14@example.com', 'June 10, 2025', 114),
        ('Cadet15', 'cadet15@example.com', 'July 5, 2025', 115),
        ('Cadet16', 'cadet16@example.com', 'August 1, 2025', 116),
        ('Cadet17', 'cadet17@example.com', 'September 15, 2025', 117),
        ('Cadet18', 'cadet18@example.com', 'October 20, 2025', 118),
        ('Cadet19', 'cadet19@example.com', 'November 10, 2025', 119),
        ('Cadet20', 'cadet20@example.com', 'December 5, 2025', 120),
        ('Cadet21', 'cadet21@example.com', 'January 1, 2026', 121),
        ('Cadet22', 'cadet22@example.com', 'February 15, 2026', 122),
        ('Cadet23', 'cadet23@example.com', 'March 20, 2026', 123),
        ('Cadet24', 'cadet24@example.com', 'April 10, 2026', 124),
        ('Cadet25', 'cadet25@example.com', 'May 5, 2026', 125),
        ('Cadet26', 'cadet26@example.com', 'June 1, 2026', 126),
        ('Cadet27', 'cadet27@example.com', 'July 15, 2026', 127),
        ('Cadet28', 'cadet28@example.com', 'August 20, 2026', 128),
        ('Cadet29', 'cadet29@example.com', 'September 10, 2026', 129),
        ('Cadet30', 'cadet30@example.com', 'October 5, 2026', 130),
    ]

    for entry in cadet_entries:
        cursor.execute('''
            INSERT INTO cadets (name, email, graduation_date, box_number)
            VALUES (?, ?, ?, ?)
        ''', entry)

    connection.commit()
    connection.close()

# Main script
initialize_database()
insert_cadet_entries()

print("Database initialized with 'cadets' table and example entries.")
