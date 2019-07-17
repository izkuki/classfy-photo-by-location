# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 17:33:57 2019

@author: izkuk
"""
import exifread
import os
#import sys
import shutil
import json
import pandas as pd
#sys.path.append(r'.\coordinate2address-master')

#初始文件夹在这里
path = r"D:\201808手机备份"
pathclassfy = path + "已整理"  #不把整理后的文件夹放在源文件夹之下是怕重复运行后重复分类

#通过经纬度查地址函数
def findlocation(alldata,lati,longi):
    item1 = {}
    dist1 = 0
    
    #遍历寻找最小值
    for item in alldata:
        latix1 = item['lati']
        longix1 = item['longi']
        dist = ((lati-latix1)**2 + (longi-longix1)**2)**0.5
        if item1 == {}:
            item1 = item
            dist1 = dist
            continue
        
        if dist1 > dist:
            dist1 = dist
            item1 = item
        
        continue
    
    return item1

#打开经纬度查询地址数据库
with open('map_data_new.json', 'r', encoding='utf8') as fp:
    json_str = json.load(fp)
fp.close()


#GPS格式转换
def gpstoint(gpsdata):
    gpsdata = gpsdata[1:-1]
    gpsdata1 = gpsdata.split(",")
    gpsdata2 = int(gpsdata1[0]) + int(gpsdata1[1])/60
    return gpsdata2

#归类文件类型
def groupfiles(alldatainput):
    allfolder = []
    onefolder = {}
    subcity = []
    urllist = []
    
    df = pd.DataFrame(alldatainput)
    df1 = df.sort_values(by = ['area0','area1','date0'])
    
    for name, group in df1.groupby('area0'):
        onefolder = {}
        subcity = name + ''.join(group['area1'].unique())
        urllist = group['urls'].values.tolist()
        onefolder['folder'] = subcity
        onefolder['filelist'] = urllist
        allfolder.append(onefolder)
    
    return allfolder

#建立及检测文件夹
def mkdir(pathtemp):
    # 去除首位空格
    pathtemp=pathtemp.strip()
    # 去除尾部 \ 符号
    pathtemp=pathtemp.rstrip("\\")
    # 判断路径是否存在 存在True 不存在   False
    isExists=os.path.exists(pathtemp)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录 创建目录操作函数
        os.makedirs(pathtemp) 
        print(pathtemp,'不存在，已创建')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(pathtemp,'已存在')
        return False




alldata_outsc = []  #省外
alldata_outcd = []  #省内
alldata_incd = []   #市内
alldata_noclass = []  #未分类
singledata = {}



i = 0
filecount = 0

#遍历源文件夹下所有文件
for root, dirs, files in os.walk(path):
    if len(files) != 0:
        print('正在分析文件夹',root,'中的',len(files),'个文件……')
        filecount = filecount + len(files)
        for file in files:
            
            photo_location_data = {} #清空一行数据
            
            ffp = os.path.join(root,file) #ffp = full file path
            

            
            f = open(ffp, 'rb')
            tags = exifread.process_file(f)
            
            latix = 0
            longix = 0

            #print(tags.keys())
            if 'GPS GPSLatitude' in tags.keys():   #取纬度
                lati = str(tags['GPS GPSLatitude'])
                latix = gpstoint(lati)
                #print(latix,end=' ')
                
            if 'GPS GPSLongitude' in tags.keys():    #取经度
                longi = str(tags['GPS GPSLongitude'])
                longix = gpstoint(longi)
                #print(longix,end=' ')

            if 'EXIF DateTimeOriginal' in tags.keys():    #取时间
                photodate = str(tags['EXIF DateTimeOriginal'])
                photodate = photodate[0:10]
                #print(photodate)


            if latix !=0 and longix !=0:
                photo_location_data = findlocation(json_str,latix,longix)
                photo_location_data['ffp'] = ffp
                photo_location_data['date'] = photodate
                #print(photo_location_data)
            else:
                photo_location_data['ffp'] = ffp
                photo_location_data['date'] = photodate                
            
            f.close()
            #singledata = {}
            #建立新列表
            singledata = {}
            if 'province' in photo_location_data:
                #四川省外以省+地级市命名
                if photo_location_data['province'] != '四川':  #四川省外以省+地级市命名
                    singledata['area0'] = photo_location_data['date'][0:4] + photo_location_data['date'][5:7] + photo_location_data['province'] 
                    singledata['area1'] = photo_location_data['city']                        
                    singledata['urls'] = photo_location_data['ffp']
                    singledata['date0'] = photo_location_data['date']
                    alldata_outsc.append(singledata)
                #四川省内成都市外以地级市+县命名    
                elif photo_location_data['province'] == '四川' and photo_location_data['city'] != '成都':
                    singledata['area0'] = photo_location_data['date'][0:4] + photo_location_data['date'][5:7] + photo_location_data['city'] 
                    singledata['area1'] = photo_location_data['county'][0:2]                        
                    singledata['urls'] = photo_location_data['ffp']
                    singledata['date0'] = photo_location_data['date']
                    alldata_outcd.append(singledata)
                #成都市内二圈城以外以成都+县命名，以内不加县 
                elif photo_location_data['province'] == '四川' and photo_location_data['city'] == '成都':
                    
                    singledata['area0'] = photo_location_data['date'][0:4] + photo_location_data['date'][5:7] +  photo_location_data['city']
                    if photo_location_data['county'] in ['武侯区','锦江区','金牛区','成华区','青羊区']:
                        singledata['area1'] = ''
                    elif photo_location_data['county'] in ['都江堰市','龙泉驿区','青白江区']:
                        singledata['area1'] = photo_location_data['county'][0:3]
                    else:
                        singledata['area1'] = photo_location_data['county'][0:2]                        
                    singledata['urls'] = photo_location_data['ffp']
                    singledata['date0'] = photo_location_data['date']
                    alldata_incd.append(singledata)
            #未分类区域不分类
            else:
                    singledata['area0'] = photo_location_data['date'][0:4] + photo_location_data['date'][5:7] + '未分类' 
                    singledata['area1'] = ''                        
                    singledata['urls'] = photo_location_data['ffp']
                    singledata['date0'] = photo_location_data['date']
                    alldata_noclass.append(singledata)

            

#合并数据列表，其实之前也可以直接复制，现在只是为了分析需要
alldata_all = alldata_outsc
alldata_all.extend(alldata_outcd)
alldata_all.extend(alldata_incd)
alldata_all.extend(alldata_noclass)


filecounting = 0
foldercount = 0

#对文件按分类进行归集，生成新的list
groupedfile = groupfiles(alldata_all)

mkdir(pathclassfy)

#循环copy到新目录
for eachitem in groupedfile:
    foldercount += 1
    filecounting = filecounting + len(eachitem['filelist'])
    
    print(eachitem['folder'],'共有',len(eachitem['filelist']),'个文件',end='')
    
    destpath = pathclassfy + "\\" + eachitem['folder']
    mkdir(destpath)
    

    countfive=5
    for eachdest in eachitem['filelist']:
        shutil.copy2(eachdest,destpath)
        
        #每5个文件输出一个进度符号，避免太长
        countfive = countfive + 1
        if countfive >5:
            countfive = countfive - 5
            print('#',end='')

              
    print('已完成',"%.0f%%" % (filecounting/filecount*100))

        

        
        
        
#总结输出  
print('')
print('')
print('')
print('*******************************************')
print('**                                       **')
print('**     共有',foldercount,'个文件夹， ',filecount,'个文件。  **')
print('**                                       **')
print('*******************************************')

