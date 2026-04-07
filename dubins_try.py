import matplotlib.pyplot as plt
import numpy as np

# initial_config = 
# final_config = 

# plt.plot

speed = 1
steering_angle = 5
L = 1 # distance between front and rear axis of wheels

# angular_velocity = speed / L * np.tan(steering_angle)
angle = 0
point = [0, 0]
points = [point]

def update_pars(x, y, angle, steering_angle, speed):
    diff_x = speed * np.cos(angle)
    diff_y = speed * np.sin(angle)
    diff_angle = speed / L * np.tan(steering_angle)

    return (x + diff_x, y + diff_y), angle + diff_angle

# plt.xlim(-0.3, 0.4)
# plt.ylim(-0.7, 0.1)

ax = plt.gca()
ax.set_aspect('equal', adjustable='box')

steering_angle = 0
for _ in range(100):
    # steering_angle = 2*(steering_angle + 1) % 90 - 180
    point, angle = update_pars(point[0], point[1], angle, steering_angle, speed * 0.01)
    plt.plot([point[0] for point in points], [point[1] for point in points], color = 'green')
    plt.pause(0.001)
    # print(point, angle)
    points.append(point)

steering_angle = 5
for _ in range(100):
    # steering_angle = 2*(steering_angle + 1) % 90 - 180
    point, angle = update_pars(point[0], point[1], angle, steering_angle, speed * 0.01)
    plt.plot([point[0] for point in points], [point[1] for point in points], color = 'green')
    plt.pause(0.001)
    # print(point, angle)
    points.append(point)

# plt.plot([point[0] for point in points], [point[1] for point in points])



plt.show()
