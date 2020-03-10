import cv2
import numpy as np
import os
BLUR = 15
CANNY_THRESH_1 = 85
CANNY_THRESH_2 = 120
MASK_DILATE_ITER = 10
MASK_ERODE_ITER = 10
MASK_COLOR = (1.0,1.0,1.0) # In BGR format

def makeWhite(img):
	seuil = 200
	rows,cols, wtf = img.shape
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	for y in range(rows):
		for x in range(cols):
			if (gray[y,x])>seuil:
				img[y,x,0]=255
				img[y,x,1]=255
				img[y,x,2]=255
	return img



def removeBorders(img):
	
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	seuil = 254
	marge = 0
	rows,cols, wtf = img.shape
	ymin = cols
	ymax = 0
	xmin = rows
	xmax = 0
	#Y MIN AND MAX

	for y in range(rows):
	    rowSum = 0
	    for x in range(cols):
	        rowSum = rowSum + gray[y,x]
	    if rowSum/rows < seuil:
	        ymin = y
	        break
	y = rows -1
	while y > 0:
	    rowSum = 0
	    for x in range(cols):
	        rowSum = rowSum + gray[y,x]
	    if rowSum/rows < seuil:
	        ymax = y
	        break
	    y = y - 1
	#X MIN AND MAX
	for x in range(cols):
	    colSum = 0
	    for y in range(rows):
	        colSum = colSum + gray[y,x]
	    if colSum/cols < seuil:
	        xmin = x
	        break
	x = cols -1
	while x > 0:
	    colSum = 0
	    for y in range(rows):
	        colSum = colSum + gray[y,x]
	    if colSum/cols < seuil:
	        xmax = x
	        break
	    x = x - 1
	xmin = max(0, xmin-marge)
	xmax = min(cols, xmax+marge)
	ymin = max(0, ymin-marge)
	ymax = min(rows,ymax+marge)
	crop_img = img[ymin:ymax, xmin:xmax]
	crop_img = cv2.resize(crop_img, (200, 200))
	return crop_img


def contrast (img):
	
	lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	l, a, b = cv2.split(lab)
	clahe = cv2.createCLAHE(clipLimit=0.2, tileGridSize=(8,8))
	cl = clahe.apply(l)
	limg = cv2.merge((cl,a,b))
	final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
	return final

def removeBG (img):
 

	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#-- Edge detection -------------------------------------------------------------------
	edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
	edges = cv2.dilate(edges, None)
	edges = cv2.erode(edges, None)
	#-- Find contours in edges, sort by area ---------------------------------------------
	contour_info = []
	contours,_ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
	#  contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
	# Thanks to notes from commenters, I've updated the code but left this note
	for c in contours:
	    contour_info.append((
	        c,
	        cv2.isContourConvex(c),
	        cv2.contourArea(c),
	    ))
	contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
	max_contour = contour_info[0]

	#-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
	# Mask is black, polygon is white
	mask = np.zeros(edges.shape)
	cv2.fillConvexPoly(mask, max_contour[0], (255))

	#-- Smooth mask, then blur it --------------------------------------------------------
	mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
	mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
	mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
	mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

	#-- Blend masked img into MASK_COLOR background --------------------------------------
	mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
	img         = img.astype('float32') / 255.0                 #  for easy blending

	masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
	masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 

	return masked

def main ():
	root = 'NORMALIZED/'
	paths = [('circinatum/'), ('garryana/'), ('glabrum/'), ('kelloggii/'),('macrophyllum/'),('negundo/')]
	for path in paths:
		print("DOING PATH " +path)
		dirs = os.listdir(path)
		for item in dirs:
			if os.path.isfile(path+item):
				print(path+item)
				img = cv2.imread(path+item, 1) 

				img = cv2.medianBlur(img, 5)
				img = cv2.resize(img, (300, 300))

				img=makeWhite(img)
				img = removeBorders(img)
				#img = contrast(img)

				#img = removeBG(img)
				
				cv2.imwrite( 'NORMALIZED/'+path+item, img )

main()

