from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "https://todobackend-11vr.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Utility functions for reading and writing JSON file
def read_todos():
    with open("./app/data.json", "r") as file:
        return json.load(file)

def write_todos(todos):
    with open("./app/data.json", "w") as file:
        json.dump(todos, file, indent=4)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    todos = read_todos()
    return {"data": todos}

@app.post("/todo", tags=["todos"])
async def add_todo(todo: dict) -> dict:
    todos = read_todos()
    todos.append(todo)
    write_todos(todos)
    return {"data": "Todo added."}

@app.put("/todo/{id}", tags=["todos"])
async def update_todo(id: int, body: dict) -> dict:
    todos = read_todos()
    for todo in todos:
        if int(todo["id"]) == id:
            todo["item"] = body["item"]
            write_todos(todos)  # Write the updated list, not the single todo
            return {"data": f"Todo with id {id} has been updated."}
    return {"data": f"Todo with id {id} not found."}


@app.delete("/todo/{id}", tags=["todos"])
async def delete_todo(id: int) -> dict:
    todos = read_todos()
    for todo in todos:
        if int(todo["id"]) == id:
            todos.remove(todo)
            write_todos(todos)
            return {
                "data": f"Todo with id {id} has been removed."
            }

    return {
        "data": f"Todo with id {id} not found."
    }
