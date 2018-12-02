#!/root/.virtualenvs/neo3/bin/python
import redis
import time
import traceback
import cv2
import base64
from io import BytesIO
from PIL import Image
import numpy as np

try:
  r = redis.from_url('redis://:z******6@redis-15901.c1.asia-northeast1-1.gce.cloud.redislabs.com:15901/0')
  fps=30
  img_param = [int(cv2.IMWRITE_JPEG_QUALITY), fps]
  #LIST CAM
  cap = cv2.VideoCapture(0)
  ret,frame = cap.read()
  timeCheck = time.time()
  future = 20 # delay
  while(True):
    #print time.time()
    if time.time() >= timeCheck:
      #print "============== time.time() > ----"
      ret, frame = cap.read()
      img_resize = cv2.resize(frame, (320,240))
      gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
      _, img_encode = cv2.imencode('.jpg', gray, img_param)
      base64_str2 = base64.b64encode(BytesIO(img_encode).getvalue())
      #print len(base64_str2)
      #print("%s" % base64_str2)
      r.publish('cam', base64_str2)
      #cv2.imshow('frame', gray)
      timeCheck = time.time()+future
    else:
      ret = cap.grab()
      #print "grab %d" % ret
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #  break
    time.sleep(10)
  cap.release()
  
except Exception as e:
  print(str(e))
  print(traceback.format_exc())
