import sqlite3
import ebooklib
from ebooklib import epub
from Chapter import Chapter

MIN_CHAPTER_LEN = 1000 * 6
DB_FILE_NAME = "PsychoDB.db"
SQL_CREATE_BOOK = "INSERT INTO books (name, max_chapters) VALUES (?, ?)"
SQL_CHECK_NAME = "SELECT EXISTS (SELECT 1 FROM books WHERE name = ?);"
SQL_GET_ID = "SELECT rowid FROM books WHERE name = ?;"
SQL_GET_MAX_CP = "SELECT max_chapters FROM books WHERE name = ?;"
SQL_UPDATE_CP_NUM = "UPDATE books SET max_chapters = ? WHERE name = ?;"


class Book:
    """
    a Book entity
    the main function of the class is creating new book, and in this way making new chapters
    """

    def __init__(self, filename):
        self._filepath = 'books\\' + filename + '.epub'
        self._name = filename
        try:
            with sqlite3.connect(DB_FILE_NAME) as db_file:
                self._book_id = db_file.execute(SQL_GET_ID, (self._name,)).fetchone()[0]
                self._max_cp = db_file.execute(SQL_GET_MAX_CP, (self._name,)).fetchone()[0]
        except sqlite3.OperationalError:
            print("Error opening DB. book: " + self._name)
            exit(1)

    def get_book_id(self):
        """
        :return: book id getter
        """
        return self._book_id

    def get_name(self):
        """
        :return: name getter
        """
        return self._name

    def get_max_cp(self):
        """
        :return: maximum chapter num getter
        """
        return self._max_cp

    @staticmethod
    def is_book_exists(name):
        """
        checks if the book is already in the db
        :param name: the books name
        :return: true if its in the db, false otherwise
        """
        with sqlite3.connect(DB_FILE_NAME) as db_file:
            return db_file.execute(SQL_CHECK_NAME, (name,)).fetchone()[0]

    @staticmethod
    def create_new_book(filename):
        """
        adds new book to the table. creates new chapter and them to their table
        :param filename: the name of the file
        """
        # creating new book at the table with 0 chapters
        with sqlite3.connect(DB_FILE_NAME) as db_file:
            db_file.execute(SQL_CREATE_BOOK, (filename, 0))
            book_id = db_file.execute(SQL_GET_ID, (filename,))
        # reading bool file
        filepath = 'books\\' + filename + '.epub'
        new_book = epub.read_epub(filepath)
        cp_num = 0
        # runs over the items in the new book
        for item in new_book.get_items():
            # for each doc item
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                cp_text = str(item.get_body_content())
                if len(cp_text) > MIN_CHAPTER_LEN:
                    cp_num += 1
                    Chapter.create_new_chapter(book_id, cp_num, None, cp_text)
        # update max_chapters
        with sqlite3.connect(DB_FILE_NAME) as db_file:
            db_file.execute(SQL_UPDATE_CP_NUM, (cp_num, filename))
