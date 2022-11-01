"""Comment Requests"""
import sqlite3
import json
from models import Comment


def create_comment(new_comment):
    """Creates Comment"""
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO comments
            (author_id, post_id, content)
        VALUES
            (?, ?, ?);
        """, (new_comment['author_id'], new_comment['post_id'], new_comment['content'], ))
      
        comment_id = db_cursor.lastrowid
      
        new_comment['id'] = comment_id
    
    return json.dumps(new_comment)
  
