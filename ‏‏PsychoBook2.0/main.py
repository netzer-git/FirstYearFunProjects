import sqlite3
from Book import Book
from Chapter import Chapter
from Errors import UserNameException, ReadingParameterException, BookNameException
from User import User
import random as rnd

MAIN_MENU = "****************************************\n" \
            "Hey! please choose starting option:\n" \
            "1 --- Start reading!\n" \
            "2 --- Add new Book\n" \
            "3 --- Add new User\n" \
            "q --- Quit\n" \
            "****************************************\n"
STARS = "****************************************\n" \
        "****************************************\n" \
        "****************************************\n"
EMPTY = '-1'
MAX_TRY = 15
OUT = ['q', 'Q']


# ****************************** Read Chapter *************************
def do_you_know(word):
    """
    the function takes a word and asks the user if he know it
    :param word
    :return: True if the user knows, False otherwise
    """
    ans = input("Do you know the word: " + word + " (y/n): ")
    while True:
        if ans in ['y', 'Y']:
            return True
        elif ans in ['n', 'N']:
            return False
        elif ans in OUT:
            print("In the middle? ok...")
            quit(0)
        else:
            ans = input("Please enter (y/n): ")


def get_word_unknown_from_list(cp_words, db_words, cp_list):
    """
    the function takes an unknown word from the chapter wanted words
    :param cp_words: chapter words
    :param db_words: user known words
    :param cp_list: the list of target words for the chapter
    :return: the chosen word, or False in case of no match
    """
    try_counter = 0
    while try_counter < MAX_TRY:
        word = cp_words[rnd.randint(0, len(cp_words) - 1)]
        if word not in db_words and word not in cp_list:
            return word
        try_counter += 1
    return False


def create_target_list(user, chapter):
    """
    the function create a list of words from the chapter specific for the user
    :param user
    :param chapter
    :return: the list of user
    """
    # todo: second half of the changes
    target_list = set()
    user_db = user.get_words()
    # the secret spice
    print("\nNow its time to find the words for your next chapter!")
    word_counter = 0
    # 1 words between 5 and 50
    specified_words = chapter.get_specified_words(5, 50)
    while word_counter < 1:
        word = get_word_unknown_from_list(specified_words, user_db, target_list)
        if not word:
            print("We got " + str(word_counter) + " words in 5-50.")
            break
        elif do_you_know(word):
            user_db.add(word)
        else:
            target_list.add(word)
            word_counter += 1
    # 3 words between 2 and 5
    specified_words = chapter.get_specified_words(2, 5)
    while word_counter < 4:
        word = get_word_unknown_from_list(specified_words, user_db, target_list)
        if not word:
            print("We got " + str(word_counter - 2) + " words in 2-5.")
            break
        elif do_you_know(word):
            user_db.add(word)
        else:
            target_list.add(word)
            word_counter += 1
    # 6 words between 1 and 2
    specified_words = chapter.get_specified_words(1, 2)
    while word_counter < 10:
        word = get_word_unknown_from_list(specified_words, user_db, target_list)
        if not word:
            print("We got " + str(word_counter - 5) + " words in 1-2.")
            break
        elif do_you_know(word):
            user_db.add(word)
        else:
            target_list.add(word)
            word_counter += 1
    user.update_db(user_db)
    print(STARS)
    # checks the whole list
    if len(target_list) > 0:
        print("We got " + str(word_counter) + " new words for you from the chapter!")
        return target_list
    else:
        print("We couldn't find new words for you in the chapter")
        return False


def chapter_text_file(file_name):
    """
    reads the chapter text
    :param file_name: the chapter file name
    :return: the file text
    """
    with open("temp_text/" + file_name + ".txt") as cp_file:
        text = cp_file.read()
    return text


def get_user_name():
    """
    takes one of the reading parameters
    :return: the reader name
    """
    name = EMPTY
    while not User.is_user_exists(name):
        name = input("Please Enter your User name (make sure you have one!): ")
        if name in OUT:
            raise ReadingParameterException
    return name


