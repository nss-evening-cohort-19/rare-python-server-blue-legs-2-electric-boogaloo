"""post requests"""

import sqlite3
import json
from models import Post
from views.category_requests import get_single_category
from .comment_requests import get_comments_by_post
from .post_reaction_request import get_post_reactions_by_post_id
from .post_tags_request import get_post_tags_by_post_id

def create_post(new_post):
    """create a post"""
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            (user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content'], new_post['approved'], ))

        post_id = db_cursor.lastrowid

        new_post['id'] = post_id

    return json.dumps(new_post)

def get_single_post(id):
    """gets single post"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.first_name,
            u.last_name
        FROM posts p
        JOIN users u
            ON p.user_id = u.id
        WHERE p.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        
        post = Post(data['id'], data['user_id'], data['category_id'], data['title'], data['publication_date'], data['image_url'], data['content'], data['approved'])
        
        post.author = f"{data['first_name']} {data['last_name']}"
        post.comments = json.loads(get_comments_by_post(id))
        post.post_reactions = json.loads(get_post_reactions_by_post_id(id))
        post.post_tags = json.loads(get_post_tags_by_post_id(id))
        
        
        return json.dumps(post.__dict__)
    
def get_all_posts():
    """Gets all posts"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.first_name,
            u.last_name
        FROM posts p
        JOIN users u
            ON p.user_id = u.id
        """)
        
        posts = []

        dataset = db_cursor.fetchall()
        
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['image_url'], row['content'], row['approved'])
           
            post.author = f"{row['first_name']} {row['last_name']}"
            post.comments = json.loads(get_comments_by_post(row['id']))
            post.post_reactions = json.loads(get_post_reactions_by_post_id(row['id']))
            post.post_tags = json.loads(get_post_tags_by_post_id(row['id']))
            post.category = json.loads(get_single_category(row['category_id']))
            
            
            posts.append(post.__dict__)
        
    return json.dumps(posts)

def get_posts_by_category(category_id):
    """gets posts by category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM Posts p
        WHERE p.category_id = ?
        """, ( category_id, ))

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'] , row['publication_date'], row['image_url'], row['content'], row['approved'])
            posts.append(post.__dict__)

    return json.dumps(posts)

def get_posts_by_tag(tag_id):
    """gets posts by category"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM Posts p
        JOIN posttags pt
            ON pt.post_id = p.id
        JOIN tags t
            ON t.id = pt.tag_id
        WHERE t.id = ?
        """, ( id, ))

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'] , row['publication_date'], row['image_url'], row['content'], row['approved'])
            posts.append(post.__dict__)

    return json.dumps(posts)

def update_post(id, new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Posts
            SET
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?,
                approved = ?
        WHERE id = ?
        """, (new_post['category_id'], new_post['title'],
              new_post['publication_date'], new_post['image_url'],
              new_post['content'], new_post['approved'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (id, ))
        
def get_posts_by_author_id(author_id):
    """gets posts by author id"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.first_name,
            u.last_name
        FROM Posts p
        JOIN users u
            ON p.user_id = u.id
        WHERE p.user_id = ?
        """, (author_id, ))

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'], row['approved'])

            post.category = json.loads(get_single_category(row['category_id']))
            post.author = f"{row['first_name']} {row['last_name']}"
            post.comments = json.loads(get_comments_by_post(row['id']))
            post.post_reactions = json.loads(get_post_reactions_by_post_id(row['id']))
            post.post_tags = json.loads(get_post_tags_by_post_id(row['id']))
            posts.append(post.__dict__)

    return json.dumps(posts)
