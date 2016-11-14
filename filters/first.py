# -*- coding: utf-8 -*-
import sys
# import cv2
from PIL import Image
from PIL import ImageFilter
from PIL import ImageStat
from os import walk

pathToImages = '/home/squary/images/cat/'
pathRoot = '/home/squary/'

d = {}

def parts(img, minsize):
    # print(im.size)
    if img.size[0] < minsize or img.size[1] < minsize:
        return None
    lst = []
    lst.append(img.crop((0, 0, int(img.size[0] / 2), int(img.size[1] / 2))))
    lst.append(img.crop((lst[0].size[0], 0, img.size[0], int(img.size[1] / 2))))
    lst.append(img.crop((0, lst[0].size[1], lst[0].size[0], img.size[1])))
    lst.append(img.crop((lst[0].size[0], lst[0].size[1], img.size[0], img.size[1])))
    return lst


def toParts(img, eps, minsize):
    m = ImageStat.Stat(img).mean  # may be mean, median, stddev, rms
    reqs = parts(img, minsize)

    doParts = False

    delta = 0
    if reqs:
        for i in range(4):
            delta += ((ImageStat.Stat(reqs[i]).mean[0] - m[0]) ** 2 +
                      (ImageStat.Stat(reqs[i]).mean[1] - m[1]) ** 2 +
                      (ImageStat.Stat(reqs[i]).mean[2] - m[2]) ** 2) ** 0.5
        delta /= 4

    if delta < eps:
		# TODO: insert a photo
		# print(im.size, m, " HUY ")
		img = Image.new("RGB", img.size, tuple(map(int, m)))
		'''
		ident = int(m[0] * 256 ** 2 + m[1] * 256 + m[2])
		minim = 2 ** 24
		mini = 0
		for i in d:
			temp = ((m[0] - int(i / (256 ** 2))) ** 2 + (m[1] - int(i / (256 ** 2) % 256)) ** 2 + (
				m[2] - i % 256) ** 2) ** 0.5
			if (temp < minim):
				minim = temp
				mini = i
		img = Image.open(d[mini]).resize(img.size, Image.ANTIALIAS)
		'''
    else:
        # TODO: parts
        for i in range(4):
            reqs[i] = toParts(reqs[i], eps, minsize)
        img.paste(reqs[0], (0, 0, int(img.size[0] / 2), int(img.size[1] / 2)))
        img.paste(reqs[1], (reqs[0].size[0], 0, img.size[0], int(img.size[1] / 2)))
        img.paste(reqs[2], (0, reqs[0].size[1], reqs[0].size[0], img.size[1]))
        img.paste(reqs[3], (reqs[0].size[0], reqs[0].size[1], img.size[0], img.size[1]))

    return img

	
def main(imgsrc):
	outputFile = imgsrc + '_out.jpg'
	outputFileBlend = imgsrc + '_out_blend.jpg'

	# ImageStat.mean - средний цвет - {R, G, B}

	'''
	for (dirpath, dirnames, filenames) in walk(pathToImages):
		print(dirpath)
		for filename in filenames:
			try:
				ig = Image.open(dirpath + filename)
				m = ImageStat.Stat(ig).mean
				ident = int(m[0] * 256 ** 2 + m[1] * 256 + m[2])
				d[ident] = dirpath + filename
				# print(dirpath + filename, m[0], m[1], m[2])
			except:
				pass

	print(len(d), 'images loaded')
	print('[stage 2]')
	'''
	im = Image.open(imgsrc)
	im.thumbnail((1400, 1000))
	print(im.format, im.size, im.mode)


	aa = toParts(im, 5, 11)
	aa.save(outputFile)
	Image.blend(im, aa, 0.5).save(outputFileBlend)
	return outputFileBlend

im = main("/Users/devernua/proga/images/test1.jpg")
im.show()
#im = Image.open("/Users/devernua/proga/images/test1.jpg")

'''box = (0, 0, 500, 500)
region = im.crop(box)
region = region.transpose(Image.ROTATE_180)
im.paste(region,box)
#region.show()
r,g,b = im.split()

out = im.filter(ImageFilter.DETAIL)
out = im.point(lambda i : i * 1.2)
im.save('test1.jpg', quality=100)

mask = Image.open(imgsrc)
mask = Image.blend(mask,im, 0.5)
#mask.show()

print (ImageStat.Stat(im).rms)
'''
