#! /usr/bin/env python
import cv2.cv as cv

class panograph:
    def __init__(self):
        self.imgName_1 = "1.jpg"
        self.imgName_2 = "2.jpg"
        
        in1 = cv.LoadImageM("hydepark1.jpg")
        in2 = cv.LoadImageM("hydepark2.jpg")
        #dst = cv.CreateMat(in1.rows, in1.cols, cv.CV_8UC3)
        persp = cv.CreateMat(3, 3, cv.CV_32FC1)
        src = [
            (218, 106),
            (421, 406),
            (70, 405),
            (143, 439)]
        dst = [
            (118, 22),
            (282, 260),
            (0, 265),
            (56, 292)]
        cv.GetPerspectiveTransform(src, dst, persp)

        cv.WarpPerspective(in1, in2, persp, 0)
        cv.ShowImage("test", in2)
#good features:
    def findFeature(self):
        imgName_1 = "1.jpg"
        imgName_2 = "2.jpg"
        imgName_1 = "hydepark1.jpg"
        imgName_2 = "hydepark2.jpg"
        ori_in1 = cv.LoadImageM(imgName_1)
        ori_in2 = cv.LoadImageM(imgName_2)
        img1 = cv.LoadImageM("hydepark1.jpg",cv.CV_LOAD_IMAGE_GRAYSCALE)
        cv.Smooth(img1, img1, cv.CV_MEDIAN,5,5)
        img2 = cv.LoadImageM("hydepark2.jpg",cv.CV_LOAD_IMAGE_GRAYSCALE)
        cv.Smooth(img2, img2, cv.CV_MEDIAN,5,5)

        cv.ShowImage("blr", img1)

        eig_image_1 = cv.CreateMat(img1.rows, img1.cols, cv.CV_32FC1)
        temp_image_1 = cv.CreateMat(img1.rows, img1.cols, cv.CV_32FC1)
        eig_image_2 = cv.CreateMat(img2.rows, img2.cols, cv.CV_32FC1)
        temp_image_2 = cv.CreateMat(img2.rows, img2.cols, cv.CV_32FC1)
        font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.3, 0.3, 0, 1, 8)
        featurePointArr_1 = cv.GoodFeaturesToTrack(\
                img1, eig_image_1, temp_image_1, 300, 0.04, 1.0, useHarris = True)
        featurePointArr_2 = cv.GoodFeaturesToTrack(\
                img1, eig_image_2, temp_image_2, 300, 0.04, 5.0, useHarris = True)

        for (x,y) in featurePointArr_1: 
            cv.PutText(ori_in1,"o",(int(x),int(y)),font,cv.Scalar(10, 200, 200))
        for (x,y) in featurePointArr_2: 
            cv.PutText(ori_in2,"o",(int(x),int(y)),font,cv.Scalar(10, 200, 200))
        cv.ShowImage("features_1", ori_in1)
        cv.ShowImage("features_2", ori_in2)
    def surf(self):
        #not implemented yet
        dummy = "not implemented yet"
        
