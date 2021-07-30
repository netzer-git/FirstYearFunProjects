import sqlite3

from Errors import UserNameException

DB_FILE_NAME = "PsychoDB.db"
SQL_ADD_WORD = "INSERT OR IGNORE INTO user_words (word, user_id) VALUES (?, ?);"
SQL_CREATE_USER = "INSERT INTO user_names (name) VALUES (?);"
SQL_CHECK_NAME = "SELECT EXISTS (SELECT 1 FROM user_names WHERE name = ?);"
SQL_ADD_KNOWN = "SELECT word FROM user_words WHERE user_id = ?"
SQL_GET_USER_ID = "SELECT rowid FROM user_names WHERE name = ?;"


class User:
    """
    the class represent and handles the known words to the user
    """

    def __init__(self, name):
        """
        loads user from DB
        :param name: the user name
        """
        self._user_name = name
        self._known = set()

        try:
            with sqlite3.connect(DB_FILE_NAME) as db_file:
                self._current_user_id = db_file.execute(SQL_GET_USER_ID, (self._user_name,)).fetchone()[0]
                cursor = db_file.execute(SQL_ADD_KNOWN, (self._current_user_id,))
                for word in cursor:
                    self._known.add(word)
        except sqlite3.OperationalError:
            print("Error opening DB. user: " + self._user_name)
            exit(1)

    @staticmethod
    def create_new_user(name):
        """
        creates new user and adds it to the users DB
        :param name: the name of the new user
        :raise: in case of taken name
        """
        with sqlite3.connect(DB_FILE_NAME) as db_file:
            if User.is_user_exists(name):
                raise UserNameException()
            db_file.execute(SQL_CREATE_USER, (name,))

    @staticmethod
    def is_user_exists(name):
        """
        check if user name exists in db
        :param name: the user's name
        :return: true if the name exists, false otherwise
        """
        with sqlite3.connect(DB_FILE_NAME) as db_file:
            return db_file.execute(SQL_CHECK_NAME, (name,)).fetchone()[0]

    def get_words(self):
        """
        :return: the set of known words
        """
        return self._known

    def add_word(self, word):
        """
        takes a word and adds it to known words
        :param word: the new word the user know
        """
        self._known.add(word)

    def update_db(self, new_known):
        """
        takes a set of words and adds it to known words
        :param new_known: the new set of words the user know
        """
        self._known = new_known

    def save_changes(self):
        """
        saves the new known words set to user db file
        """
        with sqlite3.connect(DB_FILE_NAME) as db_file:
            for word in self._known:
                db_file.execute(SQL_ADD_WORD, (word, self._current_user_id))
