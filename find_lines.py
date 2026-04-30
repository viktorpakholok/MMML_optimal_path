import numpy as np
import matplotlib.pyplot as plt

class Line():
    def __init__(self, angle, x_offset, y_offset):
        if isinstance(angle, (float, int)):
            self.angle = angle
        elif len(angle) == 2:
            self.angle = np.arctan(angle[1] / angle[0])
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.zero_x = -(y_offset + x_offset * np.tan(angle))/np.tan(angle)

    def __call__(self, x):
        return np.tan(self.angle) * (x + self.x_offset) + self.y_offset


def find_out_point(line: Line):
    point_x = -line.x_offset #+ abs(min_turn_r*np.sin(angle))
    point_y = line.y_offset  #- min_turn_r*(np.cos(angle) if angle > 0 else np.cos(np.pi - angle))

    return point_x, point_y

# def _circle_distance(circle, in_vec, in_point, out_point):
#     radius = circle.radius
#     # angle = in_angle

#     # in_vec = np.array([np.cos(angle), np.sin(angle)])

#     # print(f'{in_vec=}')

#     diff_vec = out_point - in_point
#     # print(f'{diff_vec=}')
#     diff_angle = np.arccos((in_vec @ diff_vec) / np.sqrt(diff_vec @ diff_vec))
    
#     # print(f'diff_angle: {np.rad2deg(diff_angle)}')

#     center_in_vec = np.array((in_point[0] - circle.center[0], in_point[1] - circle.center[1]))
#     center_out_vec = np.array((out_point[0] - circle.center[0], out_point[1] - circle.center[1]))

#     # print(f'{center_in_vec=}')
#     # print(f'{center_out_vec=}')

#     dot_product = center_in_vec @ center_out_vec
#     # print(f'{dot_product=}')

#     dis_center_in_vec = np.sqrt(center_in_vec @ center_in_vec)
#     dis_center_out_vec = np.sqrt(center_out_vec @ center_out_vec)

#     # print(f'{dis_center_in_vec=}')
#     # print(f'{dis_center_out_vec=}')

#     res_angle = np.arccos(dot_product / (dis_center_in_vec * dis_center_out_vec))

#     #3596*/+

#     if diff_angle > np.deg2rad(90):
#         res_angle = np.deg2rad(360) - res_angle

#     # print(f'res_angle: {np.rad2deg(res_angle)}')

#     return res_angle * radius

# def _measure_distance(line: Line, ini_circle, fin_circle, initl_conf, final_conf, diagonal = False):

#     min_turn_r = ini_circle.radius
#     assert ini_circle.radius == fin_circle.radius

#     direction = -1 if ini_circle.center[0] > initl_conf[0] else 1
#     is_ini_left_to_fin = ini_circle.center[0] <= fin_circle.center[0]

#     c = np.deg2rad(180) - line.angle
#     assert c >= 0, c
#     ini_circle_seg_len = c * min_turn_r
#     out_vec = np.array(find_out_point(line))
    
#     out_ini_circle = np.array(out_vec)

#     center_half_vec = np.array((fin_circle.center[0] - ini_circle.center[0], fin_circle.center[1] - ini_circle.center[1])) / 2

#     out_vec[0] += direction * min_turn_r

#     cathet_vec = center_half_vec - out_vec
#     cathet = np.sqrt(cathet_vec @ cathet_vec)

#     out_ini_circle = np.array(find_out_point(line))
#     out_ini_circle += 2*(center_half_vec if not diagonal else cathet_vec)
#     plt.scatter(*out_ini_circle, marker='x', c='r')

#     in_angle = line.angle if is_ini_left_to_fin else np.deg2rad(180) + line.angle
#     fin_circle_seg_len = _circle_distance(fin_circle, in_angle, out_ini_circle, final_conf[:2])
#     distance = ini_circle_seg_len + 2*cathet + fin_circle_seg_len

#     return distance

