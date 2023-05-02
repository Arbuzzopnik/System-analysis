import matplotlib.pyplot as plt
import numpy as np
import openpyxl


def plotting(x, y, h,results, title):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel('Days')
    ax.set_ylabel('Ruble/Gram')
    ax.grid()
    ax.plot(x, y)
    ax.plot(x, results[0])
    ax.plot(x, results[1])
    ax.plot(x, results[2])
    ax.legend(('y(x)',
               f'h1 = {h[0]}',
               f'h2 = {h[1]}',
               f'h3 = {h[2]}'))
    plt.show()


def read_data(title):
    wb = openpyxl.load_workbook(f'{title}.xlsx')
    current_sheet = wb.sheetnames[0]
    rows_numbers = int(wb.worksheets[0].dimensions[4:]) + 1
    x_data = [wb[current_sheet][f'A{i}'].value for i in range(2, rows_numbers)]
    y_data = [wb[current_sheet][f'B{i}'].value for i in range(2, rows_numbers)]
    x_form = [0, ]
    for i in range(1, len(x_data)):
        x_form.append(x_form[-1] + abs((x_data[::-1][i] - x_data[::-1][i - 1]).days))
    y_form = y_data[::-1]
    return x_form, y_form


def get_noise(x, koeff):
    x_n = list(map(lambda value: value + (koeff * np.random.normal()), x))
    return x_n


def get_kernel_regression_estimation(y, h):
    sse = 10000
    approximated_y = []
    while sse > 1000:
        for i in range(len(y)):
            w = [(1 / np.sqrt(2 * np.pi)) * np.exp((-1 / 2) * (((i + 1) - j) / h) ** 2) for j in range(1, len(y))]
            approximated_y.append(sum(list(map(lambda w_value, y_value: w_value * y_value, w, y))) / sum(w))
        sse = sum([(y[i] - approximated_y[i]) ** 2 for i in range(len(y))])
        y = approximated_y[:]
        approximated_y = []
    return y


def main():
    title = 'argentum'
    x, y = read_data(title)  # Чтение файла
    approximation_results = []
    y = np.array(y)
    noise = get_noise(y, 0.9)  # Добавление шума
    h = [2, 4, 8]  # Список значений ширины окна
    # Получение результатов
    for i in h:
        approximation_results.append(get_kernel_regression_estimation(noise, i))
    # Вывод результатов
    plotting(x, y, h, approximation_results, 'Реализация гауссовского процесса')
    plotting(x, noise, h, approximation_results, 'Реализация гауссовского процесса')

if __name__ == '__main__':
    main()
