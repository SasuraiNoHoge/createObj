from PIL import Image
import numpy as np

def outerProduct(x,y,z,xd,yd,zd):
    a = y*zd - z*yd
    b = z*xd - x*zd
    c = x*yd - y*xd
    a /= np.sqrt(x*x + y*y + z*z) * np.sqrt(xd*xd + yd*yd + zd*zd)
    b /= np.sqrt(x*x + y*y + z*z) * np.sqrt(xd*xd + yd*yd + zd*zd)
    c /= np.sqrt(x*x + y*y + z*z) * np.sqrt(xd*xd + yd*yd + zd*zd)
    return a, b, c

def vector(x1,y1,z1,x2,y2,z2,xo,yo,zo):
    return outerProduct(x1-xo,y1-yo,z1-zo,x2-xo,y2-yo,z2-zo)

#sixdot2x3

#手の深度画像
#img_depth = Image.open('imageLoader/test_depth.jpg')
 #皿の画像

#実験画像
dot_origin = Image.open('imageLoader/circle.jpg')

#マスク画像
mask = Image.open('imageLoader/circle.jpg')

w, h = mask.size

dot = dot_origin.resize((w,h))
width, height = dot.size

#RGB値に+フラグを追加した配列を設定
img_pixels = np.array([[
    (dot.getpixel((x,y))[0],dot.getpixel((x,y))[1],dot.getpixel((x,y))[2],0)
for x in range(width)] for y in range(height)])

#マスク画像の配列も生成
mask_resize = mask.resize((width,height))
img_resize = img.resize((width,height))

mask_pixels = np.array([[
    (mask_resize.getpixel((x,y))[0],mask_resize.getpixel((x,y))[1],mask_resize.getpixel((x,y))[2],0)
for x in range(width)] for y in range(height)])

cnt = 0

print("/////////////////////////////")

with open("circle.obj", "w") as f:
    f.write("circle\ng circle\n")

#頂点の座標を保存
s = ''
vlist = []

for y in range(width*height):
    if mask_pixels[(int)(y/width),y%width][0] >= 250 and mask_pixels[(int)(y/width),y%width][1] >= 250 and mask_pixels[(int)(y/width),y%width][2] >= 250:
        #img_resize.putpixel((y%width,int(y/width)),(0, 0, 0))
        mask_pixels[(int)(y/width),y%width][3] = 1
        #print(mask_pixels[(int)(y/width),y%width][3])
        v = 'v '
        w = str(y%width)
        h = str((int)(y/width))
        #RGBのR値だけ取ってる
        d = str(img_pixels[(int)(y/width),y%width][0]*-1)
        #debug用
        #d = str(0)
        #img_pixels[(int)(y/width),y%width][0] = 0
        s += v + w + ' ' + h + ' ' + d+ '\n'
        v = ''
        
        vlist.append((y%width,(int)(y/width),img_pixels[(int)(y/width),y%width][0]))

#法線を扱う
normalList = []
nom = ''
skip = 0
with open("circle.obj", "a") as f:
    f.write(s)

print("/////////////////////////////")

fi=''
#次の行に入ったかを調べるフラグ
row =-1
nextRow = -1
startColum = -1
nextStartColum = -1
tmpNextStartColum = -1
endColum = -1
nextEndColum = -1
rowEnd = []
for i in range(height):
    rowEnd.append(-1)

cnt = 0

