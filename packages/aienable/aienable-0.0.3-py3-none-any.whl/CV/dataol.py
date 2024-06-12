# -*- coding: utf-8 -*-
# Author: Lin WeiCheng  84318968
# Description:
# Created: 2024-06-03
# Last Modified: 2024-06-03
# version: 1.0


import os, shutil, cv2
import numpy as np
import json
import xml.etree.ElementTree as ET
from lxml import etree


class JPG_XML(object):
    """Aclass is to represent the jpg and xml files

    Attributes
    ----------
        loc_dir: str
            suggested to be the absolute path
        basename: str
            the basename of the jpg and xml files without the extension
    Methods
    -------
        get_jpg_path():
            return the absolute path of the jpg file
        get_xml_path():
            return the absolute path of the xml file
        get_jpg_xml_path():
            return the absolute path of the jpg and xml files
        get_basename():
            return the basename of the jpg and xml files
        get_loc_dir():
            return the absolute path of the directory
        get_annotation():
            return the bounding box and label of the jpg file
        read_xml():
            return the xml tree of the xml file
        save_tree_2_xml():
            save the xml tree to a new xml file
        modify_from_file():
            modify the label of the xml file
    """

    def __init__(self, loc_dir, basename):
        """all these attributes describe the jpg and xml files
        Args
        ----
            loc_dir: suggested to be the absolute path
            basename: the basename of the jpg and xml files without the extension
        """
        self.loc_dir = loc_dir
        self.basename = basename
        self.jpg_path, self.xml_path = self.get_jpg_xml_path()

        # self.JPG = cv2.imread(self.jpg_path)
        # self.XML = self.read_xml()

    def get_jpg_path(self):
        return os.path.join(self.loc_dir, self.basename + '.jpg')

    def get_xml_path(self):
        return os.path.join(self.loc_dir, self.basename + '.xml')

    def get_jpg_xml_path(self):
        return self.get_jpg_path(), self.get_xml_path()

    def get_basename(self):
        return self.basename

    def get_loc_dir(self):
        return self.loc_dir

    def get_annotation(self):
        tree = ET.parse(self.get_xml_path())
        BBGT = []
        for obj in tree.findall('object'):
            label = obj.find('name').text
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            BBGT.append([xmin, ymin, xmax, ymax, label])
        return BBGT

    def read_xml(self):
        tree = ET.parse(self.get_xml_path())

        return tree

    def save_tree_2_xml(self, tree, new_file):
        tree.write(new_file)

    def modify_from_file(self, old_name, new_name):
        """modify the label of the xml file
        :param old_name: old label name
        :param new_name: new label name
        :return: new tree for save
        """
        tree = ET.parse(self.get_xml_path())
        root = tree.getroot()
        for name in root.iter('name'):
            if name.text == old_name:  # can be changed to other conditions
                name.text = new_name
        return tree

    def get_width_height(self):
        tree = ET.parse(self.get_xml_path())
        root = tree.getroot()
        for size in root.iter('size'):
            width = int(size.find('width').text)
            height = int(size.find('height').text)
        return width, height


class JPG_JSON(object):
    def __init__(self, loc_dir, basename):
        """all these attributes describe the jpg and json files
        :param loc_dir: suggested to be the absolute path
        :param basename: the basename of the jpg and json files without the extension
        """
        self.loc_dir = loc_dir
        self.basename = basename

    def get_jpg_path(self):
        return os.path.join(self.loc_dir, self.basename + '.jpg')

    def get_json_path(self):
        return os.path.join(self.loc_dir, self.basename + '.json')

    def get_jpg_json_path(self):
        return self.get_jpg_path(), self.get_json_path()

    def get_basename(self):
        return self.basename

    def get_loc_dir(self):
        return self.loc_dir

    def get_annotation(self):
        ss = json.load(open(self.get_json_path()))
        BBGT = []
        for obj in ss['shapes']:
            label = obj['label']
            points = obj['points']
            xmin = int(points[0][0])
            ymin = int(points[0][1])
            xmax = int(points[1][0])
            ymax = int(points[1][1])
            BBGT.append([xmin, ymin, xmax, ymax, label])
        return BBGT

    def get_width_height(self):
        ss = json.load(open(self.get_json_path()))
        return ss['imageWidth'], ss['imageHeight']


