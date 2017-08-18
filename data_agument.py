import argparse
import os
import cv2
import numpy as np
from math import *
from dirop import *

def add_noise(im,percent=0.3):
	image=im[:]
	sumcount=im.shape[0]*im.shape[1]
	noisecount=int(sumcount*percent)
	dim=im.ndim
	for i in range(noisecount):
		rx=int(np.random.uniform(0,im.shape[0]))
		ry=int(np.random.uniform(0,im.shape[1]))
		if dim==1:
			im[rx,ry]=255
		elif dim==3:
			rr=int(np.random.uniform(0,255))
			rb=int(np.random.uniform(0,255))
			rg=int(np.random.uniform(0,255))
			im[rx,ry,0]=rr
			im[rx,ry,1]=rb			
			im[rx,ry,2]=rg
	return im
def im_sharp(im,ksize=3):
	kernel=np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
	im=cv2.filter2D(im,-1,kernel)
	return im
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
    

im_format=[".jpg",".png",".JPG",".PNG"]

def dir_flip(dirpath,code):	
	ims=GetFullPathFormatFileList(dirpath,im_format)
	for im in ims:
		im_data=cv2.imread(im)
		new_im=cv2.flip(im_data,code)
		cv2.imwrite("{}_fliped{}.{}".format(im.split(".")[0],str(code),im.split(".")[1]),new_im)
		print("{} flipped!!".format(im))
def dir_blur(dirpath,ksize=(5,5),sigma=1.5):
	ims=GetFullPathFormatFileList(dirpath,im_format)
	for im in ims:
		im_data=cv2.imread(im)
		new_im=cv2.GaussianBlur(im_data,ksize,sigma)
		cv2.imwrite("{}_blur.{}".format(im.split(".")[0],im.split(".")[1]),new_im)
		print("{} blured!!".format(im))
def dir_noise(dirpath,percent=0.3):
	ims=GetFullPathFormatFileList(dirpath,im_format)
	for im in ims:
		im_data=cv2.imread(im)
		new_im=add_noise(im_data,percent)
		cv2.imwrite("{}_noise.{}".format(im.split(".")[0],im.split(".")[1]),new_im)
		print("{} noiseed!!".format(im))
def dir_clear(dirpath,ksize=3):
	ims=GetFullPathFormatFileList(dirpath,im_format)
	for im in ims:
		im_data=cv2.imread(im)
		new_im=im_sharp(im_data,ksize=3)
		cv2.imwrite("{}_clear.{}".format(im.split(".")[0],im.split(".")[1]),new_im)
		print("{} cleared!!".format(im))
def dir_rotate(dirpath,angle=90,scale=1):
	ims=GetFullPathFormatFileList(dirpath,im_format)
	for im in ims:
		im_data=cv2.imread(im)
		new_im=im_rotate(im_data,angle,scale)
		cv2.imwrite("{}_rotate{}_{}.{}".format(im.split(".")[0],angle,scale,im.split(".")[1]),new_im)
		print("{} rotated {}_{}!!".format(im,angle,scale))
	
	
		
		



if __name__=="__main__":
	parser=argparse.ArgumentParser()
	parser.add_argument("im_dir",help="image directory")
	parser.add_argument("-depth",type=int,default=0,help="depth of the rename dirs",dest="depth")
	parser.add_argument("-type",dest="type",default="flip_x",help="agument type")
	args=parser.parse_args()
                                                    
	im_dirs=[args.im_dir]
	for depth in range(args.depth):
		nextdir=[]
		for d in im_dirs:
			nextdir.extend(GetFullPathDirList(d))
		im_dirs=nextdir[:]
	if args.type=="flip_x":
		for d in im_dirs:
			dir_flip(d,1)
	if args.type=="flip_y":
		for d in im_dirs:
			dir_flip(d,0)
	if args.type=="blur":
		for d in im_dirs:
			dir_blur(d)
	if args.type=="noise":
		for d in im_dirs:
			dir_noise(d)
	if args.type=="clear":
		for d in im_dirs:
			dir_clear(d)
	if args.type=="rotate":
		for d in im_dirs:
			dir_rotate(d)


















