import os
from abc import ABC, abstractmethod
import cv2
from ultralytics import YOLO
from .imageprocessing import normalize_img
import easyocr
import pathlib
import re

CURR_DIR = pathlib.Path(__file__).parent.resolve()


class Ocr(ABC):
    model = None

    @abstractmethod
    def read_text(self, image, allowed_chars=None):
        raise NotImplementedError
    
    def preprocess(self, image):
        #blurred = cv2.GaussianBlur(image, (5, 5), 0)
        alpha = 1.5
        beta = 0
        enhanced = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
        equalized = cv2.equalizeHist(gray)
        
        return equalized
    

    def postprocess(text: str | list) -> list:
        return text
    

class OcrEasy(Ocr):
    model = easyocr.Reader(['en', 'ru'])

    def top_teft_x(self, text):
        return text[0][0]

    def read_text(self, image, allowed_chars=None) -> list:
        text = []
        try:
            text = self.model.readtext(image, allowlist=allowed_chars, detail=1)
        except Exception as err:
            print(err)
        return text
    
    def postprocess(self, array: list) -> list:
        car_plate_pattern = r'[A-Z]{2}[0-9]{4}[A-Z]{2}'
        result = []
        
        array_to_str = ''
        array_sorted = sorted(array, key=self.top_teft_x)
        for (bbox, text, prob) in array_sorted:
            array_to_str += text
        
        array_to_str = array_to_str.replace(' ','')
        
        sub_str = []
        for i in range(0, len(array_to_str)-8 + 1):
            sub_str.append(array_to_str[i:8+i])
        
        for s in sub_str:
            region = s[0:2]
            number = s[2:6]
            seria = s[6:]

            region = region.replace('8', 'B').replace('0', 'O').replace('1', 'I').replace('4', 'A')
            number = number.replace('B', '8').replace('O', '0').replace('I', '1').replace('C', '6').replace('A', '4')
            seria = seria.replace('8', 'B').replace('0', 'O').replace('1', 'I').replace('4', 'A')
            
            is_match = re.search(car_plate_pattern, region+number+seria)
            if is_match:
                result.append(is_match[0])
        
        return result

class CarPlateReader:
    model_path=CURR_DIR.joinpath('runs','detect', 'train', 'weights','best.pt')
    allowed_chars = {'ua': 'ABCEHIKMOPTX0123456789'}
    detector = YOLO(model_path)
    image=None


    def __init__(self, recognizer: Ocr=OcrEasy() , output_dir=None, from_buffer=True) -> None:
        self.output_dir = output_dir
        self.from_buffer = from_buffer
        self.recognizer = recognizer

    def img_read(self, image_file: str | bytearray):
        if self.from_buffer:
            image = self.read_from_buffer(image_file)
        else:
            image = cv2.imread(image_file)

        return image
    

    def read_from_buffer(self, image_file: bytearray):
        image = np.asarray(image_file, dtype="uint8") 
        image = cv2.imdecode(image, cv2.IMREAD_COLOR) 

        return image
    

    def detect(self, delta=15):
        car_plates = self.detector(self.image)[0]
        car_plate_croped = []
        for idx, car_plate in enumerate(car_plates.boxes.data.tolist()):
            x1, y1, x2, y2, score, class_id = car_plate
            # Вирізати номерний знак
            car_plate_croped.append(self.image[int(y1-delta):int(y2+delta), int(x1-delta): int(x2+delta), :])

        return car_plate_croped
    

    def recognize(self, car_plate):
        return self.recognizer.read_text(car_plate, self.allowed_chars)
    
    
    def img_process(self, image_file) -> list[str]:
        self.image = self.img_read(image_file)
        
        if self.image is None:
            print(f"file was not read!")
            return []
        
        plates = self.detect()
        if not plates:
            print('Was not detected')
            plates.append(self.image)

        text = []
        for plate in plates:
            #plate = self.recognizer.preprocess(plate)
            #cv2.imwrite('plate.jpg', plate)
            result = self.recognizer.read_text(plate, allowed_chars=self.allowed_chars['ua'])
            text.extend(self.recognizer.postprocess(result))
        
        return text

from imageprocessing import normalize_img


# Функція для виявлення та вирізання номерних знаків з зображення
def detect_and_crop_license_plates(image_path, output_dir, model_path=CURR_DIR.joinpath('runs','detect', 'train', 'weights','best.pt')):
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
#detect_and_crop_license_plates('car9.jpg', 'output')

