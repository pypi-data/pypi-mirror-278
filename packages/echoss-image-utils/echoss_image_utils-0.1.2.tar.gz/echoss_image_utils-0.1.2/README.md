# **labelme2yolo**

## 소개

labelme를 이용하여 어노테이션 작업을 한 josn파일을 yolo학습이 가능하도록 txt파일로 변환해주는 기능

## 사용법
Commad line
```
    python labelme2yolo.py --json_dir=<s3데이터를 사용한다면 None, 아니면 json파일들이 있는 폴더 경로> --s3_data=<s3데이터를 사용하는지 아닌지에대한 bool값>\
    --s3_yaml=<s3접속 정보가 담긴 .yaml파일의 경로>  --json_db_table=<사용하려는 json 데이터 베이스의 테이블 명>
```
--s3_data에 입력되는 .yaml파일의 양식 및 필수 키 값
```
    # labelme2yolo config
    db_region: 'kr_local'
    image_data_path: images/bb_seg_data/
    json_data_path: json_labels/bb_seg_data/
    yolo_data_path: yolo_labels/bb_seg_data/
    detect_save_path: 'results/'

    # s3 config
    s3: True  # True or False

    bucket: 'bucket-name'
    endpoint_url: 'https://kr.object.ncloudstorage.com'
    region_name: 'kr-standard'
    access_key: 'access-key'
    access_token: 'secret-token-key'
```

## 사용 예시
.59 서버에서 작동 시
```
    cd jupyter_notebooks/image_utils
    
    python labelme2yolo.py --json_dir=None --s3_data=True --s3_yaml=../data/45_abalone_data/yolo_data/ai_solution_dataset_test.yaml --json_db_table='p1_json_info'

```


# **img_dataset_split**

## 소개
어노테이션 작업이 완료 된 json 혹은 txt 파일을 기준으로 Train, Validation, Test를 원하는 비율에 맞게 나누어서 목록을 생성해주는 기능

## 사용법
Commad line
```
    python img_dataset_split.py --yaml_file_path=<s3접속 정보가 담긴 .yaml파일의 경로> --ratio=<train,val,test 비율 기입 예) 8,1,1 > \
    --db_config_file_path=<db 접속정보가 담긴 config파일 경로> --save_path=<저장하고 싶은 경로 및 이름> --random_seed=55 \
    --json_db_table=<json data의 정보가 있는 테이블 명> --image_db_table=<image data의 정보가 있는 테이블 명> --use_s3=<s3데이터를 사용하는지 아닌지에대한 bool값>
```

--yaml_file_path 입력되는 .yaml파일의 양식 및 필수 키 값
```
    # labelme2yolo config
    db_region: 'kr_local'

    # s3 config
    s3: True  # True or False

    bucket: 'bucket-name'
    endpoint_url: 'https://kr.object.ncloudstorage.com'
    region_name: 'kr-standard'
    access_key: 'access-key'
    access_token: 'secret-token-key'
```
```

## 사용 예시
.59 서버에서 작동 시
```
    cd jupyter_notebooks/image_utils
    
    python img_dataset_split.py --yaml_file_path=../data/45_abalone_data/yolo_data/ai_solution_dataset_test.yaml --ratio=8,1,1 \
    --db_config_file_path=../echoss_query/config/config.yaml --save_path=split_dataset_list.json --random_seed=55 \
    --json_db_table=p1_json_info --image_db_table=p1_image_info --use_s3=True
```

내부 함수를 직접사용하고자 할 때
```
    sd = SplitDataset(<solution config yaml file path>, (8,1,1), <db config yaml file path>, <json data db table>, <image data db table>, True or False)
    
    sd.save_data_split_json(<save file path>, <random seed : int>)
```