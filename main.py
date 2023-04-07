"""
С клавиатуры вводятся два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц,
B,C,D,E заполняется случайным образом целыми числами в интервале [-10,10]. Для тестирования использовать не случайное
заполнение, а целенаправленное.
Вид матрицы А:
D   Е
С   В
Каждая из матриц B,C,D,E имеет вид:
     4
  3     1
     2
 Вариант 4:
Формируется матрица F следующим образом: если в Е количество нулевых элементов в нечетных столбцах в области 4 больше, чем количество отрицательных  элементов в четных
строках в области 1, то поменять в В симметрично области 4 и 3 местами, иначе В и Е поменять местами несимметрично. При этом матрица А не меняется. После чего
вычисляется выражение: ((F+A)– (K * F) )*AT . Выводятся по мере формирования А, F и все матричные операции последовательно.
"""

from math import ceil
import random as r


def print_matrix(matrix):  # функция вывода матрицы
    matrix1 = list(map(list, zip(*matrix)))
    for i in range(len(matrix1)):
        c = len(max(list(map(str, matrix1[i])), key=len))
        matrix1[i] = [f'{elem:{c+1}d}' for elem in matrix1[i]]
    matrix1 = list(map(list, zip(*matrix1)))
    for row in matrix1:
        print(*row)


try:
    n = int(input('Введите число N: '))
    k = int(input('Введите число K: '))
    while n < 5:
        n = int(input('Введите число N больше 4: '))

    middle = ceil(n / 2)  # Середина матрицы
    A = [[r.randint(-10, 10) for i in range(n)] for j in range(n)]  # Задаём матрицу A
    AT = [[0 for i in range(n)] for j in range(n)]  # Заготовка под транспонированную матрицу А
    F = A.copy()  # Задаём матрицу F
    KF = [[0 for i in range(n)] for j in range(n)]  # Заготовка под результат умножения матрицы F на коэффициент K
    vichit = [[0 for i in range(n)] for j in range(n)] # Заготовка под результат (F+A)– (K * F)
    summa = [[0 for i in range(n)] for j in range(n)]  # Заготовка под результат сложения матрицы F и А
    result = [[0 for i in range(n)] for j in range(n)]  # Заготовка под результат

    for i in range(n):  # Транспонируем матрицу А
        for j in range(n):
            AT[i][j] = A[j][i]

    print('\nМатрица А:')
    print_matrix(A)
    print('\nТранспонированная А:')
    print_matrix(AT)

    # Выделяем матрицы E B
    if n % 2 == 1:
        E = [A[i][middle - 1:n] for i in range(middle)]
        B = [A[i][middle - 1:n] for i in range(middle - 1, n)]
    else:
        E = [A[i][middle:n] for i in range(0, middle)]
        B = [A[i][middle:n] for i in range(middle, n)]

    for i in range(middle):  # Считаем в Е количество нулевых элементов в нечетных столбцах в области 4
        zero_4 = 0
        for j in range(middle):
            if (i + j + 1) <= middle and (i <= j) and (j + 1) % 2 == 1:
                if E[i][j] == 0:
                    zero_4 += 1

    ch_1 = 0
    for i in range(middle):  # Считаем  количество отрицательных  элементов в четных строках в области 1
        for j in range(middle):
            if (i <= j) and ((i + j + 1) <= middle) and ((i + 1) % 2 == 1):
                if E[i][j] < 0:
                    ch_1 += 1

    if zero_4 > ch_1:
        print(f'\nВ матрице "E" количество нулевых элементов в нечетных столбцах области 4 ({zero_4})')
        print(f'больше, чем количество отрицательных элементов в четных строках области 1 ({ch_1})')
        print('поэтому симметрично меняем местами области 4 и 3 в B.')
        for i in range(middle):
            for j in range(middle):
                if i >= j and (i + j + 1) <= middle:
                    B[i][j], B[j][i] = B[j][i], B[i][j]
                    # Cимметрично меняем местами области 4 и 3 в В

        if n % 2 == 1:
            for i in range(middle, n):
                for j in range(middle, n):
                    F[i][j] = B[i - (middle - 1)][j - (middle - 1)]  # Перезаписываем B
        else:
            for i in range(middle, n):
                for j in range(middle, n):
                    F[i][j] = B[i - middle][j - middle]
    else:
        print(f'\nВ матрице "E"  количество нулевых элементов в нечетных столбцах области 4 ({zero_4})')
        print(f'меньше, чем количество отрицательных элементов в четных строках области 1 ({ch_1})  или равно ей')
        print('поэтому несимметрично меняем местами подматрицы B и E:')
        B, E = E, B
        if n % 2 == 1:
            for i in range(middle, n):  # Перезаписываем B
                for j in range(middle - 1, n):
                    F[i][j] = B[i - (middle)][j - (middle - 1)]
            for i in range(middle):  # Перезаписываем Е
                for j in range(middle - 1, n):
                    F[i][j] = E[i][j - (middle - 1)]
        else:
            for i in range(middle, n):
                for j in range(middle, n):
                    F[i][j] = B[i - middle][j - middle]
            for i in range(0, middle):
                for j in range(middle, n):
                    F[i][j] = E[i][j - middle]

    # K * F
    for i in range(n):
        for j in range(n):
            KF[i][j] = k * F[i][j]
    # F+A
    for i in range(n):
        for j in range(n):
            summa[i][j] = F[i][j] + A[i][j]
    # (F+A)– (K * F)
    for i in range(n):
        for j in range(n):
            vichit[i][j] = summa[i][j] - KF[i][j]

    # ((F+A)– (K * F) )*AT
    for i in range(n):
        for j in range(n):
          result[i][j] = vichit[i][j] * AT[i][j]

    # Вывод всех операций
    print('\nМатрица F:')
    print_matrix(F)
    print('\nРезультат K * F:')
    print_matrix(KF)
    print('\nРезультат F+A:')
    print_matrix(summa)
    print("\nРезультат ((F+A)– (K * F) : ")
    print_matrix(vichit)
    print('\nРезультат ((F+A)– (K * F) )*AT :')
    print_matrix(result)
    print('\nРабота программы завершена.')
except ValueError:  # ошибка на случай введения не числа в качестве порядка или коэффициента
    print('\nВведенный символ не является числом. Перезапустите программу и введите число.')
