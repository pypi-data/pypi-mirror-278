# *-* coding: utf-8 *-*

import numpy as np


def nearBorder(ymin, ymax, thresh, img_h):
    if ymin < thresh or img_h - ymax < thresh:
        return False

def acceptMerge(rectA, rectB, img_h):
    # A_xmin = rectA['Box']['X']
    # A_ymin = rectA['Box']['Y']
    # A_xmax = rectA['Box']['X'] + rectA['Box']['Width']
    # A_ymax = rectA['Box']['X'] + rectA['Box']['Height']
    # B_xmin = rectB['Box']['X']
    # B_ymin = rectB['Box']['Y']
    # B_xmax = rectB['Box']['X'] + rectB['Box']['Width']
    # B_ymax = rectB['Box']['X'] + rectB['Box']['Height']
    # print(rectA, rectB)
    A_xmin = rectA[0]
    A_ymin = rectA[1]
    A_xmax = rectA[2]
    A_ymax = rectA[3]
    B_xmin = rectB[0]
    B_ymin = rectB[1]
    B_xmax = rectB[2]
    B_ymax = rectB[3]
    # 两个中轴误差不超10
    if abs(A_xmax + A_xmin - B_xmax - B_xmin) > 20:
        return False
    # 合并的框的宽度要接近，两个框都要宽度小于40.
    # if max(A_xmax - A_xmin, B_xmax - B_xmin) > 40:
    #     return False
    # 框gap如果小于50的时候，直接合并
    if max(A_ymin, B_ymin) - min(A_ymax, B_ymax) < 50:
        return True
    # 两个框有一个靠边
    # if not (nearBorder(A_ymin, A_ymax, 20, img_h) or nearBorder(B_ymin, B_ymax, 20, img_h)):
    #     return False
    #
    # # 两个框每个都要长度大于200
    # if min(A_ymax - A_ymin, B_ymax - B_ymin) < 200:
    #     return False
    #
    # # 总长度大于500
    # if A_ymax - A_ymin + B_ymax - B_ymin < 500:
    #     return False
    return True


def merge(bbox_list, score_list, label_list):
    new_list = []
    length = len(bbox_list)

    flag = (1 + length) * length / 2 - length
    flag_map = np.zeros((length, length))
    if len(bbox_list) <= 1:
        return bbox_list
    for i in range(len(bbox_list)):
        for j in range(len(bbox_list)):
            if i <= j:
                continue
            elif acceptMerge(bbox_list[i], bbox_list[j], 1200):
                tmp_bbox = []
                tmp_bbox.append(min(bbox_list[i][0], bbox_list[j][0]))
                tmp_bbox.append(min(bbox_list[i][1], bbox_list[j][1]))
                tmp_bbox.append(max(bbox_list[i][2], bbox_list[j][2]))
                tmp_bbox.append(max(bbox_list[i][3], bbox_list[j][3]))
                if tmp_bbox in new_list:
                    pass
                else:
                    new_list.append(tmp_bbox)
                    flag_map[i][j] = 1
            else:

                flag -= 1
    for i in range(length):
        if np.sum(flag_map[i::]) == 0:
            new_list.append(bbox_list[i])

    if flag > 0:
        return merge(new_list)
    if np.sum(flag_map) == 0:
        return new_list
    else:
        return new_list


if __name__ == '__main__':
    dbbox, dscores, dlabel = [[841, 614, 1059, 806], [841, 806, 1060, 999], [842, 360, 1059, 617]], [1.0, 1.0, 1.0], [
        'C111_11', 'C111_11', 'C111_11']

    elongated_labels = ["C111_1", "C111_3", "C111_11", "C111_16", "C111_17", "C111_53", "C111_65", "C311_1", "C311_25",
                        "C311_44", "C311_49"]
    cls_box = {}
    # 将框按照类别进行分类
    for i, label in enumerate(dlabel):
        if dlabel[i] not in cls_box:
            cls_box[dlabel[i]] = []
        cls_box[dlabel[i]].append(dbbox[i])
    print(cls_box)

    for k, v in cls_box.items():
        if k not in elongated_labels or len(v) == 1:  # 如果不是细长条形状的类别或者只有一个框，则不需要合并
            continue
        else:
            print("processing:{}".format(v))

            rst = merge(v)
            print(rst)

