'''
Task 46/47 - SQL and SQLite
'''

import sqlite3

try:
    # set up the db and table
    db = sqlite3.connect('data/pp_db')
    c = db.cursor()
    c.execute('''CREATE TABLE python_programming (
        id int PRIMARY KEY,
        name varchar,
        grade int
    )''')
    c.executemany(
        '''INSERT INTO python_programming VALUES (?,?,?)''', [(55, 'Carl Davis', 61), (66, 'Dennis Fredrickson', 88), (77,
                                                                                                                       'Jane Richards', 78), (12, 'Peyton Sawyers', 45), (2, 'Lucas Brooker', 99)])

    def _status(cursor, msg):
        ''' Print the table as it currently looks. '''
        print(msg)
        cursor.execute('''SELECT * from python_programming''')
        print([row for row in cursor])

    # boot camp answers
    grades = c.execute(
        '''SELECT * FROM python_programming WHERE grade >= 60 AND grade <= 80;''')
    print('Details of all those with grades between 60 and 80: \n%s' %
          [row for row in grades])

    c.execute('''UPDATE python_programming SET grade = 65 WHERE id = 55''')
    _status(c, 'State after replacing Carl Davis\' grade: ') 

    c.execute('''DELETE FROM python_programming WHERE id = 66''')
    _status(c, 'State after deleting Dennis Fredrickson\'s row: ')

    c.execute('''UPDATE python_programming SET grade = 0 WHERE id < 55''')
    _status(c, 'Wipe the grade of everyone with an id below 55!: ')

finally:
    # make the file easier to run multiple times
    c.execute('''DROP TABLE python_programming''')
    db.close()
