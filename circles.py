import matplotlib.pyplot as plt
import numpy as np

from find_lines import find_straight, find_diagonal, find_circular, Line, _find_circular, _circle_distance

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

# def _measure_distance_circular(circle_ini, circle_mid, circle_fin, final_conf):
#     radius = circle_ini.radius
#     assert circle_ini.radius == circle_mid.radius == circle_fin.radius

#     is_ini_left_to_fin = circle_ini.center[0] < circle_fin.center[0]

#     dx, dy = circle_fin.center[0] - circle_ini.center[0], circle_fin.center[1] - circle_ini.center[1]
#     beta = np.arctan(dy/dx)
#     print(f'beta: {np.rad2deg(beta)}')

#     center_vec = np.array((dx, dy))
#     center_dis = np.sqrt(center_vec @ center_vec)
#     assert center_dis <= 4*radius + 0.0000001, (center_dis, 4*radius)

#     # print(f'look: {center_dis / (4 * radius)}')

#     alpha = np.arccos(center_dis / (4 * radius))
#     print(f'alpha: {np.rad2deg(alpha)}')

#     # if not is_ini_left_to_fin:
#     #     alpha = np.deg2rad(180) - alpha

#     sum_angle = alpha + beta
#     print(f"sum_angle: {np.rad2deg(sum_angle)}")
#     ini_circle_seg_len = sum_angle * radius
#     print(f'{ini_circle_seg_len=}')

#     print(f'alpha: {np.rad2deg(alpha)}')
#     mid_circle_seg_len = (np.deg2rad(180) + 2*alpha) * radius
#     print(f'{mid_circle_seg_len=}')

#     in_angle = np.deg2rad(90) - alpha + beta
#     # print(f'in_angle: {np.rad2deg(in_angle)}')

#     alpha_2 = alpha - beta
#     print(f'alpha_2: {np.rad2deg(alpha_2)}')
#     in_point_direction = np.array((np.cos(alpha_2) * (-1 if circle_mid.center[0] < circle_fin.center[0] else 1), np.sin(alpha_2)))
#     in_point = np.array(circle_fin.center) + radius * in_point_direction
#     plt.scatter(*in_point, marker='x', c='orange')

#     # line = Line(in_angle, -in_point[0], in_point[1])
#     # plt.plot(xs, line(xs), c='orange')

#     # if is_ini_left_to_fin:
#     #     in_angle = np.deg2rad(180) + in_angle
#     # print(f'in_angle: {np.rad2deg(in_angle)}')
#     in_vec = np.array([np.cos(in_angle), np.sin(in_angle)])

#     fin_circle_seg_len = _circle_distance(circle_fin, in_vec, in_point, final_conf[:2])
#     print(f'{fin_circle_seg_len=}')

#     res = ini_circle_seg_len + mid_circle_seg_len + fin_circle_seg_len
#     return res


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
correct_straight, dis = find_straight(ini_circles, fin_circles, initl_conf, final_conf, None)
plt.plot(xs, correct_straight(xs))
print(f'{dis=}')

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
correct_diagonal, dis_diagonal = find_diagonal(ini_circles, fin_circles, initl_conf, final_conf, None)
plt.plot(xs, correct_diagonal(xs))

# _find_circular(ini_left, fin_left, initl_conf, final_conf, ax)

points, circle, dis = find_circular(ini_circles, fin_circles, initl_conf, final_conf, None)
ax.add_patch(circle)

plt.show()