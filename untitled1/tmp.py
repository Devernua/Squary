from tarantool import Connection
from PIL import Image
from PIL import ImageStat
import numpy as np

pathToImages = '/Users/devernua/proga/images/'
imgsrc = pathToImages + 'test1.jpg'

im = Image.open(imgsrc)
im.thumbnail((int(im.size[0]/150), int(im.size[1]/150)))
print(im.size)
data = np.asarray(im, dtype=np.uint8)
print(im.size)
print(data.shape)
#print(type(data.data))

#print(data.ravel())

'''
data = im.getdata()

print(im.format, im.size, im.mode)

in_data = np.asarray(im, dtype=np.uint8)
print (in_data)
im = Image.fromarray(in_data)
im.show()
print(type(in_data))
im = Image.frombuffer(im.mode, im.size, in_data)
im.show()


'''
#print("list :", list(data))

c = Connection("127.0.0.1", 3301)

data = np.asarray(im, dtype=np.uint8)

#print( (1,tuple(data.ravel())))
data = data.ravel()

#print("list :", list(data))
#print (data[.)
data = list(data)
tkey = int(data[0])
print(tkey, type(tkey))
print(c.select("examples", int(tkey)))
if(c.select("examples", int(tkey))):
    c.delete("examples", int(tkey))
print(c.select("examples", int(tkey)))

print(tuple(data[0:4:]))
lst= tuple([i for i in data])
c.insert("examples", lst)
#c.insert("examples", tuple(lst))
res = c.select("examples", tkey)
print(res)
c.delete("examples", tkey)


res = c.select("examples", 255)

print(res)

'''
res = c.select("examples", 1)
if (res):
    print ("URA")
else:
    res = c.insert("examples",(1, "asd"))
    print (res)

res = c.select("examples", 1)
print (res)
res[0].append(2)
print(res)
c.delete("examples",1)
c.insert("examples", tuple(res[0]))

res = c.select("examples", 1)

print("last : ", res)
c.delete("examples", 1)
'''