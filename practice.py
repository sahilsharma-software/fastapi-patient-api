from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def first():
    return {"message":"hello world"}

@app.get("/new")
def kill():
    return {"sahil":"kill the new force"}


@app.get("/user/{name}")
def get_user(name:str):
    return {"user":name}