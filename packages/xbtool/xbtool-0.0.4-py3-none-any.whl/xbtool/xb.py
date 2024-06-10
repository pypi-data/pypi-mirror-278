import time,datetime
import os
import pyodbc
import pandas as pd
from pyecharts.charts import *
from sqlalchemy import create_engine,text
import requests
import json
import configparser
import base64
import hashlib
import matplotlib.pyplot as plt
import numpy as np

class qywx:
    def send_picture(webhook_url,picture_name):
        #发送图片到企业微信
        with open(picture_name, 'rb') as f:
            image_data = f.read()
        md5 = hashlib.md5(image_data).hexdigest()
        data = {
            "msgtype": "image",
            "image": {
                "base64": str(base64.b64encode(image_data), encoding='utf-8'),
                "md5": md5
            }
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(webhook_url, json=data, headers=headers)
        if response.status_code == 200 and response.json()['errcode'] == 0:
            print('图片消息发送成功')
        else:
            print('图片消息发送失败：', response.json())
        
    def send_message(webhook_url,txt):
        # 发送消息到企业微信
        message = {
            'msgtype': 'text',
            'text': {'content': txt}
        }
        json_message = json.dumps(message)
        response = requests.post(webhook_url, data=json_message)
class itw:
    def send_message(url,txt):
        # 发送消息到i通威
        header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
        }
        message ={
        "content": txt
        }
        message_json = json.dumps(message)
        info = requests.post(url=url,data=message_json,headers=header)#i通威发消息
        
class myini:
    def get_value(file_path, section, key):
        #file_path：配置文件, section：节, key：值
        config = configparser.ConfigParser()
        config.read(file_path)
        value = config.get(section, key, raw=True)
        return value

    def set_value(file_path, section, key, new_value):
        #替换配置文件里面节、键对应的值
        #file_path：配置文件, section：节, key：值，new_value：新值
        config = configparser.RawConfigParser()
        config.read(file_path)
        if config.has_option(section, key):
            if config.get(section, key,raw=True) != new_value:
                new_value="{}".format(new_value)
                config.set(section, key, new_value)
                with open(file_path, 'w') as config_file:
                    config.write(config_file)
                return "前后分档不一致,已修改"
            else:
                return "前后分档一致"
        else:
            return "没有对应的键"
        
class access:
    def to_connect(path, sql):   
        try:  
            # 使用with语句自动管理数据库连接和游标的生命周期  
            with pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' + 'DBQ=' + path + ';') as conn:  
                with conn.cursor() as cur:  
                    cur.execute(sql)    
                    rows = cur.fetchall()
                    rows=np.array(rows)
                    data = pd.DataFrame(rows,columns=[col[0] for col in cur.description])
                    return data
        except Exception as e:  
            print(f"An error occurred: {e}")
            return None
    def to_connect1(path, sql):   
        try:  
            # 使用with语句自动管理数据库连接和游标的生命周期  
            with pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' + 'DBQ=' + path + ';') as conn:  
                with conn.cursor() as cur:  
                    cur.execute(sql)    
                    rows = cur.fetchall()
                    return rows  
        except Exception as e:  
            print(f"An error occurred: {e}")
            return None
    
    def to_connect2(path, sql):
        engine=None
        try:
            # 创建SQLAlchemy引擎
            def connection():
                return pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' + 'DBQ=' + path + ';')
            
            engine = create_engine('access+pyodbc://', creator=connection)
            
            # 使用上下文管理器确保连接关闭
            with engine.connect() as con:
                data = pd.read_sql(text(sql), con)
            return data
        except Exception as e:
            return str(e)
        finally:
            if engine is not None:
                engine.dispose()

def data_to_image(data,data1,data2,data3,filename,yyy):
    # 绘制折线图并保存
    fig,ax=plt.subplots(2,2,figsize=(10,8))
    ax[0][0].plot(data)
    ax[0][0].set_ylim([min(data)-0.1,max(data)+0.1])
    ax[0][0].set_title('eta')
    
    ax[0][1].plot(data1)
    ax[0][1].set_ylim([min(data1)-0.1,max(data1)+0.1])
    ax[0][1].set_title('isc')
    
    ax[1][0].plot(data2)
    ax[1][0].set_ylim([min(data2)-1,max(data2)+1])
    ax[1][0].set_title('ff')
    
    ax[1][1].plot(data3)
    ax[1][1].set_ylim([min(data3)-0.4,max(data3)+0.4])
    ax[1][1].set_title('flash')
    fig.suptitle(yyy)
    plt.savefig(filename)
    plt.close(fig)

