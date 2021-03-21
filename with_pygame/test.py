def vlc_play_video(file_path):
	cap = cv2.VideoCapture(file_path)
	fps = cap.get(cv2.CAP_PROP_FPS)
	print("fps =", fps)
	if not cap.isOpened():
		print("File Cannot be Opened")

	# init face detection
	# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
	# eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

	# init ORB // not working
	#orb = cv2.ORB()

	# init HOG
	#hog = cv2.HOGDescriptor()
	#hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

	timer = time.time()
	while(True):
		time_to_read = time.time()
		# Capture frame-by-frame
		ret, frame = cap.read()
		#print cap.isOpened(), ret
		if frame is not None:
			# faces detection
			#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			#faces = face_cascade.detectMultiScale(gray, 1.3, 5)
			#for (x,y,w,h) in faces:
			#	frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
			#	roi_gray = gray[y:y+h, x:x+w]
			#	roi_color = frame[y:y+h, x:x+w]
			#	eyes = eye_cascade.detectMultiScale(roi_gray)
			#	for (ex,ey,ew,eh) in eyes:
			#		cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

			# draw contours
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
			edged = cv2.Canny(gray, 0, 255)
			contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
			cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

			# ORB // not working
			#kp = orb.detect(frame,None)
			#kp, des = orb.compute(frame, kp)
			#img2 = cv2.drawKeypoints(frame,kp,color=(0,255,0), flags=0)

			# HSV colored object tracking
			#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			#lower_blue = np.array([110,50,50])
			#upper_blue = np.array([130,255,255])
			#mask = cv2.inRange(hsv, lower_blue, upper_blue)
			#res = cv2.bitwise_and(frame,frame, mask= mask)

			# canny Edge
			#frame = cv2.Canny(frame,10,255)

			# fourrier transform // pas compris
			#f = np.fft.fft2(frame)
			#fshift = np.fft.fftshift(f)
			#magnitude_spectrum = 20*np.log(np.abs(fshift))
			#rows, cols, _ = frame.shape
			#crow,ccol = int(rows/2) , int(cols/2)
			#fshift[crow-30:crow+30, ccol-30:ccol+30] = 0
			#f_ishift = np.fft.ifftshift(fshift)
			#img_back = np.fft.ifft2(f_ishift)
			#img_back = np.abs(img_back)

			# draw circles // not working
			#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
			#img = cv2.medianBlur(gray,5)
			#cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
			#circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
			#                            param1=50,param2=30,minRadius=0,maxRadius=0)
			#circles = np.uint16(np.around(circles))
			#for i in circles[0,:]:
				# draw the outer circle
			#    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
				# draw the center of the circle
			#    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

			# draw body
			#found, w = hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
			#for x, y, w, h in found:
			#	pad_w, pad_h = int(0.15*w), int(0.05*h)
			#	cv2.rectangle(frame, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), 1)

			#draw body v2
			#frame = imutils.resize(frame , width=min(800, frame.shape[1]))
			#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			#bounding_box_cordinates, weights =  hog.detectMultiScale(gray, winStride = (4, 4),
			#	padding = (8, 8), scale = 1.03)
			#bounding_box_cordinates, weights =  hog.detectMultiScale(frame, winStride = (4, 4),
			#	padding = (8, 8), scale = 1.10, useMeanshiftGrouping=True)
			#person = 1
			#for x,y,w,h in bounding_box_cordinates:
			#	cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
			#	cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
			#	person += 1
			#cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
			#cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
			#cv2.imshow('output', frame)

			cv2.imshow('frame', frame)
			#cv2.imshow('edges', edges)
			#cv2.imshow('fourrier', img_back)
			#cv2.imshow('circles', cimg)
			#cv2.imshow('mask', mask)
			#cv2.imshow('res', res)
			#timer = time.time() * 1000
			#while time.time() * 1000 - timer < 1000 / fps:
			#	pass
			#if 0xFF == ord('q'):
			#	break
			# if (time.time() - time_to_read) * 1000 >= 1000 / fps:
			# 	print("time to print:", time.time() - time_to_read)
			expected = 1000 / fps
			to_print = (time.time() - time_to_read) * 1000
			add_delay = max(int(1000 / fps - (time.time() - time_to_read) * 1000), 1)
			total_delay = to_print + add_delay
			#print("expected:", expected, "to_print:", to_print, "add_delay:", add_delay, "total_delay:", total_delay)
			if cv2.waitKey(max(int(1000 / fps - (time.time() - time_to_read) * 1000), 1)) & 0xFF == ord('q'):
				break
		else:
			print("Frame is None")
			break
	print("time to show entire video :", time.time() - timer)
	cap.release()
	cv2.destroyAllWindows()