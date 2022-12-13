import sys
import numpy as np
import cv2

modelFile = "visual_part\mask\opencv_face_detector_uint8.pb"  # 模型文件
configFile = "visual_part\mask\opencv_face_detector.pbtxt"  # 配置文件
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)  # 加载人脸识别模型
conf_threshold = 0.7


def detectFaceOpenCVDnn(net, frame):
    """
    函数 blobFromImage(InputArray image,
               double scalefactor=1.0,
               const Size& size = Size(),
               const Scalar& mean = Scalar(),
               bool swapRB = false,
               bool crop = false,
               int ddepth = CV_32F)

     param1:预处理的图像frame；
     param2:图片像素缩放为1.0；
     param3:神经网络在训练的时候要求输入的图片尺寸300*300；
     param4:对RGB图片的三个通道分别减去不同的值 104 117 123
     param5:openCV中认为我们的图片通道顺序是BGR，但是我平均值假设的顺序是RGB，所以如果需要交换R和G，那么就要为true
     param6:图像裁剪False.当值为True时，先按比例缩放，然后从中心裁剪成size尺寸
     ddepth:输出的图像深度，可选CV_32F 或者 CV_8U.
     """
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)  # 对图像进行预处理放在blob
    frameHeight = frame.shape[0]  # 图片垂直尺寸 放在frameHeight
    frameWidth = frame.shape[1]  # 图片水平尺寸 放在frameWidth
    net.setInput(blob)  # 输入预处理后的图像
    detections = net.forward()  # 分类预测 向前传播
    bboxes = []
    ret = 0
    ROI = None
    """
    如果一个图像的位深度是8位，说明这张图像是灰度图像。
    如果一个图像的位深度是24位，说明这张图像是3通道图像。
    如果一个图像的位深度是32位，说明这张图像是4通道图像。
    除了RGB三个通道外，还有一个Alpha通道。Alpha就是反应图像透明程度的量，值也是0~255之间。0表示全透明，255表示不透明。
    """
    for i in range(detections.shape[2]):  # shape[2] 图片通道数
        confidence = detections[0, 0, i, 2]
        # print(detections[0, 0, i, 2])
        if confidence > conf_threshold:  # 如果大于设定概率（检测到人脸）
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            # print(detections[0, 0, i, 3])
            # print(detections[0, 0, i, 4])
            # print(detections[0, 0, i, 5])
            # print(detections[0, 0, i, 6])
            ROI = frame[y1:y2, x1:x2].copy()  # 把识别到的人脸框出来后 提取框内人脸 提高准确率
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 框出人脸区域
            ret += 1
    return ret, ROI


def cnt_area(cnt):
    """
    :param cnt:输入的单个轮廓值
    :return:计算轮廓的面积
    """
    area = cv2.contourArea(cnt)
    return area


