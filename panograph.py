import cv

class panograph:
    def __init__(self):
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

panograph()
cv.WaitKey()
