# FastAPI Books Project

from typing import Optional

from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Books:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BooksRequest(BaseModel):

    id: Optional[int] = Field(default=None, title="The ID of the book")
    title: str = Field(min_length=3, max_length=50, title="The title of the book")
    author: str = Field(min_length=1, max_length=50, title="The author of the book")
    description: str = Field(min_length=1, max_length=100, title="The description of the book")
    rating: int = Field(ge=1, le=5, title="The rating of the book")
    published_date: int = Field(ge=2000, le=2050, title="The published date of the book")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "A Book Title",
                "author": "Author Name",
                "description": "A Book Description",
                "rating": 5,
                "published_date": 2021,
            }
        }


BOOKS = [
    Books(1, "Computer Science", "John Doe", "This is a book about computer science", 5, 2021),
    Books(2, "Mathematics", "Jane Doe", "This is a book about mathematics", 4, 2020),
    Books(3, "Physics", "John Smith", "This is a book about physics", 3, 2019),
    Books(4, "Chemistry", "Jane Smith", "This is a book about chemistry", 2, 2018),
    Books(5, "Biology", "John Doe", "This is a book about biology", 1, 2017),
    Books(6, "History", "Jane Doe", "This is a book about history", 5, 2016),
    Books(7, "Geography", "John Smith", "This is a book about geography", 4, 2015),
    Books(8, "Economics", "Jane Smith", "This is a book about economics", 3, 2014),
    Books(9, "Politics", "John Doe", "This is a book about politics", 2, 2013),
    Books(10, "Philosophy", "Jane Doe", "This is a book about philosophy", 1, 2012),
]


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(rating: int = Query(gt=0, le=5)):
    return [book for book in BOOKS if book.rating == rating]


@app.get("/books/by-publish-date/", status_code=status.HTTP_200_OK)
async def read_book_by_publish_date(published_date: int = Query(gt=2000, le=2050)):
    return [book for book in BOOKS if book.published_date == published_date]


@app.get("/books/{book_id}/", status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(gt=0)):
    book = next((book for book in BOOKS if book.id == book_id), None)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found!")


@app.delete("/delete-books/{book_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_books(book_id: int = Path(gt=0)):
    book = next((book for book in BOOKS if book.id == book_id), None)
    if book:
        BOOKS.remove(book)
        return "Deleted Successfully!"
    raise HTTPException(status_code=404, detail="Book not found!")


@app.post("/create-books/", status_code=status.HTTP_201_CREATED)
async def create_books(book_request: BooksRequest):
    new_book = Books(**book_request.dict())
    BOOKS.append(find_book_by_id(new_book))
    return BOOKS


def find_book_by_id(book: Books):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/update-books/{book_id}/", status_code=status.HTTP_200_OK)
async def update_books(book_request: BooksRequest, book_id: int = Path(gt=0)):
    book = next((book for book in BOOKS if book.id == book_id), None)
    if book:
        book.title = book_request.title
        book.author = book_request.author
        book.description = book_request.description
        book.rating = book_request.rating
        return book
    raise HTTPException(status_code=404, detail="Book not found!")
