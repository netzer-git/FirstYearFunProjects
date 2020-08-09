class Chapter:
    """
    A class used to represent the words in a chapter in a book
    """

    def __init__(self, name, text):
        parsing_by = ["/", "\"", "<", ">", "=", "!", "?", ",", ".", "&",
                      "#", "%", "\'", "\\", ";", "-", "_", ")", "("
                      "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        invalid_words = ["\n", "div", "class", "id", "href", "xe", "calibre", "bac", "img", "src",
                         "html", "alt", "jpeg", "image", "span", "calibre1", "xhtml"]
        # variables
        self._file_name = "temp_text/" + name + ".txt"
        self._text = text

        self._words = []
        self._word_list = []
        self._set_of_word_file = set()
        # parsing the text to get rid of html tags
        self._text = self._text.replace("\'", "")
        for letter in parsing_by:
            self._text = self._text.replace(letter, " ")
        # spiting text to words
        self._words = self._text.split()
        # finalizing valid word list
        for word in self._words:
            # change the 100 if needed
            if 100 > len(word) > 2 and word not in invalid_words:
                self._word_list.append(word)

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

    def save_chapter_as_text(self, cp_name):
        """
        save the chapter text as text file
        """
        # either write as all of the words or words+num
        file_name = "temp_text/" + cp_name + ".txt"
        with open(file_name, 'w') as chap_file:
            for word in self._word_list:
                chap_file.write(word + "\n")

        # file_name = "temp_text/" + cp_name + ".txt"
        # with open(file_name, 'w') as chap_file:
        #     for word, value in self._word_count.items():
        #         chap_file.write(word + " " + str(value) + "\n")
