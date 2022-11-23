''' Project 3 / Task 26 '''
import datetime
import re


def main_menu():
    '''Exit to the main menu. '''
    print('Exiting...')
    return


def user_exists(user):
    '''Check if the supplied user has already been registered.
       Returns True if they have. '''

    with open('user.txt', 'r') as f:
        users = [line.split(', ')[0] for line in f]
        if user in users:
            print('User already exists.')
            return True


def reg_user():
    '''Register a new user. '''

    # ask for the username and password
    user = input('Please supply the username: ')
    pwd = input('Please supply the password: ')
    pwd2 = input('Please confirm the password: ')

    # check the password was entered correctly
    while not pwd == pwd2:
        print('The password entries did not match.')
        pwd = input('Please supply the password: ')
        pwd2 = input('Please confirm the password: ')

    # check if the user already exists
    if user_exists(user):
        return
    # update user.txt with the new user
    with open('user.txt', 'a') as f:
        f.write(f'\n{user}, {pwd}')
        print('User successfully added.')


def due_fn():
    ''' Function for parsing the due date entered by user. '''

    # get the date off the user
    due_string = input('By when is the task due? Enter as YYYY,MM,DD: ')
    due_date = None
    while not due_date:
        try:
            # check the provided due date is in a vaguely correct format
            if not re.match('20\d{2},\d{2},\d{2}', due_string):
                raise ValueError
            # attempt to put the dates in the specified format
            due_string = due_string.split(',')
            due_date = datetime.date(int(due_string[0]),
                                     int(due_string[1]),
                                     int(due_string[2])).strftime("%d %b %Y")
        except:
            # provide more info if not in the correct format. loop until it's correct
            print('That\'s the wrong format.')
            print('Help: include the commas, digits only, 0 padded month if necessary')
            due_string = input('Please use YYYY,MM,DD: ')
            continue
    return due_date


def add_task(vm=False, contents=None):
    ''' Add a new task. '''
    # ask for each of the fields needed in a task
    user = input('To whom is this task assigned: ')
    if not user_exists(user):  # immediately exit if the user isn't registered
        print('User does not exist.')
        return
    title = input('What is the title of the task?: ')
    desc = input('Please supply a description of the task: ')
    due_date = due_fn()
    current_date = datetime.date.today().strftime("%d %b %Y")

    task_str = f'\n{user}, {title}, {desc}, {current_date}, {due_date}, %s'

    if vm:  # extra logic regarding completiong status used in the vm section
        with open('tasks.txt', 'r+') as f:
            status = input('Is this task complete? Yes or No: ')
            while status not in ('Yes', 'No'):
                status = input('Please only enter Yes or No: ')
            f.write(task_str % status)
    else:
        # add the compiled task to tasks.txt
        with open('tasks.txt', 'a') as f:
            f.write(task_str % 'No')
    print('Task successfully assigned.')


def pprint(vm=False):
    ''' Printing the contents of files in a pretty tabular format. '''

    with open('tasks.txt', 'r') as f:
        contents = [line for line in f]
    task_ns = []
    for n, line in enumerate(contents, 1):
        line = line.split(', ')
        user = line[0]
        if vm:  # bool means this function can be used for va and vm
            if not current_user == user:  # filter out everything not for the current user
                continue
        task_ns.append(n)  # for indexing the tasks later
        title = line[1]
        desc = line[2]
        current_date = line[3]
        due_date = line[4]
        status = line[5].strip('\n')

        # print the nice table
        print('-'*50+'\n')
        print(f'Task number:\t\t{n}')
        print(f'Task title:\t\t{title}')
        print(f'Assigned to:\t\t{user}')
        print(f'Date assigned:\t\t{current_date}')
        print(f'Due date:\t\t{due_date}')
        print(f'Task complete?:\t\t{status}')
        print(f'Task description:\n\n\t{desc}')

    # some extra logging for vm
    if vm and not task_ns:
        print('\nYou have no assigned tasks.\n')
        return [], []
    print('\n'+'-'*50)
    return contents, task_ns


