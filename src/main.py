from library import Library, Book, Dvd


book1 = Book(title="The Lord of the Rings - Trilogy",
             genre="fantasy fiction",
             availability_status=False,
             author="J.R.R. Tolkien",
             isbn="978-0261103252")

book2 = Book(title="The hobbit, or There and back again",
             genre="fantasy fiction",
             availability_status=False,
             author="J.R.R. Tolkien",
             isbn="978-0007458424")

book3 = Book(title="Harry Potter Box Set: The Complete Collection",
             genre="fantasy fiction",
             availability_status=False,
             author="J.K. Rowling",
             isbn="978-1408856772")

book4 = Book(title="Deep Work: Rules for Focused Success in a Distracted World",
             genre="self-help",
             availability_status=False,
             author="Cal Newport",
             isbn="978-0349411903")

dvd1 = Dvd(title="Gladiator",
           genre="historical fiction",
           availability_status=False,
           director="Ridley Scott",
           duration="2h 18min")

library1 = Library()
library1.add_resource(book1)
library1.add_resource(dvd1)
library1.add_resource(book2)
library1.add_resource(book3)
library1.add_resource(book4)

print(library1.resources)
print(library1.books)

# todo: Implement Pytest unit tests as a learning exercise
# todo: Create an interface for creating new library resources?


