#-*-coding:utf-8-*-
#/etc/bin/python
#Programed by wangjd@2017
import os
import Tkinter
import shutil
import difflib

def create_Window():
    top = Tkinter.Tk()
    # 进入消息循环
    top.title("标准文件对比工具")
    e=Tkinter.StringVar()
    #刷新路径
    def refreshEntry():
        f1 = e1.get()
        f2 = e2.get()
        f3 = e3.get()
        main_way(f1,f2,f3)
    #标准路径
    lable1 = Tkinter.Label(top, text="标准路径：").pack()
    e1 = Tkinter.StringVar()
    box1 = Tkinter.Entry(top,bg='lightblue',textvariable = e1)
    box1.pack(ipadx=100)
    e1.set("/var/standard")
    #目标路径
    lable2 = Tkinter.Label(top, text="目标路径：").pack()
    e2 = Tkinter.StringVar()
    box2 = Tkinter.Entry(top,bg='lightblue',textvariable = e2)
    box2.pack(ipadx=100)
    e2.set("/var/test")
    #日志路径
    lable3 = Tkinter.Label(top, text="对比结果文档-生成路径：").pack()
    e3 = Tkinter.StringVar()
    box3 = Tkinter.Entry(top,bg='lightgray', textvariable=e3)
    box3.pack(side='left',ipadx=50)
    e3.set("/var/diff")
    # 核弹发射按钮
    Tkinter.Button(top, bg='lightgreen', text='开始对比', command=refreshEntry).pack(ipadx=10)
    top.mainloop()
def main_way(f1,f2,log_path):
    #获取输入的标准路径和对比路径
   #print "f1:"+f1+"-----f2:"+f2
   if os.path.exists(log_path) == False:
        # 创建输出路径
     os.mkdir(log_path)
   else:
     #shutil.rmtree(log_path, ignore_errors=True)
     #清空目录
     #默认禁止删除目录，防止其他问题
     #os.mkdir(log_path)
     pass

   for root, dirs, files in os.walk(f1):
      for fileName in files:
         findOriginalpath(fileName,f1,f2,log_path)
   alert=Tkinter.Tk()
   alert.title("完成通知！")
   a0 = Tkinter.Label(alert, text="**所有文档全部对比完成!").pack()
   a1=Tkinter.Label(alert,text="查看对比报告HTML：" + log_path + "/" + "diff.html").pack()
   a2 =Tkinter.Label(alert, text="或者查看对比报告log：" + log_path + "/" + "diff.log").pack()
   alert.mainloop()
def readfile(filename):
    #读取文件内容
    handleFile=open(filename,'r')
    text = handleFile.read().splitlines()
    return text
    handleFile.close()

def findOriginalpath(FindpathFilename,f1,f2,log_path):
    # print "++++现实文档文件++++"
     for root,dirs,files in os.walk(f2):
        for fileName in files:
           compare_filename=fileName
           #对比的文件名
           try:
               if compare_filename == FindpathFilename:
                   #difflib生成报告
                   ori=readfile(f2+"/"+fileName)
                   stan=readfile(f1+"/"+fileName)
                   diff=difflib.HtmlDiff()
                   p_txt=diff.make_file(stan, ori,context=True,numlines=0)

                   #创建报告文件
                   f = open(log_path +"/"+ "diff.html", 'a')
                   #............
                   f.write("<meta charset='UTF-8'>")
                   f.write("<a>这是"+fileName+"的对比不同的地方：</a>")
                   #解决中文乱码
                   f.write(p_txt)
                   f.close()
                   #-------------
                   #创建报告文件HTML
                   #---------
                   #创建log文档方便shell查看
                   stan_lines = stan
                   ori_lines = ori
                   d = difflib.Differ()
                   log_diff = d.compare(stan_lines, ori_lines)
                   open_log=open(log_path + "/" + "diff.log", 'a')
                   open_log.write('\n'+"#这是" + fileName + "的对比不同的地方：<->"+'\n')
                   open_log.write('\n'.join(list(log_diff)))
                   open_log.close()
                   #创建log文档方便shell查看

               else:
                   exit()
           except:StandardError
#main 入口
if __name__ == '__main__':
    #mian()
    create_Window()
