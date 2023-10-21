import sqlite3

def add_known_face(name, face_encoding):
    """
    Add a known face to the database.

    Args:
        name (str): The name of the individual.
        face_encoding (list): A list of face encodings (e.g., obtained from face recognition).
    """
    db_conn = sqlite3.connect('known_faces.db')
    cursor = db_conn.cursor()

    # Check if the name already exists in the database
    cursor.execute("SELECT * FROM known_faces WHERE name=?", (name,))
    existing_face = cursor.fetchone()

    if existing_face:
        # If the name exists, update the face encoding
        cursor.execute("UPDATE known_faces SET face_encoding=? WHERE name=?", (face_encoding, name))
    else:
        # If the name doesn't exist, insert a new record
        cursor.execute("INSERT INTO known_faces (name, face_encoding) VALUES (?, ?)", (name, face_encoding))

    db_conn.commit()
    db_conn.close()

def update_known_face(name, updated_info):
    """
    Update information about a known face.

    Args:
        name (str): The name of the individual.
        updated_info (dict): A dictionary with fields to update (e.g., name or additional information).
    """
    db_conn = sqlite3.connect('known_faces.db')
    cursor = db_conn.cursor()

    # Check if the name exists in the database
    cursor.execute("SELECT * FROM known_faces WHERE name=?", (name,))
    existing_face = cursor.fetchone()

    if existing_face:
        # Update the fields specified in updated_info
        update_query = "UPDATE known_faces SET "
        update_values = []
        for key, value in updated_info.items():
            update_query += f"{key}=?, "
            update_values.append(value)
        update_query = update_query.rstrip(", ")  # Remove the trailing comma
        update_query += " WHERE name=?"
        update_values.append(name)

        cursor.execute(update_query, tuple(update_values))
        db_conn.commit()
    else:
        print(f"Known face '{name}' not found in the database.")

    db_conn.close()

def remove_known_face(name):
    """
    Remove a known face from the database.

    Args:
        name (str): The name of the individual to remove.
    """
    db_conn = sqlite3.connect('known_faces.db')
    cursor = db_conn.cursor()

    cursor.execute("DELETE FROM known_faces WHERE name=?", (name,))
    db_conn.commit()
    db_conn.close()
