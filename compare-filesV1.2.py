#_*_coding:utf-8_*_
# !/etc/bin/env python2.7
#coded by wangjd@2017
#compare files 1.2
import os
import difflib
import Tkinter
import shutil

def check_path_exists(folder):
    if os.path.exists(folder) == False:
        # 创建输出路径
        os.mkdir(folder)
    else:
        #shutil.rmtree(folder, ignore_errors=True)
        # 清空目录
        #默认禁止删除，防止其他问题
        #os.mkdir(folder)
        pass
def readfile(filename):
    #读取文件内容
    handleFile=open(filename,'r')
    text = handleFile.read().splitlines()
    return text
    handleFile.close()

def compary_files(standardFile,original_File,log_path):
    #对比文档
    print standardFile
    print original_File
    print log_path
    #------
    stan=readfile(standardFile)
    ori=readfile(original_File)
    diff=difflib.HtmlDiff()
    p_txt=diff.make_file(stan,ori,context=True,numlines=0)
    #------
    # 创建报告文件
    f = open(log_path + "/" + "diff.html", 'a')
    # ............
    f.write("<meta charset='UTF-8'>")
    f.write("<a>这是"+original_File+"和"+standardFile+ "的对比不同的地方：</a>")
    # 解决中文乱码
    f.write(p_txt)
    f.close()
    #.............创建log文档
    d = difflib.Differ()
    log_diff = d.compare(stan, ori)
    open_log=open(log_path + "/" + "diff.log", 'a')
    open_log.write('\n'+"#这是" + fileName + "的对比不同的地方：<->"+'\n')
    open_log.write('\n'.join(list(log_diff)))
    open_log.close()
    #创建log文档方便shell查看
def show_files(standard_path,ori_path,log_path,len_f1):
    cycle_path=standard_path
    #初始化路径节点
    content=os.walk(cycle_path)
    for root,folder,file in content:
        for item_folder in folder:
            cycle_path=root+item_folder
            show_files(cycle_path,ori_path,log_path,len_f1)
        for item in file:
            goal_file_dir=root+"/"+item
            #print goal_file_dir
            #print ori_path+goal_file_dir[len_f1:]
            compary_files(goal_file_dir,ori_path+goal_file_dir[len_f1:],log_path)

def CreateWindow():
    top = Tkinter.Tk()
    # 进入消息循环
    top.title("标准文件对比工具")
    e = Tkinter.StringVar()

    # 刷新路径
    def refreshEntry():
        f1 = e1.get()
        f2 = e2.get()
        f3 = e3.get()
        len_f1=len(f1)
        #print f1+f2+f3
        #print len_f1
        check_path_exists(f3)
        show_files(f1, f2, f3,len_f1)
        alert = Tkinter.Tk()
        alert.title("完成通知！")
        Tkinter.Label(alert, text="**所有文档全部对比完成!").pack()
        Tkinter.Label(alert, text="查看对比报告HTML：" + f3 + "/" + "diff.html").pack()
        alert.mainloop()

    # 标准路径
    lable1 = Tkinter.Label(top, text="标准路径：").pack()
    e1 = Tkinter.StringVar()
    box1 = Tkinter.Entry(top, bg='lightblue', textvariable=e1)
    box1.pack(ipadx=100)
    e1.set("/var/standard")
    # 目标路径
    lable2 = Tkinter.Label(top, text="目标路径：").pack()
    e2 = Tkinter.StringVar()
    box2 = Tkinter.Entry(top, bg='lightblue', textvariable=e2)
    box2.pack(ipadx=100)
    e2.set("/var/ori")
    # 日志路径
    lable3 = Tkinter.Label(top, text="对比结果文档-生成路径：").pack()
    e3 = Tkinter.StringVar()
    box3 = Tkinter.Entry(top, bg='lightgray', textvariable=e3)
    box3.pack(side='left', ipadx=50)
    e3.set("/var/diff")
    # 核弹发射按钮
    Tkinter.Button(top, bg='lightgreen', text='开始对比', command=refreshEntry).pack(ipadx=10)
    top.mainloop()

if __name__ == '__main__':
    CreateWindow()
    #入口
