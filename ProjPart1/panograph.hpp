#include <opencv/cv.h>

using namespace cv;

struct Panograph {

    Panograph(const Mat &base);

    void add(const Mat& image, const vector<Point2f>& panoPoints, const vector<Point2f>& imgPoints);

    Mat pano;
    Mat mask;

};

