import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
  connection = mysql.connector.connect(
      host=os.getenv('DB_HOST'),        
      user=os.getenv('DB_USER'),             
      password=os.getenv('DB_PASSWORD'),        
      database=os.getenv('DB_NAME')  
  )
  return connection

# users functions
def get_all_users_from_db():
  connection = get_db_connection()
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM users")
  users = cursor.fetchall()
  cursor.close()
  connection.close()
  return users

def get_user_by_id_from_db(user_id: int):
  connection = get_db_connection()
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
  user = cursor.fetchone()
  cursor.close()
  connection.close()
  return user

def update_user_by_id_from_db(user_id: int, username: str, user_type: str):
  connection = get_db_connection()
  cursor = connection.cursor()
  query = "UPDATE users SET username = %s, user_type = %s WHERE user_id = %s"
  cursor.execute(query, (username, user_type, user_id))
  connection.commit()
  cursor.close()
  connection.close()

def delete_user_from_db(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    connection.commit()
    cursor.close()
    connection.close()

def create_user_in_db(username: str, password: str, user_type: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    query = "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, hashed_password, user_type))
    connection.commit()
    cursor.close()
    connection.close()


# Blogs Functions
def create_blog_in_db(title: str, body: str, visibility: str, username: str, image_url: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO blogs (title, body, visibility, username, file_path) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (title, body, visibility, username, image_url))
    connection.commit()
    cursor.close()
    connection.close()

def update_blog_by_id_from_db(title: str, body: str, visibility: str, image_url: str, blog_id: int):
  connection = get_db_connection()
  cursor = connection.cursor()
  query = "UPDATE blogs SET title = %s, body = %s, visibility = %s, file_path = %s WHERE blog_id = %s"
  cursor.execute(query, (title, body, visibility, image_url, blog_id))
  connection.commit()
  cursor.close()
  connection.close()

def get_blog_by_id_from_db(blog_id: int):
  connection = get_db_connection()
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM blogs WHERE blog_id = %s", (blog_id,))
  blog = cursor.fetchone()
  cursor.close()
  connection.close()
  return blog

def get_all_blogs_from_db():
  connection = get_db_connection()
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM blogs WHERE visibility IN ('public', 'member')")
  blogs = cursor.fetchall()
  cursor.close()
  connection.close()
  return blogs

def delete_blog_from_db(blog_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM blogs WHERE blog_id = %s", (blog_id,))
    connection.commit()
    cursor.close()
    connection.close()