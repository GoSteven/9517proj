#include <opencv/cv.h>

using namespace cv;

struct Panograph {

    Panograph(const Mat &base);

    void add(const Mat& image, const vector<Point2f>& panoPoints, const vector<Point2f>& imgPoints);

    Mat pano;
    Mat mask;

};

void GetMachingPair(const char* img1, const char* img2, vector<int>& p1x, vector<int>& p1y, vector<int>& p2x, vector<int>& p2y);

