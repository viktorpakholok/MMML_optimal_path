import numpy as np
import matplotlib.pyplot as plt

from find_lines import Line, get_tangent, get_out_vector, seek_correct_from2

def find_best_rdp(ini_circles, fin_point, initl_conf, xs, ax):

    best_straight, best_straight_dis = find_straight(ini_circles, fin_point, initl_conf, None)
    
    variants = [(best_straight, best_straight_dis)]
    res = find_circular(ini_circles, fin_point, initl_conf, None, None)
    if res is not None:
        variants.append(res)

    if xs is not None and ax is not None:
        plt.plot(xs, best_straight(xs), label=str(round(best_straight_dis, 3)), c='pink')

        if res is not None:
            best_circular, best_circular_dis = res
            best_circular.set_label(str(round(best_circular_dis, 3)))
            ax.add_patch(best_circular)

        plt.legend()

    best = min(variants, key=lambda x: x[1])
    return best

def _find_straight(ini_circle, fin_point, initl_conf, xs = None):
    min_turn_r = ini_circle.radius

    ini_point = np.array(initl_conf[:2])
    ini_angle = initl_conf[2]
    ini_vec = np.array((np.cos(ini_angle), np.sin(ini_angle)))

    center_vec = fin_point - ini_circle.center
    center_dis = np.sqrt(center_vec @ center_vec)

    alpha = np.arccos(min_turn_r / center_dis)

    an_dis = min_turn_r * np.cos(alpha)
    an_vec = an_dis * center_vec / np.sqrt(center_vec @ center_vec)

    nb_dis = min_turn_r * np.sin(alpha)
    nb_vec1 = np.array((1/center_vec[0], -1/center_vec[1]))

    assert np.isclose(nb_vec1 @ an_vec, 0)
    nb_vec1 = nb_dis * nb_vec1 / np.sqrt(nb_vec1 @ nb_vec1)

    ab_vec1 = an_vec + nb_vec1
    assert np.isclose(ab_vec1 @ ab_vec1, min_turn_r**2)

    bc_vec1 = center_vec - ab_vec1
    ini_out_point1 = ini_circle.center + ab_vec1

    tangent1 = get_tangent(bc_vec1, ini_out_point1)
    ini_out_vec1, ini_len1 = get_out_vector(ini_circle, ini_point, ini_vec, ini_out_point1)

    if xs is not None:
        plt.scatter(*ini_out_point1, marker='x')
        plt.plot(xs, tangent1(xs))

    nb_vec2 = np.array((-1/center_vec[0], 1/center_vec[1]))
    nb_vec2 = nb_dis * nb_vec2 / np.sqrt(nb_vec2 @ nb_vec2)

    ab_vec2 = an_vec + nb_vec2
    bc_vec2 = center_vec - ab_vec2

    ini_out_point2 = ini_circle.center + ab_vec2
    tangent2 = get_tangent(bc_vec2, ini_out_point2)
    ini_out_vec2, ini_len2 = get_out_vector(ini_circle, ini_point, ini_vec, ini_out_point2)

    if xs is not None:
        plt.scatter(*ini_out_point2, marker='x', c='r')
        plt.plot(xs, tangent2(xs), c='r')

    mid_len1 = np.sqrt(bc_vec1 @ bc_vec1)
    mid_len2 = np.sqrt(bc_vec2 @ bc_vec2)

    variants = [(tangent1, ini_len1+mid_len1), (tangent2, ini_len2+mid_len2)]
    correct_idx = seek_correct_from2([ini_out_vec1, ini_out_vec2], [bc_vec1, bc_vec2])

    # print(f'{correct_idx=}')
    return variants[correct_idx]


def find_straight(ini_circles, fin_point, initl_conf, xs = None):

    correct = []
    for ini_circle in ini_circles:
        res = _find_straight(ini_circle, fin_point, initl_conf, None)
        correct.append(res)

    if xs is not None:
        for tangent, dis in correct:
            plt.plot(xs, tangent(xs), label=str(round(dis, 2)))

        plt.legend()

    best = min(correct, key=lambda x: x[1])
    return best


