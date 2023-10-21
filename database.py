import sqlite3

# Connect to the SQLite database
db_conn = sqlite3.connect('attendance.db')

def log_attendance(name):
    """
    Log attendance by inserting a record into the 'attendance' table.

    Args:
        name (str): The name of the person whose attendance is being logged.
    """
    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO attendance (name) VALUES (?)", (name,))
    db_conn.commit()

def get_attendance_records():
    """
    Retrieve all attendance records from the 'attendance' table.

    Returns:
        list: A list of attendance records, where each record is a dictionary with 'id', 'name', and 'timestamp'.
    """
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()

    attendance_records = []
    for record in records:
        record_dict = {
            'id': record[0],
            'name': record[1],
            'timestamp': record[2]
        }
        attendance_records.append(record_dict)

    return attendance_records

# Close the database connection (optional, if not used in the same script)
# db_conn.close()
