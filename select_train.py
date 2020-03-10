import os
import cv2

train_root = 'TRAIN/'
validation_root = 'VALIDATION/'
paths = [('NORMALIZED/circinatum/'), ('NORMALIZED/garryana/'), ('NORMALIZED/glabrum/'), ('NORMALIZED/kelloggii/'),('NORMALIZED/macrophyllum/'),('NORMALIZED/negundo/')]


def main():
    for path in paths:
        print("DOING PATH " +path)
        dir = os.listdir(path)
        img_count = len(dir)
        i = 1
        for item in dir:
            if os.path.isfile(path+item):
                i = i+1
                img = cv2.imread(path+item)
                if i < img_count/3:
                    imgname = validation_root + path + item
                else:
                    imgname = train_root + path + item
                cv2.imwrite(imgname, img)


main()