import cv2
import base64
import requests
import json
import time


class InferTool:
    """A class to manage the inference process of a model.
    Attributes
    ----------
    url : str
        The url of the model.
    image_path : str
        The path of the image.
    """

    def __init__(self,
                 url="",
                 image_path="",
                 ):
        self.url = url
        self.image_path = image_path

    @staticmethod
    def arr2base64(img):
        """transform image to base64 style"""
        _, buffer = cv2.imencode('.jpg', img)
        jpg_as_text = base64.b64encode(buffer)

        return jpg_as_text.decode('utf-8')

    def box_magic(self, xmin, ymin, xmax, ymax):
        h = ymax - xmax
        w = xmax - xmin
        if h / w >= 5:
            x_center = int(0.5 * (xmin + xmax))
            raw_width = int(w / 2)
            xmin = x_center - int(raw_width / 2)
            xmax = x_center + int(raw_width / 2)

        return xmin, ymin, xmax, ymax

    def inference_image(self, img_arr, iam=False):
        """A method to inference image.
        """
        dbbox = []
        dscores = []
        dlabel = []
        if iam:
            appcode = ""
            token = ""
            headers = {
                "Content-Type": "application/json",
                "X-Apig-Appcode": appcode,
                "X-Auth-Token": token,
                "X-HW-ID": "9eacf8c2-402b-4265-a14a-b2a6a6fe6425",
                "Host": "iit-online-infer.js-dl-1.dlcloud.com",  # appcode认证使用
                # "Host": "10.200.8.42"  # token认证使用
            }
        else:
            headers = {
                "Content-Type": "application/json",
            }
        body = {"images": InferTool.arr2base64(img_arr)}

        res = requests.post(url=self.url, json=body, headers=headers, verify=False)

        out = res.text.encode('utf-8')
        out = json.loads(out)
        out = out['result'][1:]

        for item in out:
            scores = item['Score']
            box = item['Box']
            label = item['label']
            xmin = box['X']
            ymin = box['Y']
            xmax = box['X'] + box['Width']
            ymax = box['Y'] + box['Height']

            # xmin, ymin, xmax, ymax = self.box_magic(xmin, ymin, xmax, ymax)  # 需要宽还原的情况下修改此处

            dbbox.append([xmin, ymin, xmax, ymax])
            dscores.append(scores)
            dlabel.append(label)

        return dbbox, dscores, dlabel

    def infer_one_pic(self):
        """A method to infer one pic"""
        abbox = []
        ascore = []
        alabel = []
        s = time.time()  # 推理一张图像的起始时间
        image = cv2.imread(self.image_path)
        bbox, scores, label = self.inference_image(image)
        abbox = abbox + bbox
        ascore = ascore + scores
        alabel = alabel + label
        tt = time.time() - s  # 推理一张图像的时间
        print("infer time:", tt)

        out = {'result': [{'RegisterMatrix': [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}]}
        for i in range(len(abbox)):
            # print(new_boxes[i])
            [xmin, ymin, xmax, ymax] = abbox[i]
            label = alabel[i]
            score = ascore[i]
            tmp_dict = {
                'Box': {'Angle': 0, 'Height': int(ymax - ymin), 'Width': int(xmax - xmin), 'X': int(xmin),
                        'Y': int(ymin)},
                'Score': score, 'label': label
            }

            out['result'].append(tmp_dict)

        return out, tt

    def batch_inference(self, image_list):
        """A method to batch inference image"""
        out_list = []
        for image_path in image_list:
            self.image_path = image_path
            out, tt = self.infer_one_pic()
            out_list.append(out)

        return out_list


class Eval_model:
    """A class to manage the evaluation of a model.
    Attributes
    ----------
    gt_json : str
        The path of the ground truth json file.
    pred_json : str
        The path of the prediction json file.
    iou_threshold : float
        The threshold of iou.
    score_threshold : float
        The threshold of score.
    post_iou : float
        The threshold of post iou.
    is_post : bool
        Whether to post process.

    Return
    -------
    precision : float
        The precision of the model.
    recall : float
        The recall of the model.
    f1 : float
        The f1 of the model.
    mAP : float
        The mAP of the model.
    """
    def __init__(self,
                 iou_threshold=0.5, score_threshold=0.3,
                 post_iou=0.5, is_post=False):
        self.iou_threshold = iou_threshold
        self.score_threshold = score_threshold
        self.post_iou = post_iou
        self.is_post = is_post

    def