def _find_straight(circle_1, circle_2, initl_conf, final_conf, xs = None):
    min_turn_r = circle_1.radius
    assert circle_1.radius == circle_2.radius

    ini_point = np.array(initl_conf[:2])
    ini_angle = initl_conf[2]
    ini_vec = np.array((np.cos(ini_angle), np.sin(ini_angle)))
    ini_center = np.array(circle_1.center)

    fin_point = np.array(final_conf[:2])
    fin_angle = final_conf[2]
    fin_vec = np.array((np.cos(fin_angle), np.sin(fin_angle)))
    fin_center = np.array(circle_2.center)

    dx, dy = circle_2.center[0] - circle_1.center[0], circle_2.center[1] - circle_1.center[1]
    center_vec = np.array((dx, dy))
    # center_dis = np.sqrt(center_vec @ center_vec)
    tan_angle = center_vec[1] / center_vec[0]

    orthogonal_to_ac1 = np.array((1/center_vec[0], -1/center_vec[1]))
    assert np.isclose(orthogonal_to_ac1 @ center_vec, 0)

    orthogonal_to_ac1 = min_turn_r * orthogonal_to_ac1 / np.sqrt(orthogonal_to_ac1 @ orthogonal_to_ac1)
    assert np.isclose(orthogonal_to_ac1 @ orthogonal_to_ac1, min_turn_r**2)

    mid_len = np.sqrt(center_vec @ center_vec)

    ini_out_1 = ini_center + orthogonal_to_ac1
    # print(f'{ini_out_1=}')

    b = ini_out_1[1] - tan_angle*ini_out_1[0]
    tangent1 = Line(center_vec, 0, b)

    if xs is not None:
        plt.scatter(*ini_out_1, marker='x', c='red')
        plt.scatter(*(center_vec + orthogonal_to_ac1 + ini_center), marker='x', c='red')

    out_vec_1, ini_len1 = get_out_vector(circle_1, ini_point, ini_vec, ini_out_1)

    fin_in_1 = fin_center + orthogonal_to_ac1

    out_fin_vec_1, fin_len1 = get_out_vector(circle_2, fin_in_1, center_vec, fin_point)
    len1 = ini_len1 + mid_len + fin_len1
    # print(f'{ini_len1=} + {mid_len=} + {fin_len1=}')

    ini_out_2 = ini_center - orthogonal_to_ac1
    out_vec_2, ini_len2 = get_out_vector(circle_1, ini_point, ini_vec, ini_out_2)

    b = ini_out_2[1] - tan_angle*ini_out_2[0]
    tangent2 = Line(center_vec, 0, b)

    fin_in_2 = fin_center - orthogonal_to_ac1
    out_fin_vec_2, fin_len2 = get_out_vector(circle_2, fin_in_2, center_vec, fin_point)
    len2 = ini_len2 + mid_len + fin_len2

    ini_angle_1 = out_vec_1 @ center_vec / (np.sqrt(out_vec_1@out_vec_1) * np.sqrt(center_vec@center_vec))
    ini_angle_2 = out_vec_2 @ center_vec / (np.sqrt(out_vec_2@out_vec_2) * np.sqrt(center_vec@center_vec))

    # print(f'{ini_angle_1=} and {ini_angle_2=}')

    if np.isclose(ini_angle_1, 1):
        assert np.isclose(ini_angle_2, -1)
        tangent = tangent1
        len_ = len1
        out_fin_vec = out_fin_vec_1
    else:
        assert np.isclose(ini_angle_1, -1), ini_angle_1
        assert np.isclose(ini_angle_2, 1)
        tangent = tangent2
        len_ = len2
        out_fin_vec = out_fin_vec_2

    fin_angle_check = out_fin_vec @ fin_vec / (np.sqrt(out_fin_vec@out_fin_vec) * np.sqrt(fin_vec@fin_vec))
    # print(f'{fin_angle_check=}')

    assert any(np.isclose(fin_angle_check, [-1, 1]))
    if np.isclose(fin_angle_check, -1):
        return None
    
    return tangent, len_

def find_straight(ini_circles, fin_circles, initl_conf, final_conf, xs = None):
    ini_left, ini_right = ini_circles
    fin_left, fin_right = fin_circles

    corrects = []

    res = _find_straight(ini_left, fin_right, initl_conf, final_conf)
    if res is not None:
        corrects.append(res)

    res = _find_straight(ini_left, fin_left, initl_conf, final_conf)
    if res is not None:
        corrects.append(res)

    res = _find_straight(ini_right, fin_right, initl_conf, final_conf)
    if res is not None:
        corrects.append(res)

    res = _find_straight(ini_right, fin_left, initl_conf, final_conf)
    if res is not None:
        corrects.append(res)

    if xs is not None:
        for correct in corrects:
            tangent, len_ = correct
            plt.plot(xs, tangent(xs), label=str(round(len_, 2)))

        plt.legend()
    
    best = min(corrects, key=lambda x: x[1])
    return best

