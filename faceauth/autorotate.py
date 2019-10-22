import time
import math 

import cv2


def get_rotation(img):
  eyeclassifier = cv2.CascadeClassifier("../data/haarcascade_eye_tree_eyeglasses.xml")

  coord = ()
  minNeighbors = 30

  starttime = time.time()
  while True:
    coords = eyeclassifier.detectMultiScale(
      img,
      scaleFactor=1.01,
      minNeighbors=minNeighbors,
      minSize=(30,30),
      flags=cv2.CASCADE_SCALE_IMAGE
    )
    if len(coords)>1 or minNeighbors<0:
      #print("final minNeighbors {}".format(minNeighbors))
      if len(coords)<=1:
        #print("cant get eyes")
        return 0
      break
    minNeighbors -= 1
  #print("eye search finish in {}".format(time.time()-starttime))

  #coords [(x,y,w,h), (...)]
  righteye = coords[0]
  lefteye = coords[1]
  if coords[1][0]>coords[0][0]:
    righteye = coords[1]
    lefteye = coords[0]

  if abs(righteye[3]-lefteye[3])>(min([righteye[3],lefteye[3]])/5):
    #print("cant detect eyes correctly, skipping")
    return 0

  #print(coords)
  rotation = math.atan2(
    righteye[1]+righteye[3]/2 - (lefteye[1]+lefteye[3]/2),
    righteye[0]+righteye[2]/2 - (lefteye[0]+lefteye[2]/2)
  )
  #print(rotation)
  return rotation

# h,w = img.shape
# M = cv2.getRotationMatrix2D( (w/2,h/2), math.degrees(rotation), 1)
# dst = cv2.warpAffine(img, M, (w,h))

# cv2.imwrite("{}.aligned.jpg".format(args.photo), dst)
