import matplotlib.pyplot as plt
import random
import math

class uniform_generator:
	def __iter__(self):
		return self
	
	def __next__(self):
		return random.uniform(0,1)

def exponential_u(rand: float, u: float):
    return -1 * math.log(1 - rand) * u

def uniform_ab(rand: float, a: float, b: float):
    return a + (rand * (b - a))

if __name__ == "__main__":
    unif = uniform_generator()
    plt.hist([next(unif) for i in range(2000)])
    plt.show()
    plt.hist([exponential_u(next(unif), 20) for i in range(2000)])
    plt.show()
    plt.hist([uniform_ab(next(unif), 2.6, 4.1) for i in range(2000)])
    plt.show()