def vm_edit(contents, task_ns):
    ''' For the user to edit their tasks.'''

    # their tasks are printed before this for them to choose
    print('Are there any tasks you\'d like to edit?')
    while True:
        task_n = input('Enter the task number or -1 to exit: ')
        try:
            task_n = int(task_n)
        except:  # they've entered a letter or something
            print('That\'s not one of the options.')
            continue
        if task_n == -1:
            main_menu()
            break
        elif task_n not in task_ns:  # only allowed to edit their own tasks
            print('That\'s not one of your task numbers.')
            continue
        else:
            # decide how they want to edit the task
            edit_task = input(
                '''Enter 1 to mark the task as complete
                    2 to edit the task details
                    -1 to exit: ''')
            try:
                edit_task = int(edit_task)
            except:  # they've entered a letter or something
                print('That\'s not one of the options.')
                continue
            if edit_task == -1:  # exit
                main_menu()
                break
            elif edit_task == 1:
                # mark the task as complete. for tasks already complete, it's a no-op
                task_line = contents[task_n-1]
                task_info, task_status = task_line.rsplit(', ', 1)
                task_line = task_info + ', ' + \
                    task_status.replace('No', 'Yes')
                contents[task_n-1] = task_line
                with open('tasks.txt', 'r+') as f:
                    for line in contents:
                        f.write(line)
                    print(f'Task {task_n} marked as complete.')
            elif edit_task == 2:
                user, title, desc, a_date, due_date, status = contents[task_n-1].split(
                    ', ')
                # return to options if they choose a completed one
                if 'No' not in status:
                    print(
                        'Only tasks which are yet to be completed can be edited.')
                    continue
                else:
                    user_ddate = None
                    while user_ddate not in ('user', 'due_date', '-1'):
                        user_ddate = input(
                            'Would you like to edit the user (enter user) the due date (enter due date) or exit (enter -1)?: ')
                        if user_ddate == 'user':
                            # edit the user on the chosen task
                            print(f'Current user: {user}')
                            new_user = input(
                                'Enter/re-enter the user this task should be assigned to: ')
                            while not user_exists(new_user):
                                new_user = input(
                                    'That\'s not a registered user, pls try again: ')
                            # remove the task from your view asap
                            if not new_user == user:
                                task_ns.remove(task_n)
                                user = new_user
                        elif user_ddate == 'due date':
                            # edit the due date on the chosen task
                            due_date = due_fn()
                        elif user_ddate == '-1':  # exit
                            main_menu()
                            break
                        else:
                            print('That\'s not one of the options.')
                            continue
                        # write the updated task changes
                        with open('tasks.txt', 'w') as f:
                            contents[task_n-1] = ', '.join(
                                (user, title, desc, a_date, due_date, status))
                            for line in contents:
                                f.write(line)
                        print('Task successfully updated.')
            elif edit_task == -1:  # exit
                main_menu()
                return
        _, _ = pprint(vm=True)  # print the lastest at the end


def view_all():
    ''' View all the tasks in task.txt '''
    _, _ = pprint(vm=False)


def view_mine():
    ''' View and edit all the tasks assigend to the current user in task.txt '''
    contents, task_ns = pprint(vm=True)

    # section to edit user's tasks if they so wish
    vm_edit(contents, task_ns)


