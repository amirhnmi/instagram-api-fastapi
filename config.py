from fastapi import FastAPI, staticfiles
from routers import users, posts, auth, comments

app = FastAPI()

app.mount("/files" ,staticfiles.StaticFiles(directory="uploaded_file"), name="files",)

# app.include_router(home.router, tags=["home"])
app.include_router(users.router, tags=["users"])
app.include_router(posts.router, tags=["posts"])
app.include_router(comments.router, tags=["comments"])
app.include_router(auth.router, tags=["authentication"])