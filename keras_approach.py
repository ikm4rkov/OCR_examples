import keras_ocr # version 0.9.3
import matplotlib.pyplot as plt # version 3.9.2
import cv2 # 4.10.0.84

# Initialisation, required tensorflow 2.15.0 and subsequently python 3.9.13
pipeline = keras_ocr.pipeline.Pipeline()

# Loading image
image_path = 'cocacola_logo.png'  # CocaCola
image = keras_ocr.tools.read(image_path)

# Recognition
predictions = pipeline.recognize([image])[0]

# Drawing
for text, box in predictions:
    # Text spotting box
    cv2.polylines(image, [box.astype(int)], isClosed=True, color=(0, 255, 0), thickness=2)

    # Recognised text
    cv2.putText(image, text, (int(box[0][0]) + 10, int(box[0][1] + 50)), # Margins
                cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3) # Fonts

# Display
plt.imshow(image)
plt.axis('off')
plt.show()

# Found text output
for text, _ in predictions:
    print(f"Detected text: '{text}'")