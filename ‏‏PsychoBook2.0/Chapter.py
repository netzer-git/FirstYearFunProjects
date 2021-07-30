import sqlite3

PARSING_BY = ["/", "\"", "<", ">", "=", "!", "?", ",", ".", "&",
              "#", "%", "\'", "\\", ";", "-", "_", ")", "(", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
INVALID_WORDS = ["\n", "div", "class", "id", "href", "xe", "calibre", "bac", "img", "src",
                 "html", "alt", "jpeg", "image", "span", "calibre1", "xhtml"]

DB_FILE_NAME = "PsychoDB.db"
SQL_CREATE_CHAPTER = "INSERT INTO chapters (book_id, number, title) VALUES (?, ?, ?);"
SQL_ADD_CP_WORD = "INSERT OR IGNORE INTO book_words (book_id, chapter_id, word, appearance) VALUES (?, ?, ?, ?);"
SQL_GET_ID = "SELECT rowid FROM chapters WHERE book_id = ? AND cp_num = ?;"


class Chapter:
    """
    A class used to represent the words in a chapter in a book
    """

    def __init__(self, book_id, cp_num):
        # gets the cp_id by book name and cp number
        with sqlite3.connect(DB_FILE_NAME) as db_file:
            self.cp_id = db_file.execute(SQL_GET_ID, (book_id, cp_num)).fetchone()[0]

    def get_words_num(self):
        """
        :return: the number of words in the chapter
        """
        return len(self._word_list)

    def get_word_list(self):
        """
        :return: the list of the actual words in the chapter
        """
        return self._word_list

    def get_words_dict(self):
        """
        :return: the words in the chapter as dictionary
        """
        _word_count = {}
        for word in self._word_list:
            if word in _word_count:
                _word_count[word] += 1
            else:
                _word_count[word] = 1
        return _word_count

    def get_specified_words(self, start, end):
        """
        the function returns specific
        :param start: minimum times in the chapter
        :param end: limit of times in the chapter
        :return: the specific words in the chapter
        """
        _word_dict = self.get_words_dict()
        _specified_words = []
        # takes only the words in the limit
        for key, value in _word_dict.items():
            if start <= value <= end:
                _specified_words.append(key)
        return _specified_words

    @staticmethod
    def create_new_chapter(book_id, cp_num, header, text):
        """
        adds new chapter to the 'chapters' table and adds all the chapter words to the 'book_words' table
        :param book_id: the name of the book
        :param cp_num: number of chapter
        :param header: the header of the chapter
        :param text: the text of the chapter
        """
        # adds chapter to chapters table
        with sqlite3.connect(DB_FILE_NAME) as db_file:
            db_file.execute(SQL_CREATE_CHAPTER, (book_id, cp_num, header))
            # gets chapter id
            cp_id = db_file.execute(SQL_GET_ID, (book_id, cp_num)).fetchone()[0]

        word_dict = dict()
        # parsing the text to get rid of html tags
        text = text.replace("\'", "")
        for letter in PARSING_BY:
            text = text.replace(letter, " ")
        # spiting text to words
        words = text.split()
        # organizing the words into a list
        for word in words:
            # adds each part of words to the dictionary
            if 100 > len(word) > 2 and word not in INVALID_WORDS:
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
        # adding words to DB
        with sqlite3.connect(DB_FILE_NAME) as db_file:
            for word, appearance in word_dict.items():
                db_file.execute(SQL_ADD_CP_WORD, (book_id, cp_id, word, appearance))
