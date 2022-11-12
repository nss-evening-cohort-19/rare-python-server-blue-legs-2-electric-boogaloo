import sqlite3
import json
from models import PostTag

def create_post_tag(new_post_tag):
    """create a post tag"""
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute(""" 
        INSERT INTO posttags
            (post_id, tag_id)
        VALUES
            (?, ?)
        """, (new_post_tag['post_id'], new_post_tag['tag_id']), )
        
        post_tag_id = db_cursor.lastrowid
        
        new_post_tag['id'] = post_tag_id
    
    return json.dumps(new_post_tag)

def get_all_post_tags():
    """"get all post tags"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            p.id,
            p.post_id,
            p.tag_id
        FROM posttags p
        """)
        
        post_tags = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            post_tag = PostTag(row['id'], row['post_id'], row['tag_id'])
            
            post_tags.append(post_tag.__dict__)
            
    return json.dumps(post_tags)


def get_single_post_tag(id):
    """"get single post tag"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute(""" 
        SELECT
            p.id,
            p.post_id,
            p.tag_id
        FROM posttags p
        WHERE p.id = ?
        """, (id, ))
        
        data = db_cursor.fetchone()
        
        post_tag = PostTag(data['id'], data['post_id'], data['tag_id'])
        
        return json.dumps(post_tag.__dict__)
    
def update_post_tag(id, new_post_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute(""" 
        UPDATE posttags
            SET
                post_id = ?,
                tag_id = ?
            WHERE id = ?
        """, (new_post_tag['post_id'], new_post_tag['tag_id'], id, ))
    
        rows_affected = db_cursor.rowcount
        
    if rows_affected == 0:
        return False
    else:
        return True
    
def delete_post_tag(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute(""" 
        DELETE FROM posttags
        WHERE id = ?                  
        """, (id, ))

def get_post_tags_by_post_id(post_id):
    """get post tag by post id"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pt.id,      
            pt.post_id,
            pt.tag_id,
            t.label
        FROM posttags pt
        JOIN tags t
            ON pt.tag_id = t.id
        WHERE post_id = ?          
                          """, (post_id, ))
        
        dataset = db_cursor.fetchall()
        
        post_tags = []
        
        for row in dataset:
            post_tag = PostTag(row['id'], row['post_id'], row['tag_id'])
            
            post_tag.label = f"{row['label']}"
        
            post_tags.append(post_tag.__dict__)
        
        return json.dumps(post_tags)
