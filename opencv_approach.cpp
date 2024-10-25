#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs.hpp>
#include <iostream>
#include <fstream>
#include <vector>
#include <opencv2/dnn/dnn.hpp>
using namespace cv;
using namespace cv::dnn;
// source https://docs.opencv.org/4.x/d4/d43/tutorial_dnn_text_spotting.html
// requires OpenCV, tested via OpenCV4
int main() {
    // Load a cropped text line image
    int rgb = IMREAD_COLOR; // This should be changed according to the model input requirement.
    Mat image = imread("google_logo.png", rgb);

    // Check if the image was loaded successfully
    if (image.empty()) {
        std::cerr << "Error: Could not open or find the image!" << std::endl;
        return -1;
    }

    // Load model weights
    TextRecognitionModel model("crnn_cs.onnx");

    // The decoding method
    model.setDecodeType("CTC-greedy");

    // Load vocabulary
    std::ifstream vocFile("alphabet_94.txt");
    if (!vocFile.is_open()) {
        std::cerr << "Error: Could not open vocabulary file!" << std::endl;
        return -1;
    }

    std::string vocLine;
    std::vector<std::string> vocabulary;
    while (std::getline(vocFile, vocLine)) {
        vocabulary.push_back(vocLine);
    }
    model.setVocabulary(vocabulary);

    // Normalization parameters
    double scale = 1.0 / 511.5;
    Scalar mean = Scalar(511.5, 511.5, 511.5);

    // The input shape
    Size inputSize = Size(100, 32);
    model.setInputParams(scale, inputSize, mean);

    // Recognize the text
    std::string recognitionResult = model.recognize(image);
    std::cout << "'" << recognitionResult << "'" << std::endl;

    return 0;
}
