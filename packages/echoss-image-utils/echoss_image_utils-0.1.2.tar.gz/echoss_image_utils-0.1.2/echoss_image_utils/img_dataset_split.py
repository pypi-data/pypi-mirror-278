# Split the dataset in the bucket and output it to a json file
import os
import sys
import json
import yaml
import random
import argparse
import numpy as np
from tqdm import tqdm
from echoss_s3handler import s3_handler
from echoss_query.query import echoss_query

import logging
from .echoss_logger import get_logger, set_logger_level

logger = get_logger("echoss_image_utils")

class SplitDataset():
    def __init__(self, config_file_path, ratio, db_config_path, json_db_table, image_db_table, use_s3=True):
        self.config_file_path = config_file_path
        self.ratio = ratio
        self.db_config_path = db_config_path
        self.json_db_table = json_db_table
        self.image_db_table = image_db_table
        with open(self.config_file_path) as f:
            config_file = yaml.load(f, Loader=yaml.SafeLoader)  # data dict
        self.config_file = config_file
        self.use_s3 = use_s3
        if self.use_s3:
            self.s3handler = s3_handler.S3ResourceHandler(self.config_file)

            # 경로를 input으로 받을지 확인 뒤 수정할수도
            # DB관련 함수 config파일
            with open(self.db_config_path, 'r') as file:
                self.db_yaml_info = yaml.load(file, Loader=yaml.FullLoader)
            self.mysql = echoss_query.MysqlQuery(self.db_yaml_info[self.config_file['db_region']])
            json_db_list = self.mysql.select_list(f'SELECT prefix, file_name FROM {self.json_db_table}')
            self.object_lists = [json_db_list[idx - 1] + json_db_list[idx] for idx, x in enumerate(json_db_list) if idx % 2 == 1]

            # Use s3 get object list
            # print("Make s3 object lists...")
            # self.object_lists = self.s3handler.get_object_list(self.config_file['bucket'], self.config_file['json_data_path'])
            # print("Finish s3 object lists...")

    def save_data_split_json(self, save_path="split_dataset_list.json", random_seed=55):
        """
        :param ratio: (8, 1, 1) | (7, 2, 1)의 꼴로 입력
        :param save_path: split된 데이터 목록을 json으로 저장하기 위한 경로 입력
        :return: s3를 이용한다면 설정된 경로에 업로드가 되며, s3를 이용하지 않으면 로컬에 json 저장됨
        """
        ## 아래의 sql query는 수정할 필요가 있음
        img_path_list = self.mysql.select_list(f'SELECT prefix, file_name FROM {self.image_db_table}')
        img_paths = [img_path_list[idx - 1] + img_path_list[idx] for idx, x in enumerate(img_path_list) if idx % 2 == 1]
        label_paths = self.object_lists

        class_dict = self.count_class()
        class_img_path, class_label_path = self.class_split_dataset(img_paths, label_paths)
        tot_dict = dict()
        tot_image = {'train': [], 'val': [], 'test': []}
        tot_label = {'train': [], 'val': [], 'test': []}
        for key in class_dict.keys():
            logger.log(level=logging.DEBUG,msg=' ')
            logger.log(level=logging.DEBUG,msg=f'***** {key} *****')
            X_train, y_train, X_val, y_val, X_test, y_test = self.train_val_test_split(class_img_path[key],
                                                                                     class_label_path[key],
                                                                                     self.ratio, random_seed=random_seed)
            tot_image['train'] += list(X_train)
            tot_image['val'] += list(X_val)
            tot_image['test'] += list(X_test)
            tot_label['train'] += list(y_train)
            tot_label['val'] += list(y_val)
            tot_label['test'] += list(y_test)

        tot_dict['images'] = tot_image
        tot_dict['labels'] = tot_label

        if self.use_s3:
            self.s3handler.put_object(tot_dict, save_path, self.config_file['bucket'])
        else:
            with open(save_path, 'w') as f:
                json.dump(tot_dict, f, indent=4)
        with open(self.config_file_path, 'a+') as yaml_file:
            yaml_file.write("\ndataset_split_path: '%s'\n" % save_path)

    def train_val_test_split(self, img_paths, label_paths, ratio, random_seed=None):
        """
            ratio = (train, val, test) 꼴로 입력, 예) (8, 1, 1)
             - 전체 데이터에 비율을 구하는데 소수점은 버림이 됨 인지하고 있어야 함
                -> 버림이 되는 문제와 모든 데이터를 사용하기 위해서 test dataset은 train, val데이터를 구하고 남은 모든 데이터를 넣음

            random_seed=None이면 shuffle을 하지 않겠다는 뜻 이와 반대는 정수를 입력하면 됨, 예) random_seed=55
            """
        img_dir = os.path.dirname(img_paths[0])
        label_dir = os.path.dirname(label_paths[0])

        img_paths.sort()  # 혹시 몰라서 label_paths와 순서가 일치되도록 이름 순 정렬
        label_paths.sort()  # 혹시 몰라서 img_paths와 순서가 일치되도록 이름 순 정렬

        if (ratio[0] % 1 == 0) & (ratio[2] % 1 == 0) & (ratio[2] % 1 == 0):
            train_ratio = ratio[0] * 0.1
            val_ratio = ratio[1] * 0.1
            test_ratio = ratio[2] * 0.1
        else:
            train_ratio = ratio[0]
            val_ratio = ratio[1]
            test_ratio = ratio[2]

        if (os.path.basename(img_paths[0]).split(".")[0] == os.path.basename(label_paths[0]).split(".")[0]) and \
                (os.path.basename(img_paths[-1]).split(".")[0] == os.path.basename(label_paths[-1]).split(".")[
                    0]):  # 이미지 파일과 라벨 파일의 매칭 상태를 대략적으로 확인
            train_num = int(len(img_paths) * train_ratio)
            val_num = int(len(img_paths) * val_ratio)
            test_num = int(len(img_paths) - train_num - val_num)

            X = np.array(img_paths)
            y = np.array(label_paths)
            if random_seed != None:
                np.random.seed(random_seed)
                shuffled = np.random.permutation(X.shape[0])
                X = X[shuffled]
                y = y[shuffled]
                X_train = X[:train_num]
                y_train = y[:train_num]
                X_val = X[train_num:train_num + val_num]
                y_val = y[train_num:train_num + val_num]
                X_test = X[train_num + val_num:]
                y_test = y[train_num + val_num:]
            else:
                X_train = X[:train_num]
                y_train = y[:train_num]
                X_val = X[train_num:train_num + val_num]
                y_val = y[train_num:train_num + val_num]
                X_test = X[train_num + val_num:]
                y_test = y[train_num + val_num:]
            for x, y, x_name, y_name in zip([X_train, X_val, X_test], [y_train, y_val, y_test],
                                            ["X_train", "X_val", "X_test"], ["y_train", "y_val", "y_test"]):
                logger.log(level=logging.DEBUG,msg="=" * 30)
                logger.log(level=logging.DEBUG,msg=f"{x_name} : {len(x)} | {y_name} : {len(y)}")
            logger.log(level=logging.DEBUG,msg="=" * 30)
            return X_train, y_train, X_val, y_val, X_test, y_test

        else:
            print("image 파일과 label 파일의 매칭을 다시 한번 확인해주세요.")

    def class_split_dataset(self, img_paths, label_paths):
        """
        img_paths와 label_paths는 서로 매칭이 된 상태여야 한다.

        class의 개수가 불균형 한 상황일때에 class별로 그룹을 나누어 분류하기 위함

        class의 개수가 적은 것부터 분류를 한다.
        """
        # img_paths와 label_paths는 서로 매칭이 된 상태여야 한다.를 만족하기 위하여
        # image데이터는 기본적으로 항상 label의 데이터 개수보다 같거나 많음 아래를 통하여 label파일이 존재하는 이미지만 list로 만든다.
        img_paths = [x for x in img_paths if os.path.basename(x).split(".")[0] in [os.path.basename(x).split(".")[0] for x in label_paths]]

        img_paths.sort()  # 혹시 몰라서 label_paths와 순서가 일치되도록 이름 순 정렬
        label_paths.sort()  # 혹시 몰라서 img_paths와 순서가 일치되도록 이름 순 정렬

        labels_cnt_dict = self.count_class(label_paths, print_prog=True)
        labels_cnt_dict = sorted(labels_cnt_dict.items(), key=lambda x: x[1])  # label count한 dictionary를 value기준으로 정렬
        # print(labels_cnt_dict)
        labels_list = [x[0] for x in labels_cnt_dict]
        # print(labels_list)

        labels = []
        class_label_path = dict()
        class_image_path = dict()
        if (os.path.basename(img_paths[0]).split(".")[0] == os.path.basename(label_paths[0]).split(".")[0]) and \
                (os.path.basename(img_paths[-1]).split(".")[0] == os.path.basename(label_paths[-1]).split(".")[
                    0]):  # 이미지 파일과 라벨 파일의 매칭 상태를 대략적으로 확인
            for image_path, label_path in zip(img_paths, label_paths):  # 이 함수를 돌리기 전 모든 전처리가 끝나다는 전제하 - 이미지와 라벨링 파일의 매칭이 끝났다고 가정
                if not self.use_s3:
                    with open(label_path, 'r') as f:
                        json_data = json.load(f)
                else:
                    f = self.s3handler.read_file(self.config_file['bucket'], label_path)
                    f.seek(0)
                    dict_ = f.read().decode()
                    del (f)
                    json_data = json.loads(dict_)
                for i, _ in enumerate(json_data['shapes']):
                    label = json_data['shapes'][i]['label']
                    labels.append(label)  # 현재 label파일의 label을 하나의 list로 만든다.
                for label in labels_list:
                    if label in labels:  # class의 개수가 적은 순서로 확인한다.
                        if label in class_label_path:  # label과 일치하는 key가 있다면 value인 list에 append
                            class_label_path[label].append(label_path)
                            class_image_path[label].append(image_path)
                        else:  # label과 일치하는 key가 없다면 value에 list로 입력
                            class_label_path[label] = [label_path]
                            class_image_path[label] = [image_path]
                        break  # class의 개수가 적은 부분에 걸렸다면 break를 통해 현재 loop를 멈추고 다음 loop를 진행한다.
                labels = []
            #         print("image : ", class_image_path)
            #         print("label : ", class_label_path)
            return class_image_path, class_label_path
        else:
            print("image 파일과 label 파일의 매칭을 다시 한번 확인해주세요.")

    def count_class(self, label_paths: list or str = None, print_prog=False):
        """
        The label_paths is formatted as json.

        If the files are local, input the list obtained using glob,
        and if the data is s3, input object_lists.


        :param label_paths: Json label file path
        :return: Dict
        """
        if label_paths == None:
            label_paths = self.object_lists
        labels = []
        labels_cnt_dict = dict()
        extension = os.path.basename(label_paths[0]).split(".")[-1]
        try:
            if extension == "json":
                for label_path in tqdm(label_paths):
                    if not self.use_s3:
                        with open(label_path, 'r') as f:
                            json_data = json.load(f)
                    else:
                        f = self.s3handler.read_file(self.config_file['bucket'], label_path)
                        f.seek(0)
                        dict_ = f.read().decode()
                        del(f)
                        json_data = json.loads(dict_)
                    for i, _ in enumerate(json_data['shapes']):
                        label = json_data['shapes'][i]['label']
                        labels.append(label)
                labels_arr = np.array(labels)
                unique, counts = np.unique(labels_arr, return_counts=True)
                for uniq, count in zip(unique, counts):
                    labels_cnt_dict[uniq] = count
                # result = np.column_stack((unique, counts))
                if print_prog:
                    logger.log(level=logging.DEBUG,msg=f"전체 label 개수 : {len(labels)}")
                    logger.log(level=logging.DEBUG,msg=labels_cnt_dict)

                return labels_cnt_dict
            else:
                raise Exception("To use json files, you must enter the json format files.")
        except Exception as e:
            print(e)