def _find_circular(ini_circle, fin_point, initl_conf, xs = None, ax = None):
    min_turn_r = ini_circle.radius

    # print(f'{min_turn_r=}')
    center_vec = fin_point - ini_circle.center
    # print(f'{center_vec=}')
    center_dis = np.sqrt(center_vec @ center_vec)
    # print(f'{center_dis=}')

    if center_dis > 3 * min_turn_r:
        return None
    
    ini_point = np.array(initl_conf[:2])
    ini_angle = initl_conf[2]
    ini_vec = np.array((np.cos(ini_angle), np.sin(ini_angle)))

    alpha = np.arccos((np.square(center_dis) + 3*np.square(min_turn_r)) / (4*center_dis*min_turn_r))
    checks = []

    x_b = (2*min_turn_r/center_dis)

    x1 = x_b * (center_vec[0]*np.cos(alpha) + np.abs(center_vec[1]*np.sin(alpha)))

    y11 = np.sqrt(4*np.square(min_turn_r) - np.square(x1))
    ao11 = np.array((x1, y11))
    assert np.isclose(ao11@ao11, 4*min_turn_r**2)
    # assert np.isclose(ao11@center_vec, 2*min_turn_r*center_dis*np.cos(alpha))
    # print(f'check1: {ao11@center_vec} vs {2*min_turn_r*center_dis*np.cos(alpha)}')
    
    co11 = ao11 - center_vec
    # assert np.isclose(co11@co11, min_turn_r**2), (co11@co11, min_turn_r**2)

    circle11_center = ini_circle.center + ao11
    circle11 = plt.Circle(circle11_center, min_turn_r, fill = False, ec='grey')
    outpoint11 = ini_circle.center + ao11/2
    checks.append((circle11, ao11, outpoint11))


    y12 = -np.sqrt(4*np.square(min_turn_r) - np.square(x1))
    ao12 = np.array((x1, y12))
    assert np.isclose(ao12@ao12, 4*min_turn_r**2)
    # print(f'check2: {ao12@center_vec} vs {2*min_turn_r*center_dis*np.cos(alpha)}')

    circle12_center = ini_circle.center + ao12
    circle12 = plt.Circle(circle12_center, min_turn_r, fill = False, ec='purple')
    outpoint12 = ini_circle.center + ao12/2
    checks.append((circle12, ao12, outpoint12))


    x2 = x_b * (center_vec[0]*np.cos(alpha) - np.abs(center_vec[1]*np.sin(alpha)))

    y21 = np.sqrt(4*np.square(min_turn_r) - np.square(x2))
    ao21 = np.array((x2, y21))
    assert np.isclose(ao21@ao21, 4*min_turn_r**2)
    # print(f'check3: {ao21@center_vec} vs {2*min_turn_r*center_dis*np.cos(alpha)}')

    circle21_center = ini_circle.center + ao21
    circle21 = plt.Circle(circle21_center, min_turn_r, fill = False, ec='orange')
    outpoint21 = ini_circle.center + ao21/2
    checks.append((circle21, ao21, outpoint21))


    y22 = -np.sqrt(4*np.square(min_turn_r) - np.square(x2))
    ao22 = np.array((x2, y22))
    assert np.isclose(ao22@ao22, 4*min_turn_r**2)
    # print(f'check4: {ao22@center_vec} vs {2*min_turn_r*center_dis*np.cos(alpha)}')

    circle22_center = ini_circle.center + ao22
    circle22 = plt.Circle(circle22_center, min_turn_r, fill = False, ec='yellow')
    outpoint22 = ini_circle.center + ao22/2
    checks.append((circle22, ao22, outpoint22))

    
    if xs is not None:
        plt.scatter(*ini_circle.center, marker='x', c='r')
        plt.scatter(*circle11.center, marker='x', c='purple')
        plt.scatter(*circle12.center, marker='x')
        plt.scatter(*circle21.center, marker='x')
        plt.scatter(*circle22.center, marker='x')

        plt.scatter(*(ini_circle.center + center_vec), marker='x', c='orange')

        plt.scatter(*(circle11.center - co11), color = 'pink')

        plt.scatter(*outpoint11, marker='x')
        plt.scatter(*outpoint12, marker='x')
        plt.scatter(*outpoint21, marker='x')
        plt.scatter(*outpoint22, marker='x')

        # if ax is not None:
        #     ax.add_patch(circle11)
        #     ax.add_patch(circle12)
        #     ax.add_patch(circle21)
        #     ax.add_patch(circle22)

    correct = []
    for circle, ao, _ in checks:
        # print(ao @ center_vec, 4*min_turn_r*center_dis*np.cos(alpha))
        if np.isclose(ao @ center_vec, 2*min_turn_r*center_dis*np.cos(alpha)) and not any([(ao_ == ao).all() for circle_, ao_, __ in correct]):
            correct.append((circle, ao, _))

    # print(f'{correct=}')
    assert len(correct) == 2

    variants = []
    for circle, ao, outpoint in correct:
        ini_out_vec, ini_len = get_out_vector(ini_circle, ini_point, ini_vec, outpoint)
        fin_out_vec, fin_len = get_out_vector(circle, outpoint, ini_out_vec, fin_point)
        len_ = ini_len + fin_len

        if ax is not None:
            circle.set_label(str(round(len_, 2)))
            ax.add_patch(circle)

        variants.append((circle, len_))

    if xs is not None:
        plt.legend()

    best = min(variants, key=lambda x: x[1])
    return best    
    

def find_circular(ini_circles, fin_point, initl_conf, xs = None, ax = None):
    corrects = []
    for ini_circle in ini_circles:
        res = _find_circular(ini_circle, fin_point, initl_conf, None, None)

        if res is not None:
            corrects.append(res)

    if ax is not None:
        for circle, dis in corrects:
            circle.set_label(str(round(dis, 2)))
            ax.add_patch(circle)

        plt.legend()

    best = min(corrects, key= lambda x: x[1])
    return best