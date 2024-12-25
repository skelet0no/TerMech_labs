import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

STEP = 500  # Количество шагов для анимации (количество кадров)
Xo, Yo, R = 3, 4, 0.5  # Координаты точки блока (Xo, Yo) и его радиус R
y0, r = 2.3, 0.1  # Амплитуда смещения y0 и радиус маленького круга r
Np = 20  # Количество точек для моделирования пружины

t = np.linspace(0, 2 * math.pi, STEP)  # Временной массив от 0 до 2π (для анимации колебаний)
Alp = np.linspace(0, 2 * np.pi, 100)  # Углы для построения окружности
Xc, Yc = np.cos(Alp), np.sin(Alp)  # Координаты для построения единичной окружности
phi = np.pi / 18 * np.sin(2 * t)  # Угловое отклонение маятника
y = np.sin(t)  # Вертикальное синусоидальное движение
y_l = y + y0  # Смещённое синусоидальное движение вверх (левая граница)
y_r = y - y0  # Смещённое синусоидальное движение вниз (правая граница)
Yp = np.linspace(0, 1, 2 * Np + 1)  # Вертикальные координаты для пружины
Xp = 0.15 * np.sin(np.pi / 2 * np.arange(2 * Np + 1))  # Горизонтальные координаты для пружины

def init_plot():
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(0, 6)
    ax.set_ylim(-1, 6)
    ax.plot([1, 5], [0, 0], 'black', linewidth=3)  # Горизонтальная опора
    ax.plot([2, 4], [Yo + 0.7, Yo + 0.7], 'black', linewidth=3)  # Верхняя платформа
    ax.plot([Xo - 0.1, Xo, Xo + 0.1], [Yo + 0.7, Yo, Yo + 0.7], 'black')  # Треугольник над блоком
    return fig, ax


fig, ax = init_plot()

# Координаты точек
Xb, Yb = Xo - R, Yo
Xa = Xb + y_l * np.sin(phi)
Ya = Yb - y_l * np.cos(phi)

# Элементы графика
AB_line, = ax.plot([], [], 'blue')
L_line, = ax.plot([], [], 'blue')
m_circle, = ax.plot([], [], 'black')
Pruzh, = ax.plot([], [], 'red')
Block, = ax.plot(Xo + R * Xc, Yo + R * Yc, 'black')

# Текстовые аннотации для длин и суммы
text_AB = ax.text(0.5, 5.5, '', fontsize=10, color='blue')
text_L = ax.text(0.5, 5.3, '', fontsize=10, color='red')
text_sum = ax.text(0.5, 5.1, '', fontsize=10, color='green')


def run(i):
    # Обновляем маленький круг на конце маятника
    m_circle.set_data(Xa[i] + r * Xc, Ya[i] + r * Yc)

    # Обновляем маятник AB
    AB_line.set_data([Xa[i], Xb], [Ya[i], Yb])
    length_AB = np.hypot(Xa[i] - Xb, Ya[i] - Yb)  # Длина AB

    # Обновляем пружину
    L_line.set_data([Xo + R, Xo + R], [Yo, Yo + y_r[i]])
    length_L = np.abs(y_r[i])  # Длина пружины

    # Обновляем пружину визуально
    Pruzh.set_data(Xo + R + Xp, (Yo + y_r[i]) * Yp)

    # Сумма длин
    total_length = length_AB + length_L

    # Обновляем текстовые аннотации
    text_AB.set_text(f"Длина AB: {length_AB:.2f}")
    text_L.set_text(f"Длина L: {length_L:.2f}")
    text_sum.set_text(f"Сумма: {total_length:.2f}")

    return m_circle, AB_line, L_line, Pruzh, text_AB, text_L, text_sum


ani = FuncAnimation(fig, run, frames=STEP, interval=9, blit=True)

plt.show()
