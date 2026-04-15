import matplotlib.pyplot as plt
import numpy as np

from find_lines import find_straight, find_diagonal, Line

def find_closer(ini_circles, fin_circles):
    # ini_left, ini_right = ini_circles
    # fin_left, fin_right = fin_circles

    smallest_distance = float('inf')
    smallest_idx = None

    for idx_ini, ini_circle in enumerate(ini_circles):
        for idx_fin, fin_circle in enumerate(fin_circles):

            ini_x, ini_y = ini_circle.center
            fin_x, fin_y = fin_circle.center
            dis = (ini_x - fin_x)**2 + (ini_y - fin_y)**2

            if dis < smallest_distance:
                smallest_distance = dis
                smallest_idx = (idx_ini, idx_fin)

    return ini_circles[smallest_idx[0]], fin_circles[smallest_idx[1]]



fig = plt.gcf()
ax = fig.gca()
ax.set_aspect(1)


initl_conf = (0, 0, np.deg2rad(90))
final_conf = (1, 0, np.deg2rad(0))

L = 1
max_turn_angle = 20

min_turn_r = L / np.tan(max_turn_angle)
# print(f'{min_turn_r=}')

ini_x, ini_y, ini_a = initl_conf

ini_left = plt.Circle((ini_x-min_turn_r*np.sin(ini_a), ini_y+min_turn_r*np.cos(ini_a)), min_turn_r)
ini_right = plt.Circle((ini_x+min_turn_r*np.sin(ini_a), ini_y-min_turn_r*np.cos(ini_a)), min_turn_r)

ax.add_patch(ini_left)
ax.add_patch(ini_right)

plt.plot([ini_x, ini_x+min_turn_r*np.cos(ini_a)], [ini_y, ini_y+min_turn_r*np.sin(ini_a)], color='r')


fin_x, fin_y, fin_a = final_conf

fin_left = plt.Circle((fin_x-min_turn_r*np.sin(fin_a), fin_y+min_turn_r*np.cos(fin_a)), min_turn_r)
fin_right = plt.Circle((fin_x+min_turn_r*np.sin(fin_a), fin_y-min_turn_r*np.cos(fin_a)), min_turn_r)

ax.add_patch(fin_left)
ax.add_patch(fin_right)

plt.plot([fin_x, fin_x+min_turn_r*np.cos(fin_a)], [fin_y, fin_y+min_turn_r*np.sin(fin_a)], color='r')
xs = np.linspace(plt.xlim()[0], plt.xlim()[1], 100)

ini_circles = [ini_left, ini_right]
fin_circles = [fin_left, fin_right]

print(f'{ini_left}, {fin_right}')
(correct_straight_1, dis_s1), (correct_straight_2, dis_s2) = find_straight(ini_circles, fin_circles, initl_conf, final_conf, None)
plt.plot(xs, correct_straight_1(xs))
plt.plot(xs, correct_straight_2(xs))

# ini_closer, fin_closer = find_closer([ini_left, ini_right], [fin_left, fin_right])
# print(fin_closer)

# dx, dy = ini_closer.center[0] - fin_closer.center[0], ini_closer.center[1] - fin_closer.center[1]
# beta = np.arctan(1/(dx/dy))
# straight_tangent = np.tan(beta)*(xs - min_turn_r + min_turn_r*np.sin(beta)) + min_turn_r*np.cos(beta)
# other_straight_tangent = np.tan(beta) * (xs - min_turn_r - min_turn_r*np.sin(beta)) - min_turn_r*np.cos(beta)

# plt.plot(xs, np.tan(beta)*xs - min_turn_r, color='g')
# plt.plot(xs, straight_tangent)
# plt.plot(xs, other_straight_tangent)

# ini_point = (ini_closer.center[0] - min_turn_r*np.sin(beta), ini_closer.center[1] + min_turn_r*np.cos(beta))
# print(ini_point)
# plt.scatter([ini_point[0]], [ini_point[1]], color='red')

(correct_diagonal_1, dis_d1), (correct_diagonal_2, dis_d2) = find_diagonal(ini_circles, fin_circles, initl_conf, final_conf, None)
plt.plot(xs, correct_diagonal_1(xs))
plt.plot(xs, correct_diagonal_2(xs))

print(dis_s1, dis_s2, dis_d1, dis_d2)

circle_1, circle_2 = ini_left, fin_left
radius = circle_1.radius
assert circle_1.radius == circle_2.radius

dx, dy = circle_2.center[0] - circle_1.center[0], circle_2.center[1] - circle_1.center[1]
beta = np.arctan(dy/dx)
print(f'beta: {np.rad2deg(beta)}')

center_vec = np.array((dx, dy))
center_dis = np.sqrt(center_vec @ center_vec)
assert center_dis <= 4*radius + 0.0000001, (center_dis, 4*radius)

alpha = np.arccos(center_dis / (4 * radius))
print(f'alpha: {np.rad2deg(alpha)}')

line = Line(beta, radius, 0)
plt.plot(xs, line(xs), c='r')

half_center_point = (center_dis / 2) * np.array((np.cos(beta), np.sin(beta)))
plt.scatter(*(half_center_point + np.array((circle_1.center[0], circle_1.center[1]))), marker='x', c='purple')

orthogonal = np.array((1 / half_center_point[0], -1 / half_center_point[1]))
orthogonal_line_angle = np.deg2rad(90) + beta
x_offset = center_dis / (2 * np.cos(beta))
orthogonal_line = Line(orthogonal_line_angle, radius - x_offset, 0)
plt.plot(xs, orthogonal_line(xs), c='r')

sum_angle = alpha + beta
new_center = np.array(circle_1.center) + (2*radius) * np.array((np.cos(sum_angle), np.sin(sum_angle)))
plt.scatter(*new_center, marker='x', c='purple')

new_circle_1 = plt.Circle(new_center, min_turn_r, fill = False, ec='b')
ax.add_patch(new_circle_1)


alpha_prime = np.deg2rad(180) - (alpha - beta)
print(f"alpha': {np.rad2deg(alpha_prime)}")
new_center_2 = np.array(circle_1.center) + (2*radius) * -np.array((np.cos(alpha_prime), np.sin(alpha_prime)))
plt.scatter(*new_center_2, marker='x', c='purple')

new_circle_2 = plt.Circle(new_center_2, min_turn_r, fill = False, ec='b')
ax.add_patch(new_circle_2)


plt.show()