def _find_diagonal(circle_1, circle_2, initl_conf, final_conf, xs = None):
    min_turn_r = circle_1.radius
    assert circle_1.radius == circle_2.radius

    ini_point = np.array(initl_conf[:2])
    ini_angle = initl_conf[2]
    ini_vec = np.array((np.cos(ini_angle), np.sin(ini_angle)))
    # ini_center = np.array(circle_1.center)

    fin_point = np.array(final_conf[:2])
    fin_angle = final_conf[2]
    fin_vec = np.array((np.cos(fin_angle), np.sin(fin_angle)))
    # fin_center = np.array(circle_2.center)


    dx, dy = circle_2.center[0] - circle_1.center[0], circle_2.center[1] - circle_1.center[1]
    center_vec = np.array((dx, dy))

    center_dis = np.sqrt(center_vec @ center_vec)
    if center_dis <= 2*min_turn_r: # too close
        return None 

    alpha = np.arccos(min_turn_r / (center_dis / 2))

    an_dis = min_turn_r * np.cos(alpha)
    an_vec =  an_dis * center_vec / np.sqrt(center_vec @ center_vec)
    assert np.isclose(an_vec@an_vec, an_dis**2)

    nb_dis = min_turn_r * np.sin(alpha)
    nb_vec1 = np.array((1/center_vec[0], -1/center_vec[1]))
    nb_vec1 = nb_dis * nb_vec1 / np.sqrt(nb_vec1 @ nb_vec1)
    assert np.isclose(nb_vec1@nb_vec1, nb_dis**2)

    ab_vec1 = an_vec + nb_vec1
    bo_vec1 = center_vec / 2 - ab_vec1

    ini_out_point1 = circle_1.center + ab_vec1
    ini_out_vec1, len_ini1 = get_out_vector(circle_1, ini_point, ini_vec, ini_out_point1)

    fin_in_point1 = ini_out_point1 + 2*bo_vec1
    fin_out_vec1, len_fin1 = get_out_vector(circle_2, fin_in_point1, bo_vec1, fin_point)

    tan_angle = bo_vec1[1] / bo_vec1[0]
    b = ini_out_point1[1] - tan_angle*ini_out_point1[0]

    tangent1 = Line(bo_vec1, 0, b)
    len1 = len_ini1 + 2 * np.sqrt(bo_vec1 @ bo_vec1) + len_fin1

    if xs is not None:
        plt.scatter(*ini_out_point1, marker='x', c='red')
        plt.scatter(*fin_in_point1, marker='x', c='red')
        plt.plot(xs, tangent1(xs))

    nb_vec2 = np.array((-1/center_vec[0], 1/center_vec[1]))
    nb_vec2 = nb_dis * nb_vec2 / np.sqrt(nb_vec2 @ nb_vec2)
    assert np.isclose(nb_vec2@nb_vec2, nb_dis**2)

    ab_vec2 = an_vec + nb_vec2
    bo_vec2 = center_vec / 2 - ab_vec2

    ini_out_point2 = circle_1.center + ab_vec2
    ini_out_vec2, len_ini2 = get_out_vector(circle_1, ini_point, ini_vec, ini_out_point2)

    fin_in_point2 = ini_out_point2 + 2*bo_vec2
    fin_out_vec2, len_fin2 = get_out_vector(circle_2, fin_in_point2, bo_vec2, fin_point)

    tan_angle = bo_vec2[1] / bo_vec2[0]
    b = ini_out_point2[1] - tan_angle*ini_out_point2[0]

    tangent2 = Line(bo_vec2, 0, b)
    len2 = len_ini2 + 2 * np.sqrt(bo_vec2 @ bo_vec2) + len_fin2

    if xs is not None:
        plt.scatter(*ini_out_point2, marker='x', c='orange')
        plt.scatter(*fin_in_point2, marker='x', c='orange')
        plt.plot(xs, tangent2(xs))

    ini_angle1 = (ini_out_vec1 @ bo_vec1) / (np.sqrt(ini_out_vec1 @ ini_out_vec1) * np.sqrt(bo_vec1 @ bo_vec1))
    ini_angle2 = (ini_out_vec2 @ bo_vec2) / (np.sqrt(ini_out_vec2 @ ini_out_vec2) * np.sqrt(bo_vec2 @ bo_vec2))

    # print(f'{ini_angle1=} and {ini_angle2=}')
    if np.isclose(ini_angle1, 1):
        assert np.isclose(ini_angle2, -1)

        tangent = tangent1
        len_ = len1
        out_vec = fin_out_vec1
    else:
        assert np.isclose(ini_angle1, -1)
        assert np.isclose(ini_angle2, 1)

        tangent = tangent2
        len_ = len2
        out_vec = fin_out_vec2

    angle_check = (out_vec @ fin_vec) / (np.sqrt(out_vec@out_vec) * np.sqrt(fin_vec@fin_vec))
    if np.isclose(angle_check, -1):
        return None

    assert np.isclose(angle_check, 1)    
    return tangent, len_

def find_diagonal(ini_circles, fin_circles, initl_conf, final_conf, xs = None):
    ini_left, ini_right = ini_circles
    fin_left, fin_right = fin_circles

    corrects = []

    res = _find_diagonal(ini_left, fin_left, initl_conf, final_conf)
    if res is not None:
        corrects.append(res)

    res = _find_diagonal(ini_left, fin_right, initl_conf, final_conf)
    if res is not None:
        corrects.append(res)

    res = _find_diagonal(ini_right, fin_left, initl_conf, final_conf)
    if res is not None:
        corrects.append(res)

    res = _find_diagonal(ini_right, fin_right, initl_conf, final_conf)
    if res is not None:
        corrects.append(res)

    if xs is not None:
        for tangent, len_ in corrects:
            plt.plot(xs, tangent(xs), label=str(round(len_, 2)))

        plt.legend()

    best = min(corrects, key=lambda x: x[1])
    return best

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

    if out_x1 > 1 and np.isclose(out_x1, 1):
        out_x1 = np.float64(1)
    elif out_x1 > 1:
        assert False  

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

