def fu(first_list, second_list, a):
    maximum = 0
    j = 0
    Z = [0, 0, 0, 0, 0, 0, 0]
    for i in range(a + 1):
        while j + i < a + 1:
            Z[j + i] = max(first_list[i] + second_list[j], Z[j + i])
            if first_list[i] + second_list[j] > maximum:
                maximum = first_list[i] + second_list[j]
                Z[len(Z) - 1] = i
            j += 1
        j = 0
    return Z


A = 5
a = 5
n = 3
coef = A / a
F = [[0, 3.22, 3.57, 4.12, 4, 4.85],
     [0, 3.33, 4.87, 5.26, 7.34, 9.49],
     [0, 4.27, 7.64, 10.254, 15.93, 16.12]]
x = [0, 0, 0]
Z = [0, 0, 0, 0, 0, 0]

while n > 0:
    for i in range(n):
        Z = fu(F[i], Z, a)
    x[n - 1] = Z[len(Z) - 1] * coef
    a -= Z[len(Z) - 1]
    Z = [0, 0, 0, 0, 0, 0, 0]
    n -= 1
print('Для максимально возможной прибыли необходимо вложить')
for i in range(len(x)):
    print(x[i], 'единиц средств в', i + 1, 'предприятие')
maximum = 0
for i in range(len(F)):
    maximum += F[i][int(x[i] / coef)]
print('\n максимальная прибль в таком случае составит', maximum)

