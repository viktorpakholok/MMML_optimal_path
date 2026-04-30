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

def _circle_distance(circle, in_vec, in_point, out_point):
    radius = circle.radius
    # angle = in_angle

    # in_vec = np.array([np.cos(angle), np.sin(angle)])

    # print(f'{in_vec=}')

    diff_vec = out_point - in_point
    # print(f'{diff_vec=}')
    diff_angle = np.arccos((in_vec @ diff_vec) / np.sqrt(diff_vec @ diff_vec))
    
    # print(f'diff_angle: {np.rad2deg(diff_angle)}')

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
    is_ini_left_to_fin = ini_circle.center[0] <= fin_circle.center[0]

    c = np.deg2rad(180) - line.angle
    assert c >= 0, c
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

    in_angle = line.angle if is_ini_left_to_fin else np.deg2rad(180) + line.angle
    fin_circle_seg_len = _circle_distance(fin_circle, in_angle, out_ini_circle, final_conf[:2])
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


# def _find_circular(circle_1, circle_2, xs = None):
#     radius = circle_1.radius
#     assert circle_1.radius == circle_2.radius

#     is_1_left_to_2 = circle_1.center[0] < circle_2.center[0]

#     dx, dy = circle_2.center[0] - circle_1.center[0], circle_2.center[1] - circle_1.center[1]
#     beta = np.arctan(dy/dx)
#     # print(f'beta: {np.rad2deg(beta)}')

#     center_vec = np.array((dx, dy))
#     center_dis = np.sqrt(center_vec @ center_vec)
#     assert center_dis <= 4*radius + 0.0000001, (center_dis, 4*radius)

#     # print(f'look: {center_dis / (4 * radius)}')

#     alpha = np.arccos(center_dis / (4 * radius))
#     if not is_1_left_to_2:
#         alpha = np.deg2rad(180) - alpha

#     # print(f'alpha: {np.rad2deg(alpha)}')

#     line = Line(beta, radius * (1 if is_1_left_to_2 else -1), 0)
    
#     if xs is not None:
#         plt.plot(xs, line(xs), c='r')

#     # half_center_point = (center_dis / 2) * np.array((np.cos(beta), np.sin(beta)))
#     # print(f'{center_vec=}, {center_vec/2=}')
#     plt.scatter(*(circle_1.center + (center_vec/2)), marker='x', c='purple')
    
#     # if xs is not None:
#     #     plt.scatter(*(half_center_point + np.array((circle_1.center[0], circle_1.center[1]))), marker='x', c='purple')

#     # orthogonal = np.array((1 / half_center_point[0], -1 / half_center_point[1]))
#     # orthogonal_line_angle = np.deg2rad(90) + beta
#     # x_offset = center_dis / (2 * np.cos(beta))
#     # orthogonal_line = Line(orthogonal_line_angle, radius - x_offset, 0)
    
#     # if xs is not None:
#     #     plt.plot(xs, orthogonal_line(xs), c='r')

#     sum_angle = alpha + beta
#     # print(f'sum_angle: {np.rad2deg(sum_angle)}')
#     new_center = np.array(circle_1.center) + (2*radius) * np.array((np.cos(sum_angle), np.sin(sum_angle)))
    
#     if xs is not None:
#         plt.scatter(*new_center, marker='x', c='purple')

#     new_circle_1 = plt.Circle(new_center, radius, fill = False, ec='b')


#     alpha_prime = np.deg2rad(180) - (alpha - beta)
#     # print(f"alpha': {np.rad2deg(alpha_prime)}")
#     new_center_2 = np.array(circle_1.center) + (2*radius) * -np.array((np.cos(alpha_prime), np.sin(alpha_prime)))
    
#     if xs is not None:
#         plt.scatter(*new_center_2, marker='x', c='purple')

#     new_circle_2 = plt.Circle(new_center_2, radius, fill = False, ec='b')

#     return new_circle_1, new_circle_2

