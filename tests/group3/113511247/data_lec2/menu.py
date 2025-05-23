import random

class Food(object):
    """
    A food item with a name, value, and calories
    """
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w

    def get_value(self):
        return self.value

    def get_cost(self):
        return self.calories
    
    def density(self):
        return self.get_value() / self.get_cost()

    def __str__(self):
        return (
            self.name + ': <' + str(self.value) +
            ', ' + str(self.calories) + '>'
        )

class Menu(object):
    """
    A menu of food items
    """
    # pair/pair....
    # use the frame of "Food"
    def __init__(self, names=[], values=[], calories=[]):
        self.foods = []
        for i in range(len(values)):
            self.foods.append(Food(names[i], values[i],
                              calories[i]))
    # final structure:a list of "Food" items,        
    
    def build_large_menu(self, num_items, max_val, max_cost):
        self.foods = []
        for i in range(num_items):
            self.foods.append(Food(str(i), random.randint(1, max_val), 
                              random.randint(1, max_cost)))
    #random.randint(start, end): random integer
    #random.randint(1, 10) returns a random integer N such that 1 <= N <= 10.

    def get_foods(self):
        return self.foods

    # @staticmethod: a decorator that indicates that a method 
    # does not require an instance of the class to be called.
    @staticmethod
    def get_foods_str(foods):
        foods_str = ""
        for item in foods:
            foods_str += str(item) + '; '
        return foods_str
    
    def __str__(self):
        return Menu.get_foods_str(self.foods)

# GREEDY ALGORITHMS: approaches to solving optimization problems
# build up a solution piece by piece, always choosing the next piece
# that offers the most immediate benefit.
def greedy(items, max_cost, key_function):
    """Assumes items a list, max_cost >= 0,
    key_function maps elements of items to numbers"""
    #simplified greedy because we only need to 'sort' 'once'
    items_copy = sorted(items, key=key_function, reverse=True)
    result = []
    total_value, total_cost = 0.0, 0.0
    for i in range(len(items_copy)):
        if (total_cost + items_copy[i].get_cost()) <= max_cost:
            result.append(items_copy[i])
            total_cost += items_copy[i].get_cost()
            total_value += items_copy[i].get_value()
    return (result, total_value)

def max_val(to_consider, avail):
    #recursive
    #to_consider: a list of "Food" items
    # return structure : a tuple of a integer and a tuple of "Food" items
    """Assumes 'to_consider' a list of items, 'avail' a weight
    Returns a tuple of the total value of a solution to the
    0/1 knapsack problem and the items of that solution"""
    # base case: if no items to consider or no available weight
    if to_consider == [] or avail == 0:
        result = (0, ())
    elif to_consider[0].get_cost() > avail:
        # skip it
        result = max_val(to_consider[1:], avail)
    else:
        # reduce access time to the first item
        next_item = to_consider[0]

        # take it (explore left branch)
        # with_val: a integer
        # with_to_take: a tuple of "Food" items
        with_val, with_to_take = max_val(
            to_consider[1:], avail - next_item.get_cost())
        with_val += next_item.get_value()

        # not take it (explore right branch)
        without_val, without_to_take = max_val(to_consider[1:], avail)

        # Choose better branch
        if with_val > without_val:
            result = (with_val, with_to_take + (next_item,))
        else:
            result = (without_val, without_to_take)
    return result


def fast_max_val(to_consider, avail, memo={}):
    """Assumes 'to_consider' a list of subjects, 'avail' a weight 
    'memo' supplied by recursive calls 
    Returns a tuple of the total value of a solution to the 
    0/1 knapsack problem and the subjects of that solution"""
    # memo: a dictionary to store the results of subproblems
    # key: (len(to_consider), avail)
    # value: result of the subproblem
    if (len(to_consider), avail) in memo:
        result = memo[(len(to_consider), avail)]
    elif to_consider == [] or avail == 0:
        result = (0, ())
    elif to_consider[0].get_cost() > avail:
        # Explore right branch only 
        result = fast_max_val(to_consider[1:], avail, memo)
    else:
        next_item = to_consider[0]

        # take it
        with_val, with_to_take = fast_max_val(
            to_consider[1:], avail - next_item.get_cost(), memo)
        with_val += next_item.get_value()

        # not take it
        without_val, without_to_take = fast_max_val(
            to_consider[1:], avail, memo)
        
        # Choose better branch 
        if with_val > without_val:
            result = (with_val, with_to_take + (next_item,))
        else:
            result = (without_val, without_to_take)
            
    # store the answer of the subproblem in the memo
    memo[(len(to_consider), avail)] = result
    return result