y = 0
while y <= (width*height)-1:
#for y in range(width*height):
    percent = y/(width*height-1)*100 
    if y/(width*height-1)*100 != percent:
        percent = y/(width*height-1)*100
        print(percent+'/100')
    skip = 0
    #print('test')

    #print({'画素番号':y})
    if row != (int)(y/width):
        row = (int)(y/width)
        nextRow = row + 1
        if nextRow == len(rowEnd):
            break
        startColum = row*width
        endColum = startColum + width -1
        nextStartColum = nextRow*width
        nextEndColum = nextStartColum + width - 1
        #print({'row':row, 'startColum':startColum,'endColum':endColum})
        #print({'nextRow':nextRow, 'nextStartColum':nextStartColum,'nextEndColum':nextEndColum})
        
        #ここから行の最後の列の要素を調べる
        if rowEnd[row] == -1 or rowEnd[nextRow]==-1:
            
            for i in reversed(range(y+1,endColum+1)):
                if mask_pixels[row,i%width][3] != 0:
                    rowEnd[row] = i%width
                    endColum = i
                    break
            for i in range(y+1,endColum+1):
                  if mask_pixels[row,i%width][3] != 0:
                    startColum = i
                    break
            if rowEnd[row] == -1:
                y = nextStartColum
                
                continue
            for i in reversed(range(nextStartColum,nextEndColum+1)):
                if mask_pixels[nextRow,i%width][3] != 0:
                    rowEnd[nextRow] = i%width
                    nextEndColum = i
                    break    
            for i in range(nextStartColum,nextEndColum+1):
                 if mask_pixels[nextRow,i%width][3] != 0:
                    nextStartColum = i
                    tmpNextStartColum = nextStartColum
                    break
            if rowEnd[nextRow] == -1:
                y = nextStartColum
                
                continue
        else:
            if rowEnd[row] == -1:
                
                y = nextStartColum
                
                continue
    if y > endColum-1:
        nextStartColum = tmpNextStartColum 
        y = nextStartColum
        #print(y)
        continue
    #print(mask_pixels[(int)(y/width),y%width][3])
    #y < rowEndは1行に2画素存在しなければ描画しないために使用
    if mask_pixels[row,y%width][3] != 0 and y%width < rowEnd[row]:
         for p2 in range(y+1,endColum+1):
            if mask_pixels[row,p2%width][3] == 0:
                break
            if skip == 1:
                break        

            for p4 in range(y+width,nextEndColum):
                
                if skip == 1:
                    break
                for p3 in range(p4+1,nextEndColum+1):
                    if mask_pixels[nextRow,p3%width][3] != 0 and mask_pixels[nextRow,p4%width][3] != 0 and p4 -y == width and p3 - p2 == width and p3 - p4 == 1:
                        #外積を求める
                        a,b,c = vector(p2%width,row,img_pixels[row,p2%width][0],p4%width,nextRow,img_pixels[nextRow,p4%width][0],y%width,row,img_pixels[row,y%width][0])
                        #print({'y':y,'p2':p2,'p3':p3,'p4':p4})
                        #print({'yx':y%width,'p2x':p2%width,'p3x':p3%width,'p4x':p4%width})
                        #print({'yy':row,'p2y':row,'p3y':nextRow,'p4y':nextRow})
                        #print({'a':a,'b':b,'c':c})

                        #法線が存在するかの確認
                        if (a,b,c) in normalList:
                            yno = normalList.index((a,b,c))
                            yno += 1
                        else:
                            normalList.append((a,b,c))
                            yno = len(normalList)
                            nom += 'vn '+ str(a) + ' ' + str(b) + ' ' + str(c) +'\n'

                        a,b,c = vector(p3%width,nextRow,img_pixels[nextRow,p3%width][0],y%width,row,img_pixels[row,y%width][0],p2%width,row,img_pixels[row,p2%width][0])

                        #法線が存在するかの確認
                        if (a,b,c) in normalList:
                            p2no = normalList.index((a,b,c))
                            p2no += 1
                        else:
                            normalList.append((a,b,c))
                            p2no = len(normalList)
                            nom += 'vn '+ str(a) + ' ' + str(b) + ' ' + str(c) +'\n'

                        a,b,c = vector(p4%width,nextRow,img_pixels[nextRow,p4%width][0],p2%width,row,img_pixels[row,p2%width][0],p3%width,nextRow,img_pixels[nextRow,p3%width][0])
                        
                        #法線が存在するかの確認
                        if (a,b,c) in normalList:
                            p3no = normalList.index((a,b,c))
                            p3no += 1
                        else:
                            normalList.append((a,b,c))
                            p3no = len(normalList)
                            nom += 'vn '+ str(a) + ' ' + str(b) + ' ' + str(c) +'\n'

                        a,b,c = vector(y%width,row,img_pixels[row,y%width][0],p3%width,nextRow,img_pixels[nextRow,p3%width][0],p4%width,nextRow,img_pixels[nextRow,p4%width][0])
                        
                        #法線が存在するかの確認
                        if (a,b,c) in normalList:
                            p4no = normalList.index((a,b,c))
                            p4no += 1
                        else:
                            normalList.append((a,b,c))
                            p4no = len(normalList)
                            nom += 'vn '+ str(a) + ' ' + str(b) + ' ' + str(c) +'\n'

                        v1 = vlist.index((y%width,row,img_pixels[row,y%width][0]))
                        v2 = vlist.index((p2%width,row,img_pixels[row,p2%width][0]))
                        v3 = vlist.index((p3%width,nextRow,img_pixels[nextRow,p3%width][0]))
                        v4 = vlist.index((p4%width,nextRow,img_pixels[nextRow,p4%width][0]))
                        v1+=1
                        v2+=1
                        v3+=1
                        v4+=1
                        #print(v1)

                        fi += 'f ' + str(v1) + '//'+str(yno)+' ' + str(v2) + '//'+str(p2no)+' ' + str(v3) + '//'+str(p3no)+' ' + str(v4) + '//'+str(p4no)+'\n'
                        skip = 2
                        nextStartColum = p3
                        skip = 1
                        break
    y+=1
                
print("/////////////////////////////")

with open("circle.obj", "a") as f:
    f.write(nom)
    f.write(fi)

#img_depth.show()
#img_resize.show()
#img.show()