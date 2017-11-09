import sys
import numpy as np
#import cv2
from PIL import Image
from PIL import ImageFilter
from PIL import ImageStat

from tarantool import Connection

'''
c = Connection("127.0.0.1", 3301)
'''
pathToImages = '/Users/devernua/proga/images/'
'''
d = {}

for i in range(6):
    for j in range(201):
        if(j < 10):
            sj = '00' + str(j)
        elif(j < 100):
            sj = '0' + str(j)
        else:
            sj = str(j)
        mag = pathToImages + 'wallpaper_240x320_№' + str(i+1)+'_'+ sj+'.jpg'
        try:
            ig = Image.open(mag)
            m = ImageStat.Stat(ig).mean
            #m = tuple([i[1] for i in ImageStat.Stat(ig).extrema])
            ident = int(m[0]*256**2 + m[1]*256 + m[2])
            d[ident] = mag
        except:
            pass
print (len(d))
print ('stage 2')
'''
imgsrc = pathToImages + 'test1.jpg'

im = Image.open(imgsrc)
l = im.convert("L")
print(im.format, im.size, im.mode)
mask = l.point(lambda i : i > 100 and 255)
mask.show()
print (mask)

def parts(im, minsize):
    #print(im.size)
    if (im.size[0] < minsize or im.size[1] < minsize):
        return None
    lst = []
    lst.append(im.crop((0,                0,              int(im.size[0] / 2),   int(im.size[1] / 2)) ))
    lst.append(im.crop((lst[0].size[0],   0,              im.size[0],       int(im.size[1] / 2)) ))
    lst.append(im.crop((0,                lst[0].size[1], lst[0].size[0],   im.size[1])     ))
    lst.append(im.crop((lst[0].size[0],   lst[0].size[1], im.size[0],       im.size[1])     ))
    return lst

def toParts(im, eps, minsize):
    m = ImageStat.Stat(im).mean
    reqs = parts(im, minsize)
    delta = 0
    flag = True
    if (reqs):
        for i in range(4):

            manew = tuple( [i[1] for i in ImageStat.Stat(reqs[i]).extrema])

            delta += ((manew[0] - m[0])**2 +
                    (manew[1] - m[1])**2 +
                    (manew[2] - m[2])**2)**0.5
            if delta > eps:
                flag = False
                break
            delta = 0



    if (flag):
        #TODO: insert a photo
        #print(im.size, m, " HUY ")
        ###im = Image.new("RGB", im.size, tuple(map(int, m)))
        '''ident = int(m[0]*256**2 + m[1]*256 + m[2])
        sel = c.select("examples", ident)
        i = 0
        j = 0
        while not sel:
            sel = c.select("examples", (ident + i*256**j)%(256**3))
            if (not sel):
                sel = c.select("examples", (256**3 + ident + i*256**j)%(256**3))
            j += 1
            if(not j % 3):
                i += 1
                j = 0
        print(sel)
        im = Image.open(sel[0][1]).resize(im.size, Image.ANTIALIAS)
        '''
        #TODO: insert a photo
        #print(im.size, m, " HUY ")
        im = Image.new("RGB", im.size, tuple(map(int, m)))


        #ident = int(m[0]*256**2 + m[1]*256 + m[2])
        #minim = 2**24
        #mini = 0
        #for i in d:
        #    temp = ((m[0] - int(i/(256**2)))**2 + (m[1] - int(i/(256**2)%256))**2 + (m[2] - i%256)**2) ** 0.5
        #    if (temp < minim):
        #        minim = temp
        #        mini = i
        #im = Image.open(d[mini]).resize(im.size, Image.ANTIALIAS)

    else:
        #TODO: parts
        for i in range(4):
            reqs[i] = toParts(reqs[i], eps, minsize)
        im.paste(reqs[0], (0,                0,              int(im.size[0] / 2),   int(im.size[1] / 2)) )
        im.paste(reqs[1], (reqs[0].size[0],   0,              im.size[0],       int(im.size[1] / 2)))
        im.paste(reqs[2], (0,                reqs[0].size[1], reqs[0].size[0],   im.size[1]))
        im.paste(reqs[3], (reqs[0].size[0],   reqs[0].size[1], im.size[0],       im.size[1]))

    return im
newm = toParts(im, 20, 8)
last = Image.open(imgsrc)
last.show()
newm.show()
Image.blend(im, last, 0.5).show()
last = Image.open(imgsrc)
last.paste(newm, None, mask)
last.show()
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


