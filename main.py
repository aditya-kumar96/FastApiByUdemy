from fastapi import FastAPI, Body, HTTPException
import json
from Book import Book

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
    finaldata = []
    data = load_data()
    for id, details in data.items():
        finaldata.append({"id": id, **details})
    return finaldata


@app.post("/books/createBook", status_code=201)
def createBook(book_id: str, newbook: Book):
    data = load_data()
    if book_id in data:
        raise HTTPException(status_code=409, detail="Book already Exists!")
    data[book_id] = newbook.dict()
    save_data(data)
    return {"message": "Book created successfully", "book_id": book_id, "book": newbook}


@app.put("/books/updatebook/{book_id}", status_code=200)
def updatebook(book_id: str, newbook: Book):
    data = load_data()
    if book_id in data:
        existing_book = data[book_id]
        update_data = newbook.dict(exclude_unset=True)
        existing_book.update(update_data)
        data[book_id] = existing_book        
        save_data(data)
    else:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book Updated SUccessfully", "data": data}


@app.delete('/books/{book_id}',status_code=200)
def deleteBook(book_id:str):
    data = load_data()
    if book_id in data:
        del data[book_id]
    else:
        raise HTTPException(status_code=404,detail="Book not found")
    save_data(data)
    return {
        "message":"Book deleted succesfully",
        "data":data
    }
    
@app.get('/getbookbysubject',status_code=200)
def getbookbysubject(subject):
    data = load_data()
    allBook = []
    for _,details in data.items():
        if details.get("subject", "").casefold() == subject.casefold():
            allBook.append(details)
    if not allBook:
        raise HTTPException(
            status_code=404,
            detail=f"No books found for subject '{subject}'"
        )
    return  {
        "message":"all books are",
         "count": len(allBook),
        "data":allBook
    }