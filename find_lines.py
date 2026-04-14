import numpy as np
import matplotlib.pyplot as plt

class Line():
    def __init__(self, angle, x_offset, y_offset):
        self.angle = angle
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.zero_x = -(y_offset + x_offset * np.tan(angle))/np.tan(angle)

    def __call__(self, x):
        return np.tan(self.angle) * (x + self.x_offset) + self.y_offset



def find_out_point(line: Line):
    point_x = -line.x_offset #+ abs(min_turn_r*np.sin(angle))
    point_y = line.y_offset  #- min_turn_r*(np.cos(angle) if angle > 0 else np.cos(np.pi - angle))

    return point_x, point_y

def _circle_distance(circle, line, in_point, out_point):
    radius = circle.radius
    angle = line.angle

    in_vec = np.array([np.cos(angle), np.sin(angle)])

    # print(f'{in_vec=}')

    diff_vec = out_point - in_point
    # print(f'{diff_vec=}')
    diff_angle = np.arccos((in_vec @ diff_vec) / np.sqrt(diff_vec @ diff_vec))
    
    # print(f'{np.rad2deg(diff_angle)=}')

    center_in_vec = np.array((in_point[0] - circle.center[0], in_point[1] - circle.center[1]))
    center_out_vec = np.array((out_point[0] - circle.center[0], out_point[1] - circle.center[1]))

    # print(f'{center_in_vec=}')
    # print(f'{center_out_vec=}')

    dot_product = center_in_vec @ center_out_vec
    # print(f'{dot_product=}')

    dis_center_in_vec = np.sqrt(center_in_vec @ center_in_vec)
    dis_center_out_vec = np.sqrt(center_out_vec @ center_out_vec)

    # print(f'{dis_center_in_vec=}')
    # print(f'{dis_center_out_vec=}')

    res_angle = np.arccos(dot_product / (dis_center_in_vec * dis_center_out_vec))

    #3596*/+

    if diff_angle > np.deg2rad(90):
        res_angle = np.deg2rad(360) - res_angle

    # print(f'res_angle: {np.rad2deg(res_angle)}')

    return res_angle * radius


def _measure_distance(line: Line, ini_circle, fin_circle, initl_conf, final_conf, diagonal = False):

    min_turn_r = ini_circle.radius
    assert ini_circle.radius == fin_circle.radius

    direction = -1 if ini_circle.center[0] > initl_conf[0] else 1

    c = np.deg2rad(180) - line.angle
    assert c > 0
    ini_circle_seg_len = c * min_turn_r
    out_vec = np.array(find_out_point(line))
    
    out_ini_circle = np.array(out_vec)

    center_half_vec = np.array((fin_circle.center[0] - ini_circle.center[0], fin_circle.center[1] - ini_circle.center[1])) / 2

    out_vec[0] += direction * min_turn_r

    cathet_vec = center_half_vec - out_vec
    cathet = np.sqrt(cathet_vec @ cathet_vec)

    out_ini_circle = np.array(find_out_point(line))
    out_ini_circle += 2*(center_half_vec if not diagonal else cathet_vec)
    plt.scatter(*out_ini_circle, marker='x', c='r')

    fin_circle_seg_len = _circle_distance(fin_circle, line, out_ini_circle, final_conf[:2])
    distance = ini_circle_seg_len + 2*cathet + fin_circle_seg_len

    return distance


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

def find_straight(ini_circles, fin_circles, initl_conf, final_conf, xs = None):
    ini_left, ini_right = ini_circles
    fin_left, fin_right = fin_circles

    ini_left_to_fin = True if initl_conf[0] < final_conf[0] else False

    straight_tangent, other_straight_tangent = _find_straight(ini_left, fin_right, initl_conf)
    if xs is not None:
        plt.plot(xs, straight_tangent(xs), color='r')
        plt.plot(xs, other_straight_tangent(xs), c='r')
    # print(straight_tangent(0))

    straight_tangent, other_straight_tangent = _find_straight(ini_left, fin_left, initl_conf)
    if xs is not None:
        plt.plot(xs, straight_tangent(xs), color='b')
        plt.plot(xs, other_straight_tangent(xs), c='b')

    if ini_left_to_fin:
        correct_straight_1 = other_straight_tangent
    else:
        correct_straight_1 = straight_tangent

    straight_tangent, other_straight_tangent = _find_straight(ini_right, fin_right, initl_conf)
    if xs is not None:
        plt.plot(xs, straight_tangent(xs), color='g')
        plt.plot(xs, other_straight_tangent(xs), c='g')

    if ini_left_to_fin:
        correct_straight_2 = straight_tangent
    else:
        correct_straight_2 = other_straight_tangent

    straight_tangent, other_straight_tangent = _find_straight(ini_right, fin_left, initl_conf)
    if xs is not None:
        plt.plot(xs, straight_tangent(xs), color='y')
        plt.plot(xs, other_straight_tangent(xs), c='y')

    distance_1 = _measure_distance(correct_straight_1, ini_left, fin_left, initl_conf, final_conf)
    distance_2 = _measure_distance(correct_straight_2, ini_right, fin_right, initl_conf, final_conf)

    return (correct_straight_1, distance_1), (correct_straight_2, distance_2)

