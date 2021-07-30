import sqlite3


def create_db():
    """
    creates the program DB
    """

    connect = sqlite3.connect("PsychoDB.db")
    # create user table
    connect.execute('''CREATE TABLE user_names
                    (name TEXT NOT NULL);''')
    # create the user words table
    connect.execute('''CREATE TABLE user_words 
                    (word TEXT NOT NULL,
                    user_id INT NOT NULL,
                    UNIQUE (word, user_id));''')
    # create the books table
    connect.execute('''CREATE TABLE books
                    (name TEXT NOT NULL UNIQUE,
                    max_chapters INT NOT NULL,
                    genre TEXT);''')
    # create chapter table
    connect.execute('''CREATE TABLE chapters 
                    (book_id INT NOT NULL,
                    cp_num INT NOT NULL,
                    title TEXT);''')
    # create the book words table
    connect.execute('''CREATE TABLE book_words
                    (book_id INT NOT NULL,
                    chapter_id INT NOT NULL,
                    word TEXT NOT NULL,
                    appearance INT NOT NULL,
                    UNIQUE (book_id, chapter_id, word));''')


def test():
    con = sqlite3.connect('test.db')
    con.execute('''INSERT INTO user_names (name) VALUES ("Yarden");''')
    v = ("Yarden",)
    cru = con.execute("SELECT EXISTS (SELECT 1 FROM user_names WHERE name = ?);", ("bh",))
    print(cru.fetchone()[0])
    for row in cru:
        print(row)
    connect = sqlite3.connect("user_words.db")

    connect.execute("INSERT OR IGNORE INTO words (word, user_id) VALUES (?, ?)", ("No", "Netzer"))


if __name__ == "__main__":
    create_db()
    # test()
