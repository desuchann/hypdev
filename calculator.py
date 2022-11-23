''' Task 29 '''

# set up/ explain how the calculator works to the user
print('''Calculator on.
         Type "off" to turn the calculator off.
         Enter a number, an operation, and then another number.
         
         Do you want to enter the numbers via manually (enter 1) or a file (enter 2)?''')

ops = '+ - x / % ^'
msg = 'You have not entered a number, an operation, and then another number.'

# let the user pick how they want the input entered
choice = input(': ')
while choice not in ('1', '2'):
    choice = input('Your options are manually (enter 1) or a file (enter 2): ')


def calculate(exp):
    ''' The body of the calculator. '''

    def fn(op, num1, num2):
        ''' Do the math as entered.'''

        if op == '+':
            return num1+num2
        elif op == '-':
            return num1-num2
        elif op == 'x':
            return num1*num2
        elif op == '/':
            return num1 / num2 if not num2 == 0 else 'NaN'
        elif op == '%':
            return num1 % num2
        elif op == '^':
            return num1 ** num2

    for i in ops.split():  # iterate through the available operations
        if i in exp:
            try:
                num1, num2 = exp.split(i)
            except ValueError:  # catch multiple (identical) operations
                print(msg)
                return  # start over
            try:
                num1 = int(num1)
                num2 = int(num2)
            # catch multiple (different) operations and random non-numbers
            except ValueError:
                print(msg)
                return
            # the actual math part with a sanitised input
            print(f'{exp} = {fn(i, num1, num2)}')
            return
        # catch when no operation / nothing at all is entered
        elif not any(i for i in ops.split() if i in exp):
            print(msg)
            return


if choice == '1':
    # keep the calculator on until the user turns it off
    while True:

        # save the expression entered by the user
        print(f'Available operations: {ops}')
        exp = input(': ')
        calculate(exp)

        # turn the calculator off
        if 'off' in exp.lower():
            print('Calculator off.')
            exit()

elif choice == '2':
    f = None
    while not f: # loop til a good file is provided
        file = input('Please enter the full path of your .txt file: ')
        try:
            # accept if extension not added + fail if bad extension added
            file += '.txt' if not file.endswith('.txt') else ''
            f = open(file, 'r')
        except FileNotFoundError:
            print(f'{file} does not exist.')
    for line in f:
        calculate(line.strip("\n"))
