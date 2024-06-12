import sys

# package_path
package_paths = [
    r"C:\Users\Administrator\Desktop\nginx\html\download\LM_Projects\0-codes\CV\Annotation_tool",
    r"C:\Users\Administrator\Desktop\nginx\html\download\LM_Projects\0-codes\FS\folder",
]

for s in package_paths:
    sys.path.append(s)

import generate_Annotation
import read_Annotation
import dir_tool

import xml.etree.ElementTree as ET
import cv2
import os
import shutil
import tqdm


def rewrite_elongated_xml(src_path, dst_path, in_path, out_path, spilt_list, H_ratio=0.8, HW_ratio=20, i=0):
    """
    重写xml文件，将长宽比大于10的标注框按照3：3：4的比例进行裁剪
    xml_path:    待处理的xml文件路径
    output_path: 输出的xml文件路径
    """
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    img = cv2.imread(os.path.join(src_path, in_path + '.jpg'), 1)
    shape = img.shape
    ann = generate_Annotation.GEN_Annotations(out_path + ".xml")
    ann.set_size(shape[0], shape[1], shape[2])

    # tree= ET.parse(in_path, out_path)
    # root = tree.getroot()
    BBGT = read_Annotation.get_Annotation2list(os.path.join(src_path, in_path + '.xml'), mode="xml")
    for obj in BBGT:
        xmin, ymin, xmax, ymax, label = obj
        # check if the bounding box is elongated
        # if (ymax - ymin) > ratio * (xmax - xmin):
        # print("========================== ",type(label))
        if label in spilt_list:
            if (ymax - ymin) > H_ratio * shape[0] or (ymax - ymin) > HW_ratio * (xmax - xmin):
                i += 1
                # print("i: ", i)
                # split in 4:3:3
                total_length = ymax - ymin
                part1 = total_length * 4 // 10
                part2 = total_length * 3 // 10
                part3 = total_length - part1 - part2
                # create 3 new bounding boxes
                for part in [(ymin, ymin + part1), (ymin + part1, ymin + part1 + part2), (ymin + part1 + part2, ymax)]:
                    ann.add_pic_attr(label, xmin, part[0], xmax, part[1])
            else:
                ann.add_pic_attr(label, xmin, ymin, xmax, ymax)
        else:
            ann.add_pic_attr(label, xmin, ymin, xmax, ymax)

    ann.savefile(os.path.join(dst_path, out_path + ".xml"))
    shutil.copy(os.path.join(src_path, in_path + '.jpg'), os.path.join(dst_path, out_path + '.jpg'))

    return i


def restore(src_path, dst_path, in_path, out_path):
    """复原xml文件，将裁切后的多个目标框还原为原来的框
    xml_path:    待处理的xml文件路径
    output_path: 输出的复原xml文件路径
    """
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    img = cv2.imread(os.path.join(src_path, in_path + '.jpg'), 1)
    shape = img.shape
    ann = generate_Annotation.GEN_Annotations(out_path + ".xml")
    ann.set_size(shape[0], shape[1], shape[2])

    # tree= ET.parse(in_path, out_path)
    # root = tree.getroot()
    BBGT = read_Annotation.get_Annotation2dict(os.path.join(src_path, in_path + '.xml'), mode="xml")
    xminf, yminf, xmaxf, ymaxf, label = 0, float('inf'), 0, 0, ""
    for obj in BBGT:
        if obj[0] != xminf:
            xminf = obj[0]
        if obj[1] < yminf:
            yminf = obj[1]
        if obj[2] != xmaxf:
            xmaxf = obj[2]
        if obj[3] > ymaxf:
            ymaxf = obj[3]
        if obj[-1] != label:
            label = obj[-1]
    ann.add_pic_attr(label, xminf, yminf, xmaxf, ymaxf)
    ann.savefile(os.path.join(dst_path, out_path + ".xml"))

    shutil.copy(os.path.join(src_path, in_path + '.jpg'), os.path.join(dst_path, out_path + '.jpg'))









if __name__ == "__main__":
    # test_dir_path = r"C:\Users\Administrator\Desktop\nginx\html\download\LM_Projects\0-codes\CV\Annotation_tool\object_dection\example\xml"
    # test_split_path = r"C:\Users\Administrator\Desktop\nginx\html\download\LM_Projects\0-codes\CV\Annotation_tool\object_dection\example\xml_split"
    # test_restored_path = r"C:\Users\Administrator\Desktop\nginx\html\download\LM_Projects\0-codes\CV\Annotation_tool\object_dection\example\xml_restored"
    #
    # mode = "split"  # "split" or "restore"
    # if mode == "split":
    #     file_without_ext = dir_tool.get_filename_without_extension(test_dir_path)
    #     for f in tqdm.tqdm(file_without_ext):
    #         rewrite_elongated_xml(src_path=test_dir_path, dst_path=test_split_path, in_path=f, out_path=f + "_splitto3",
    #                               ratio=10)
    # elif mode == "restore":
    #     # 当作还原的时候split_path为推理之后，图片的输出目录，restored_path为还原之后的图片的输出目录
    #     file_without_ext = dir_tool.get_filename_without_extension(test_split_path)
    #     for f in tqdm.tqdm(file_without_ext):
    #         restore(src_path=test_split_path, dst_path=test_restored_path, in_path=f, out_path=f + "_restore")
    # else:
    #     raise ValueError("mode must be one of ['split', 'restore']")

    dir_path = r"C:\Users\Administrator\Desktop\nginx\html\download\LM_Projects\datapool\20240418-BW-OD-POC\crop3"
    split_path = r"C:\Users\Administrator\Desktop\nginx\html\download\LM_Projects\datapool\20240418-BW-OD-POC\crop3_ratio08"
    restored_path = r"C:\Users\Administrator\Desktop\nginx\html\download\LM_Projects\3-SHBG\1-CV_SCENE\data\crop3_restored"

    mode = "split"  # "split" or "restore"
    spilt_list = ["C111_1", "C111_3", "C111_11", "C111_16", "C111_17", "C111_53", "C111_65", "C311_1", "C311_25",
                  "C311_44", "C311_49"]
    if mode == "split":
        file_without_ext = dir_tool.get_filename_without_extension(dir_path)

        count = 0
        for f in tqdm.tqdm(file_without_ext):
            nums = rewrite_elongated_xml(src_path=dir_path, dst_path=split_path, in_path=f, out_path=f + "_splitto3",
                                         spilt_list=spilt_list, )

            count += nums
        print("total:{}".format(count))

    elif mode == "restore":
        # 当作还原的时候split_path为推理之后，图片的输出目录，restored_path为还原之后的图片的输出目录
        file_without_ext = dir_tool.get_filename_without_extension(split_path)
        for f in tqdm.tqdm(file_without_ext):
            restore(src_path=split_path, dst_path=restored_path, in_path=f, out_path=f + "_restore")
    else:
        raise ValueError("mode must be one of ['split', 'restore']")
