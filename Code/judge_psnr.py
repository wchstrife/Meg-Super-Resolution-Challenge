import numpy as np
import sys
import cv2
from brainpp.oss import OSSPath
import tarfile
import io

fin=tarfile.open(fileobj=OSSPath('s3://emc-share/work/topaz_release/gt.tar').open('rb'))
#fin=tarfile.open(fileobj=open('./gt.tar','rb'))

out_path='s3://fhq-dataproc/work/topaz/release/prediction_bicubic.tar'
#out_path='s3://fhq-dataproc/work/topaz/release/prediction_unet.tar'
fout_s3=OSSPath(out_path).open('rb')
#fout_s3=open('./prediction_bicubic.tar','rb')
fout=tarfile.open(fileobj=fout_s3)

cnt=0
rms=0
while True:
	tinfo=fin.next()
	if tinfo is None:
		break
	oldname=tinfo.name
	print(tinfo.name,file=sys.stderr)
	if not tinfo.isfile():
		continue
	content=fin.extractfile(tinfo).read()
	img=cv2.imdecode(np.fromstring(content,dtype='uint8'),1)

	while True:
		tinfo=fout.next()
		if tinfo is None:
			break
		if tinfo.isfile():
			break
	#print(tinfo.name)
	if tinfo is None:
		print('0')
		print('number of files mismatch',cnt)
		sys.exit(0)
	if tinfo.name != oldname.replace('gt','test'):
		print('0')
		print('filename mismatch')
		sys.exit(0)
	content=fout.extractfile(tinfo).read()
	img_out=cv2.imdecode(np.fromstring(content,dtype='uint8'),1)
	if img.shape!=img_out.shape or img.dtype!=img_out.dtype:
		print('0')
		print('image size mismatch',img.shape,img_out.shape)
		sys.exit(0)
	
	#if cnt==100:
		#import balls.supershow2 as s2
		#s2.submit('debug',{
			#'img':img,
			#'img_out':img_out,
			#'path':out_path
		#},topic='topaz_release',post_key=out_path)
	
	r=np.square(np.float32(img)-img_out).mean()
	rms+=r
	cnt+=1
	psnr=np.log10(256*256/max((rms/cnt),1e-10))*10

	print(tinfo.name,img.shape,'rms',rms/cnt,'psnr',psnr,'r',r,file=sys.stderr)
psnr=np.log10(256*256/max((rms/cnt),1e-10))*10
print(psnr)
print('looks good')

#    unet: 28.03
# bicubic: 28.61