def get_out_vector(circle, in_point, in_vec, out_point):

    center_out_vec = out_point - circle.center
    dot_prod_1 = in_vec @ center_out_vec
    angle_1 = np.arccos((dot_prod_1 / np.sqrt(in_vec @ in_vec)) / np.sqrt(center_out_vec @ center_out_vec))
    center_in_vec = in_point - circle.center
    
    dot_prod_2 = center_out_vec @ center_in_vec
    angle_2 = np.arccos((dot_prod_2 / np.sqrt(center_in_vec @ center_in_vec)) / np.sqrt(center_out_vec @ center_out_vec))

    if angle_1 > np.deg2rad(90):
        angle_2 = np.deg2rad(360) - angle_2
    # print(f'angle2: {np.rad2deg(angle_2)}')

    in_vec_normalized = in_vec / np.sqrt(in_vec @ in_vec)
    assert np.isclose(np.square(in_vec_normalized[1]), 1 - np.square(in_vec_normalized[0]))

    determinant_sqrt = np.abs(in_vec_normalized[1] * np.sin(angle_2))
    # print(f'{determinant_sqrt=}')

    out_x1 = in_vec_normalized[0]*np.cos(angle_2) + determinant_sqrt
    out_x2 = in_vec_normalized[0]*np.cos(angle_2) - determinant_sqrt

    try_vec_1_1 = np.array([out_x1, np.sqrt(1 - np.square(out_x1))])
    try_vec_1_2 = np.array([out_x1, -np.sqrt(1 - np.square(out_x1))])
    try_vec_2_1 = np.array([out_x2, np.sqrt(1 - np.square(out_x2))])
    try_vec_2_2 = np.array([out_x2, -np.sqrt(1 - np.square(out_x2))])

    # print(f'cos: {np.cos(angle_2)}')

    # print(try_vec_1_1, try_vec_1_1@in_vec_normalized, try_vec_1_1@center_out_vec)
    # print(try_vec_1_2, try_vec_1_2@in_vec_normalized, try_vec_1_2@center_out_vec)
    # print(try_vec_2_1, try_vec_2_1@in_vec_normalized, try_vec_2_1@center_out_vec)
    # print(try_vec_2_2, try_vec_2_2@in_vec_normalized, try_vec_2_2@center_out_vec)

    # print(f'{in_vec_normalized=}')
    # print(f'{circle.center=}')
    # point = circle.center + circle.radius*try_vec_1_1
    # plt.scatter(*point, marker='x')
    # point = circle.center + circle.radius*try_vec_1_2
    # plt.scatter(*point, marker='x')
    # point = circle.center + circle.radius*try_vec_2_1
    # plt.scatter(*point, marker='x')
    # point = circle.center + circle.radius*try_vec_2_2
    # plt.scatter(*point, marker='x')
    # if np.isclose(np.rad2deg(angle_2), 313.1318141743598):
    #     plt.show()

    res = None
    for vec in [try_vec_1_1, try_vec_1_2, try_vec_2_1, try_vec_2_2]:
        if np.isclose(vec @ in_vec_normalized, np.cos(angle_2)) and np.isclose(vec @ center_out_vec, 0):
            res = vec
            break

    assert np.isclose(res @ center_out_vec, 0)

    length = angle_2 * circle.radius
    return res, length

