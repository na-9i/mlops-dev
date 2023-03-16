from fastapi import FastAPI
import csv


app = FastAPI()

@app.get("/")
async def main():
    return {"message": "hello world!"}
