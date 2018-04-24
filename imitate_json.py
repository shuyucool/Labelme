#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
# author:"Zhang Shuyu"

"""半自动标注图像，并生成可供labelme接口解析的json类型的文件"""
import cv2
import scipy.io as sio
from pylab import *
from json import dumps
import json
from img2json import img_to_json
import customserializer
import glob
from base64 import b64encode
# json_file_input = "D:\\Practice\\JSON\\1.json"
# data = json.load(open(json_file_input))

mat_path = "D:\\Practice\\coordinate\\img_coordinate_3"  # 连通域轮廓坐标数据文件路径，其中img_coordinate_3是mat文件，在MATLAB中生成的元胞数组
img_coordinate = sio.loadmat(mat_path)  # 加载指定数据

def dict_other_json(imagePath, imageData, shapes, fillColor=None, lineColor=None):
    """
    :param lineColor: list
    :param fillColor: list
    :param imageData: str
    :param imagePath: str
    :return: dict""
    """
    # return {"shapes": shapes, "lineColor": lineColor, "fillColor": fillColor, "imageData": imageData,
    #         "imagePath": imagePath}
    return {"imagePath": imagePath, "imageData": imageData, "shapes": shapes, "fillColor": fillColor, "lineColor": lineColor
            }


def dict_shapes(points, label, fill_color=None, line_color=None):
    return {'points': points, 'label': label, 'fill_color': fill_color, 'line_color': line_color}


def coordiante_xy(coordinate_x,coordinate_y):
    return [float(coordinate_x),float(coordinate_y)]

fillColor = [0, 0, 255, 128]
lineColor = [0, 255, 0, 128]

# 参考labelme的json格式重新生成json文件，使用labelme的接口解析数据

class data_mat_read(object):
    """
    读取MATLAB提取的坐标数据MAT文件，结合图像生成的json数据，
    生成一个模仿labelme软件标记object后生成的.json文件
    """
    def __init__(self, img_type=".jpeg",img_json_path="D:\\Practice\\Origin_picture_json\\",
                 fusion_path = "D:\\Practice\\fusion_json\\",
                 imgPath ="D:\\Practice\\Origin_picture\\",img_json_type=".json"):

        """
        :param coordinate: MATLAB得到的.mat数据文件，包含了每一帧中不同个体的轮廓坐标
        :param img_type: 图片的格式
        :param img_json_path: img2json将图片转成json文件存放的路径
        :param img_json_type: img2json将图片转成json文件的格式
        :param imgPath: 待标注图像的路径
        """
        """
        使用glob从指定路径中获取所有的img_type的json文件
        """
        self.img_json = glob.glob(img_json_path + "/*" + img_json_type)
        self.img_json_path = img_json_path
        self.img_json_type = img_json_type
        self.fusion_path = fusion_path
        self.img_type = img_type
        self.imagePath = imgPath

    def fusion(self):
        """将坐标数据与对应的图像进行融合，生成可以替代labelme生成的json文件"""
        print('-' * 30)
        print("读取坐标，开始生成json文件")
        print('-' * 30)

        img_json_path = self.img_json_path
        img_path = self.imagePath
        img_type = self.img_type
        fusion_path = self.fusion_path
        """key:代表第number帧的坐标数据"""
        for key in img_coordinate.items():
            shapes = []
            key_name = key[0]  # 获得坐标保存的名字 img_number:第number帧的坐标
            key_name_number = key_name[key_name.rindex("_") + 1:]  # 获得的坐标对应是第几帧 number
            if key_name_number != "":
                imageData = json.load(open(img_json_path + str(key_name_number) + self.img_json_type))
                imagePath = str(key_name_number) + img_type
                object_num = range(1, shape(key[1])[0] + 1)  # (1,鱼的数目)
                """每帧图像中个体的汇总"""
                for j in object_num:
                    label = 'fish' + str(j)
                    """坐标数据汇总"""
                    fish_coordinate = key[1][0:6][j - 1]
                    points = []
                    fish_coordinate_x = fish_coordinate[0:2][0][0:1][0][0:1][0]  # Todo: fish_coordinate[][][][][][]这么多[],数据存储的具体位置，在debug模式下可以看到，可依据自己的需要修改
                    fish_coordinate_y = fish_coordinate[0:2][1][0:1][0][0:1][0]  # Todo:同上
                    for i in range(shape(fish_coordinate_x)[0]):
                        points.append(
                            coordiante_xy(fish_coordinate_x[i][0:1][0], fish_coordinate_y[i][0:1][0]))  # Todo:coordinate_xy会将数据的格式转为float类型，这样可以不必调用customserializer.py
                    shapes.append(dict_shapes(points, label))
                data = dict_other_json(imagePath, imageData, shapes, fillColor, lineColor)

                # 写入json文件
                json_file = fusion_path + str(key_name_number) + self.img_json_type
                json.dump(data, open(json_file, 'w'))

                # json_img_data = dumps(data)

                # with open(json_file, 'w', encoding='utf-8') as f:
                #     json.dump(data, f, default=customserializer.to_json)Todo:如果在108行没有调用coordinate_xy，而是points.append(x,y),此时需要调用customserializer.py，防止程序报错

                # with open(json_file, 'w') as json_file:
                #     json_file.write(json_img_data)



if __name__=="__main__":
    data_read = data_mat_read()
    data_read.fusion()