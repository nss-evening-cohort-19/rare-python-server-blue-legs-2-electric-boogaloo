"""subscription requests"""

import sqlite3
import json
from models import Subscription


def create_subscription(new_subscription):
    """create a subscription"""
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO subscriptions
            (follower_id, author_id, created_on)
        VALUES
            ( ?, ?, ?);
        """, (new_subscription['follower_id'], new_subscription['author_id'], new_subscription['created_on'], ))

        subscription_id = db_cursor.lastrowid

        new_subscription['id'] = subscription_id

    return json.dumps(new_subscription)
  
def get_all_subscriptions():
  """Gets all subscriptions"""
  with sqlite3.connect('./db.sqlite3') as conn:
      conn.row_factory = sqlite3.Row
      db_cursor = conn.cursor()
      
      db_cursor.execute("""
      SELECT
          s.id,
          s.follower_id,
          s.author_id,
          s.created_on
      FROM subscriptions s
      """)
      
      subscriptions = []

      dataset = db_cursor.fetchall()
      
      for row in dataset:
          post = Subscription(row['id'], row['follower_id'], row['author_id'], row['created_on'])
          
          subscriptions.append(post.__dict__)
      
  return json.dumps(subscriptions)