def _find_diagonal(circle_1, circle_2, initl_conf, final_conf):
    min_turn_r = circle_1.radius
    assert circle_1.radius == circle_2.radius

    direction = -1 if circle_1.center[0] > initl_conf[0] else 1
    ini_left_from_fin = 1 if initl_conf[0] < final_conf[0] else -1

    dx, dy = circle_2.center[0] - circle_1.center[0], circle_2.center[1] - circle_1.center[1]
    beta = np.arctan(dy/dx)

    center_dis = np.sqrt((circle_1.center[0] - circle_2.center[0])**2 + (circle_1.center[1] - circle_2.center[1])**2)
    alpha = np.arccos(min_turn_r / (center_dis / 2))

    gamma = alpha + ini_left_from_fin*beta - np.deg2rad(90)

    x_offset = min_turn_r * np.sin(gamma)
    y_offset = min_turn_r * np.cos(gamma)

    diagonal_tangent = Line(ini_left_from_fin*gamma, direction*min_turn_r + ini_left_from_fin*x_offset, y_offset)
    # plt.plot(xs, diagonal_tangent, color='y')

    alpha_prime = alpha - ini_left_from_fin*beta
    # print(f'alpha_prime: {np.rad2deg(alpha_prime)}')

    diag_to_interest = np.deg2rad(90) - (alpha_prime)
    phi = diag_to_interest

    x_offset = min_turn_r * np.cos(alpha_prime)
    y_offset = min_turn_r * np.sin(alpha_prime)

    # other_diagonal_tangent = np.tan(phi) * (xs - min_turn_r - y_offset) - x_offset
    other_diagonal_tangent = Line(ini_left_from_fin*phi, direction*min_turn_r - ini_left_from_fin*x_offset, -y_offset)
    # plt.plot(xs, other_diagonal_tangent, color='pink')
    if ini_left_from_fin == -1:     # for mirror effect
        return other_diagonal_tangent, diagonal_tangent
    return diagonal_tangent, other_diagonal_tangent

def find_diagonal(ini_circles, fin_circles, initl_conf, final_conf, xs = None):
    ini_left, ini_right = ini_circles
    fin_left, fin_right = fin_circles

    correct_diagonal_1, correct_diagonal_2 = None, None

    diagonal_tangent, other_diagonal_tangent = _find_diagonal(ini_left, fin_left, initl_conf, final_conf)
    if xs is not None:
        plt.plot(xs, diagonal_tangent(xs), c='r')
        plt.plot(xs, other_diagonal_tangent(xs), c='r')

    diagonal_tangent, other_diagonal_tangent = _find_diagonal(ini_left, fin_right, initl_conf, final_conf)
    if xs is not None:
        plt.plot(xs, diagonal_tangent(xs), c='b')
        plt.plot(xs, other_diagonal_tangent(xs), c='b')

    correct_diagonal_1 = other_diagonal_tangent

    diagonal_tangent, other_diagonal_tangent = _find_diagonal(ini_right, fin_left, initl_conf, final_conf)
    if xs is not None:
        plt.plot(xs, diagonal_tangent(xs), c='pink')
        plt.plot(xs, other_diagonal_tangent(xs), c='pink')
    
    correct_diagonal_2 = diagonal_tangent

    diagonal_tangent, other_diagonal_tangent = _find_diagonal(ini_right, fin_right, initl_conf, final_conf)
    if xs is not None:
        plt.plot(xs, diagonal_tangent(xs), c='y')
        plt.plot(xs, other_diagonal_tangent(xs), c='y')

    distance_1 = _measure_distance(correct_diagonal_1, ini_left, fin_right, initl_conf, final_conf, True)
    distance_2 = _measure_distance(correct_diagonal_2, ini_right, fin_left, initl_conf, final_conf, True)

    return (correct_diagonal_1, distance_1), (correct_diagonal_2, distance_2)

