'''
Task 30 - simulate email messaging in an inbox
'''

# define Email class
class Email:

    def __init__(self, from_address, email_contents, has_been_read=False, is_spam=False):
        self.from_address = from_address
        self.email_contents = email_contents
        self.has_been_read = has_been_read
        self.is_spam = is_spam

    def mark_as_read(self):
        self.has_been_read = True

    def mark_as_spam(self):
        self.is_spam = True


# for in-memory assignment of email objs
inbox = []


def add_email(from_address, contents):
    ''' Add a new email obj to the inbox. '''
    inbox.append(Email(from_address, contents))


def get_count():
    ''' See how many mails are in the inbox. '''
    return len(inbox) if inbox else 0


def get_email(idx):
    ''' Pick an email to read from the inbox then mark it as read. '''
    e = inbox[idx]
    print(
        f'''\nStatus: {'Read' if e.has_been_read else 'Unread'}\nFrom: {e.from_address}\nBody: {e.email_contents}\n''')
    e.mark_as_read()


def get_unread_emails():
    ''' Return the "index" at which all the unread emails live in the inbox. '''
    return [k for k, i in enumerate(inbox, 1) if not i.has_been_read]


def get_spam_emails():
    ''' Return the "index" at which all the spam emails live in the inbox. '''
    return [k for k, i in enumerate(inbox, 1) if i.is_spam]


def delete(idx):
    ''' Choose an email to delete from the inbox. '''
    inbox.pop(idx)
    print(f'Email deleted.')


user_choice = ""
while user_choice != "quit":
    # print the latest state of the inbox and ask what the user would like next
    print(
        f'\nThere are {get_count()} emails in the inbox, of which {len(get_unread_emails())} are unread.')
    user_choice = input(
        "\nWhat would you like to do - read/mark spam/send/delete/quit?")
    # send an email
    if user_choice == "send":
        fa = input('From which address is this being sent?: ')
        body = input('Please type the body of the email: ')
        add_email(fa, body)
    # a hasty exit
    elif user_choice == "quit":
        print("Goodbye")
        break
    else:
        # save some unnecessary compute and exit if the inbox is empty
        if not inbox:
            print('\nThere are no emails on which to do that option.')
            continue
        # pick an email
        idx = int(input('\nWhich number email in the inbox do you want?: '))-1
        try:
            email = inbox[idx]
        except:
            print('That is not an option.')
            continue
        # read the email
        if user_choice == "read":
            get_email(idx)
            print(f'Unread emails left at {get_unread_emails()}.')
        # mark the email as spam
        elif user_choice == "mark spam":
            email.mark_as_spam()
            print(f'Spam emails left at {get_spam_emails()}.')
        # delete the email
        elif user_choice == "delete":
            delete(idx)
        else:
            print("Oops - incorrect input")
