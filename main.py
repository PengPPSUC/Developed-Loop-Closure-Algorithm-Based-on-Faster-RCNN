# -*- coding: utf-8 -*-
from numpy import *
import os
import matplotlib.pyplot as plt
import math
from skimage import io
from PIL import Image



'''新建白色背景，新建两个文件夹，一个用来存放结果，一个用来存放坐标'''
newImg = Image.new("RGBA",(3264,2448),"white")
newImg.save("background.jpg","PNG")
path1=os.path.exists(os.getcwd()+'\\results')
if not path1:
    os.makedirs(os.getcwd()+'\\results')
path2=os.path.exists(os.getcwd()+'\\zuobiao')
if not path2:
    os.makedirs(os.getcwd()+'\\zuobiao ')



'''定义两个函数，分别用来读取result.txt的内容以及用来计数图片数量'''
def loadData(fileName):
    messege=[]
    with open(fileName) as txtData:
        lines=txtData.readlines()
        for line in lines:
            messege.append(line.split())
    return messege
def count(fileName):
    lines= loadData(fileName)
    a = 0
    b = "0"
    for line in lines:
        if b != line[0]:
            a += 1
        b = line[0]
    return a


'''对result.txt进行预处理，按照图片分类，新建图片专属坐标文件'''
a=0
x=loadData("result.txt")

b="0"
for line in x:

    if b != line[0]:
        a += 1
    i = "zuobiao\\" + str(a) + ".txt"
    out = open(str(i), 'a')
    for z in line:
        print(z,end=' ', file=out)
    print(file=out)
    b=line[0]


'''把每幅图的对应坐标点按照从左到右的顺序排序'''
a=1
while a<=count("result.txt"):
    i = "zuobiao\\" + str(a) + ".txt"
    x = loadData(i)
    if len(x) == 2:
        if (int(x[0][2]) + int(x[0][4])) >= (int(x[1][2]) + int(x[1][4])):
            x[0][2], x[0][4], x[1][2], x[1][4] = x[1][2], x[1][4], x[0][2], x[0][4]
            x[0][3], x[0][5], x[1][3], x[1][5] = x[1][3], x[1][5], x[0][3], x[0][5]
            x[0][1], x[1][1] = x[1][1], x[0][1]
    if len(x) == 3:
        if (int(x[0][2]) + int(x[0][4])) >= (int(x[1][2]) + int(x[1][4])):
            x[0][2], x[0][4], x[1][2], x[1][4] = x[1][2], x[1][4], x[0][2], x[0][4]
            x[0][3], x[0][5], x[1][3], x[1][5] = x[1][3], x[1][5], x[0][3], x[0][5]
            x[0][1], x[1][1] = x[1][1], x[0][1]
        if (int(x[1][2]) + int(x[1][4])) >= (int(x[2][2]) + int(x[2][4])):
            x[1][2], x[1][4], x[2][2], x[2][4] = x[2][2], x[2][4], x[1][2], x[1][4]
            x[1][3], x[1][5], x[2][3], x[2][5] = x[2][3], x[2][5], x[1][3], x[1][5]
            x[1][1], x[2][1] = x[2][1], x[1][1]
        if (int(x[0][2]) + int(x[0][4])) >= (int(x[1][2]) + int(x[1][4])):
            x[0][2], x[0][4], x[1][2], x[1][4] = x[1][2], x[1][4], x[0][2], x[0][4]
            x[0][3], x[0][5], x[1][3], x[1][5] = x[1][3], x[1][5], x[0][3], x[0][5]
            x[0][1], x[1][1] = x[1][1], x[0][1]
    a += 1

    out = open(str(i), 'w')
    for z in x:
        for r in z:
            print(r, end=' ', file=out)
        print(file=out)
    del x



'''输出结果包括图片相关信息，矢量图和叠加图'''
print("共有" + str(count("result.txt")) + "张图片需要处理")
r=1

while r<=count("result.txt"):
    x = []
    y = []
    del x[:]
    del y[:]
    xuhao = str(r)
    a ="zuobiao\\" + xuhao + ".txt"
    b =xuhao + ".jpg"
    c = "results\\"
    out = open(c + xuhao + ".txt", 'w')
    k = 0.95
    result = loadData(a)
    print(result[0][0], file=out)

    names = []
    for line in result:
        i = int(line[2]) / 2 + int(line[4]) / 2
        j = int(line[3]) / 2 + int(line[5]) / 2
        names.append(line[1])
        x.append(int(line[2]) / 2 + int(line[4]) / 2)
        y.append(int(line[3]) / 2 + int(line[5]) / 2)
        print(line[1] + "(" + str(i) + "," + str(j) + ")", file=out)

    plt.figure("叠加图")
    plt.plot(x, y, color='red', marker='.')
    ax = plt.gca()
    ax.xaxis.set_ticks_position('top')
    ax.invert_yaxis()

    i = 0

    plt.figure("叠加图")
    while (i < len(x) - 1):
        plt.arrow(x[i], y[i], (x[i + 1] - x[i]) * k, (y[i + 1] - y[i]) * k, width=20, color='red')
        distant = math.sqrt((x[i + 1] - x[i]) ** 2 + (y[i + 1] - y[i]) ** 2)
        angle = math.atan((y[i + 1] - y[i]) / (x[i + 1] - x[i]))
        print("distant from " + result[i][1] + " to " + result[i + 1][1] + " = " + str(distant), file=out)
        print("angle = " + str(180 * angle / math.pi * (-1)) + "°", file=out)
        i += 1
    plt.plot(x, y, color='red', marker='.')
    ax = plt.gca()
    ax.xaxis.set_ticks_position('top')
    ax.invert_yaxis()
    img = io.imread(b)
    io.imshow(img)
    plt.savefig(c+"叠加图" + xuhao + ".jpg")
    plt.axis('on')
    plt.close()

    plt.figure("矢量图")
    plt.plot(x, y, color='red', marker='.')
    ax = plt.gca()
    ax.xaxis.set_ticks_position('top')
    ax.invert_yaxis()
    img = io.imread('background.jpg')
    io.imshow(img)
    i = 0
    while (i < len(x) - 1):
        plt.arrow(x[i], y[i], (x[i + 1] - x[i]) * k, (y[i + 1] - y[i]) * k, width=20, color='red')
        i += 1
    plt.savefig(c+"矢量图" + xuhao + ".jpg")

    out.close()
    plt.close()
    print("已处理"+str(r)+"张图片,还剩" + str(count("result.txt")-r) + "张图片未处理")
    r+=1