class JPG_TXT(object):
    def __init__(self, loc_dir, basename):
        """all these attributes describe the jpg and txt files
        :param loc_dir: suggested to be the absolute path
        :param basename: the basename of the jpg and txt files without the extension
        """
        self.loc_dir = loc_dir
        self.basename = basename

    def get_jpg_path(self):
        return os.path.join(self.loc_dir, self.basename + '.jpg')

    def get_txt_path(self):
        return os.path.join(self.loc_dir, self.basename + '.txt')

    def get_jpg_txt_path(self):
        return self.get_jpg_path(), self.get_txt_path()

    def get_basename(self):
        return self.basename

    def get_loc_dir(self):
        return self.loc_dir

    def get_annotation(self):
        BBGT = []
        f = open(self.get_txt_path(), 'r')
        liness = f.readlines()

        for lines in liness:
            lines = lines.split(',')
            if len(lines) == 5:
                lines = [line.strip() for line in lines]
                xmin = int(lines[0][1:])
                ymin = int(lines[1][:-1])
                xmax = int(lines[2][1:])
                ymax = int(lines[3][:-1])
                label = int(lines[4])
                BBGT.append([xmin, ymin, xmax, ymax, label])
        return BBGT


class XML_Generator(object):
    """A class to generate a xml file
    Attributes
    ----------
        filename: str
            the absolute path of the xml file

    Methods
    -------
        set_size(witdh, height, channel):
            set the size of the image, including width, height and channel
        add_pic_attr(label, xmin, ymin, xmax, ymax):
            add the bounding box and label of the image
        savefile(filename):
            save the xml file
    """

    def __init__(self, filename):
        self.root = etree.Element("annotation")

        child1 = etree.SubElement(self.root, "folder")
        child1.text = "VOC2007"

        child2 = etree.SubElement(self.root, "filename")
        child2.text = filename

        child3 = etree.SubElement(self.root, "source")

        child4 = etree.SubElement(child3, "annotation")
        child4.text = "PASCAL VOC2007"
        child5 = etree.SubElement(child3, "database")
        child5.text = "Unknown"

        child6 = etree.SubElement(child3, "image")
        child6.text = "flickr"
        child7 = etree.SubElement(child3, "flickrid")
        child7.text = "35435"

    def set_size(self, witdh, height, channel):
        """set the size of the image, including width, height and channel which should be string type
        :param witdh:
        :param height:
        :param channel:
        :return: None
        """
        size = etree.SubElement(self.root, "size")
        widthn = etree.SubElement(size, "width")
        widthn.text = str(witdh)
        heightn = etree.SubElement(size, "height")
        heightn.text = str(height)
        channeln = etree.SubElement(size, "depth")
        channeln.text = str(channel)

    def add_pic_attr(self, label, xmin, ymin, xmax, ymax):
        """add the bounding box and label of the image
        :param label:
        :param xmin:
        :param ymin:
        :param xmax:
        :param ymax:
        :return: None
        """
        object = etree.SubElement(self.root, "object")
        namen = etree.SubElement(object, "name")
        namen.text = label
        bndbox = etree.SubElement(object, "bndbox")
        xminn = etree.SubElement(bndbox, "xmin")
        xminn.text = str(xmin)
        yminn = etree.SubElement(bndbox, "ymin")
        yminn.text = str(ymin)
        xmaxn = etree.SubElement(bndbox, "xmax")
        xmaxn.text = str(xmax)
        ymaxn = etree.SubElement(bndbox, "ymax")
        ymaxn.text = str(ymax)

    def savefile(self, filename):
        tree = etree.ElementTree(self.root)
        tree.write(filename, pretty_print=True, xml_declaration=False, encoding='utf-8')


