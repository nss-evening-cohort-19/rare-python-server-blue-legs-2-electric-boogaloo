import sqlite3
import json
from models import Tag

def create_tag(new_tag):
    """"create a tag"""
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute(""""
        INSERT INTO Tags
            (label)
        VALUES
            (?)
        """, (new_tag['label']))
        
        post_id = db_cursor.lastrowid
        
        new_tag['id'] = post_id
        
    return json.dumps(new_tag)
