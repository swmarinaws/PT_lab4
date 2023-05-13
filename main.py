import random
from math import log

class ShiftXorGenerator:
    def __init__(self, seed):
        self.seed = seed

    def rand(self):
        # Сдвигаем текущее значение seed на 4 бита влево и применяем операцию XOR
        new_seed = self.seed ^ (self.seed << 4)
        new_seed ^= new_seed >> 9
        new_seed ^= new_seed << 2

        self.seed = new_seed
        new_seed = int((new_seed & 0xffffffff) ** (1/2))
        new_seed = float('0.' + str(new_seed))
        return new_seed

class LCGenerator:
    def __init__(self, seed):
        self.seed = seed

    def rand(self):
        a = 1303525241
        c = 123456
        m = 2 ** 32
        self.seed ^= (self.seed << 13)
        self.seed ^= (self.seed >> 17)
        self.seed ^= (self.seed << 5)
        self.seed = (a * self.seed + c) % m
        return self.seed / m

sizes = [50, 100, 250, 500, 666, 1000, 2500, 5000, 7500, 10000]
time_shift, time_LC, time_standart = [], [], []
samples_shift = {}
samples_LC = {}

for i in sizes:
    first = ShiftXorGenerator(int(str(random.random())[2:]))
    samples_shift[i] = []
    for _ in range(i):
        samples_shift[i].append(first.rand())

#print(samples_shift)
print("----------ShiftXorGenerator----------:")
print("Cреднее, отклонение и коэффициент вариации:")
characteristics_shift = {}

for i in sizes:
    characteristics_shift[i] = [sum(samples_shift[i]) / i]
    temp = 0
    for j in range(i):
        temp += (samples_shift[i][j] - characteristics_shift[i][0]) ** 2
    temp /= i
    characteristics_shift[i].append(temp ** (1 / 2))
    characteristics_shift[i].append(100 * characteristics_shift[i][1] / characteristics_shift[i][0])
    print(f'size = {i}, {characteristics_shift[i]}')

for i in sizes:
    if characteristics_shift[i][2] > 33:
        print(f'Выборка объёма {i} не является однородной')
    else:
        print(f'Выборка объёма {i} является однородной')

Xi_theor = {}
Xi_theor[13] = [6.3, 18.5]
Xi_theor[16] = [8.5, 22.3]
Xi_theor[19] = [10.9, 26]
Xi_theor[21] = [12.4, 28.4]
Xi_theor[22] = [13.2, 29.6]
Xi_theor[23] = [14, 30.6]
Xi_theor[26] = [16.5, 34.4]
Xi_theor[29] = [18.9, 37.9]
Xi_theor[30] = [19.8, 39.1]
Xi_theor[31] = [20.6, 40.3]

Xi_shift = {}
for i in sizes:
    k = int(1 + 3.322 * log(i))
    Xi_shift[k] = 0
    p = 1 / k
    nj = []
    pos = 0
    for _ in range(k):
        temp = 0
        for el in samples_shift[i]:
            if pos <= el <= (pos + p):
                temp += 1
        nj.append(temp)
        pos += p
    for j in nj:
        Xi_shift[k] += j**2 / p
    Xi_shift[k] /= i
    Xi_shift[k] -= i
    print(f'k = {k}, size = {i}, Xi_exp = {Xi_shift[k]}')
    if Xi_theor[k][0] <= Xi_shift[k] <= Xi_theor[k][1]:
        print('Гипотеза о случайности равномерного генератора выполняется')
    else:
        print('Гипотеза о случайности равномерного генератора не выполняется')

#------------------------------------------------------------------------------------------------------------

for i in sizes:
    first = LCGenerator(int(str(random.random())[2:]))
    samples_LC[i] = []
    for _ in range(i):
        samples_LC[i].append(first.rand())

#print(samples_LC)
print("----------LCGenerator:----------")
print("Cреднее, отклонение и коэффициент вариации:")
characteristics_LC = {}

for i in sizes:
    characteristics_LC[i] = [sum(samples_LC[i]) / i]
    temp = 0
    for j in range(i):
        temp += (samples_LC[i][j] - characteristics_LC[i][0]) ** 2
    temp /= i
    characteristics_LC[i].append(temp ** (1 / 2))
    characteristics_LC[i].append(100 * characteristics_LC[i][1] / characteristics_LC[i][0])
    print(f'size = {i}, {characteristics_LC[i]}')

for i in sizes:
    if characteristics_LC[i][2] > 33:
        print(f'Выборка объёма {i} не является однородной')
    else:
        print(f'Выборка объёма {i} является однородной')

Xi_LC = {}
for i in sizes:
    k = int(1 + 3.322 * log(i))
    Xi_LC[k] = 0
    p = 1 / k
    nj = []
    pos = 0
    for _ in range(k):
        temp = 0
        for el in samples_LC[i]:
            if pos <= el <= (pos + p):
                temp += 1
        nj.append(temp)
        pos += p
    for j in nj:
        Xi_LC[k] += j**2 / p
    Xi_LC[k] /= i
    Xi_LC[k] -= i
    print(f'k = {k}, size = {i}, Xi_exp = {Xi_LC[k]}')
    if Xi_theor[k][0] <= Xi_LC[k] <= Xi_theor[k][1]:
        print('Гипотеза о случайности равномерного генератора выполняется')
    else:
        print('Гипотеза о случайности равномерного генератора не выполняется')

# for i in [1000, 10000, 50000, 80000, 100000, 1000000]:
#     starttime = timeit.default_timer()
#     first = ShiftXorGenerator(int(str(random.random())[2:]))
#     for _ in range(i):
#         print(first.rand())
#     end = timeit.default_timer() - starttime
#     time_shift.append(end)
# print(time_shift)
#
# for i in [1000, 10000, 50000, 80000, 100000, 1000000]:
#     starttime = timeit.default_timer()
#     for _ in range(i):
#         print(random.random())
#     end = timeit.default_timer() - starttime
#     time_standart.append(end)
# print(time_standart)
#
# for i in [1000, 10000, 50000, 80000, 100000, 1000000]:
#     starttime = timeit.default_timer()
#     first = LCGenerator(int(str(random.random())[2:]))
#     for _ in range(i):
#         print(first.rand())
#     end = timeit.default_timer() - starttime
#     time_LC.append(end)
# print(time_LC)