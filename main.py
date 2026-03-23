from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def print():
    return {"satish":"anime lover"}

@app.get("/about")
def grind():
    return {"Sahil Sharma ":"also start loving anime"}

