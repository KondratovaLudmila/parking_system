import os

import cv2
from ultralytics import YOLO

from imageprocessing import normalize_img


# Функція для виявлення та вирізання номерних знаків з зображення
def detect_and_crop_license_plates(image_path, output_dir, model_path='runs/detect/train/weights/best.pt'):
    # Створити вихідний каталог, якщо він не існує
    os.makedirs(output_dir, exist_ok=True)
    # Завантажити модель для виявлення номерних знаків
    license_plate_detector = YOLO(model_path)

    # Зчитати зображення
    image = cv2.imread(image_path)
    if image is None:
        print(f"Не вдалося завантажити зображення {image_path}")
        return

    # Виявити номерні знаки
    license_plates = license_plate_detector(image)[0]
    license_plate_crop = None
    # Вирізати та зберегти номерні знаки
    for idx, license_plate in enumerate(license_plates.boxes.data.tolist()):
        x1, y1, x2, y2, score, class_id = license_plate
        # Вирізати номерний знак
        license_plate_crop = normalize_img(image[int(y1):int(y2), int(x1): int(x2), :])
        output_path = os.path.join(output_dir, f"license_plate_{idx}.png")
        cv2.imwrite(output_path, license_plate_crop)
        break

    return license_plate_crop


# Викликати функцію з прикладом використання
detect_and_crop_license_plates('./sddefault.jpg', './cropped_license_plates')
