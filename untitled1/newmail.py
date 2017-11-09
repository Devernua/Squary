from PIL import Image
from PIL import ImageStat
import time
import random

def parts(im, minsize):
    if (im.size[0] <= minsize or im.size[1] <= minsize):
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
            manew = ImageStat.Stat(reqs[i]).mean
            delta += ((manew[0] - m[0])**2 +
                    (manew[1] - m[1])**2 +
                    (manew[2] - m[2])**2)**0.5
            if delta > eps:
                flag = False
                break
            delta = 0
    if (flag):
        im = Image.new("RGB", im.size, tuple(map(int, m)))

    else:
        for i in range(4):
            reqs[i] = toParts(reqs[i], eps, minsize)
        im.paste(reqs[0], (0,                0,              int(im.size[0] / 2),   int(im.size[1] / 2)) )
        im.paste(reqs[1], (reqs[0].size[0],   0,              im.size[0],       int(im.size[1] / 2)))
        im.paste(reqs[2], (0,                reqs[0].size[1], reqs[0].size[0],   im.size[1]))
        im.paste(reqs[3], (reqs[0].size[0],   reqs[0].size[1], im.size[0],       im.size[1]))

    return im


def dist(rgb1, rgb2):
    res = 0
    for i in range(3):
        res = (rgb1[i] - rgb2[i])**2
    return res**0.5

def newParts(im, eps, minsize):
    flag = True
    if (im.size[0] <= minsize or im.size[1] < minsize):
        l = [0,0,0]
        size = im.size

        n = 8
        for i in range(n):
            x = i
            y = i
            p = im.getpixel((x,y))
            for j in range(3):
                l[j] += p[j]
        for i in range(3):
            l[i] = int(l[i]/n)

        return [im, l, flag]

        #return [im, im.getpixel((1,1)), True]
    lst = []
    lst.append(im.crop((0,                0,              int(im.size[0] / 2),  int(im.size[1] / 2))))
    lst.append(im.crop((lst[0].size[0],   0,              im.size[0],           int(im.size[1] / 2))))
    lst.append(im.crop((0,                lst[0].size[1], lst[0].size[0],       im.size[1])         ))
    lst.append(im.crop((lst[0].size[0],   lst[0].size[1], im.size[0],           im.size[1])         ))

    newlst = []
    for i in range(4):
        newlst.append(newParts(lst[i], eps, minsize))
        if (not newlst[i][2]):
            flag = False
        elif(flag):
            for j in range(i):
                if (dist(newlst[j][1], newlst[i][1]) > eps):
                    flag = False


    l = [0,0,0]
    for i in range(3):
        for j in newlst:
            l[i] += j[1][i]
    l = tuple([i/4.0 for i in l])

    if(flag):
        return [im, l, True]

    for i in newlst:
        if i[2]:
            i[0] = Image.new("RGB", i[0].size, tuple(map(int, i[1])))

    newsize = newlst[0][0].size
    im.paste(newlst[0][0], (0,     0,              int(im.size[0] / 2),   int(im.size[1] / 2)) )
    im.paste(newlst[1][0], (newsize[0],   0,              im.size[0],       int(im.size[1] / 2)))
    im.paste(newlst[2][0], (0,                newsize[1], newsize[0],   im.size[1]))
    im.paste(newlst[3][0], (newsize[0],   newsize[1], im.size[0],       im.size[1]))

    return [im, l, False]




pathToImages = '/Users/devernua/proga/images/'

imgsrc = pathToImages + 'test3.jpg'

im = Image.open(imgsrc)
im = im.resize((1024,1024))
start = time.time()
toParts(im, 10, 8).show()
end = time.time()
print(end-start)


im = Image.open(imgsrc)
im = im.resize((1024,1024))
start = time.time()
newParts(im, 10, 8)[0].show()
end = time.time()
print(end-start)

'''
tmpmean = im.resize((8,8))
im = Image.open(imgsrc)
im = im.resize((1024,1024))
start = time.time()
for i in range(128):
    for j in range(128):
        tmp = im.crop((i*8, j*8, i*8 + 8, j*8+8))
        mean = ImageStat.Stat(tmpmean).mean
        mean = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        tmp = Image.new("RGB", tmp.size, tuple(map(int, mean)))
        im.paste(tmp, (i*8, j*8, i*8 + 8, j*8+8))
im.show()
end = time.time()
print(end-start)


'''


