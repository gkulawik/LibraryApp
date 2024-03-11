import pytest
from LibraryApp.src.library import Library, Book


class TestLibrary:

    def test_add_book_resource(self):
        """
        Adding a Book resource
        """
        self.library1 = Library()
        self.book1 = Book(title="The Lord of the Rings - Trilogy",
                          genre="fantasy fiction",
                          availability_status=False,
                          author="J.R.R. Tolkien",
                          isbn="978-0261103252")

        self.library1.add_resource(self.book1)
        assert self.library1.resources == [Book(title='The Lord of the Rings - Trilogy',
                                                genre='fantasy fiction',
                                                availability_status=False,
                                                author='J.R.R. Tolkien',
                                                isbn='978-0261103252')]

    def test_add_unsupported_resource(self):
        """
       Adding a resource of not supported type, e.g., a list
       """
        self.library1 = Library()
        self.book1 = ["Book"]
        with pytest.raises(TypeError):
            self.library1.add_resource(self.book1)


if __name__ == '__main__':
    pytest.main(['-v', 'test_library.py'])