def if_have_mask(img):
    """
    通过肤色轮廓面积与ROI面积比值判断是否佩戴口罩
    :return: 是否佩戴口罩结果
    """
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    """
    将摄像头读取的RGB数据（图像）转换为HSV数据（图像）
    
    因为RGB通道并不能很好地反映出物体具体的颜色信息 ， 
    而相对于RGB空间，HSV空间能够非常直观的表达色彩的明暗，色调，以及鲜艳程度，
    方便进行颜色之间的对比
    """
    # cv2.imshow('检测到人脸后第一次处理',hsv_img)
    # cv2.waitKey(6000)
    lower_hsv_1 = np.array([0, 30, 30])  # 颜色范围低阈值
    upper_hsv_1 = np.array([40, 255, 255])  # 颜色范围高阈值

    lower_hsv_2 = np.array([140, 30, 30])  # 颜色范围低阈值
    upper_hsv_2 = np.array([180, 255, 255])  # 颜色范围高阈值

    mask1 = cv2.inRange(hsv_img, lower_hsv_1, upper_hsv_1)
    mask2 = cv2.inRange(hsv_img, lower_hsv_2, upper_hsv_2)
    # cv2.imshow("mask1", mask1)
    # cv2.waitKey(6000)
    # cv2.imshow("mask2", mask2)
    # cv2.waitKey(6000)
    mask = mask1 + mask2
    # cv2.imshow("mask1+mask2", mask)
    # cv2.waitKey(6000)
    mask = cv2.blur(mask, (3, 3))
    """
    cv2.blur(img,ksize) 均值滤波
    img：原图像
    ksize：核大小
    原理：它只取内核区域下所有像素的平均值并替换中心元素。3x3标准化的盒式过滤器如下所示：
    特征：核中区域贡献率相同。
    作用：对于椒盐噪声的滤除效果比较好。
    
    椒盐噪声概念：
    • 椒盐噪声又称为脉冲噪声，它是一种随机出现的白点或者黑点。
    • 椒盐噪声 = 椒噪声 （pepper noise）+ 盐噪声（salt noise）。 椒盐噪声的值为0(椒)或者255(盐)。
    • 前者是低灰度噪声，后者属于高灰度噪声。一般两种噪声同时出现，呈现在图像上就是黑白杂点。
    • 对于彩色图像，也有可能表现为在单个像素BGR三个通道随机出现的255或0。
    • 如果通信时出错，部分像素的值在传输时丢失，就会发生这种噪声。
    • 盐和胡椒噪声的成因可能是影像讯号受到突如其来的强烈干扰而产生等。例如失效的感应器导致像 素值为最小值，饱和的感应器导致像素值为最大值。
    """
    # cv2.imshow("检测到人脸后第二次处理", mask)
    # cv2.waitKey(6000)

    mask_color = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    """
    轮廓检测函数cv2.findContours()
    cv2.findContours(image, mode, method[, contours[, hierarchy[, offset ]]])  
    函数参数：

    image：参数是寻找轮廓的图像；
    mode：参数表示轮廓的检索模式，有四种（此处为新的cv2接口）：
        cv2.RETR_EXTERNAL：表示只检测外轮廓
        cv2.RETR_LIST：检测的轮廓不建立等级关系
        cv2.RETR_CCOMP：建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
        cv2.RETR_TREE：建立一个等级树结构的轮廓。
    method：轮廓的近似办法：
        cv2.CHAIN_APPROX_NONE：存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max（abs（x1-x2），abs（y2-y1））==1
        cv2.CHAIN_APPROX_SIMPLE：压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
        cv2.CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS：使用teh-Chinl chain 近似算法

    返回值：

    cv2.findContours()函数返回两个值，一个是轮廓本身，还有一个是每条轮廓对应的属性。
    contour返回值：
    返回一个list，list中每个元素都是图像中的一个轮廓，用numpy中的ndarray表示。
    hierarchy返回值：
    返回一个ndarray，其中的元素个数和轮廓个数相同，每个轮廓 c o n t o u r s [ i ] contours[i] contours[i]对应4个hierarchy元素 h i e r a r c h y [ i ] [ 0 ]   h i e r a r c h y [ i ] [ 3 ] hierarchy[i][0] ~hierarchy[i][3] hierarchy[i][0] hierarchy[i][3]，分别表示后一个轮廓、前一个轮廓、父轮廓、内嵌轮廓的索引编号，如果没有对应项，则该值为负数。
    """
    if len(contours) < 1:  # 如果没找到轮廓
        return "No Mask"
    contours = list(contours)
    contours.sort(key=cnt_area, reverse=True)  # 按照轮廓面积升序排序
    print(cv2.contourArea(contours[0]))  # 输出轮廓面积最小数
    area = cv2.contourArea(contours[0])
    """yj：最小的轮廓面积除以脸部轮廓面积，不一定就是用口罩轮廓来做分子"""
    mask_rate = area / (img.shape[0] * img.shape[1])  # 口罩面积除以面部面积 查看口罩占面部大小
    print(mask_rate)
    """yj: 我觉得这里0.5可能合适一点"""
    if mask_rate < 0.6:
        return "Have Mask"
    else:
        return "No Mask"


if __name__ == '__main__':
 # while True:
    camera = cv2.VideoCapture(0)  # 读取相机组件
    ret, frame = camera.read()  # 从摄像头读取图像 存放在frame
    """
    cap.read()按帧读取视频，ret,frame是获cap.read()方法的两个返回值。
    其中ret是布尔值，如果读取帧是正确的则返回True，如果文件未读取到结尾，它的返回值就为False。
    frame就是每一帧的图像，是个三维矩阵。
    """
    cv2.imshow('video', frame)
    """
    cv2.imshow()函数需要两个输入，一个是图像窗口的名字即title，一个是所展示图片的像素值矩阵。
    """
    cv2.waitKey(6000)
    """
     参数是1，表示延时1ms切换到下一帧图像，参数过大如cv2.waitKey(1000)，会因为延时过久而卡顿感觉到卡顿。
     参数为0，如cv2.waitKey(0)只显示当前帧图像，相当于视频暂停。
     """

    ret, frame = detectFaceOpenCVDnn(net, frame)
    """
     ret存放是否检测到人脸 如果检测到 ret==1
     frame存放经过人脸识别后 裁切出来的人脸部分图像 
    """

    if ret == 1:
        print(if_have_mask(frame))
    else:
        print("未识别到人脸")
