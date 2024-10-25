import easyocr  # version 1.7.2
import cv2  # version 3.9.2
import matplotlib.pyplot as plt  # 4.10.0.84

# Initialization for English
reader = easyocr.Reader(['en'])

# Image loading
image_path = 'site_header.png'
image = cv2.imread(image_path)

# Text recognition
results = reader.readtext(image)

# Drawing the image with recognized text
for (bbox, text, prob) in results:
    print(f"Detected text: {text} (Confidence: {prob:.2f})")  # Printing to console
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))

    # Spotting text box
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    # Putting the recognized text on the image
    text_position = (top_left[0], top_left[1] - 10)
    cv2.putText(image, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

# Displaying the image
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()