def cliff_datas(filename,lst,condition,threshold=2):
    lst=block_mean(lst)
    if abs(lst[0] - lst[-1]) < condition:
        print("数据正常")
        return 0
    #断崖式数据识别1
    for i in range(len(lst) - 1):
        print(f"第{i}次循环开始")
        if abs(lst[i] - lst[i + 1]) > condition:
            print(lst[i] - lst[i + 1])
            count=1
            for y in range(i+2, len(lst) - 1):  # 从i开始到lst的最后一个元素
                if abs(lst[i] - lst[y]) < condition:  # 检查lst[i]和lst[y]
                    print(f"{lst[i]}-{lst[y]}={abs(lst[i] - lst[y])}")
                    break
                else:
                    count +=1
                    if count>threshold:
                        print("数据异常")
                        ss=""
                        for i in lst:
                            ss=ss+str(i)+","
                        write_to_txt(ss,filename)
                        return False
        else:
            continue
        
def my1(lst,fz=2):
    #中间异常值处理
    yc=0
    for i in range(len(lst)-1):
        count=0
        for y in range(i+1,len(lst)):
            if abs(lst[i]-lst[y])>fz :
                count=count+1
            else:
                if count>0 and i<5:
                    lst[i+1]=sum(lst[:i+1])/len(lst[:i+1])
                    break
                elif count>0 and i>5:
                    lst[i+1]=sum(lst[i-5:i+1])/len(lst[i-5:i+1])
                    break
                else:
                    break
            print(f"{count},{len(lst[i:])}")
            if count==len(lst[i:])-2:
                yc +=1
                break
        if yc==1:
            yc=0
            return lst          
    return lst

def cliff_data(filename,lst,bianlian,ss):
    lst=block_mean(lst)
    lst=my1(lst,ss)
    #异常数据识别2
    if abs(lst[0]-lst[-2])>bianlian:
        if abs(lst[0]-lst[-1])>bianlian:
            if abs(lst[1]-lst[-1])>bianlian:
                if abs(lst[1]-lst[-1])>bianlian:
                    print("数据异常")
                    ss=""
                    for i in lst:
                        ss=ss+str(i)+","
                    write_to_txt(ss,filename)
                    return False
    else:
        pass
        
def write_to_txt(string,filename):
    #写入txt文件
    with open(filename,"a")as f:
        f.write(string+"\n")

def block_mean(nums):
    #计算平均值
    group=[]
    for i in range(1,11):
        x=(i-1)*200
        x1=i*200
        mean=sum(nums[x:x1])/200
        mean=round(mean,3)
        group.append(mean)
        print(mean)
    return group
        
def date_class(ban):
    #自动计算当前班次
    config = configparser.ConfigParser()
    config.read(r"D:\alarm\user.ini")
    day_shift = config.get(ban, 'day_shift')
    night_shift = config.get(ban, 'night_shift')
    now = datetime.datetime.now()
    hour = now.hour + now.minute / 60 
    date = datetime.date.today()
    if hour < 8.5:
        date = date - datetime.timedelta(days=1)
        shift = night_shift
    elif hour > 20.5:
        shift = night_shift
    else:
        shift = day_shift
    date=date.strftime("%Y-%#m-%#d")
    return shift,date


def exception_handling(nums):
    # 对传入的数据10组计算判断是否异常
    count = 0
    if abs(nums[0]-nums[-1])<0.05:
        return True
    for i in range(2):
        loses = [abs(nums[i] - nums[j]) for j in range(9, 7, -1)]
        print(loses)
        if all(lose_s <= 0.03 for lose_s in loses):
            count = 0
        else:
            count += 1
            if count >= 2:
                return False
            
def print_file_time(file_path):
    #打印文件创建时间
    created_time=os.path.getctime(file_path)
    created_datetime=datetime.datetime.fromtimestamp(created_time).hour
    return created_datetime

def abnormal_cause(x):
    #获取异常原因
	x=str.upper(x)
	if "TXCW" in x:
		return("生产测试【图形错误】")
	elif "QDFG" in x:
		return("生产测试【前段返工】")
	elif "SWFG" in x:
		return("生产测试【丝网返工】")
	elif "HB" in x:
		return("生产测试【黑边】")
	elif "JZCC" in x or "GDW" in x:
		return("生产测试【静置重测】")
	elif "PY" in x or "GDW" in x:
		return("生产测试【偏移】")
	elif "YL" in x or "GDW" in x:
		return("生产测试【隐裂】")
	else:
		return("待排查")

