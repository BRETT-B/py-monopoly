import random


class Dice(object):
   def __init__(self):
       self.random = random
       self.doubles = False

   def roll(self):

       r1 = (self.random.randrange(6) + 1)
       r2 = (self.random.randrange(6) + 1)
       self.doubles = r1 == r2
        

       return r1 + r2