
from collections import namedtuple
from sys import setprofile


def orginal(*args):

    list_one = list(args)

    for i in list_one:
        print(str(i) + " GoodBye")

    print(list_one)


orginal('rafi', 'mly', 'rafi', 'sldjf')


def test(*args, **kwargs):

    for i in kwargs.values():
        print(i[0])

    for i in args:
        print(i, " new list")



test('rafi', 'mly', 'rafi', 'sldjf', name = ['rafi','name'], birth = ['2524', '5585'])

print("Time to create class Huh")



class Animal:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        print(self.args)
        print(self.kwargs)
    
    def print_something(self):

        for i in self.kwargs.values():
            print(i)
        
        print("something print ")



Animal("lol", "miow",  name = ['rafi','name'], birth = ['2524', '5585']  )

bar =  Animal("lol", "miow",  name = ['rafi','name'], birth = ['2524', '5585']  )

bar.print_something()


class Dog(Animal):

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name

        print(name)

    def print_list(self):

        for i in self.args:

            print(i)


puppy = Dog("r",'c', 'b',  sss = ['rafi','name'], birth = ['2524', '5585']  )

puppy.print_something()

puppy.print_list()



class pupu(Dog):

    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

barr = pupu(1, 2, 3, 5, 6, sss = ['ddddddddddddddd','name'], birth = ['2524', '5585'])

barr.print_list()

barr.print_something()