class Transformer_Annotation_Format(object):
    """This class is to transform the annotation format, including json, xml and txt.
    New annotation file would be saved in the new directory with the same basename as the original directory
    """
    def __init__(self, loc_dir, basename, raw_format, new_format):
        self.loc_dir = loc_dir
        self.basename = basename
        self.raw_format = raw_format
        self.new_format = new_format

    def json2xml(self):
        JJ = JPG_JSON(self.loc_dir, self.basename)
        width, height = JJ.get_width_height()
        new_loc_dir = JJ.get_loc_dir() + "_xml"
        os.makedirs(new_loc_dir, exist_ok=True)

        xml_filename = os.path.join(JJ.get_loc_dir() + "_xml", self.basename + ".xml")
        coordis = JJ.get_annotation()

        XG = XML_Generator(xml_filename)
        XG.set_size(width, height, 3)
        for xmin, ymin, xmax, ymax, label in coordis:
            XG.add_pic_attr(label, int(xmin), int(ymin), int(xmax), int(ymax))
        XG.savefile(xml_filename)
        shutil.copy(JJ.get_jpg_path(), new_loc_dir)

    def batch_transform(self):
        """batch transform the annotation format
        :return: None

        example
        -------
        >>> loc_dir = 'D:/data'
        >>> basename = 'test'
        >>> raw_format = '.json'
        >>> new_format = '.xml'
        >>> TA = Transformer_Annotation_Format(loc_dir, basename, raw_format, new_format)
        >>> TA.batch_transform()
        """
        for root, dirs, files in os.walk(self.loc_dir):
            for file in files:
                if file.endswith(self.raw_format):
                    self.basename = file.split('.')[0]  # update the basename
                    if self.raw_format == '.json' and self.new_format == '.xml':
                        self.json2xml()
                    elif self.raw_format == '.json' and self.new_format == '.txt':
                        pass
                    elif self.raw_format == '.xml' and self.new_format == '.json':
                        pass
                    elif self.raw_format == '.xml' and self.new_format == '.txt':
                        pass
                    elif self.raw_format == '.txt' and self.new_format == '.json':
                        pass
                    elif self.raw_format == '.txt' and self.new_format == '.xml':
                        pass
                    else:
                        print('Please check the format you want to transform!')


