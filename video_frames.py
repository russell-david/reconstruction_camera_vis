import cv2
vidname = 'MAX_0009'
vidcap = cv2.VideoCapture('/home/david/Documents/'+vidname+'.MP4')
success,image = vidcap.read()
count = 0
print('Vidcap read: ', success)
success = True
while success:
  success,image = vidcap.read()
  count += 1
  if count % 100 ==0:
      print("this is the %dth frame" % count)
  if count % 10 == 0:
      #print('Read a new frame: ', success)
      cv2.imwrite('../sampled_frames/'+vidname+"_%d.jpg" % count, image)     # save frame as JPEG file
