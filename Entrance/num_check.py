import cv2
import time


def getTrainingData(window_name, camera_id, path_name, max_num):
    cv2.namedWindow(window_name)
    cap = cv2.VideoCapture(camera_id)
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    color = (0, 255, 0)
    num = 0

    while cap.isOpened():
        ok, frame = cap.read()
        print(frame)
        if not ok:
            break
        time.sleep(1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faceRects = classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))

        if len(faceRects) > 0:
            for faceRect in faceRects:
                x, y, w, h = faceRect

                image_name = ('E:\\shengtuo_face_recognition\\face_pictures_2\\%s%07d.jpg' % (path_name, num))
                image = frame[y:y + h, x:x + w]
                cv2.imwrite(image_name, image)
                num += 1

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, ('%d' % num), (x + 30, y + 30), font, 1, (255, 0, 255), 4)
        if num > max_num:
            break

        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print('Finished.')


if __name__ == '__main__':
    # print ('catching your face and writting into disk...')
    getTrainingData('capture_video', 0, 'face_data', 1000000)