class Pre_Process(object):
    """This class is to preprocess the images and annotations based on xml format
    """

    def __init__(self, loc_dir, basename):
        self.loc_dir = loc_dir
        self.basename = basename

        self.JX = JPG_XML(self.loc_dir, self.basename)

    def crop_big2small(self,
                       # imgname,
                       # dirsrc,
                       # dirdst,
                       # class_dict,
                       subsize_h=640,
                       subsize_w=640,
                       gap=620,
                       iou_thresh=0.0,
                       ext='.jpg'):
        """crop a big image into small images in the remote sensing and surface detection scenarios
        :param imgname:
        :param dirsrc:
        :param dirdst:
        :param class_dict:
        :param subsize_h: the height of the small image
        :param subsize_w: the width of the small image
        :param gap: the gap between the small images
        :param iou_thresh: the threshold of the iou
        :param ext: the extension of the image
        :return: None

        example
        -------
        >>> loc_dir = 'D:/data'
        >>> basename = 'test'
        >>> PP = Pre_Process(loc_dir, basename)
        >>> PP.crop_big2small()
        """
        JX = JPG_XML(self.loc_dir, self.basename)

        @staticmethod
        def iou(BBGT, imgRect):
            """
            并不是真正的iou。计算每个BBGT和图像块所在矩形区域的交与BBGT本身的的面积之比，比值范围：0~1
            输入：BBGT：n个标注框，大小为n*4,每个标注框表示为[xmin,ymin,xmax,ymax]，类型为np.array
                  imgRect：裁剪的图像块在原图上的位置，表示为[xmin,ymin,xmax,ymax]，类型为np.array
            返回：每个标注框与图像块的iou（并不是真正的iou），返回大小n,类型为np.array
            """
            left_top = np.maximum(BBGT[:, :2], imgRect[:2])
            right_bottom = np.minimum(BBGT[:, 2:], imgRect[2:])
            wh = np.maximum(right_bottom - left_top, 0)
            inter_area = wh[:, 0] * wh[:, 1]
            iou = inter_area / ((BBGT[:, 2] - BBGT[:, 0]) * (BBGT[:, 3] - BBGT[:, 1]))
            for id in range(len(BBGT)):
                flag = imgRect[0] < BBGT[id, 0] and imgRect[2] > BBGT[id, 2] and iou[id] > 0.2 and BBGT[id, 3] - BBGT[
                    id, 1] > 100
                if flag:
                    iou[id] = 1
            return iou

        img = cv2.imread(JX.get_jpg_path(), 1)
        BBGT = np.array(JX.get_annotation())
        img_h, img_w = JX.get_width_height()
        subsize_h, subsize_w = int(img_h / 2), int(img_w / 2)

        # #####测试硬编码########
        # BBGTiner=[]
        # BBGTiner.append([2894, 0, 2908, 568, 'AG'])
        # BBGTiner.append([10, 10, 300, 300, 'AP'])
        # BBGT = np.array(BBGTiner)
        # ####测试硬编码结束######

        top = 0
        reachbottom = False
        valid_num = 0
        split_num = 0
        while not reachbottom:
            reachright = False
            left = 0
            if top + subsize_h >= img_h:
                reachbottom = True
                top = max(img_h - subsize_h, 0)
            while not reachright:
                if left + subsize_w >= img_w:
                    reachright = True
                    left = max(img_w - subsize_w, 0)
                imgsplit = img[top:min(top + subsize_h, img_h), left:min(left + subsize_w, img_w)]
                # print('print imgsplit')
                # print(imgsplit)
                # print('print imgsplit done')
                if imgsplit.shape[:2] != (subsize_h, subsize_w):
                    template = np.zeros((subsize_h, subsize_w, 3), dtype=np.uint8)
                    # print('print template')
                    # print(template)
                    # print('print template done')
                    template[0:imgsplit.shape[0], 0:imgsplit.shape[1]] = imgsplit
                    imgsplit = template
                imgrect = np.array([left, top, left + subsize_w, top + subsize_h]).astype('float32')
                ious = iou(BBGT[:, :4].astype('float32'), imgrect)
                # print('print iou start')
                # print(ious, iou_thresh)
                # print('print iou done')

                BBpatch = BBGT[ious > iou_thresh]
                split_num += 1
                # print('split num ----', split_num, imgrect)
                ## abandaon images with 0 bboxes
                if len(BBpatch) > 0:
                    # valid_num  += len(BBpatch)
                    # print('valid ---------', valid_num)
                    # print(len(BBpatch))
                    save_loc_dir = self.loc_dir + '_crop'
                    os.makedirs(save_loc_dir, exist_ok=True)
                    cv2.imwrite(os.path.join(save_loc_dir,
                                             self.basename.split('.')[0] + '_' + str(left) + '_' + str(top) + ext),
                                imgsplit)
                    xml = os.path.join(save_loc_dir,
                                       self.basename.split('.')[0] + '_' + str(left) + '_' + str(
                                           top) + '.xml')  # the filename keeps the original xml filename and the crop position information,which would be used to recover

                    XG = XML_Generator(xml)
                    # print(imgsplit.shape)
                    XG.set_size(imgsplit.shape[0], imgsplit.shape[1], imgsplit.shape[2])
                    for bb in BBpatch:
                        x1, y1, x2, y2, label_name = int(bb[0]) - left, int(bb[1]) - top, int(bb[2]) - left, int(
                            bb[3]) - top, bb[4]
                        # target_id, x1, y1, x2, y2 = XGo_info
                        x1 = max(x1, 0)
                        y1 = max(y1, 0)
                        x2 = min(subsize_w, x2)
                        y2 = min(subsize_h, y2)
                        XG.add_pic_attr(label_name, x1, y1, x2, y2)
                    XG.savefile(xml)

                left += subsize_w - gap
            top += subsize_h - gap

    def batch_crop(self, gap=0):
        """batch crop the big images into small images
        :return: None

        example
        -------
        >>> loc_dir = 'D:/data'
        >>> basename = 'test'
        >>> PP = Pre_Process(loc_dir, basename)
        >>> PP.batch_crop()
        """
        for root, dirs, files in os.walk(self.loc_dir):
            for file in files:
                if file.endswith('.jpg'):
                    self.basename = file.split('.')[0]
                    self.crop_big2small(gap=gap)


