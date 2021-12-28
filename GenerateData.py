import random
import math
import numpy as np

DataNum = 50000 # how many simulation packets

prob_list = np.arange(0, 1.1, 0.1)


def generate(rate):
    result = []
    for _ in range(DataNum):
        F = random.random()
        x = -math.log(1-F)/rate
        result.append(x)
    return result

if __name__ == '__main__':
    testing_date = generate(30)
    print(prob_list)

