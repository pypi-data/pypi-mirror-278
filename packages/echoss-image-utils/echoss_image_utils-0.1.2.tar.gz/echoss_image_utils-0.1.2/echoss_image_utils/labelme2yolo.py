'''
Created on Aug 18, 2021

@author: xiaosonh
'''
import os
import sys
import argparse
import shutil
import math
import yaml
import numpy as np
from tqdm import tqdm
from collections import OrderedDict

import json
import cv2
import PIL.Image

from sklearn.model_selection import train_test_split
from echoss_s3handler import s3_handler
from echoss_query.query import echoss_query

import logging
from .echoss_logger import get_logger, set_logger_level

logger = get_logger("echoss_image_utils")

# from labelme import utils
class Labelme2YOLO(object):
    def __init__(self, json_dir, img_copy, s3_data, s3_yaml, json_db_table):
        self._json_dir = json_dir
        self.img_copy = img_copy
        self.s3_data = s3_data
        self.s3_yaml = s3_yaml
        self.json_db_table = json_db_table


        if self.s3_data:
            try:
                if self.s3_yaml != None:
                    with open(self.s3_yaml) as f:
                        self.data_dict = yaml.load(f, Loader=yaml.SafeLoader)  # data dict
                    self.s3handler = s3_handler.S3ResourceHandler(self.data_dict)

                    # 경로를 input으로 받을지 확인 뒤 수정할수도
                    with open('../echoss_query/config/config.yaml', 'r') as file:
                        self.db_yaml_info = yaml.load(file, Loader=yaml.FullLoader)
                    self.mysql = echoss_query.MysqlQuery(self.db_yaml_info[self.data_dict['db_region']])
                    # 아래의 테이블이 없을때 오류 처리가 될 수 있도록 수정 필요할수도
                    json_db_list = self.mysql.select_list(f'SELECT prefix, file_name FROM {self.json_db_table}')
                    self.object_lists = [json_db_list[idx - 1] + json_db_list[idx] for idx, x in enumerate(json_db_list)
                                         if idx % 2 == 1]

                    # Not use S3 get_object_list
                    # print("Make s3 object lists...")
                    # self.object_lists = self.s3handler.get_object_list(bucket=self.data_dict['bucket'],
                    #                                                     s3_prefix=self.data_dict['json_data_path'])
                    # print("Finish s3 object lists...")
                    self._label_id_map = self._get_label_id_map(self.object_lists)
                else:
                    raise Exception("To use s3 data, you must enter the s3 config file.")
            except Exception as e:
                logger.log(level=logging.DEBUG,msg=e)
        else:
            self._label_id_map = self._get_label_id_map(self._json_dir)


    def _make_train_val_dir(self):
        """
        s3 데이터를 사용할 때에는 해당 함수를 사용하지 않음
        왜냐하면 s3데이터의 경우 train, val, test가 나뉘어져 있는 파일 목록을 사용하기 때문.
        """
        self._label_dir_path = os.path.join(self._json_dir,
                                            'YOLODataset/labels/')
        self._image_dir_path = os.path.join(self._json_dir,
                                            'YOLODataset/images/')

        for yolo_path in (os.path.join(self._label_dir_path + 'train/'),
                          os.path.join(self._label_dir_path + 'val/'),
                          os.path.join(self._image_dir_path + 'train/'),
                          os.path.join(self._image_dir_path + 'val/')):
            if os.path.exists(yolo_path):
                shutil.rmtree(yolo_path)

            os.makedirs(yolo_path)

    def _get_label_id_map(self, json_dir):  ## modified dwnam 23.02.16
        label_set = set()

        if type(json_dir) != list:
            for file_name in os.listdir(json_dir):
                if file_name.endswith('json'):
                    json_path = os.path.join(json_dir, file_name)
                    data = json.load(open(json_path))
                    for shape in data['shapes']:
                        label_set.add(shape['label'])
        else:
            for file_name in json_dir:
                if file_name.endswith('json'):
                    f = self.s3handler.read_file(self.data_dict['bucket'], file_name)
                    f.seek(0)
                    dict_ = f.read().decode()
                    data = json.loads(dict_)
                    for shape in data['shapes']:
                        label_set.add(shape['label'])
        label_list = list(label_set)
        label_list.sort()
        return OrderedDict([(label, label_id) \
                            for label_id, label in enumerate(label_list)])

    def _train_test_split(self, folders, json_names, val_size):
        """
        s3 데이터를 사용할 때에는 해당 함수를 사용하지 않음
        왜냐하면 s3데이터의 경우 train, val, test가 나뉘어져 있는 파일 목록을 사용하기 때문.
        """
        if len(folders) > 0 and 'train' in folders and 'val' in folders:
            train_folder = os.path.join(self._json_dir, 'train/')
            train_json_names = [train_sample_name + '.json' \
                                for train_sample_name in os.listdir(train_folder) \
                                if os.path.isdir(os.path.join(train_folder, train_sample_name))]

            val_folder = os.path.join(self._json_dir, 'val/')
            val_json_names = [val_sample_name + '.json' \
                              for val_sample_name in os.listdir(val_folder) \
                              if os.path.isdir(os.path.join(val_folder, val_sample_name))]

            return train_json_names, val_json_names

        train_idxs, val_idxs = train_test_split(range(len(json_names)),
                                                test_size=val_size)
        train_json_names = [json_names[train_idx] for train_idx in train_idxs]
        val_json_names = [json_names[val_idx] for val_idx in val_idxs]

        return train_json_names, val_json_names

    def convert(self, val_size):
        if not self.s3_data:
            json_names = [file_name for file_name in os.listdir(self._json_dir) \
                          if os.path.isfile(os.path.join(self._json_dir, file_name)) and \
                          file_name.endswith('.json')]
            folders = [file_name for file_name in os.listdir(self._json_dir) \
                       if os.path.isdir(os.path.join(self._json_dir, file_name))]
            train_json_names, val_json_names = self._train_test_split(folders, json_names, val_size)

            self._make_train_val_dir()

            # convert labelme object to yolo format object, and save them to files
            # also get image from labelme json file and save them under images folder
            for target_dir, json_names in zip(('train/', 'val/'),
                                              (train_json_names, val_json_names)):
                for json_name in json_names:
                    json_path = os.path.join(self._json_dir, json_name)
                    json_data = json.load(open(json_path))

                    logger.log(level=logging.DEBUG,msg='Converting %s for %s ...' % (json_name, target_dir.replace('/', '')))

                    img_path = self._save_yolo_image(json_data,
                                                     json_name,
                                                     self._image_dir_path,
                                                     target_dir)

                    yolo_obj_list = self._get_yolo_object_list(json_data, img_path)
                    self._save_yolo_label(json_name,
                                          self._label_dir_path,
                                          target_dir,
                                          yolo_obj_list)

            logger.log(level=logging.DEBUG,msg='Generating dataset.yaml file ...')
            self._save_dataset_yaml()
        else:
            for json_name in tqdm(self.object_lists):
                f = self.s3handler.read_file(self.data_dict['bucket'], json_name)
                f.seek(0)
                dict_ = f.read().decode()
                json_data = json.loads(dict_)

                # print('Converting %s for ...' % (json_name))

                img_name = json_data['imagePath']
                img_ext = img_name.split(".")[-1]
                lower_check = img_ext.islower()  # image extension check(upper or lower)
                if not lower_check:  # 일부 과제의 업로드 데이터에 확장자가 대문자로 입력된 데이터가 있었음.
                    img_name = ".".join([img_name.split(".")[0], img_ext.lower()])
                img_path = os.path.join(self.data_dict['image_data_path'], img_name)

                yolo_obj_list = self._get_yolo_object_list(json_data, img_path)
                self._save_yolo_label(json_name,
                                      "not_use",  # self._label_dir_path
                                      None,
                                      yolo_obj_list)
            self._save_dataset_yaml()

    def convert_one(self, json_name):  # Not used in s3
        if not self.s3_data:
            json_path = os.path.join(self._json_dir, json_name)
            json_data = json.load(open(json_path))

            logger.log(level=logging.DEBUG,msg='Converting %s ...' % json_name)

            img_path = self._save_yolo_image(json_data, json_name,
                                             self._json_dir, '')

            yolo_obj_list = self._get_yolo_object_list(json_data, img_path)
            self._save_yolo_label(json_name, self._json_dir,
                                  '', yolo_obj_list)
        else:
            logger.log(level=logging.DEBUG,msg="Not used in s3")

    def _get_yolo_object_list(self, json_data, img_path):
        yolo_obj_list = []
        if self.s3_data:  ## modified dwnam 23.02.16
            img = self.s3handler.read_image(self.data_dict['bucket'], img_path, "cv2")
            img_h, img_w, _ = img.shape
        else:
            img_h, img_w, _ = cv2.imread(img_path).shape
        for shape in json_data['shapes']:
            # labelme circle shape is different from others
            # it only has 2 points, 1st is circle center, 2nd is drag end point
            if shape['shape_type'] == 'circle':
                yolo_obj = self._get_circle_shape_yolo_object(shape, img_h, img_w)
            elif shape['shape_type'] == 'polygon':
                yolo_obj = self._get_other_shape_yolo_object(shape, img_h, img_w, shape['shape_type'])
            else:
                yolo_obj = self._get_other_shape_yolo_object(shape, img_h, img_w, shape['shape_type'])
            if yolo_obj != False:  # Not empty label file, if empty label file(yolo_obj_list = [])
                yolo_obj_list.append(yolo_obj)
        return yolo_obj_list

    def _get_circle_shape_yolo_object(self, shape, img_h, img_w):
        obj_center_x, obj_center_y = shape['points'][0]

        radius = math.sqrt((obj_center_x - shape['points'][1][0]) ** 2 +
                           (obj_center_y - shape['points'][1][1]) ** 2)
        obj_w = 2 * radius
        obj_h = 2 * radius

        yolo_center_x = round(float(obj_center_x / img_w), 6)
        yolo_center_y = round(float(obj_center_y / img_h), 6)
        yolo_w = round(float(obj_w / img_w), 6)
        yolo_h = round(float(obj_h / img_h), 6)

        label_id = self._label_id_map[shape['label']]

        return label_id, yolo_center_x, yolo_center_y, yolo_w, yolo_h

    def _get_other_shape_yolo_object(self, shape, img_h, img_w, shape_type="rectangle"):
        if shape['points'] != []:
            def __get_object_desc_rect(obj_port_list):
                __get_dist = lambda int_list: max(int_list) - min(int_list)
                x_lists = [port[0] for port in obj_port_list]
                y_lists = [port[1] for port in obj_port_list]

                return min(x_lists), __get_dist(x_lists), min(y_lists), __get_dist(y_lists)

            def __get_object_desc_poly(obj_port_list):
                x_lists = [port[0] for port in obj_port_list]
                y_lists = [port[1] for port in obj_port_list]

                return x_lists, y_lists

            if shape_type == 'polygon':
                x_lists, y_lists = __get_object_desc_poly(shape['points'])

                yolo_x_lists = [round(float(obj_x / img_w), 6) for obj_x in x_lists]
                yolo_y_lists = [round(float(obj_y / img_h), 6) for obj_y in y_lists]

                label_id = self._label_id_map[shape['label']]

                return label_id, yolo_x_lists, yolo_y_lists
            else:
                obj_x_min, obj_w, obj_y_min, obj_h = __get_object_desc_rect(shape['points'])

                yolo_center_x = round(float((obj_x_min + obj_w / 2.0) / img_w), 6)
                yolo_center_y = round(float((obj_y_min + obj_h / 2.0) / img_h), 6)
                yolo_w = round(float(obj_w / img_w), 6)
                yolo_h = round(float(obj_h / img_h), 6)

                label_id = self._label_id_map[shape['label']]

                return label_id, yolo_center_x, yolo_center_y, yolo_w, yolo_h
        else:  # empty label file
            return False

    def _save_yolo_label(self, json_name, label_dir_path, target_dir, yolo_obj_list):  ## modified dwnam 23.02.16
        if not self.s3_data:
            txt_path = os.path.join(label_dir_path,
                                    target_dir,
                                    json_name.replace('.json', '.txt'))
        yolo_obj_lines = ''
        if yolo_obj_list == []:  # empty label file
            if not self.s3_data:
                with open(txt_path, 'w+') as f:
                    f.write("\n")
            else:
                self.s3handler.put_object("\n", json_name.replace('.json', '.txt').replace(self.data_dict['json_data_path'], self.data_dict['yolo_data_path']),
                                           self.data_dict['bucket'])

        else:
            for yolo_obj_idx, yolo_obj in enumerate(yolo_obj_list):
                if len(yolo_obj_list[0]) == 5:  # circle, rectangle
                    yolo_obj_lines += '%s %s %s %s %s\n' % yolo_obj \
                        if yolo_obj_idx + 1 != len(yolo_obj_list) else \
                        '%s %s %s %s %s' % yolo_obj

                elif len(yolo_obj_list[0]) == 3:  # polygon
                    yolo_obj_label_id = yolo_obj[0]
                    yolo_x_lists = yolo_obj[1]
                    yolo_y_lists = yolo_obj[2]
                    yolo_obj_line = yolo_obj_label_id
                    if yolo_obj_idx + 1 != len(yolo_obj_list):
                        for idx, (x, y) in enumerate(zip(yolo_x_lists, yolo_y_lists)):
                            if idx + 1 != len(yolo_x_lists):
                                yolo_obj_line = " ".join([str(yolo_obj_line), str(x), str(y)])
                            else:
                                yolo_obj_line = " ".join([str(yolo_obj_line), str(x), str(y)])
                                yolo_obj_lines += f"{yolo_obj_line}\n"
                    #                            yolo_obj_line += f" {x} {y}\n"
                    else:
                        for idx, (x, y) in enumerate(zip(yolo_x_lists, yolo_y_lists)):
                            yolo_obj_lines += " ".join([str(yolo_obj_line), str(x), str(y)])
                    #                        yolo_obj_line += f" {x} {y}"
            if not self.s3_data:
                with open(txt_path, 'w+') as f:
                    f.write(yolo_obj_lines)
            else:
                self.s3handler.put_object(yolo_obj_lines, json_name.replace('.json', '.txt').replace(self.data_dict['json_data_path'], self.data_dict['yolo_data_path']),
                                           self.data_dict['bucket'])

    def _save_yolo_image(self, json_data, json_name, image_dir_path, target_dir):  # 해시값이 아닌 json내부의 파일명을 가지고 와서 파일 이동 by dwnam
        img_name = json_data['imagePath']
        if not self.s3_data:
            # img_name = json_name.replace('.json', '.png')
            img_path = os.path.join(image_dir_path, target_dir, img_name)

            import shutil
            src = self._json_dir + img_name
            dst = img_path
            if self.img_copy is False:
                shutil.move(src=src, dst=dst)  # 파일을 이동시키고 싶을때 사용
            else:
                shutil.copy2(src=src, dst=dst)  # 파일을 이동이 아닌 복사하고 싶을때 사용
            # if not os.path.exists(img_path):  # imageData값이 없으면 오류가 발생하고 시간도 오래걸려서 주석 처리
            #     img = utils.img_b64_to_arr(json_data['imageData'])
            #     PIL.Image.fromarray(img).save(img_path)

        else:
            img_path = os.path.join(self.data_dict['image_data_path'], img_name)

        return img_path

    def _save_dataset_yaml(self):  # .yaml is_file() check
        if not self.s3_data:
            yaml_path = os.path.join(self._json_dir, 'YOLODataset/', 'dataset.yaml')

            with open(yaml_path, 'w+') as yaml_file:
                yaml_file.write('train: %s\n' % \
                                os.path.join(self._image_dir_path, 'train/'))
                yaml_file.write('val: %s\n\n' % \
                                os.path.join(self._image_dir_path, 'val/'))
                yaml_file.write('nc: %i\n\n' % len(self._label_id_map))

                names_str = ''
                names_numbers_str = ''
                for label, numbers in self._label_id_map.items():
                    names_str += "'%s', " % label
                    names_numbers_str += "'%s': %s, " % (label, numbers)
                names_str = names_str.rstrip(', ')
                names_numbers_str = names_numbers_str.rstrip(', ')
                yaml_file.write('names: [%s]\n' % names_str)
                yaml_file.write('label_mapping: {%s}\n' % names_numbers_str)
        else:
            with open(self.s3_yaml, 'a+') as yaml_file:
                yaml_file.write('\n%s\n' % '# YOLOv7 config')
                yaml_file.write('train: %s\n' % None)
                yaml_file.write('val: %s\n' % None)
                yaml_file.write('test: %s\n\n' % None)

                yaml_file.write('nc: %i\n\n' % len(self._label_id_map))

                names_str = ''
                names_numbers_str = ''
                for label, numbers in self._label_id_map.items():
                    names_str += "'%s', " % label
                    names_numbers_str += "%s: '%s', " % (numbers, label)
                names_str = names_str.rstrip(', ')
                names_numbers_str = names_numbers_str.rstrip(', ')
                yaml_file.write('names: [%s]\n' % names_str)
                yaml_file.write('label_mapping: {%s}\n' % names_numbers_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_dir', type=str,
                        help='Please input the path of the labelme json files.')
    parser.add_argument('--img_copy', type=bool, default=True,
                        help='If you want to copy and use an image, change it to True.')
    parser.add_argument('--val_size', type=tuple, nargs='?', default=None,
                        help='Please input the validation dataset size, for example (val_size, test_size), (0.1) or (0.2, 0.1)')
    parser.add_argument('--json_name', type=str, nargs='?', default=None,
                        help='If you put json name, it would convert only one json file to YOLO.')
    parser.add_argument('--s3_data', type=bool, default=False,
                        help='If you use data from s3, change to True')
    parser.add_argument('--s3_yaml', type=str, default=None,
                        help='If you use data from s3, input s3 config yaml file path')
    parser.add_argument('--json_db_table', type=str, default="p1_json_info",
                        help='Please input the json db table.')
    args = parser.parse_args(sys.argv[1:])

    convertor = Labelme2YOLO(args.json_dir, args.img_copy, args.s3_data, args.s3_yaml, args.json_db_table)
    if args.json_name is None:
        convertor.convert(val_size=args.val_size)
    else:
        convertor.convert_one(args.json_name)