def ratio2tuple(ratio):
    ratio_str = ratio
    ratio_list = []
    ratio_list.append(int(ratio_str[0]))
    ratio_list.append(int(ratio_str[2]))
    ratio_list.append(int(ratio_str[4]))
    ratio_tuple = tuple(ratio_list)
    return ratio_tuple

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--yaml_file_path', type=str,
                        help='Please input the path of the yaml file.')
    parser.add_argument('--ratio', type=tuple, default=(8, 1, 1),
                        help='Input split ratio, train, val, test / ex. 8,1,1 or 7,2,1'
                             'test가 0의 값을 갖지 않게 설정 해야 합니다.')
    parser.add_argument('--db_config_file_path', type=str,
                        help='Please input the path of the db config file.')
    parser.add_argument('--save_path', type=str, default="split_dataset_list.json",
                        help='Please input the path.')
    parser.add_argument('--json_db_table', type=str, default="p1_json_info",
                        help='Please input the json db table.')
    parser.add_argument('--image_db_table', type=str, default="p1_image_info",
                        help='Please input the image db table.')
    parser.add_argument('--random_seed', type=int, default=None,
                        help='Input random seed')
    parser.add_argument('--use_s3', type=bool, default=True,
                        help='If you use not data from s3, change to False')
    args = parser.parse_args(sys.argv[1:])

    data_dict_path = args.yaml_file_path
    ratio = ratio2tuple(args.ratio)
    sd = SplitDataset(data_dict_path, ratio, args.db_config_file_path, args.json_db_table, args.image_db_table, args.use_s3)

    sd.save_data_split_json(save_path=args.save_path, random_seed=args.random_seed)
    # with open(args.db_config_file_path, 'r') as file:
    #     db_yaml_info = yaml.load(file, Loader=yaml.FullLoader)
    # mysql = echoss_query.MysqlQuery(db_yaml_info['kr_local'])
    # img_paths = mysql.select_list('SELECT prefix, file_name FROM p1_image_info')
    # label_paths = mysql.select_list('SELECT prefix, file_name FROM p1_json_info')
    # print([img_paths[idx-1] + img_paths[idx] for idx, x in enumerate(img_paths) if idx % 2 == 1])
    # print([label_paths[idx-1] + label_paths[idx] for idx, x in enumerate(label_paths) if idx % 2 == 1])
    # img_paths = mysql.select_list('SELECT FULL_PATH FROM IMAGE_INFO')
    # label_paths = mysql.select_list('SELECT FULL_PATH FROM JSON_INFO')

