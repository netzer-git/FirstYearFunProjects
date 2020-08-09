class UserDB:
    """
    the class represent and handles the known words to the user
    """

    def __init__(self, name, new_user=False):
        self._user_name = name
        self._db_file_name = "user_db/" + self._user_name + ".txt"
        self._known = set()

        if new_user:
            with open(self._db_file_name, 'w') as db_file:
                db_file.write("points 5000000")

        try:
            with open(self._db_file_name, 'r') as db_file:
                self._points = int(db_file.readline().split()[1])
                for line in db_file:
                    for word in line.split():
                        self._known.add(word)
        except FileNotFoundError:
            print("Error opening DB. user: " + self._user_name)
            exit(1)

    def get_points(self):
        """
        :return: the user points
        """
        return self._points

    def update_points(self, update):
        """
        :param update: the new update to the points
        """
        self._points += update

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
        saves the new knon words set to user db file
        """
        with open(self._db_file_name, 'w') as db_file:
            db_file.write("points " + str(self._points) + "\n")
            for word in self._known:
                db_file.write(word + "\n")
