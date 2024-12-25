import numpy as n
import matplotlib.pyplot as plot
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint


# Определение системы дифференциальных уравнений
def sys_diff_eq(y, t, m, M, l0, c, g, R):
    dy = n.zeros_like(y)  # Создаем массив нулей для производных переменных
    dy[0] = y[2]  # Первая производная x (скорость x')
    dy[1] = y[3]  # Первая производная угла phi (угловая скорость φ')

    L = l0 + y[0]  # Текущая длина пружины как l0 + x

    # Ускорение x'' с учетом сил: упругости, силы тяжести и центробежной силы
    x_tt = (-c * y[0] - m * g * n.cos(y[1]) + m * L * y[3] ** 2) / (M + m)

    # Угловое ускорение phi'' с учетом гравитации и центробежных сил
    phi_tt = (-g * n.sin(y[1]) - 2 * y[2] * y[3]) / L

    dy[2] = x_tt  # Вторая производная x (ускорение x'')
    dy[3] = phi_tt  # Вторая производная угла phi (ускорение φ'')

    return dy  # Возвращаем массив производных

# Определение временной сетки
step = 500  # Количество временных шагов
t = n.linspace(0, 10, step)  # Создаем временную сетку от 0 до 10 с 500 шагами

# Начальные условия: x=0, φ=π/6, x'=0, φ'=0
y0 = [0, n.pi / 6, 0, 0]

# Параметры системы
m = 0.1 * 10  # Масса груза
M = 1  # Масса блока
R = 0.4  # Радиус блока
l0 = 1  # Ненапряженная длина пружины
c = 50  # Жесткость пружины
g = 9.81  # Ускорение свободного падения

# Решаем систему дифференциальных уравнений
Y = odeint(sys_diff_eq, y0, t, args=(m, M, l0, c, g, R))

# Извлечение значений из решения
x = Y[:, 0]  # x(t) - растяжение пружины
phi = Y[:, 1]  # φ(t) - угол
x_t = Y[:, 2]  # x'(t) - скорость
phi_t = Y[:, 3]  # φ'(t) - угловая скорость

# Дополнительные расчеты
L = l0 + x  # Текущая длина пружины
x_tt = [sys_diff_eq(y, t, m, M, l0, c, g, R)[2] for y, t in zip(Y,t)]
phi_tt = [sys_diff_eq(y, t, m, M, l0, c, g, R)[3] for y, t in zip(Y, t)]


# Расчет сил реакции на груз
N_eps = -m * (L * phi_tt + 2 * x_t * phi_t) * n.cos(phi) - m * (x_tt - L * phi_t ** 2) * n.sin(phi)
N_ita = -m * (L * phi_tt + 2 * x_t * phi_t) * n.sin(phi) + m * (x_tt - L * phi_t ** 2) * n.cos(phi) - c * x - (M + m) * g

# Создание области для графиков
fgr = plot.figure()  # Создаем фигуру
gr = fgr.add_subplot(4, 2, (1, 7))  # Основной график с пружиной и грузом
gr.axis('equal')  # Одинаковый масштаб по осям

# График x(t)
x_plt = fgr.add_subplot(4, 2, 2)
x_plt.plot(t, x)  # Строим x(t)
x_plt.set_title('x(t)')  # Заголовок графика

# График φ(t)
phi_plt = fgr.add_subplot(4, 2, 4)
phi_plt.plot(t, phi)  # Строим φ(t)
phi_plt.set_title('phi(t)')  # Заголовок графика

# График N_eps(t)
n_eps_plt = fgr.add_subplot(4, 2, 6)
n_eps_plt.plot(t, N_eps)  # Строим N_eps(t)
n_eps_plt.set_title('N_eps(t)')  # Заголовок графика

# График N_ita(t)
n_ita_plt = fgr.add_subplot(4, 2, 8)
n_ita_plt.plot(t, N_ita)  # Строим N_ita(t)
n_ita_plt.set_title('N_ita(t)')  # Заголовок графика

# Начальные геометрические параметры для анимации
Yo = 1.4  # Высота оси блока
r = 0.1  # Радиус груза
h_p0 = 0.7  # Начальная высота пружины

Xb = -R  # Координата блока по x
Yb = Yo  # Координата блока по y

# Координаты груза
Xa = Xb + L * n.sin(phi)
Ya = Yb - L * n.cos(phi)

# Построение статических элементов системы
gr.plot([-2 * R, 2 * R], [0, 0], 'black', linewidth=3)  # Пол для блока
gr.plot([-2 * R, 2 * R], [Yo + 0.7, Yo + 0.7], 'black', linewidth=3)  # Верхняя граница блока
gr.plot([-0.1, 0, 0.1], [Yo + 0.7, Yo, Yo + 0.7], 'black')  # Треугольник, изображающий блок

# Анимационные элементы
AB = gr.plot([Xa[0], Xb], [Ya[0], Yb], 'red')[0]  # Прямая между блоком и грузом
String_r = gr.plot([R, R], [Yo, h_p0 + x[0]], 'red')[0]  # Пружина (вертикальная)

# Окружность для груза
Alp = n.linspace(0, 2 * n.pi, 100)
Xc = n.cos(Alp)
Yc = n.sin(Alp)

Block = gr.plot(R * Xc, Yo + R * Yc, 'black')[0]  # Изображение блока
Ticker = gr.plot(Xa[0] + r * Xc, Ya[0] + r * Yc, 'black')[0]  # Изображение груза

# Пружина в виде зигзага
Np = 20  # Количество точек на пружине
Yp = n.linspace(0, 1, 2 * Np + 1)
Xp = 0.05 * n.sin(n.pi / 2 * n.arange(2 * Np + 1))
Spring = gr.plot(R + Xp, (h_p0 + x[0]) * Yp)[0]

# Функция для обновления анимации
def run(i):
    Ticker.set_data([Xa[i] + r * Xc], [Ya[i] + r * Yc])  # Перемещение груза
    AB.set_data([Xa[i], Xb], [Ya[i], Yb])  # Обновление линии пружины
    String_r.set_data([R, R], [Yo, h_p0 + x[i]])  # Обновление вертикальной пружины
    Spring.set_data(R + Xp, (h_p0 + x[i]) * Yp)  # Обновление зигзага пружины
    return [Ticker, AB, String_r, Spring]


ani = FuncAnimation(fgr, run, frames=step, interval=1)

plot.show()
