import json

class LibraryError(Exception):
    pass

class Book:
    def __init__(self, title: str, author: str, isbn: str, checked_out = False):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.checked_out = checked_out
        
    def __str__(self):
        status = "Checked Out" if self.checked_out else "Available"

        return (
            f"Title: {self.title} | "
            f"Author: {self.author} | "
            f"ISBN: {self.isbn} | "
            f"Status: {status}"
        )
    

class Member:
    def __init__(self, name: str, member_id: str, borrow_limit: int = 3, borrowed_book = None):
        self.name = name
        self.member_id = member_id
        self.borrow_limit = borrow_limit
        
        self.borrowed_book = borrowed_book if borrowed_book is not None else []
        
    def __str__(self):
        return (
            f"Name: {self.name} | "
            f"Member ID: {self.member_id} | "
            f"Borrowed: {len(self.borrowed_book)}/{self.borrow_limit}"
        )

class Library:
    def __init__(self, filename = "library.json"):
        self.books = {}
        self.members = {}
        self.filename = filename

        

    def add_book(self, title, author, isbn):
        
        if isbn in self.books:
            raise LibraryError(f"Error: Book with ISBN {isbn}Already Exists In Library")
        
        self.books[isbn] = Book(title, author, isbn)
        print("Book Added Successfully")
        
    def register_member(self, name, member_id):
        
        if member_id in self.members:
            raise LibraryError(f"Error: Member with this id {member_id} alreay exists in Library")
        
        self.members[member_id] = Member(name, member_id)
        print("Member Added Successfully")

    def checkout(self, member_id: str, isbn: str):
       
        if member_id not in self.members:
            raise LibraryError("Error: Member Not Registered")
        if isbn not in self.books:
            raise LibraryError("Error: ISBN Does Not Exits")
        
        book = self.books[isbn]
        if book.checked_out:
            raise LibraryError("Book Is Already Checked Out")
        
        member = self.members[member_id]
        if len(member.borrowed_book) >= member.borrow_limit:
            raise LibraryError("Your Borrow Limit Is Full")
        
        book.checked_out = True
        member.borrowed_book.append(book)

    def return_book(self, member_id: str, isbn: str):
        
        if member_id not in self.members:
            raise LibraryError("Error: Member Not Registered")
        if isbn not in self.books:
            raise LibraryError("Error: ISBN Does Not Exits")
        
        book = self.books[isbn]
        member = self.members[member_id]

        if not book.checked_out:
            raise LibraryError("Error: Book is not checked out yet")
        
        if book not in member.borrowed_book:
            raise LibraryError("Error: This member did not borrow this book")
            
        book.checked_out = False
        member.borrowed_book.remove(book)
        

    def search(self, query: str) -> list[Book]:
        
        result = []
        for book in self.books.values():
            
            if query in book.author.lower() or query in book.title.lower():
                result.append(book) 
        
        return result

    def save_to_file(self, path: str | None = None):
        
        if path is None:
            path = self.filename
        
        def to_dict(book):
                
            return {
                "title": book.title,
                "author": book.author,
                "isbn": book.isbn,
                "checked_out": book.checked_out,
            }
            
        
        book_data = {}
        
        for isbn, book in self.books.items():
            book_data[isbn] = to_dict(book)
        
        def member_to_dict(member):
            return {

                    "name": member.name,
                    "borrow_limit": member.borrow_limit,
                    "borrowed_book": [book.isbn for book in member.borrowed_book],
                
            }
        
        member_data = {}

        for member_id, member in self.members.items():
            member_data[member_id] = member_to_dict(member)
        
        data = {"books": book_data, "members": member_data}

        with open(path, "w") as f:
            json.dump(data, f, indent = 2)
        
        print("Data Saved Successfully")
        
        
    def load_from_file(self, path: str | None = None):
        
        if path is None:
            path = self.filename

        with open(path, "r") as f:
            data = json.load(f)

        self.books = {}
        for isbn, book_dict in data["books"].items():
            
            book = Book(
                title=book_dict["title"],
                author=book_dict["author"],
                isbn=book_dict["isbn"],
                checked_out=book_dict.get("checked_out", False)
            )

            self.books[isbn] = book

        self.members = {}
        for member_id, member_dict in data["members"].items():
            
            member = Member(
                name=member_dict["name"],
                member_id=member_id,
                borrow_limit=member_dict["borrow_limit"]
            )
        
            for isbn in member_dict.get("borrowed_book", []):

                if isbn not in self.books:
                    raise LibraryError(
                        f"Error: Book with ISBN {isbn} "
                        f"was borrowed by member {member_id}, "
                        f"but that book does not exist."
                    )

                member.borrowed_book.append(self.books[isbn])

            self.members[member_id] = member

        print("Data Loaded Successfully")
    
    def show_books(self):

        if not self.books:
            print("No books in library.")
            return

        print("\n===== Books =====")

        for book in self.books.values():
            print(book)

    def show_members(self):

        if not self.members:
            print("No members registered.")
            return

        print("\n===== Members =====")

        for member in self.members.values():
            print(member)

def print_menu():
    
    print("\n===== Library Management System =====")
    print("1. Add a book")
    print("2. Register a member")
    print("3. Checkout a book")
    print("4. Return a book")
    print("5. Search books")
    print("6. Save Data")
    print("7. Load Data")
    print("8. Show all Books")
    print("9. Show all Members")
    print("10. Exit")
    print("======================================")

if __name__ == "__main__":
    
    library = Library()
    
    while True:
        print_menu()
        choice = input("Enter Your Choice (1-10): ")
        
        try:
            if choice == "1":
                title = input("Enter the title of Book: ")    
                author = input("Enter Author Name of Book: ")
                isbn = input("Enter ISBN No of Book: ")

                library.add_book(title, author, isbn)
            
            elif choice == "2":
                
                name = input("Enter Your Name: ")
                member_id = input("Enter Your Member Id: ")

                library.register_member(name, member_id, )
                
            elif choice == "3":

                member_id = input("Enter member ID: ").strip()
                isbn = input("Enter ISBN: ").strip()

                library.checkout(member_id, isbn)
                
            elif choice == "4":
                
                member_id = input("Enter Member Id: ")
                isbn = input("Enter ISBN No of Book: ")

                library.return_book(member_id, isbn)
                
            elif choice == "5":
                
                query = input("Enter the Books (author/title): ").strip().lower()

                result = library.search(query)
                if not result:
                    print("Book Not Found")
                else:
                    for book in result:
                        print(book)
                
            elif choice == "6":
                
                library.save_to_file()
                
            elif choice == "7":
                
                library.load_from_file()
            
            elif choice == "8":
                
                library.show_books()
            
            elif choice == "9":
                
                library.show_members()

            elif choice == "10":
                print("Goodbye!")
                break
            
            else:
                print("Invalid Input")
            
        except LibraryError as e:
            print(e)
