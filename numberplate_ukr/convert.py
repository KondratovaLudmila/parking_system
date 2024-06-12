import os
import shutil
from util import convert_dataset_to_yolo_format

PATH_TO_DATASET = 'C:/Users/vlad/PycharmProjects/pythonProject2/numberplate_ukr/dataset/autoriaNumberplateDataset-2021-03-01'
PATH_TO_RES_ANN = os.path.join(os.path.dirname(PATH_TO_DATASET), "./npdata/labels/{}")
PATH_TO_RES_IMAGES = os.path.join(os.path.dirname(PATH_TO_DATASET), "./npdata/images/{}")

PATH_TO_JSON = os.path.join(PATH_TO_DATASET, '{}/via_region_data.json')  # Updated path
PATH_TO_IMAGES = os.path.join(PATH_TO_DATASET, '{}/')

CLASSES = ['numberplate']
STATES = ["val", "train"]
EXIST_STRATEGY = "exist_ok"

for state in STATES:
    path_to_res_ann = PATH_TO_RES_ANN.format(state)
    path_to_res_images = PATH_TO_RES_IMAGES.format(state)

    if os.path.exists(path_to_res_ann) and os.path.exists(path_to_res_images) and EXIST_STRATEGY == "exist_ok":
        print("[INFO]", state, "data exists")
        continue
    if os.path.exists(path_to_res_ann) and os.path.exists(path_to_res_images) and EXIST_STRATEGY == "delete":
        shutil.rmtree(path_to_res_ann)
        shutil.rmtree(path_to_res_images)

    print("[INFO]", state, "data creating...")
    os.makedirs(path_to_res_ann, exist_ok=True)
    os.makedirs(path_to_res_images, exist_ok=True)

    path_to_json = PATH_TO_JSON.format(state)
    path_to_images = PATH_TO_IMAGES.format(state)

    convert_dataset_to_yolo_format(
        path_to_res_ann,
        path_to_res_images,
        path_to_images,
        path_to_json,
        debug=False,
        is_generate_image_rotation_variants=True
    )
