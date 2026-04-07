import numpy as np
import matplotlib.pyplot as plt

class Line():
    def __init__(self, angle, x_offset, y_offset):
        self.angle = angle
        self.x_offset = x_offset
        self.y_offset = y_offset

    def __call__(self, x):
        return np.tan(self.angle) * (x + self.x_offset) + self.y_offset

def _find_straight(circle_1, circle_2, initl_conf):
    min_turn_r = circle_1.radius
    assert circle_1.radius == circle_2.radius

    # print(circle_1.center[0])
    direction = -1 if circle_1.center[0] > initl_conf[0] else 1

    dx, dy = circle_2.center[0] - circle_1.center[0], circle_2.center[1] - circle_1.center[1]
    # print(f'{dx=}, {dy=}')
    # print(dx/dy)
    beta = np.arctan(dy/dx)
    # print(f'beta: {np.rad2deg(beta)}')

    # straight_tangent = np.tan(beta) * (xs + direction*min_turn_r + min_turn_r*np.sin(beta)) + min_turn_r*np.cos(beta)
    # other_straight_tangent = np.tan(beta) * (xs + direction*min_turn_r - min_turn_r*np.sin(beta)) - min_turn_r*np.cos(beta)
    straight_tangent = Line(beta, direction*min_turn_r + min_turn_r*np.sin(beta), min_turn_r*np.cos(beta))
    other_straight_tangent = Line(beta, direction*min_turn_r - min_turn_r*np.sin(beta), -min_turn_r*np.cos(beta))
    
    return straight_tangent, other_straight_tangent

def find_straight(ini_circles, fin_circles, initl_conf, xs = None):
    ini_left, ini_right = ini_circles
    fin_left, fin_right = fin_circles

    straight_tangent, other_straight_tangent = _find_straight(ini_left, fin_right, initl_conf)
    if xs is not None:
        plt.plot(xs, straight_tangent(xs), color='r')
        plt.plot(xs, other_straight_tangent(xs), c='r')
    # print(straight_tangent(0))

    straight_tangent, other_straight_tangent = _find_straight(ini_left, fin_left, initl_conf)
    if xs is not None:
        plt.plot(xs, straight_tangent(xs), color='b')
        plt.plot(xs, other_straight_tangent(xs), c='b')
    correct_straight_1 = other_straight_tangent

    straight_tangent, other_straight_tangent = _find_straight(ini_right, fin_right, initl_conf)
    if xs is not None:
        plt.plot(xs, straight_tangent(xs), color='g')
        plt.plot(xs, other_straight_tangent(xs), c='g')
    correct_straight_2 = straight_tangent

    straight_tangent, other_straight_tangent = _find_straight(ini_right, fin_left, initl_conf)
    if xs is not None:
        plt.plot(xs, straight_tangent(xs), color='y')
        plt.plot(xs, other_straight_tangent(xs), c='y')

    return correct_straight_1, correct_straight_2