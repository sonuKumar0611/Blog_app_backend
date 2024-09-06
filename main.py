from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import db
import os
import shutil
from schemas import UserCreate, UserUpdate, BlogCreate, BlogUpdate
from fastapi.staticfiles import StaticFiles


app = FastAPI()

UPLOAD_DIRECTORY = "uploads"

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Users controller
@app.get("/users")
async def get_all_users():
    users = db.get_all_users_from_db()
    return {"data": users}

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    user = db.get_user_by_id_from_db(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": user}

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    db.update_user_by_id_from_db(user_id, user.username, user.user_type)
    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = db.get_user_by_id_from_db(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete_user_from_db(user_id)
    return {"message": "User deleted successfully"}

@app.post("/users")
async def create_user(user: UserCreate):
    db.create_user_in_db(user.username, user.password, user.user_type)
    return {"message": "User created successfully"}


# Blogs controllers
@app.post("/blogs")
async def create_blog(title: str = Form(...),body: str = Form(...),visibility: str = Form(...),username: str = Form(...),image: UploadFile = File(None)):
    image_url = None

    if image:
        image_path = os.path.join(UPLOAD_DIRECTORY, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        # Generate the URL to be saved in the database
        image_url = f"/uploads/{image.filename}"

    db.create_blog_in_db(title, body, visibility, username, image_url)
    return {"message": "Blog created successfully", "image_url": image_url}

@app.put("/blogs/{blog_id}")
async def update_blog(blog_id,title: str = Form(...),body: str = Form(...),visibility: str = Form(...), image: UploadFile = File(None)):
    image_url = None

    if image:
        image_path = os.path.join(UPLOAD_DIRECTORY, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        image_url = f"/uploads/{image.filename}"
    
    db.update_blog_by_id_from_db(title, body, visibility, image_url, blog_id)
    return {"message": "Blog updated successfully", "image_url": image_url}

@app.get("/blogs")
async def get_all_blogs():
    blogs = db.get_all_blogs_from_db()
    return {"data": blogs}

@app.get("/blogs/{blog_id}")
async def get_blog_by_id(blog_id: int):
    blog = db.get_blog_by_id_from_db(blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"data": blog}

@app.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: int):
    blog = db.get_blog_by_id_from_db(blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete_blog_from_db(blog_id)
    return {"message": "Blog deleted successfully"}







