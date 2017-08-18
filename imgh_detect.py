import cv2
import sys
import numpy as np
from dirop import *
from math import *

im_format=[".jpg",".png",".JPG",".PNG"]

def im_rotate(im,angle=90,scale=1):
	width=im.shape[1]
	height=im.shape[0]

	heightNew=int(width*fabs(sin(radians(angle)))+height*fabs(cos(radians(angle))))
	widthNew=int(height*fabs(sin(radians(angle)))+width*fabs(cos(radians(angle))))

	matRotation=cv2.getRotationMatrix2D((width/2,height/2),angle,1)

	matRotation[0,2] +=(widthNew-width)/2  #
	matRotation[1,2] +=(heightNew-height)/2  #
	imgRotation=cv2.warpAffine(im,matRotation,(widthNew,heightNew),borderValue=(255,255,255))
	return imgRotation
def check_h(im,top=20,bdisplay=False):
	im_gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	lineresult=im_gray.copy()
	im_edge=cv2.Canny(im_gray,50,100)
	liness=cv2.HoughLines(im_edge,1,np.pi/180,118)
	if bdisplay:
		print liness[:top]
		for lines in liness[:top]:
			line=lines[0]
			rho=line[0]
			theta=line[1]
			if theta<np.pi/4 or theta>np.pi/4*3:
				print "vertical:",rho,theta
				p1=(int(rho/np.cos(theta)),0)
				p2=(int((rho-lineresult.shape[0]*np.sin(theta))/np.cos(theta)),lineresult.shape[0])
				cv2.line(lineresult,p1,p2,(255))
			else:
				print "horizon:",rho,theta
				p1 = (0,int(rho/np.sin(theta)))    
        			p2 = (lineresult.shape[1], int((rho-lineresult.shape[1]*np.cos(theta))/np.sin(theta)))  
        			cv2.line(lineresult, p1, p2, (255), 1) 
		#im_edge=cv2.Laplacian(im_gray,-1)
		cv2.imshow("originim",lineresult)
		cv2.waitKey(10000)
	
	theta=liness[0][0][1]
	if theta<np.pi/4 or theta>np.pi/4*3:
		return True
	else:
		return False	
def dir_rotate(dirpath,angle=90,scale=1,replace=True):
	ims=GetFullPathFormatFileList(dirpath,im_format)
	for im in ims:
		im_data=cv2.imread(im)
		if check_h(im_data):
			new_im=im_rotate(im_data,angle,scale)
			if replace:
				cv2.imwrite(im,new_im)
			else:
				cv2.imwrite("{}_rotate.{}".format(im.split(".")[0],im.split(".")[1]),new_im)
			print("checked and rotated {}!!".format(im))
def dir_check(dirpath):
	ims=GetFullPathFormatFileList(dirpath,im_format)
	for im in ims:
		im_data=cv2.imread(im)
		check_h(im_data,top=1,bdisplay=True)
def dir_edge(dirpath):
	ims=GetFullPathFormatFileList(dirpath,im_format)
	for im in ims:
		im_gray=cv2.imread(im,0)
		im_edge=cv2.Canny(im_gray,50,100)
		cv2.imshow("imedge",im_edge)
		cv2.waitKey(10000)
if __name__=="__main__":
	dirname=sys.argv[1]
	#modified here to `False` to remain the original image
	replace=True
	
	#dir_rotate(dirname,replace=replace)
	#dir_check(dirname)
	dir_edge(dirname)
	

	
			