class findFeatureByEdge:
    def __init__(self):
        
        self.imgName_1 = "1.jpg"
        self.imgName_2 = "2.jpg"

        self.win_name = "Edge"
        self.ori_win_name_1 = self.imgName_1
        self.ori_win_name_2 = self.imgName_2
        self.trackbar_name = "Threshold"
        
        self.in1 = cv.LoadImage(self.imgName_1, cv.CV_LOAD_IMAGE_COLOR)
        self.in2 = cv.LoadImage(self.imgName_2, cv.CV_LOAD_IMAGE_COLOR)

        # create the output self.in1
        self.col_edge = cv.CreateImage((self.in1.width, self.in1.height), 8, 3)

        # convert to grayscale
        self.gray = cv.CreateImage((self.in1.width, self.in1.height), 8, 1)
        self.edge = cv.CreateImage((self.in1.width, self.in1.height), 8, 1)
        cv.CvtColor(self.in1, self.gray, cv.CV_BGR2GRAY)

        # create the window
        cv.NamedWindow(self.win_name, cv.CV_WINDOW_AUTOSIZE)
        cv.NamedWindow(self.ori_win_name_1, cv.CV_WINDOW_AUTOSIZE)
        cv.NamedWindow(self.ori_win_name_1, cv.CV_WINDOW_AUTOSIZE)

    def show(self):
        # create the trackbar
        cv.CreateTrackbar(self.trackbar_name, self.win_name, 1, 100, self.on_trackbar)
        # show the self.in1
        self.on_trackbar(0)

    def surfExtract(self, img, threshold):
        grey = cv.CreateImage(cv.GetSize(img),8,1)
        cv.CvtColor(img, grey, cv.CV_BGR2GRAY)
        (keypoints,descriptors) = cv.ExtractSURF(grey, None, cv.CreateMemStorage(),(0,threshold,3,1))
        print len(keypoints), len(descriptors)
        if 0:
            for ((x, y), laplacian, size, dir, hessian) in keypoints:
                print "x=%d y=%d laplacian=%d size=%d dir=%f hessian=%f" % (x, y, laplacian, size, dir, hessian)
        return keypoints

    # the callback on the trackbar
    def on_trackbar(self,position):

        print "poosiotn: ", position
        cv.Smooth(self.gray, self.edge, cv.CV_BLUR, 3, 3, 0)
        cv.Not(self.gray, self.edge)

        # run the edge dector on gray scale
        cv.Canny(self.gray, self.edge, position, position * 3, 3)

        # reset
        cv.SetZero(self.col_edge)

        # copy edge points
        cv.Copy(self.in1, self.col_edge, self.edge)

        #find and mark Feature
        eig_image_1 = cv.CreateMat(self.in1.width, self.in1.height, cv.CV_32FC1)
        temp_image_1 = cv.CreateMat(self.in1.width, self.in1.height, cv.CV_32FC1)
        
        grey = cv.CreateImage(cv.GetSize(self.col_edge),8,1)
        cv.CvtColor(self.col_edge,grey,cv.CV_BGR2GRAY)
        keypoints_1 = self.surfExtract(self.in1, position*100)
        keypoints_2 = self.surfExtract(self.in2, position*100)

        #GenericDescriptorMatcher
#        matches
#        cv.GenericDescriptorMatcher.match(self.in1, keypoints_1, self.in2, keypoints_2, matches, None, None)

        featuredOrigin_1 = cv.CloneImage(self.in1)
        featuredOrigin_2 = cv.CloneImage(self.in2)
        font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.3, 0.3, 0, 1, 8)


        choice = 2
        if choice == 1:
            #Draw goodFeatureTotrack points
            featurePointArr_1 = cv.GoodFeaturesToTrack(\
                    grey, eig_image_1, temp_image_1, 300, 0.04, 1.0, useHarris = True)
            for (x,y) in featurePointArr_1: 
                cv.PutText(featuredOrigin,"o",(int(x),int(y)),font,cv.Scalar(10, 200, 200))
        if choice == 2:
            #Draw SURF keypoints
            for ((x, y), laplacian, size, dir, hessian) in keypoints_1:
                cv.PutText(featuredOrigin_1,"o",(int(x),int(y)),font,cv.Scalar(10, 200, 200))
            for ((x, y), laplacian, size, dir, hessian) in keypoints_2:
                cv.PutText(featuredOrigin_2,"o",(int(x),int(y)),font,cv.Scalar(10, 200, 200))

        
        # show the self.in1
        cv.ShowImage(self.win_name, self.col_edge)
        cv.ShowImage(self.ori_win_name_1, featuredOrigin_1)
        cv.ShowImage(self.ori_win_name_2, featuredOrigin_2)


#pg = panograph()
#pg.findFeature()
ffbe = findFeatureByEdge()
ffbe.show()
cv.WaitKey()
