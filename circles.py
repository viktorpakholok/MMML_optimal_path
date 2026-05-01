import matplotlib.pyplot as plt
import numpy as np

from find_lines import find_straight, find_diagonal, find_circular, find_best_dubins
# from our_rdp import find_straight, find_circular

# def find_closer(ini_circles, fin_circles):
#     # ini_left, ini_right = ini_circles
#     # fin_left, fin_right = fin_circles

#     smallest_distance = float('inf')
#     smallest_idx = None

#     for idx_ini, ini_circle in enumerate(ini_circles):
#         for idx_fin, fin_circle in enumerate(fin_circles):

#             ini_x, ini_y = ini_circle.center
#             fin_x, fin_y = fin_circle.center
#             dis = (ini_x - fin_x)**2 + (ini_y - fin_y)**2

#             if dis < smallest_distance:
#                 smallest_distance = dis
#                 smallest_idx = (idx_ini, idx_fin)

#     return ini_circles[smallest_idx[0]], fin_circles[smallest_idx[1]]


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

correct_diagonal, dis_diagonal = find_diagonal(ini_circles, fin_circles, initl_conf, final_conf, None)
plt.plot(xs, correct_diagonal(xs))

points, circle, dis = find_circular(ini_circles, fin_circles, initl_conf, final_conf, None)
ax.add_patch(circle)

best_trajectory, best_distance = find_best_dubins(ini_circles, fin_circles, initl_conf, final_conf, xs, ax)
print(f'{best_distance=}')

plt.show()