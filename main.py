from fastapi import FastAPI
import json

app = FastAPI()


def load_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return data


def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)


@app.get("/")
async def welcome():
    return {"message": "Hello user"}


@app.get("/books")
def getallbooks():
    finaldata=[]
    data = load_data()
    for id, details in data.items():
        finaldata.append({"id": id, **details})
    return finaldata
