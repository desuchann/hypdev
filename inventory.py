''' Task 32 / Project 4'''

from tabulate import tabulate as tb

# ========The beginning of the class==========


class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = int(quantity.strip('\n'))

    def get_cost(self):
        '''How much does the shoe cost.'''
        return self.cost

    def get_quantity(self):
        ''' how many do we have.'''
        return self.quantity

    def __str__(self):
        ''' what is seen wrhen printing a shoe obj  '''
        return self.product


# =============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []

# ==========Functions outside the class==============


def read_shoes_data():
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list.
    '''
    with open('inventory.txt', 'r') as f:
        contents = [line for line in f][1:]  # skip the first line
    shoe_list = []
    for shoe in contents:
        try:
            # unpack each shoe for instantiation
            shoe_list.append(Shoe(*shoe.split(',')))
        except:
            print('Something up with %s' % str(shoe))
    return shoe_list


def capture_shoes():
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    # get user input
    country = input('Which country is your shoe from?: ')
    code = input('What is the shoe code?: ')
    product = input('What is the name of the shoe?: ')
    cost = input('How much does the shoe cost (format XX.XX)?: ')
    quantity = input('How many of this shoe do you have?: ')
    info = (country, code, product, cost, quantity)

    try:
        shoe = Shoe(*info)  # un[ack each shoe info for instantiation]
        with open('inventory.txt', 'a') as f:
            # write the new shoe to the file for consistency
            f.write(f'{",".join(info)}\n')
        read_shoes_data()  # and have it available for the rest of the program
    except:
        print('An issue with your input! Shoe creation failed')


def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function in a tabulate.
    '''
    shoes = [[str(shoe)] for shoe in shoe_list]
    print('All products: \n', tb(shoes))


def restock():
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be restocked.
    '''
    shoes = sorted([shoe for shoe in shoe_list],
                   key=lambda x: x.quantity)  # sort the shoes by quantity
    least = shoes[0]
    res = input(
        'You have the least of %s. Would you like to restock? Yes or No: ' % str(least))
    if res.lower() == 'yes':
        try:
            extra = int(input('How many more would you like?: '))
        except:
            print('That is not an integer.')
            return
        with open('inventory.txt', 'r') as f:
            g = []
            for line in f:
                if least.code not in line:
                    g.append(line)  # add the lines not being changed
                else:
                    # replace the new line
                    g.append(
                        f'{least.country},{least.code},{least.product},{least.cost},{least.quantity+extra}\n')
        with open('inventory.txt', 'w') as f:
            for line in g:
                f.write(line)
            read_shoes_data()  # reread the file for consistency
    elif res.lower() == 'no':
        return  # do nothing
    else:
        print('That wasn\'t one pf the options...')


def search_shoe():
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    '''
    code = input('Which code are you looking for?: ')
    print('%s corresponds to' %
          code, [shoe for shoe in shoe_list if shoe.code == code][0])


def value_per_item():
    '''
    This function will calculate the total value for each item, where value = quantity*cost.
    '''
    shoes = [(shoe, float(shoe.cost)*int(shoe.quantity)) for shoe in shoe_list]
    print(tb(shoes))


def highest_qty():
    '''
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    '''
    shoes = sorted([shoe for shoe in shoe_list],
                   key=lambda x: x.quantity, reverse=True)  # sort shoe list by quantity, highest to lowest
    print('%s is for sale!' % str(shoes[0]))


# ==========Main Menu=============
'''
Execute each function above in an endless loop.
'''
while True:
    shoe_list = read_shoes_data()
    print(''' 
            c  - capture shoe data
            v  - view all shoes
            re - restock the shoes closest to running out
            se - search a shoe by code
            va - value per shoe tabulated
            hi - most expensive shoe
            e  - exit
        ''')

    choice = input('Which option would you like?: ')
    if choice == 'v':
        view_all()
    elif choice == 'se':
        search_shoe()
    elif choice == 'ca':
        capture_shoes()
    elif choice == 're':
        restock()
    elif choice == 'va':
        value_per_item()
    elif choice == 'hi':
        highest_qty()
    elif choice == 'e':
        print('Exiting...')
        exit()
    else:
        print('That wasn\'t one of the choices...')
