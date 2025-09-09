import pandas
from utils.add import add


class MyList(list):
    def __hash__(self):
        return tuple(self).__hash__()


def main():
    # variables, conditionals, while, for loops, functions
    # classes, imports, lists, tuples, dictionaries
    # __main__ stuff
    a = 5
    if (a > 0 and a < 10 or a == 42):
        print("a is positive")

    my_list = MyList([1, 2, 3])

    my_tuple = (1, 2, 3)
    my_tuple += (6, 7, 8)

    data = {
        my_list: 1, 
        'b': 2
    }

    my_list.append(4)
    
    my_new_list = MyList([1, 2, 3])
    print(data[my_new_list])

if __name__ == "__main__":
    main()