def get_book_name():
    """
    takes book name from the user and checks the book's integrity.
    :return: the name of the book chosen by the user
    """
    book_name = EMPTY
    while not Book.is_book_exists(book_name):
        book_name = input("Please enter book name (means the epub file name): ")
        if book_name in OUT:
            raise ReadingParameterException
    return book_name


def get_chapter_num(cp_max):
    """
    takes chapter number of the book and gets the wanted chapter number from the user
    :param cp_max: the last chapter
    :return: the chapter number wanted by the user.
    """
    cp_num = 0
    while cp_num < 1 or cp_max < cp_num:
        cp_num = input("Please choose chapter number (between 1 and " + cp_max + "): ")
    return cp_num


def get_reading_parameters():
    """
    takes the parameters for the reading - book name, user name and chapter number.
    in case of an error return 0 as user name.
    :return: user name, book name and chapter number.
    """
    # gets the user name
    user_name = get_user_name()
    # gets the book name
    book_name = get_book_name()
    # open the book and take the max number of chapters todo: fix after moving to DB
    cp_max = Book(book_name).get_max_cp()

    print("\nYour book: " + book_name + "\nThere are: " + cp_max + " chapters\n")
    cp_num = get_chapter_num(cp_max)

    if not cp_num:
        raise ReadingParameterException

    return user_name, book_name, cp_num


def reading_menu():
    # todo: most of the changes needed here
    try:
        user_name, book, cp_num = get_reading_parameters()
    except ReadingParameterException:
        print("\nSending back to Main Menu\n")
        return
    # reading chapter file and turning it to string
    text = chapter_text_file(book + '_cp' + cp_num)
    # declaring user db and chapter
    user = User(user_name)
    chapter = Chapter(book + '_cp' + cp_num, text)
    # getting the list of target words for the chapter
    target_list = create_target_list(user, chapter)
    if not target_list:
        print("\nSending back to Main Menu\n")
        return
    print("Now its time to go and read!\n"
          "dont forget your new words!")
    for word in target_list:
        print("--- " + word + " ---")
    print("Good luck!")
    print(STARS)
    input("Press ENTER to start checking your progress!")
    new_words = 0
    for word in target_list:
        if do_you_know(word):
            user.add_word(word)
            new_words += 1
    user.save_changes()
    if new_words > 0:
        print("You learned " + str(new_words) + " new words!\n")


# ****************************** Other Menus *************************
def main_menu():
    """
    display the main menu of the program and takes the user choice
    :return: the user choice
    """
    first_choice = input(MAIN_MENU)
    while first_choice not in ['1', '2', '3', 'q', 'Q']:
        first_choice = input("Please Enter valid choice: ")
    return first_choice


def create_book(name):
    """
    creates new book - split to chapters and creates book file
    :param name: the epub file name
    """
    # check if the book is already in the system
    if Book.is_book_exists(name):
        raise BookNameException
    # create new book
    Book.create_new_book(name)


def create_book_menu():
    """
    prints the menu of book creation and activates book create method
    """
    while True:
        book_name = input("Please enter the new book name: ")
        try:
            create_book(book_name)
            break
        except FileNotFoundError or sqlite3.OperationalError:
            print("It seems like there is a problem, please try again: ")
        except BookNameException:
            print("The book is already loaded, enter 'q' to go back ")

    print("New book saved! good luck!\n")


def add_user_menu():
    """
    takes a new user name and create new DB file for the user
    """
    print("Welcome new User!")
    while True:
        try:
            user_name = input("Please enter your name: \n")
            User.create_new_user(user_name)
            break
        except UserNameException:
            print("The name is already taken, please try again!\n")
    print("User open successfully! Good luck! \n")


# ****************************** Main *************************
def main():
    """
    main program, handles menus
    """
    while True:
        user_choice = main_menu()
        if user_choice == '1':
            reading_menu()
        elif user_choice == '2':
            create_book_menu()
        elif user_choice == '3':
            add_user_menu()
        else:
            print("Bye!")
            quit(0)


if __name__ == '__main__':
    main()
