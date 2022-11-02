import sqlite3
import json
from models import Tag

def create_tag(new_tag):
    """create a tag"""
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO Tags
            (label)
        VALUES
            (?)
        """, (new_tag['label'], ))
        
        post_id = db_cursor.lastrowid
        
        new_tag['id'] = post_id
        
    return json.dumps(new_tag)


def get_all_tags():
    """gets all tags"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM tags t
        """)

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['label'])

            tags.append(tag.__dict__)

    return json.dumps(tags)


def get_single_tag(id):
    """gets single tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM tags t
        WHERE t.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        tag = Tag(data['id'], data['label'])

        return json.dumps(tag.__dict__)

def update_tag(id, new_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Tags
            SET
                label = ?
        WHERE id = ?
        """, (new_tag['label'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def delete_tag(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM tags
        WHERE tags.id IN (
            SELECT t.ROWID FROM tags t
            INNER JOIN posttags p
                ON (t.id=p.tag_id)
            WHERE t.id = p.tag_id
            );
        WHERE id = ?
        """, (id, ))
