from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory list to store books
books = []

# Pydantic model for Book
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int

# Helper function to generate a new ID
def generate_id():
    return len(books) + 1

# 1. Add a Book (POST /books)
@app.post("/books", response_model=Book)
def add_book(book: Book):
    new_book = Book(id=generate_id(), title=book.title, author=book.author, year=book.year)
    books.append(new_book)
    return new_book

# 2. Get All Books (GET /books)
@app.get("/books", response_model=List[Book])
def get_all_books():
    return books

# 3. Get a Book by ID (GET /books/{id})
@app.get("/books/{id}", response_model=Book)
def get_book_by_id(id: int):
    for book in books:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# 4. Update a Book (PUT /books/{id})
@app.put("/books/{id}", response_model=Book)
def update_book(id: int, book: Book):
    for b in books:
        if b.id == id:
            b.title = book.title
            b.author = book.author
            b.year = book.year
            return b
    raise HTTPException(status_code=404, detail="Book not found")

# 5. Delete a Book (DELETE /books/{id})
@app.delete("/books/{id}")
def delete_book(id: int):
    for book in books:
        if book.id == id:
            books.remove(book)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")
