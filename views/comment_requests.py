"""Comment Requests"""
import sqlite3
import json
from models import Comment
from models import User

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

def update_comment(id, new_comment):
    """Updates Comment"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        UPDATE Comments
            SET
                content = ?
        WHERE id = ? 
        """, (new_comment['content'], id, ))
        
        rows_affected = db_cursor.rowcount
    
    if rows_affected == 0:
        return False
    else:
        return True

def get_all_comments():
    """Gets all the comments"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            c.id,
            c.author_id,
            c.post_id,
            c.content
        FROM comments c
        """)
        
        comments = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            comment = Comment(row['id'], row['author_id'], row['post_id'], row['content'])
            
            comments.append(comment.__dict__)
            
    return json.dumps(comments)

def get_single_comment(id):
    """Gets single comment"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT 
            c.id,
            c.author_id,
            c.post_id,
            c.content
        FROM comments c
        Where c.id = ?
        """, (id, ))
        
        data = db_cursor.fetchone()
        
        comment = Comment(data['id'], data['author_id'], data['post_id'], data['content'])
            
        return json.dumps(comment.__dict__)

def delete_comment(id):
    """Deletes Single Comment"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        DELETE FROM comments
        WHERE id = ?
        """, (id, ))
        

def get_comments_by_author(author_id):
    """gets comments by user"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT                  
            c.id,
            c.author_id,
            c.post_id,
            c.content,
            u.first_name,
            u.last_name
        FROM comments c
        JOIN users u
            ON c.author_id = u.id
        """)
        
        comments = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
           
           comment = Comment(row['id'], row['author_id'], row['post_id'], row['content'])
           
           author = User(row['id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])
           
           comment.author = author.__dict__
           
           comments.append(comment.__dict__)
           
    return json.dumps(comments)
           
           
           