class Argumentation(object):
    def __init__(self, loc_dir, basename):
        self.loc_dir = loc_dir
        self.basename = basename

    def spin_or_flip(self, image_path, xml_path, mode='horizontal'):
        """Spin and flip the image and the bounding box coordinates
        :param image_path: absolute path of the image
        :param xml_path: absolute path of the xml file
        :param mode: mode should be one of ['horizontal', 'vertical', 'rotation']
        :return: argued_img, tree
        """
        # Load the image
        img = cv2.imread(image_path)

        # Parse the XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Get the size of the image
        size = root.find('size')

        # Update the bounding box coordinates for horizontal flip
        if mode == "horizontal":
            # Flip the image horizontally
            argued_img = cv2.flip(img, 1)
            width = int(size.find('width').text)
            for box in root.iter('bndbox'):
                xmin = int(box.find('xmin').text)
                xmax = int(box.find('xmax').text)

                # Flip the x coordinates
                new_xmin = width - xmax
                new_xmax = width - xmin

                box.find('xmin').text = str(new_xmin)
                box.find('xmax').text = str(new_xmax)

        # Update the bounding box coordinates for vertical flip
        elif mode == "vertical":
            # Flip the image vertically
            argued_img = cv2.flip(img, 0)
            height = int(size.find('height').text)
            for box in root.iter('bndbox'):
                ymin = int(box.find('ymin').text)
                ymax = int(box.find('ymax').text)

                # Flip the y coordinates
                new_ymin = height - ymax
                new_ymax = height - ymin

                box.find('ymin').text = str(new_ymin)
                box.find('ymax').text = str(new_ymax)

        # Update the bounding box coordinates for rotation
        elif mode == "rotation":
            # Rotate the image 90 degrees
            argued_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

            width = int(size.find('width').text)
            height = int(size.find('height').text)
            # Update the bounding box coordinates for rotation
            for box in root.iter('bndbox'):
                xmin = int(box.find('xmin').text)
                ymin = int(box.find('ymin').text)
                xmax = int(box.find('xmax').text)
                ymax = int(box.find('ymax').text)

                # Rotate the coordinates
                new_xmin = height - ymax
                new_ymin = xmin
                new_xmax = height - ymin
                new_ymax = xmax

                box.find('xmin').text = str(new_xmin)
                box.find('ymin').text = str(new_ymin)
                box.find('xmax').text = str(new_xmax)
                box.find('ymax').text = str(new_ymax)

            # Update the size of the image
            size.find('width').text = str(height)
            size.find('height').text = str(width)

        else:
            print("mode should be one of ['horizontal', 'vertical', 'rotation']")

        # Return the flipped image and the updated XML tree
        return argued_img, tree

    def resize_image_and_xml(self, image_path, xml_path, new_size=(1280, 736)):
        # Load the image
        img = cv2.imread(image_path)

        # Parse the XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Get the size of the image
        size = root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)

        # Resize the image
        resized_img = cv2.resize(img, new_size)

        # Calculate the scale factors
        x_scale = new_size[0] / width
        y_scale = new_size[1] / height

        # Update the bounding box coordinates
        for box in root.iter('bndbox'):
            xmin = int(box.find('xmin').text)
            ymin = int(box.find('ymin').text)
            xmax = int(box.find('xmax').text)
            ymax = int(box.find('ymax').text)

            # Scale the coordinates
            box.find('xmin').text = str(int(xmin * x_scale))
            box.find('ymin').text = str(int(ymin * y_scale))
            box.find('xmax').text = str(int(xmax * x_scale))
            box.find('ymax').text = str(int(ymax * y_scale))

        # Update the size of the image
        size.find('width').text = str(new_size[0])
        size.find('height').text = str(new_size[1])

        # Return the resized image and the updated XML tree
        return resized_img, tree

    def widen_elongated_xml(self,
                            # src_path,
                            # dst_path,
                            # in_path,
                            # out_path,
                            HW_ratio=2,
                            widden_ratio=2,
                            i=0):
        """rewrite the xml file, widen the elongated bounding boxes by 2 times the center width
        xml_path:    待处理的xml文件路径
        output_path: 输出的xml文件路径
        :return: i the number of the elongated bounding boxes
        """
        JX = JPG_XML(self.loc_dir, self.basename)
        save_loc_dir = JX.get_loc_dir() + '_widden'
        save_xml_path = os.path.join(save_loc_dir, self.basename + "_widden_{}.xml".format(widden_ratio))
        os.makedirs(save_loc_dir, exist_ok=True)
        img = cv2.imread(JX.get_jpg_path(), 1)
        shape = img.shape
        ann = XML_Generator(save_xml_path)
        ann.set_size(shape[0], shape[1], shape[2])

        # tree= ET.parse(in_path, out_path)
        # root = tree.getroot()
        BBGT = JX.get_annotation()

        for obj in BBGT:
            xmin, ymin, xmax, ymax, label = obj
            # if label in process_list:
            if True:
                width = xmax - xmin
                height = ymax - ymin
                # check if the bounding box is elongated
                # if (ymax - ymin) > H_ratio * shape[0] or (ymax - ymin) > HW_ratio * (xmax - xmin):
                if height > HW_ratio * width:
                    i += 1
                    # print("i: ", i)
                    # calculate the center of the bounding box
                    x_center = (xmin + xmax) / 2
                    # calculate the new width
                    new_width = widden_ratio * (xmax - xmin)
                    # calculate the new xmin and xmax
                    xmin = max(0, int(x_center - new_width / 2))
                    xmax = min(shape[1], int(x_center + new_width / 2))
                    # add the new bounding box to the annotation
                    ann.add_pic_attr(label, xmin, ymin, xmax, ymax)
                else:
                    ann.add_pic_attr(label, xmin, ymin, xmax, ymax)
            else:
                ann.add_pic_attr(label, xmin, ymin, xmax, ymax)

        ann.savefile(save_xml_path)
        jpg_save_path = os.path.join(save_loc_dir, self.basename + '_widden_{}.jpg'.format(widden_ratio))
        shutil.copy(JX.get_jpg_path(), jpg_save_path)

        return i

    def batch_widen_elongated_xml(self):
        """batch widen the elongated bounding boxes in the xml files
        :return: None

        example
        -------
        >>> loc_dir = 'D:/data'
        >>> basename = 'test'
        >>> PP = Pre_Process(loc_dir, basename)
        >>> PP.batch_widen_elongated_xml()
        """
        for root, dirs, files in os.walk(self.loc_dir):
            for file in files:
                if file.endswith('.jpg'):
                    self.basename = file.split('.')[0]
                    self.widen_elongated_xml()



