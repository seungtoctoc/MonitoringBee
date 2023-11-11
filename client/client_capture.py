import cv2
import time
from datetime import datetime
from numpy import numpy as np
from tensorflow.keras.models import load_model

IMAGE_HEIGHT = 480
IMAGE_WIDTH = 640

def get_number_of_bee_and_contour_image(predict_image):
    pass

if __name__ == '__main__':
    time.sleep(5)
        
    autoencoder = load_model('/home/stt-pi/autoencoder_32.h5')
    cap = cv2.VideoCapture(0)
    prev_number_of_bee = -1
    test_save = False
    
    while True:
        ret, original_image = cap.read()
        cropped_image = original_image[IMAGE_HEIGHT//2:, :]
        
        predict_image = autoencoder.predict(np.expand_dims(np.array(original_image) / 255, axis=0))
        predict_image = (predict_image[0] * 255).astype(np.uint8)
    
        number_of_bee, result_image = get_number_of_bee_and_contour_image(predict_image)
        
        # 첫 프레임이 아니고 
        # 1. 이전 프레임 속 벌의 마릿수와 현재 프레임 속 벌의 마릿수가 다른 경우
        # 2. 한번도 저장되지 않은 경우
        # 이미지들과 마릿수를 upload_list에 append하고 저장
        if prev_number_of_bee != -1:
            if prev_number_of_bee != number_of_bee or test_save == False:
                upload_list = []
                
                upload_list.append(prev_original_image)
                upload_list.append(prev_result_image)
                
                upload_list.append(original_image)
                upload_list.append(result_image)
                
                upload_list.append(prev_number_of_bee)
                upload_list.append(number_of_bee)
                
                current_time = datetime.now().strftime("%m%d%H%M%S")
                file_name = f"{current_time}.npy"
                file_path = f"/home/stt-pi/upload/{file_name}"
        
                np.save(file_path, upload_list)
                
                print("[capture] save file", current_time+".npy")
                
                test_save = True

        prev_original_image = original_image
        prev_result_image = result_image
        prev_number_of_bee = number_of_bee
        
        time.sleep(0.05)

def get_number_of_bee_and_contour_image(predict_image):
    previous_objects = []
    next_object_number = 1
    result_image = predict_image

    lower_red = np.array([0, 0, 100])
    upper_red = np.array([100, 100, 255])
    mask = cv2.inRange(result_image, lower_red, upper_red)
    result_image[mask > 0] = [255, 255, 255]

    gray = cv2.cvtColor(result_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=100, threshold2=10)
    _, binary = cv2.threshold(edges, 128, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    current_objects = []
    object_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if area >= 20.0:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(predict_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            object_count += 1

            center_x = x + w // 2
            center_y = y + h // 2
            current_objects.append((center_x, center_y))
            matched = False
            min_distance = float("inf")
            closest_matched_object = None

            for j, (prev_x, prev_y, prev_object_number) in enumerate(previous_objects):
                distance = np.linalg.norm(
                    np.array([center_x, center_y]) - np.array([prev_x, prev_y])
                )
                if distance < 30:
                    matched = True
                    if distance < min_distance:
                        min_distance = distance
                        closest_matched_object = (prev_x, prev_y, prev_object_number)

            if matched:
                object_number = closest_matched_object[2]
            else:
                object_number = next_object_number
                next_object_number += 1
            previous_objects.append((center_x, center_y, object_number))

            cv2.putText(
                predict_image,
                str(object_number),
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2,
            )
    bee = object_count
    previous_objects = current_objects

    return bee, result_image