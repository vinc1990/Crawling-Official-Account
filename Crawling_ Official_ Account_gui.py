import os
import glob
import tkinter as tk
from tkinter import filedialog
import pickle
import requests
from lxml import etree
from PIL import Image

def downloadJPG(jpgfolder, url, rule):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    contents = requests.get(url, headers=headers)
    html = etree.HTML(contents.text)
    src_list = html.xpath(rule)
    for index, img_url in enumerate(src_list):
        if index < 9:
            index = "0" + str(index + 1)
        else:
            index = str(index + 1)
        with open(jpgfolder + index + ".jpg", 'wb') as f:
            f.write(requests.get(img_url).content)
            print("正在下载第" + index + "页\n", "地址：" + img_url)


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

def open_folder():
    current_directory = filedialog.askdirectory()
    var_folder_name.set(current_directory)
    """
    if current_directory:
        file_path = os.path.join(current_directory, "*.*")
        f = glob.glob(file_path)
        print(f)
    """
def start_crawing(object):
    jpgfolder = var_folder_name.get() + "/output/"
    if not os.path.exists(var_folder_name.get() + "/output"):
        os.mkdir(var_folder_name.get() + "/output")
    pdfFile = jpgfolder + "contract.pdf"
    url = var_link_add.get()
    rule = var_craw_rule.get()
    downloadJPG(jpgfolder, url, rule)
    combine2Pdf(jpgfolder, pdfFile)
    

if __name__ == "__main__":
    window = tk.Tk()
    window.title('爬取公众号-梁')
    window.geometry('400x200')
    window.resizable(0,0)

    tk.Label(window, text='保存位置:').place(x=10, y=30)
    tk.Label(window, text='链接地址:').place(x=10, y=80)
    tk.Label(window, text='爬取规则:').place(x=10, y=130)

    var_folder_name = tk.StringVar()
    var_folder_name.set('D:')
    entry_folder_name = tk.Entry(window, width=35,textvariable=var_folder_name)
    entry_folder_name.place(x=70, y=30)
    var_link_add = tk.StringVar()
    var_link_add.set('https://mp.weixin.qq.com/s/6IleHJNr8wxGGQAi4aAtbg')
    entry_link_add = tk.Entry(window, width=44, textvariable=var_link_add)
    entry_link_add.place(x=70, y=80)
    var_craw_rule = tk.StringVar()
    var_craw_rule.set("//div[contains(@class,'rich_media_content')]//p//img[contains(@class,'rich_pages')]/@data-src")
    entry_craw_rule = tk.Entry(window, width=44, textvariable=var_craw_rule)
    entry_craw_rule.place(x=70, y=130)

    btn_browse = tk.Button(window, text='浏览', width=6, height =1, command=open_folder)
    btn_browse.place(x=330, y=25)
    btn_start_craw = tk.Button(window, text='开始爬取', width=15, state = "normal", command=lambda : start_crawing(btn_start_craw))
    btn_start_craw.place(x=140, y=160)

    window.mainloop()