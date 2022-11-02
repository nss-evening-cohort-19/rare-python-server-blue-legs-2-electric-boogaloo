import sqlite3
import json
from models import Reaction

def create_reaction(new_reaction):
    """"create a reaction"""
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO Reactions
            (label, image_url)
        VALUES
            (?, ?);
        """, (new_reaction['label'], new_reaction['image_url']))
        
        reaction_id = db_cursor.lastrowid
        
        new_reaction['id'] = reaction_id
        
    return json.dumps(new_reaction)

def get_single_reaction(id):
    """gets single reaction"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            r.id,
            r.label,
            r.image_url
        FROM reactions r
        WHERE r.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        
        reaction = Reaction(data['id'], data['label'], data['image_url'])
        
        return json.dumps(reaction.__dict__)
      
def update_reaction(id, new_reaction):
    """Update reaction"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE reactions
            SET
                label = ?,
                image_url = ?
        WHERE id = ?
        """, (new_reaction['label'],new_reaction['image_url'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def delete_reaction(id):
    """Deletes a reaction and associated postReaction"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM reactions
        WHERE id = ?
        """, (id, ))
        
        db_cursor.execute("""
        DELETE FROM postreactions
        WHERE reaction_id = ?
        """, (id, ))

def get_all_reactions():
    """Gets all reactions"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            r.id,
            r.label,
            r.image_url
        FROM reactions r
        """)
        
        reactions = []

        dataset = db_cursor.fetchall()
        
        for row in dataset:
            reaction = Reaction(row['id'], row['label'], row['image_url'])
            
            reactions.append(reaction.__dict__)
        
    return json.dumps(reactions)
