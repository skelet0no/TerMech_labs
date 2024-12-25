import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D  # Для создания элементов легенды

# Создаем временную сетку из 1000 точек от 0 до 2π
t = np.linspace(0, 2 * np.pi, 1000)

# Определяем полярные координаты для второй кривой
r2 = 2 + np.cos(6 * t)
phi2 = t + 1.2 * np.cos(6 * t)

# Переводим полярные координаты (r2, φ2) в декартовы (x2, y2)
x2 = r2 * np.cos(phi2)
y2 = r2 * np.sin(phi2)

# Вычисляем производные
x2_t = np.gradient(x2, t)
y2_t = np.gradient(y2, t)
x2_tt = np.gradient(x2_t, t)
y2_tt = np.gradient(y2_t, t)

# Радиус кривизны
curvature_radius = ((x2_t ** 2 + y2_t ** 2) ** 1.5) / np.abs(x2_t * y2_tt - y2_t * x2_tt)

# Создаем окно для построения графика
fig, ax = plt.subplots()
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)

# Линии для графика
line2, = ax.plot([], [], lw=2, label='Кривая')
point, = ax.plot([], [], 'ro', label='Текущая точка')
radius_vec, = ax.plot([], [], 'g-', lw=1, label="Радиус-вектор")

# Добавим элементы для стрелок
tangent_arrow = None
normal_arrow = None

# Легенда для всех векторов и кривой
legend_elements = [
    Line2D([0], [0], lw=2, label='Траектория'),
    Line2D([0], [0], color='red', marker='o', lw=0, label='Текущая точка'),
    Line2D([0], [0], color='green', lw=2, label='Радиус-вектор'),
    Line2D([0], [0], color='blue', lw=2, label='Вектор скорости'),
    Line2D([0], [0], color='purple', lw=2, label='Вектор ускорения'),
]

# Функция инициализации
def init():
    global tangent_arrow, normal_arrow
    line2.set_data([], [])
    point.set_data([], [])
    radius_vec.set_data([], [])
    return line2, point, radius_vec

# Функция для стрелок
def draw_arrow(start_x, start_y, end_x, end_y, color):
    return ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                       arrowprops=dict(facecolor=color, edgecolor=color, arrowstyle='->', lw=1.5))

# Функция обновления
def update(frame):
    global tangent_arrow, normal_arrow

    # Обновляем кривую и точку
    line2.set_data(x2[:frame], y2[:frame])
    point.set_data([x2[frame]], [y2[frame]])
    radius_vec.set_data([0, x2[frame]], [0, y2[frame]])

    # Удаляем старые стрелки
    if tangent_arrow: tangent_arrow.remove()
    if normal_arrow: normal_arrow.remove()

    # Касательный вектор
    tangent_length = 0.5
    tx = x2_t[frame] / np.hypot(x2_t[frame], y2_t[frame])
    ty = y2_t[frame] / np.hypot(x2_t[frame], y2_t[frame])
    tangent_arrow = draw_arrow(x2[frame], y2[frame],
                               x2[frame] + tangent_length * tx,
                               y2[frame] + tangent_length * ty, 'blue')

    # Нормальный вектор
    normal_length = 0.5
    nx = -ty
    ny = tx
    normal_arrow = draw_arrow(x2[frame], y2[frame],
                              x2[frame] + normal_length * nx,
                              y2[frame] + normal_length * ny, 'purple')

    # Заголовок с радиусом кривизны
    ax.set_title(f"Радиус кривизны: {curvature_radius[frame]:.2f}")

    return line2, point, radius_vec, tangent_arrow, normal_arrow

# Создаем анимацию
ani = FuncAnimation(fig, update, frames=len(t), init_func=init, interval=5, blit=False)

# Добавляем полную легенду
plt.legend(handles=legend_elements, loc='upper right')

# Отображаем график
plt.show()
