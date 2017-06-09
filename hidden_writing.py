#coding:utf-8
#ice_ctf also got one

import Image

img = Image.open('ifs.bmp')

X = img.size[0]
Y = img.size[1]

print X,Y

for i in range(X-2):
  for j in range(Y-2):
    a = img.getpixel((i,j))[0]+img.getpixel((i,j))[1]+img.getpixel((i,j))[2]
    b = img.getpixel((i,j+1))[0]+img.getpixel((i,j+1))[1]+img.getpixel((i,j+1))[2]
    c = img.getpixel((i,j+2))[0]+img.getpixel((i,j+2))[1]+img.getpixel((i,j+2))[2]
    if (a > b and c > b) or (a < b and c < b):
      pass
    else:
      img.putpixel((i,j),(255,255,255))

img.show()
