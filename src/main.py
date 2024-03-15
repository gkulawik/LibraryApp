from library import Library, Book, Dvd, Cd, Magazine, Member, Memberships

book1 = Book(title="The Lord of the Rings - Trilogy",
             genre="fantasy fiction",
             author="J.R.R. Tolkien",
             isbn="978-0261103252")

book2 = Book(title="The hobbit, or There and back again",
             genre="fantasy fiction",
             author="J.R.R. Tolkien",
             isbn="978-0007458424")

book3 = Book(title="Harry Potter Box Set: The Complete Collection",
             genre="fantasy fiction",
             author="J.K. Rowling",
             isbn="978-1408856772")

book4 = Book(title="Deep Work: Rules for Focused Success in a Distracted World",
             genre="self-help",
             author="Cal Newport",
             isbn="978-0349411903")

dvd1 = Dvd(title="Gladiator",
           genre="historical fiction",
           director="Ridley Scott",
           duration="2h 18min")

library = Library()
library.add_resource(book1, 2)
library.add_resource(book2, 2)
library.add_resource(book3, 2)
member1 = library.create_member(name="John Doe", membership_status=Memberships.PREMIUM)
print(member1.borrowed_resources_ids)
member1.borrow_resources([1, 3])
print(member1.borrowed_resources_ids)
member1.borrow_resources([1, 3])
print(member1.borrowed_resources_ids)

# todo:  Display available resources of each type (books, DVDs, CDs, magazines).

# todo:   Allow a member to return a resource.

# todo: Display borrowed resources for a member. Pass borrowed IDs to the library
#  and get back a list of borrowed resources with all details

# todo: Display library statistics (total number of resources, number of available resources,
#  number of borrowed resources).

# todo: Write some basic unit tests or at least 1
