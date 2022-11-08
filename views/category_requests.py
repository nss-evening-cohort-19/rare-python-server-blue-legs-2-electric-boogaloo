"""category requests"""

import sqlite3
import json
from models import Category


def create_category(new_category):
    """create a category"""
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO categories
            (label)
        VALUES
            (?);
        """, (new_category['label'], ))

        post_id = db_cursor.lastrowid

        new_category['id'] = post_id

    return json.dumps(new_category)

def get_single_category(id):
    """gets single category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM categories c
        WHERE c.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        category = Category(data['id'], data['label'])

        return json.dumps(category.__dict__)

def get_all_categories():
    """Gets all categories"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM categories c
        ORDER BY LOWER(c.label)
        """)
        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            category = Category(row['id'], row['label'])

            categories.append(category.__dict__)

    return json.dumps(categories)

def update_category(id, new_category):
    """updates category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE categories
            SET
                label = ?
        WHERE id = ?
        """, (new_category['label'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def delete_category(id):
    """deletes category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM categories
        WHERE id = ?
        """, (id, ))
