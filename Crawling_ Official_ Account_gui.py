import os
import glob
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import pickle
import requests
from lxml import etree
from PIL import Image
import threading
import re

#自定义的线程函数,防止程序无响应
def thread_it(func, *args):
  '''将函数放入线程中执行'''
  # 创建线程
  t = threading.Thread(target=func, args=args) 
  # 守护线程
  t.setDaemon(True) 
  # 启动线程
  t.start()

#爬取并保存图片函数
def downloadJPG(jpgfolder, url, rule):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    contents = requests.get(url, headers=headers)
    html = etree.HTML(contents.text)
    src_list = html.xpath(rule)
    pdfFile = html.xpath("//meta[contains(@property,'og:title')]/@content")[0]
    if not pdfFile:
        pdfFile = jpgfolder + "contract.pdf"
    else:
        print(pdfFile)
        folder_name = re.split(r'\s*[;,，\s]\s*',pdfFile)[0]
        os.mkdir(jpgfolder + folder_name)
        pdfFile = jpgfolder + folder_name +"/" + folder_name + ".pdf"
    if  not len(src_list):
        messagebox.showinfo(message="爬取失败，请更换规则重试")
        return
    for index, img_url in enumerate(src_list):
        if index < 9:
            number = "0" + str(index + 1)
        else:
            number = str(index + 1)
        with open(jpgfolder + number + ".jpg", 'wb') as f:
            f.write(requests.get(img_url).content)
        print("正在下载第" + number + "页\n", "地址：" + img_url)
        pb["value"] += 99 / len(src_list)
        pb.update()
    combine2Pdf(jpgfolder, pdfFile)

#将图片转换为PDF函数
def combine2Pdf(folderPath, pdfFilePath):
    files = os.listdir(folderPath)
    jpgFiles = []
    sources = []
    for file in files:
        if 'jpg' in file:
            jpgFiles.append(folderPath + file)
    jpgFiles.sort()
    output = Image.open(jpgFiles[0])
    jpgFiles.pop(0)
    for file in jpgFiles:
        jpgFile = Image.open(file)
        if jpgFile.mode == "RGB":
            jpgFile = jpgFile.convert("RGB")
        sources.append(jpgFile)
    output.save(pdfFilePath, "pdf", save_all=True, append_images=sources)
    print("合成PDF文件成功")
    pb["value"] = 100
    pb.update()

#选择文件夹函数
def open_folder():
    current_directory = filedialog.askdirectory()
    var_folder_name.set(current_directory)
    """
    if current_directory:
        file_path = os.path.join(current_directory, "*.*")
        f = glob.glob(file_path)
        print(f)
    """

#开始爬取入口函数
def start_crawing(object):
    pb["value"] = 0
    pb.update()
    disable_widget(object)
    jpgfolder = var_folder_name.get() + "/output/"
    if not os.path.exists(var_folder_name.get() + "/output"):
        os.mkdir(var_folder_name.get() + "/output")
    url = var_link_add.get()
    if var.get() == 0:
        rule = var_craw_rule1.get()
    elif var.get() == 1:
        rule = var_craw_rule2.get()
    else:
        rule = var_craw_rule3.get()
    if rule == '':
        messagebox.showwarning(message="爬取规则不能为空！！")
        return
    downloadJPG(jpgfolder, url, rule)
    enable_widget(object)

#启用组件    
def enable_widget(object):
    object.configure(state='enable')
    object.update()

#禁用组件
def disable_widget(object):
    object.configure(state='disable')
    object.update()

if __name__ == "__main__":
    window = tk.Tk()
    window.title('爬取公众号-梁')
    winWidth = 450
    winHeight = 320
    # 获取屏幕分辨率
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    # 设置窗口初始位置在屏幕居中
    window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, int((screenWidth - winWidth) / 2), int((screenHeight - winHeight) / 2)))
    window.geometry('450x320')
    window.resizable(0,0)

    ttk.Label(window, text='保存位置').place(x=25, y=20)
    ttk.Label(window, text='链接地址').place(x=25, y=70)


    var_folder_name = tk.StringVar()
    var_folder_name.set('D:')
    entry_folder_name = ttk.Entry(window, width=40,textvariable=var_folder_name)
    entry_folder_name.place(x=95, y=20)
    var_link_add = tk.StringVar()
    var_link_add.set('https://mp.weixin.qq.com/s/6IleHJNr8wxGGQAi4aAtbg')
    entry_link_add = ttk.Entry(window, width=48, textvariable=var_link_add)
    entry_link_add.place(x=95, y=70)

    frm1 = tk.Frame(window, height=145, width=434,bd=1,relief='sunken').place(x=8,y=110)

    var = tk.IntVar()
    var.set(0)
    r1 = ttk.Radiobutton(frm1, text='精确规则', variable=var, value=0,command=lambda : disable_widget(entry_craw_rule3))
    r1.place(x=10, y=120)
    r2 = ttk.Radiobutton(frm1, text='模糊规则', variable=var, value=1,command=lambda : disable_widget(entry_craw_rule3))
    r2.place(x=10, y=170)
    r3 = ttk.Radiobutton(frm1, text='自定义规则', variable=var, value=2,command=lambda : enable_widget(entry_craw_rule3))
    r3.place(x=10, y=220)

    var_craw_rule1 = tk.StringVar()
    var_craw_rule1.set("//div[contains(@class,'rich_media_content')]//p//img[contains(@class,'rich_pages')]/@data-src")
    entry_craw_rule1 = ttk.Entry(frm1, width=48, textvariable=var_craw_rule1, state = 'disable')
    entry_craw_rule1.place(x=95, y=120)

    var_craw_rule2 = tk.StringVar()
    var_craw_rule2.set("//div[contains(@class,'rich_media_content')]//img[contains(@data-type,'jpeg')]/@data-src")
    entry_craw_rule2 = ttk.Entry(frm1, width=48, textvariable=var_craw_rule2, state = 'disable')
    entry_craw_rule2.place(x=95, y=170)

    var_craw_rule3 = tk.StringVar()
    entry_craw_rule3 = ttk.Entry(frm1, width=48, textvariable=var_craw_rule3, state = 'disable')
    entry_craw_rule3.place(x=95, y=220)

    btn_browse = ttk.Button(window, text='浏览', width=6, command=open_folder)
    btn_browse.place(x=385, y=18)
    btn_start_craw = ttk.Button(window, text='开始爬取', width=15, state = "normal", command=lambda : thread_it(start_crawing, btn_start_craw))
    btn_start_craw.place(x=170, y=285)

    pb = ttk.Progressbar(window, length = 434, value = 0,  mode="determinate", orient=tk.HORIZONTAL)
    pb.place(x=8,y = 255)
    window.mainloop()