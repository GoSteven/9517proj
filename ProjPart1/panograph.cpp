#include <cmath>
#include "panograph.hpp"

#include <cstdio>


Panograph::Panograph(const Mat &base) : pano(base.clone()), mask(base.rows, base.cols, DataType<unsigned char>::type, Scalar(255))
{
}

void Panograph::add(const Mat& image, const vector<Point2f>& panoPoints, const vector<Point2f>& imgPoints)
{
    //adjust the parameter on the next line
    Mat src(1, imgPoints.size(), DataType<Vec<float, 2> >::type);
    Mat dst(1, panoPoints.size(), DataType<Vec<float, 2> >::type);
    for(unsigned int i = 0; i < imgPoints.size(); i++) {
        src(Rect(i, 0, 1, 1)) = Scalar(imgPoints[i].x, imgPoints[i].y);
    }
    for(unsigned int i = 0; i < panoPoints.size(); i++) {
        dst(Rect(i, 0, 1, 1)) = Scalar(panoPoints[i].x, panoPoints[i].y);
    }
    Mat H = findHomography(src, dst, CV_RANSAC, 3);

    //Get the four corners of the new image
    Mat cornerList(3, 4, DataType<double>::type, Scalar(1));
    cornerList(Rect(0,0,1,2)) = Scalar(0);
    cornerList(Rect(1,0,1,1)) = Scalar(image.cols);
    cornerList(Rect(1,1,1,1)) = Scalar(0);
    cornerList(Rect(2,0,1,1)) = Scalar(0);
    cornerList(Rect(2,1,1,1)) = Scalar(image.rows);
    cornerList(Rect(3,0,1,1)) = Scalar(image.cols);
    cornerList(Rect(3,1,1,1)) = Scalar(image.rows);

    //Translate according to H
    cornerList = H * cornerList;

    //Find bounding box
    double minx, miny, maxx, maxy;
    for(int i = 0; i < 4; ++i) {
        double x = cornerList.at<double>(0,i) / cornerList.at<double>(2,i);
        double y = cornerList.at<double>(1,i) / cornerList.at<double>(2,i);
        if (i == 0) {
            minx = maxx = x;
            miny = maxy = x;
        } else {
            if (x < minx) minx = x;
            if (y < miny) miny = y;
            if (x > maxx) maxx = x;
            if (y > maxy) maxy = y;
        }
    }

    //filter out transformations that are obviously broken
    if (maxx - minx > pano.cols * 20)
        return;
    if (maxy - miny > pano.rows * 20)
        return;
    minx = floor(minx);
    miny = floor(miny);
    maxx = ceil(maxx);
    maxy = ceil(maxy);
    if (minx > 0) minx = 0;
    if (miny > 0) miny = 0;
    if (maxx < pano.cols) maxx = pano.cols;
    if (maxy < pano.rows) maxy = pano.rows;
    int width = maxx - minx, height = maxy - miny;

    //adding this image doesn't enlarge the panograph, discard
    if (width == pano.cols && height == pano.rows)
        return;

    //Enlarge panograph frame
    Mat temp = pano;
    pano = Mat(height, width, temp.type(), Scalar(0));
    Mat subMat = pano(Rect(-minx, -miny, temp.cols, temp.rows));
    temp.copyTo(subMat);

    //Enlarge mask
    temp = mask;
    mask = Mat(height, width, temp.type(), Scalar(0));
    subMat = mask(Rect(-minx, -miny, temp.cols, temp.rows));
    temp.copyTo(subMat);
    
    //adjust the H matrix to account for the co-ordinate system change
    //that we just performed on the panograph
    //row1 -= minx * row3
    //row2 -= miny * row3
    for(int i = 0; i < 3; i++) {
        H.at<double>(0, i) -= minx * H.at<double>(2, i);
        H.at<double>(1, i) -= miny * H.at<double>(2, i);
    }

    //add the image to the panograph
    warpPerspective(image, pano, H, Size(pano.cols, pano.rows), INTER_LINEAR, BORDER_TRANSPARENT);

    //Update the mask
    temp = Mat(image.rows, image.cols, mask.type(), Scalar(255));
    warpPerspective(temp, mask, H, Size(pano.cols, pano.rows), INTER_LINEAR, BORDER_TRANSPARENT);
}



#if 1

//Simple test
#include <opencv/highgui.h>
int main(int argc, char *argv[]) {
    Mat h1 = imread("hydepark1.jpg");
    Mat h2 = imread("hydepark2.jpg");
    assert(h1.data);
    assert(h2.data);
    vector<Point2f> pts1, pts2;
    pts1.push_back(Point2f(218, 106));
    pts1.push_back(Point2f(421, 406));
    pts1.push_back(Point2f(70, 405));
    pts1.push_back(Point2f(143, 439));
    pts2.push_back(Point2f(118, 22));
    pts2.push_back(Point2f(282, 260));
    pts2.push_back(Point2f(0, 265));
    pts2.push_back(Point2f(56, 292));


    Panograph p(h1);
    p.add(h2, pts1, pts2);
    imshow("pano", p.pano);
    imshow("mask", p.mask);
    waitKey();
    return 0;
}
#endif
