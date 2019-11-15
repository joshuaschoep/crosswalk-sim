import matplotlib.pyplot as plt
import random
import math

class uniform_generator:
	def __iter__(self):
		return self
	
	def __next__(self):
		return random.uniform(0,1)

def exponential_1(rand: float):
    return -1 * math.log(1 - rand)

if __name__ == "__main__":
    unif = uniform_generator()
    plt.hist([exponential_1(next(unif)) for i in range(200)])
    plt.show()