def _find_circular(circle_ini, circle_fin, initl_conf, final_conf, ax = None):
    radius = circle_ini.radius
    assert circle_ini.radius == circle_fin.radius

    ini_point = np.array(initl_conf[:2])
    ini_angle = initl_conf[2]
    ini_vec = np.array([np.cos(ini_angle), np.sin(ini_angle)])

    fin_point = np.array(final_conf[:2])
    fin_angle = final_conf[2]
    fin_vec = np.array([np.cos(fin_angle), np.sin(fin_angle)])

    dx, dy = circle_fin.center[0] - circle_ini.center[0], circle_fin.center[1] - circle_ini.center[1]
    center_vec = np.array((dx, dy))

    center_point = circle_ini.center + center_vec / 2
    # plt.scatter(*center_point, color='r')

    oc = -center_vec / 2
    orthogonal_to_oc1 = np.array([1/oc[0], -1/oc[1]])
    assert np.isclose(oc@orthogonal_to_oc1, 0)

    d2 = np.sqrt(oc@oc)
    d1 = np.sqrt(4*np.square(radius) - np.square(d2))
    assert np.isclose(d1**2 + d2**2, 4*radius**2)

    orthogonal_to_oc1 = d1 * orthogonal_to_oc1 / (np.sqrt(orthogonal_to_oc1@orthogonal_to_oc1))
    assert np.isclose(orthogonal_to_oc1@orthogonal_to_oc1, d1**2)

    from_mid_center_to_ini = oc - orthogonal_to_oc1
    assert np.isclose(from_mid_center_to_ini @ from_mid_center_to_ini, 4*radius**2)
    # print(f'{from_mid_center_to_ini=}')

    mid_center1 = center_point + orthogonal_to_oc1
    mid_circle1 = plt.Circle(mid_center1, radius, fill=False)
    # plt.scatter(*mid_center1, color='orange')
    ini_out_1 = mid_center1 + from_mid_center_to_ini / 2
    out_vec, ini_len1 = get_out_vector(circle_ini, ini_point, ini_vec, ini_out_1)

    from_fin_to_mid_center = oc + orthogonal_to_oc1
    mid_out_1 = mid_center1 - from_fin_to_mid_center / 2
    # print(mid_circle1, ini_out_1, out_vec, mid_out_1)
    if ax is not None:
        ax.add_patch(mid_circle1)
    # plt.scatter(*ini_out_1, color='r')
    # plt.scatter(*mid_out_1, color='black')
    # plt.show()
    out_vec, mid_len1 = get_out_vector(mid_circle1, ini_out_1, out_vec, mid_out_1)
    # plt.scatter(*mid_out_1, color='r')

    out_vec, fin_len1 = get_out_vector(circle_fin, mid_out_1, out_vec, fin_point)
    # plt.scatter(*mid_out_1, color='r')
    

    # print(f'{out_1=}, {out_vec=}, {len1=}')
    # plt.scatter(*out_1, marker='x', c='r')
    # plt.scatter(*(out_1+out_vec), marker='x', c='orange')

    mid_center2 = center_point - orthogonal_to_oc1
    
    orthogonal_to_oc2 = -orthogonal_to_oc1
    from_mid_center_to_ini = oc - orthogonal_to_oc2
    ini_out_2 = mid_center2 + from_mid_center_to_ini / 2
    # plt.scatter(*ini_out_2, color='r')
    out_vec, ini_len2 = get_out_vector(circle_ini, ini_point, ini_vec, ini_out_2)

    mid_circle2 = plt.Circle(mid_center2, radius, fill=False)
    if ax is not None:
        ax.add_patch(mid_circle2)

    from_fin_to_mid_center = oc + orthogonal_to_oc2
    mid_out_2 = mid_center2 - from_fin_to_mid_center / 2
    # plt.scatter(*mid_out_2, c='orange')
    out_vec, mid_len2 = get_out_vector(mid_circle2, ini_out_2, out_vec, mid_out_2)

    out_vec, fin_len2 = get_out_vector(circle_fin, mid_out_2, out_vec, fin_point)

    dis1 = ini_len1 + mid_len1 + fin_len1
    dis2 = ini_len2 + mid_len2 + fin_len2
    # print(f'dis1: {dis1} vs dis2: {dis2}')

    if dis1 < dis2:
        res = ((ini_out_1, mid_out_1), mid_circle1, dis1)
    else:
        res = ((ini_out_2, mid_out_2), mid_circle2, dis2)

    return res

def find_circular(ini_circles, fin_circles, initl_conf, final_conf, ax = None):

    ini_left, ini_right = ini_circles
    fin_left, fin_right = fin_circles

    points1, circle1, dis1 = _find_circular(ini_left, fin_left, initl_conf, final_conf)
    points2, circle2, dis2 = _find_circular(ini_left, fin_right, initl_conf, final_conf)
    points3, circle3, dis3 = _find_circular(ini_right, fin_left, initl_conf, final_conf)
    points4, circle4, dis4 = _find_circular(ini_right, fin_right, initl_conf, final_conf)

    if ax is not None:
        ax.add_patch(circle1)
        ax.add_patch(circle2)
        ax.add_patch(circle3)
        ax.add_patch(circle4)

    if dis1 < dis4:
        return (points1, circle1, dis1)
    else:
        return (points4, circle4, dis4)

