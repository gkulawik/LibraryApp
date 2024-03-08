from library import LibraryCollection, Book, Dvd

book1 = Book(title="The Lord of the Rings - Trilogy",
             genre="fantasy fiction",
             availability_status=False,
             author="J.R.R. Tolkien",
             isbn="978-0261103252")

dvd1 = Dvd(title="Gladiator",
           genre="historical fiction",
           availability_status=False,
           director="Ridley Scott",
           duration="2h 18min")

collection1 = LibraryCollection()
collection1.add_resource(book1)
collection1.add_resource(dvd1)

print(collection1.books)
print(collection1.dvds)