def write_ini():
    #自动更新班次（A/B)
    df_ip=pd.read_csv(r"D:\alarm\IP.csv")
    now_time=datetime.datetime.now()
    fnow_hour=now_time.hour+now_time.minute / 60
    if fnow_hour>8.5 and fnow_hour<20.5:
        banci="day_shift"
    else:
        banci="night_shift"
    for i in (1,20):
        ip = df_ip['IP'][i]
        line=df_ip['Line'][i]
        path=df_ip['Path'][i]
        partment=df_ip['Partment'][i]
        if partment=="S4":
            shift,date=date_class("S4")
        else:
            shift,date=date_class("S5")
        filename=date + "-" + line + "-" + shift + ".mdb"
        path1 = f"\\\{ip}{path}\{filename}"
        try:
            csc=print_file_time(path1)
            if (fnow_hour<20.5 and csc<12) or (fnow_hour>20.5 and csc>12) :
                pass
            else:
                if shift=="A":
                    shift="B"
                else:
                    shift="A"
                filename=date + "-" + line + "-" + shift + ".mdb"
                path1 = f"\\\{ip}{path}\{filename}"
                print(path1)
                if (fnow_hour<20.5 and csc<12) or (fnow_hour>20.5 and csc>12) :
                    pzfile_write(partment,banci,)
        except:
            if shift=="A":
                shift="B"
            else:
                shift="A"
            print(shift)
            filename=date + "-" + line + "-" + shift + ".mdb"
            path1 = f"\\\{ip}{path}\{filename}"
            csc=print_file_time(path1)
            if (fnow_hour<20.5 and csc<12) or (fnow_hour>20.5 and csc>12) :
                pzfile_write(partment,banci,shift)
        time.sleep(2)
        
def kaiban(chengjian):
    #对班的文件名，批次号和时间
    df_ip=pd.read_csv(r"D:\alarm\IP.csv")
    now_time=datetime.datetime.now()
    date = datetime.date.today()
    fnow_hour=now_time.hour+now_time.minute / 60
    if fnow_hour<20.5:
        date_db = date - datetime.timedelta(days=1)
        date_db = date_db.strftime("%Y-%#m-%#d")
        db_time=date_db
    else:
        date_d = date.strftime("%Y-%#m-%#d")
        db_time=date_d
    if chengjian=="S4":
        i=1
    else:
        i=20
    ip = df_ip['IP'][i]
    line=df_ip['Line'][i]
    path=df_ip['Path'][i]
    partment=df_ip['Partment'][i]
    for x in ("A","B"):
        filename=db_time + "-" + line  + "-"+ x + ".mdb"
        path_s = f"\\\{ip}{path}\{filename}"
        try:
           xx=print_file_time(path_s)
        except:
            print("文件不存在")
        if fnow_hour<20.5 and 22>xx>=19:
            return x,db_time
        elif fnow_hour>20.5 and 9>xx>=7:
            return x,db_time
    
def shujun():
    #查看收集的电池片
    path1=r"\\10.8.138.183\Halm\PVCTData\2023-7-11-2B-A.mdb"
    cnn = pypyodbc.win_connect_mdb('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+path1)
    df_num=pd.read_sql('select count(uniqueid) from halm_results WHERE bin=6',cnn)
    x2=df_num.iloc[0,0]
    xx="现在BIN-6已经收集了：{}pcs".format(x2)
    dingmessages(xx)
    
def sbanci(today):
    #三班倒班次自动更新
    #today=datetime.datetime.today()
    target_date=datetime.datetime(2023,10,15)
    tan=(today-target_date).days+1
    tan=tan%18
    print(tan)
    D=""
    N=""
    D_DB=""
    N_DB=""
    if tan==0:
         D="B"
         N="C"
    elif tan<=3:
         D="A"
         N="C"
    elif tan<=6:
         D="A"
         N="B"
    elif tan<=9:
         D="C"
         N="B"
    elif tan<=12:
         D="C"
         N="A"
    elif tan<=15:
         D="B"
         N="A"
    elif tan<=18:
         D="B"
         N="C"
    else:
        print("数据1异常")
        
    if tan==0:
         D_DB="C"
         N_DB="B"
    elif tan<=4:
         D_DB="C"
         N_DB="A"
    elif tan<=6:
         D_DB="B"
         N_DB="A"
    elif tan<=10:
         D_DB="B"
         N_DB="C"
    elif tan<=12:
         D_DB="A"
         N_DB="C"
    elif tan<=16:
         D_DB="A"
         N_DB="B"
    elif tan<=17:
         D_DB="C"
         N_DB="B"
    else:
        print("数据2异常")
    
    return D,N,D_DB,N_DB

def lstzws(data):
    #求一个列表的中位数
    data.sort()
    s=int(len(data)/2)
    mid=0
    if len(data)%2==0:
        mid=(data[s-1]+data[s])/2
    else:
        mid=data[s]
    return mid

