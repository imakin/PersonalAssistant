import math
import numpy as np
import cv2
import argparse
from autorotate import get_rotation

cascade = cv2.CascadeClassifier("../data/lbpcascade_frontalface_improved_2.xml")

args = argparse.ArgumentParser()
args.add_argument("photo_path_1",
  help="path to the face photo A"
  )
args.add_argument(
  "photo_path_2",
  help="path to the face photo B"
  )

args.add_argument(
  "--ideal-size",
  dest="ideal_size",
  default=500,
  help="default size to use whne processing face"
)

params = args.parse_args()

img1 = cv2.imread(params.photo_path_1)
img2 = cv2.imread(params.photo_path_2)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ideal_size = params.ideal_size

# 1st detect face
coord1 = cascade.detectMultiScale(
  img1,
  scaleFactor=1.05,
  minNeighbors=4,
  minSize=(30,30),
  flags=cv2.CASCADE_SCALE_IMAGE
  )
x,y,w,h = coord1[0]
face1 = img1[y:y+h, x:x+w]

coord2 = cascade.detectMultiScale(
  img2, 
  scaleFactor=1.05,
  minNeighbors=4,
  minSize=(30,30),
  flags=cv2.CASCADE_SCALE_IMAGE
  )
x,y,w,h = coord2[0]
face2 = img2[y:y+h, x:x+w]

cv2.imwrite("temp1ori.jpg", face1)
cv2.imwrite("temp2ori.jpg", face2)


# 2 align face using eyes
# 2.a get eyes
rot1 = math.degrees(get_rotation(face1))
rot2 = math.degrees(get_rotation(face2))

print(rot1,rot2)

#2.b fix rotation
h,w = img1.shape
M = cv2.getRotationMatrix2D( (w/2,h/2), rot1, 1)
img1 = cv2.warpAffine(img1, M, (w,h))

h,w = img2.shape
M = cv2.getRotationMatrix2D( (w/2,h/2), rot2, 1)
img2 = cv2.warpAffine(img2, M, (w,h))

cv2.imwrite("temp1rot.jpg", img1)
cv2.imwrite("temp2rot.jpg", img2)


# 3 redetect face rectangle
coord1 = cascade.detectMultiScale(
  img1,
  scaleFactor=1.05,
  minNeighbors=4,
  minSize=(30,30),
  flags=cv2.CASCADE_SCALE_IMAGE
  )
x,y,w,h = coord1[0]
face1 = img1[y:y+h, x:x+w]

face1 = cv2.resize(face1, (int(w*ideal_size/h), ideal_size)) 

coord2 = cascade.detectMultiScale(
  img2, 
  scaleFactor=1.05,
  minNeighbors=4,
  minSize=(30,30),
  flags=cv2.CASCADE_SCALE_IMAGE
  )
x,y,w,h = coord2[0]
face2 = img2[y:y+h, x:x+w]

face2 = cv2.resize(face2, (int(w*ideal_size/h), ideal_size))
  


cv2.imwrite("temp1cmp.jpg", face1)
cv2.imwrite("temp2cmp.jpg", face2)



# 4 create LBPH and histcompare
facerec = cv2.face.LBPHFaceRecognizer_create()
facerec.train(
  np.asarray([face1]),
  np.asarray([0])
)
print(facerec.predict(face2))

# 5. test on flips
face2f = cv2.flip(face2, 1) # 1: flip in y axis, 0:flip in x axis, -1:flip in both
print(facerec.predict(face2f))

# cv2.imwrite("{}.aligned.jpg".format(args.photo), dst)
