from tarantool import Connection
from PIL import Image
from PIL import ImageStat

pathToImages = '/home/devernua'
imgsrc = pathToImages + 'test.jpg'

c = Connection("127.0.0.1", 3301)
c.select("test", None, iterator=tarantool.const.ITERATOR_
import tarantool
tarantool.Connection.call()

for i in range(2**24):
    c.insert("examples", (i, imgsrc))


for i in range(6):
    for j in range(201):
        if(j < 10):
            sj = '00' + str(j)
        elif (j < 100):
            sj = '0' + str(j)
        else:
            sj = str(j)

        imgsrc = pathToImages + 'wallpaper_240x320_№' + str(i+1)+'_'+ sj+'.jpg'
        try:
            im = Image.open(imgsrc)
            print(im.format, im.size, im.mode, i+1, j)
            m = ImageStat.Stat(im).mean

            ident = int(m[0]*256**2 + m[1]*256 + m[2])
            lst.append(ident) ##
            print(ident , m)
            sel = c.select("examples", ident)
            #print("1 : ", sel)
            if (sel):
                print(sel)
                c.delete("examples", ident)
                sel[0].append(imgsrc)
                c.insert("examples", tuple(sel[0]))#TODO
            else:
                c.insert("examples", (ident, imgsrc))
            sel =  c.select("examples", ident)
            print("2 : ", sel)

        except:
            pass
'''
c = Connection("127.0.0.1", 3301)
result = c.upsert("examples",(9999,'Value', 'Value'))
result = c.upsert("examples", (9999, 'MEN', 'YOU'))

res = c.select("examples", 9999)
print (res)

res = c.delete("examples", 9999)
res = c.delete("examples", 99999)

res = c.select("examples", 99999)
print (res)
'''