def gen_reports():
    ''' Generate reports about the users and their tasks. '''

    with open('tasks.txt', 'r') as f:
        contents = [line for line in f]
    contents_info = [(user, ddate, status.strip('\n')) for line in contents for user,
                     ddate, status in [line.split(', ')[:1]+line.rsplit(', ', 2)[-2:]]]  # all tasks
    incomplete = []
    complete = []
    for line in contents_info:
        # incomplete and complete tasks
        complete.append(line) if line[-1] == 'Yes' else incomplete.append(line)
    today = datetime.datetime.today()
    overdue = [line for line in incomplete if datetime.datetime.strptime(
        line[-2], '%d %b %Y') < today]  # tasks with a due date prior to today (not inclusive)
    # percentage of total incomplete
    pct_incomplete = f'{(len(incomplete)/len(contents_info))*100:0.1f}%'
    # percentage od total overdue
    pct_overdue = f'{(len(overdue)/len(contents_info))*100:0.1f}%'

    # write all the info to the overview
    with open('task_overview.txt', 'w') as f:
        f.write(f'Total number of tasks:\t\t{len(contents)}\n')
        f.write(f'Number of complete tasks:\t{len(complete)}\n')
        f.write(f'Number of incomplete tasks:\t{len(incomplete)}\n')
        f.write(f'Number of overdue tasks:\t{len(overdue)}\n')
        f.write(f'%age of incomplete tasks:\t{pct_incomplete}\n')
        f.write(f'%age of overdue tasks:\t\t{pct_overdue}')

    with open('user.txt', 'r') as f:
        users = [user for line in f for user, _ in [
            line.split(', ')]]  # all the users

    with open('user_overview.txt', 'w') as f:
        f.write(f'Total number of users:\t\t{len(users)}\n')
        f.write(f'Total number of tasks:\t\t{len(contents)}\n')
        for user in users:
            f.write('\n{dash} {user} {dash}\n'.format(
                dash='='*10, user=user))  # a nice header/ divider
            # tasks for the current user
            user_tasks = [task for task in contents_info if task[0] == user]
            # percentage of the total the user has
            pct_total = f'{(len(user_tasks)/len(contents_info))*100:0.1f}%'
            # user's complete tasks
            user_complete = [task for task in user_tasks if task[2] == 'Yes']
            # percentage of user's complete
            pct_user_complete = f'{(len(user_complete)/len(user_tasks))*100:0.1f}%'
            # user's incomplete tasks
            user_incomplete = [task for task in user_tasks if task[2] == 'No']
            # percentage of user's incomplete
            pct_user_incomplete = f'{(len(user_incomplete)/len(user_tasks))*100:0.1f}%'
            # user's overdue
            user_overdue = [line for line in user_incomplete if datetime.datetime.strptime(
                line[-2], '%d %b %Y') < today]
            # percentage of user's overdue
            pct_user_overdue = f'{(len(user_overdue)/len(user_tasks))*100:0.1f}%'

            f.write(f'Total number of tasks:\t\t{len(user_tasks)}\n')
            f.write(f'%age of total owned:\t\t{pct_total}\n')
            f.write(f'%age of complete tasks:\t\t{pct_user_complete}\n')
            f.write(f'%age of incomplete tasks:\t{pct_user_incomplete}\n')
            f.write(f'%age of overdue tasks:\t\t{pct_user_overdue}')
    print('Overview reports successfully generated.')


def display_stats():
    '''Print the overview files. Generate them first if they don't exist. '''
    try:
        f = open('task_overview.txt', 'r')
        g = open('user_overview.txt', 'r')
    except FileNotFoundError:
        gen_reports()
        f = open('task_overview.txt', 'r')
        g = open('user_overview.txt', 'r')

    for line in f:
        print(line)
    f.close()
    for line in [line for line in g][2:]:
        print(line)
    g.close()


# ==== Login Section ====#
current_user = input('Please supply your username: ')
pwd = input('Please supply your password: ')

# ==== credentials check ====#
with open('user.txt', 'r') as f:
    # make it an immutable tuple for extra safety
    contents = [tuple(line.strip('\n').split(', ')) for line in f]

    while not any((current_user, pwd) == i for i in contents):
        # learned this purposeful ambiguity from a code security course!
        print('You supplied an incorrect username and password combination.')
        current_user = input('Please supply your username: ')
        pwd = input('Please supply your password: ')

while True:

    # presenting the menu to the user (case insensitive)
    menu = input('''\nPlease select one of the following options:

                    r  - Registering a user (admin only)
                    a  - Adding a task
                    va - View all tasks
                    vm - View my tasks
                    gr - Generate reports (admin only)
                    ds - Display statistics (admin only)
                    e  - Exit

                    : ''').lower()

    # === register a new user ===#
    if menu == 'r':
        if current_user != 'admin':  # admin only check
            print('*DENIED* You do not have permission to use this menu option. *DENIED*')
            continue
        reg_user()

    # === add a new task ===#
    elif menu == 'a':
        add_task()

    # === view all tasks ===#
    elif menu == 'va':
        view_all()

    # === view your tasks only ===#
    elif menu == 'vm':
        view_mine()

    # === display task and user stats ===#
    elif menu == 'ds':
        if current_user != 'admin':  # admin only check
            print('*DENIED* You do not have permission to use this menu option. *DENIED*')
            continue
        display_stats()

    # === generate user and task reports === #
    elif menu == 'gr':
        if current_user != 'admin':  # admin only check
            print('*DENIED* You do not have permission to use this menu option. *DENIED*')
            continue
        gen_reports()

    # === a hasty exit ===#
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, please try again.")
