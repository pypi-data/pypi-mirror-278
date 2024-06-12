# -*- coding: utf-8 -*-


def merge_cropped(dbbox, dscores, dlabel):
    # dbbox, dscores, dlabel = [[841, 614, 1059, 806], [841, 806, 1060, 999], [842, 360, 1059, 617]], [1.0, 1.0, 1.0], ['C111_11', 'C111_11', 'C111_11']
    elongated_labels = ["C111_1", "C111_3", "C111_11", "C111_16", "C111_17", "C111_53", "C111_65", "C311_1", "C311_25",
                        "C311_44", "C311_49"]
    cls_box = {}
    # 将框按照类别进行分类
    for i in range(len(dlabel)):
        if dlabel[i] not in cls_box:
            cls_box[dlabel[i]] = []
        cls_box[dlabel[i]].append(dbbox[i])

    for k, v in cls_box.items():
        if k not in elongated_labels or len(v) == 1:  # 如果不是细长条形状的类别或者只有一个框，则不需要合并
            continue
        elif len(v) == 2:  #
            if accept_merge2boxes(v[0], v[1]):
                cls_box[k] = [merge2boxes(v[0], v[1])]
        elif len(v) == 3:
            i = 0
            while i < len(v) - 1:
                l = v[i]
                r = v[i + 1]
                if accept_merge2boxes(l, r):
                    merged = merge2boxes(l, r)
                    v.append(merged)
                    v.remove(l)
                    v.remove(r)
                else:
                    i += 1


def accept_merge2boxes(box1, box2):
    # box1 = [841, 614, 1059, 806]
    # box2 = [841, 806, 1060, 999]
    l_center = (box1[0] + box1[2]) / 2
    r_center = (box2[0] + box2[2]) / 2
    # 如果两个框的中心点的横坐标差值小于10，则认为可以合并
    if abs(l_center - r_center) < 10:
        return True
    # 如果两个框之间的gap小于10，则认为可以合并
    if abs(box1[3] - box2[1]) < 10:
        return True


def merge2boxes(box1, box2):
    flag = accept_merge2boxes(box1, box2)

    if flag:
        return [min(box1[0], box2[0]), min(box1[1], box2[1]), max(box1[2], box2[2]), max(box1[3], box2[3])]
    else:
        return False


if __name__ == '__main__':
    print(random.randint(0, 1))
