import sqlite3
import json
from models import PostReaction

def create_post_reaction(new_post_reaction):
    """"create a postReaction"""
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO PostReactions
            (user_id, reaction_id, post_id)
        VALUES
            (?, ?, ?);
        """, (new_post_reaction['user_id'], new_post_reaction['reaction_id'], new_post_reaction['post_id']))
        
        post_reaction_id = db_cursor.lastrowid
        
        new_post_reaction['id'] = post_reaction_id
        
    return json.dumps(new_post_reaction)

def get_single_post_reaction(id):
    """gets single postReaction"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            pr.id,
            pr.user_id,
            pr.reaction_id,
            pr.post_id
        FROM PostReactions pr
        WHERE pr.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        
        post_reaction = PostReaction(data['id'], data['user_id'], data['reaction_id'], data['post_id'])
        
        return json.dumps(post_reaction.__dict__)
      
def update_post_reaction(id, new_post_reaction):
    """Update postReaction"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE PostReactions
            SET
                user_id = ?,
                reaction_id = ?,
                post_id = ?
        WHERE id = ?
        """, (new_post_reaction['user_id'],new_post_reaction['reaction_id'], new_post_reaction['post_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def delete_post_reaction(id):
    """Delete a postReaction"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM PostReactions
        WHERE id = ?
        """, (id, ))

def get_all_post_reactions():
    """Gets all reactions"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            pr.id,
            pr.user_id,
            pr.reaction_id,
            pr.post_id
        FROM PostReactions pr
        """)
        
        post_reactions = []

        dataset = db_cursor.fetchall()
        
        for row in dataset:
            post_reaction = PostReaction(row['id'], row['user_id'], row['reaction_id'], row['post_id'])
            
            post_reactions.append(post_reaction.__dict__)
        
    return json.dumps(post_reactions)
