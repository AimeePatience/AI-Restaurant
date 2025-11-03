
class Chef:
    def __init__(self, name, ratings, score):
        self.__name = name
        self.__ratings = ratings
        self.__score = score # no. of compliments - no. of complaints

class Customer:
    def __init__(self, name, is_vip, warnings):
        self.__name = name
        self.__is_vip = is_vip
        self.__warnings = warnings

class Visitor:
    def __init__(self, name):
        self.__name = name

class DeliveryPerson:
    def __init__(self, name):
        self.__name = name
