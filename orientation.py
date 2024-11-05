import cv2
import sys
import os

def orient_document(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Ошибка: изображение по пути '{image_path}' не найдено.")
        return

    _, thresh = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    angle = rect[2]

    if angle < -45:
        angle += 90
    elif angle > 45:
        angle -= 90

    if abs(angle) < 5:
        print("Документ уже ориентирован.")
        rotated_image = image
    else:
        if angle > 0:
            angle = 90 - angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    base_name = os.path.splitext(image_path)[0]
    rotated_image_path = f"{base_name}_rotated.png"
    cv2.imwrite(rotated_image_path, rotated_image)
    print(f"Изображение сохранено по пути: {rotated_image_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python script.py <путь_к_изображению>")
    else:
        orient_document(sys.argv[1])
