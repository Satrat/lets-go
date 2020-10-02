import numpy as np
import cv2
import OSC

cap = cv2.VideoCapture(2)
c = OSC.OSCClient()
c.connect(('127.0.0.1', 8000))
print "OSC Connected"

lower = [200]
lower = np.array(lower, dtype = "uint8")
upper = [255]
upper = np.array(upper, dtype = "uint8")


# set parameters for blob detection
params = cv2.SimpleBlobDetector_Params()
paramsB = cv2.SimpleBlobDetector_Params()
 
# Change thresholds
params.minThreshold = 10
params.maxThreshold = 1000
paramsB.minThreshold = 10
paramsB.maxThreshold = 1000
 
# Filter by Area.
params.filterByArea = True
params.minArea = 300
paramsB.filterByArea = True
paramsB.minArea = 300
 
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.8
paramsB.filterByCircularity = True
paramsB.minCircularity = 0.1

 
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.1
paramsB.filterByConvexity = True
paramsB.minConvexity = 0.1
 
params.filterByColor = True
params.blobColor = 255
paramsB.filterByColor = True
paramsB.blobColor = 255

ret, image = cap.read()

# display Go board
cv2.namedWindow("output", cv2.WINDOW_NORMAL)
ret, image = cap.read()
imS = cv2.resize(image, (1100, 700))
cv2.imshow("output", imS)

left_clicks = list()
white_ons = ""
black_ons = ""
count = 0


####SET THESE######
size = 13
slack = 15
###################

whites = np.zeros((size,size))
blacks = np.zeros((size,size))
print whites
print blacks

# identify edges of board
def mouse_callback(event, x, y, flags, params):
	global count
	if(count < 4):
		if(event == 1):
			global left_clicks
			left_clicks.append((x,y))
			print left_clicks
			count = count + 1


#set mouse callback function for window
cv2.setMouseCallback("output", mouse_callback)

cv2.waitKey(0)
cv2.destroyAllWindows()


# Calculate board position in frame
# Assumes camera and baord remain stationary
points = list()

(ulx, uly) = left_clicks[0]
(urx, ury) = left_clicks[1]
(llx, lly) = left_clicks[2]
(lrx, lry) = left_clicks[3]
x1 = (ulx + llx) / 2
x2 = (urx + lrx) / 2
y1 = (uly + ury) / 2
y2 = (lly + lry) / 2

print x1,x2,y1,y2
tileX = (x2 - x1) / (size - 1)
tileY = (y2 - y1) / (size - 1)

print left_clicks

for i in xrange(size):
	y = y1 + i * tileY
	for j in xrange(size):
		x = x1 + j * tileX
		points.append((x,y))

cv2.namedWindow('Lets Go', cv2.WINDOW_NORMAL)


while(True):
	# Capture game stream frame-by-frame
	ret, frame = cap.read()
	frame = cv2.resize(frame, (1100, 700))

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	grayB = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	cv2.bitwise_not(grayB, grayB) #invert color to display black blobs

	mask = cv2.inRange(gray, lower, upper)
	output = cv2.bitwise_and(gray, gray, mask = mask)

	maskB = cv2.inRange(grayB, lower, upper)
	outputB = cv2.bitwise_and(grayB, grayB, mask = maskB)
	detector = cv2.SimpleBlobDetector_create(params)
	detectorB = cv2.SimpleBlobDetector_create(paramsB)

	keypoints = detector.detect(output)
	keypointsB = detectorB.detect(outputB)

	white_ons = ""
	black_ons = ""

	for index in xrange(len(points)):
		flagW = False
		row = index / size
		col = index % size
		for keyPoint in keypoints:
			x = keyPoint.pt[0]
			y = keyPoint.pt[1]
			(xp, yp) = points[index]
			#print row, col
			if abs(x - xp) < slack and abs(y - yp) < slack:
				whites[row][col] = 1.
				flagW = True
				#print row,col, "GOOD"
				white_ons += (str(col) + " " + str(row) + " 1 ")
				print "WHITE"
				print whites
		if flagW == False and whites[row][col] == 1.:
			whites[row][col] = 0.
			white_ons += (str(col) + " " + str(row) + " 0 ")
		flagB = False
		for keyPointB in keypointsB:
			x = keyPointB.pt[0]
			y = keyPointB.pt[1]
			(xp, yp) = points[index]
			if abs(x - xp) < slack and abs(y - yp) < slack:
				blacks[row][col] = 1.
				flagB = True
				#print row,col
				black_ons += (str(col) + " " + str(row) + " 1 ")
				#print "BLACK"
				#print blacks
		if(flagB == False and blacks[row][col] == 1.):
			blacks[row][col] = 0.
			black_ons += (str(col) + " " + str(row) + " 0 ")

	im_with_keypoints = cv2.drawKeypoints(output, keypoints, np.array([]), (255,0,255), 2)
	im_with_keypointsB = cv2.drawKeypoints(outputB, keypointsB, np.array([]), (255,0,255), 2)

	cv2.imshow("Lets Go", np.hstack([im_with_keypoints, im_with_keypointsB]))

	# send white token locations to Max over OSC
	if(len(white_ons) > 0):
		whiteMsg = OSC.OSCMessage()
		whiteMsg.setAddress("/white")
		whiteMsg.append(white_ons)
		c.send(whiteMsg)

	# send white token locations to Max over OSC
	if(len(black_ons) > 0):
		blackMsg = OSC.OSCMessage()
		blackMsg.setAddress("/black")
		blackMsg.append(black_ons)
		c.send(blackMsg)

	# Exit game
	if cv2.waitKey(1000) & 0xFF == ord('q'):
		break       

# Clean up
cap.release()
cv2.destroyAllWindows()