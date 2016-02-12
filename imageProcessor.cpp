/* Author: Brian Westerman
 * 2/11/16
 * Computer Vision
 * Project 1
 * 
 * Compile command:
 * clang++ -o proj -I /opt/local/include imageProcessor.cpp -L /opt/local/lib -lopencv_core -lopencv_highgui 
 */

#include <iostream>
#include <string>
#include <vector>
#include "opencv2/opencv.hpp"

using namespace std;
using namespace cv;

// Takes in an image, increases the intensity of the blue channel according to the 
// adjust param, and returns the adjusted image data
Mat blueify(Mat src, Mat dst, unsigned char adjust) {

	// Copy input matrix data to the output matrix
	src.copyTo(dst);
	
	// Loop through all pixels of the image
	for (int i = 0; i < dst.cols; i++) {
		for (int j = 0; j < dst.rows; j++) {
			// Grab the current pixel's blue channel and increase it by the adjust
			// parameter, capped at 255
			unsigned char *blue;
			blue = &dst.at<Vec3b>(j, i)[0];
			*blue <= 255 - adjust ? *blue += adjust : *blue = 255;
		}
	}
	
	cout << "Blue channel intensified" << endl;
	return dst;
}

// Takes in an image and returns its mirror image
Mat mirrorify(Mat src, Mat dst) {
	
	// Apply the flip method about the y axis (1)
	flip(src, dst, 1);
	
	cout << "Mirror image created" << endl;
	return dst;
}

// Takes in an image and returns a binarized image depending on bThresh, gThresh, and rThresh
Mat thresholdify(Mat src, Mat dst, double bThresh, double gThresh, double rThresh) {
	
	// Separate the image into BGR channels for the input matrix and the output matrix
	vector<Mat> srcChannels;
	vector<Mat> dstChannels;
	split(src, srcChannels);
	split(dst, dstChannels);

	
	// Run threshold method on each channel according to bThresh, gThresh, and rThresh
	threshold(srcChannels[0], dstChannels[0], bThresh, 255, THRESH_BINARY);
	threshold(srcChannels[1], dstChannels[1], gThresh, 255, THRESH_BINARY_INV);
	threshold(srcChannels[2], dstChannels[2], rThresh, 255, THRESH_BINARY_INV);
	
	// Merge channels back into an RGB image
	merge(dstChannels, dst);
	
	cout << "Image turned into binary" << endl;
	return dst;
}

// Takes in an image, runs a Gaussian blur algorithm on it with kernel size (size, size),
// and returns the resulting image
Mat blurify(Mat src, Mat dst, double size) {
	
	// Apply the GaussianBlur method with a kernel size (size, size), sigmaX = 0, sigmaY = 0
	GaussianBlur(src, dst, Size(size, size), 0, 0, BORDER_DEFAULT);
	
	cout << "Blur algorithm applied" << endl;
	return dst;
}

int main(int argc, char** argv) {
	
	// Make sure there is an image being passed in
    if (argc != 2) {
    	cout << "Usage: imageProcessor ImageToLoadAndDisplay" << endl;
    	return -1;
    }
    
    // Get image name: ../data/obamafunny.jpg
    string filename;
    filename = argv[1];
	
	// Read in image data
    Mat src, blue, mirror, threshold, blur;
    src = imread(filename, CV_LOAD_IMAGE_COLOR);

	// Make sure image data exists
    if (!src.data) {
    	cout << "No image data" << endl;
    	return -1;
    }
    
    // Display the image in a window
    namedWindow("Image", WINDOW_AUTOSIZE);
    imshow("Image", src);
    
    // Hold the program until the user presses a key, testing for 'b', 'm', 't', or 'r'
    while (true) {
    	char c = waitKey();
    	// If the user hits the 'b' key, apply the blueify function
    	if (c == 'b') {
    		Mat blueResult = blueify(src, src, 50);
    		imshow("Image", blueResult);
    		continue;
    	// If the user hits the 'm' key, apply the mirrorify function
    	} else if (c == 'm') {
    		Mat mirrorResult = mirrorify(src, src);
    		imshow("Image", mirrorResult);
    		continue;
    	// If the user hits the 't' key, apply the thresholdify function
    	} else if (c == 't') {
    		Mat thresholdResult = thresholdify(src, src, 60, 255, 255);
    		imshow("Image", thresholdResult);
    		continue;
    	// If the user hits the 'r' key, apply the blurify function
    	} else if (c == 'r') {
    		Mat blurResult = blurify(src, src, 5);
    		imshow("Image", blurResult);
    		continue;
    	// If the user hits any other keys, break out of the loop and terminate the program
    	} else {
    		break;
    	}
    }
    
    // Terminate the program
    destroyWindow("Blueify");
    destroyWindow("Mirrorify");
    destroyWindow("Thresholdify");
    destroyWindow("Blurify");
    cout << "Terminating" << endl;
    return 0;
}
