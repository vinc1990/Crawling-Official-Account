import os
import requests
from lxml import etree
from PIL import Image


def downloadJPG(jpgfolder, url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    contents = requests.get(url, headers=headers)
    html = etree.HTML(contents.text)
    src_list = html.xpath(
        "//div[contains(@class,'rich_media_content')]//p//img[contains(@class,'rich_pages')]/@data-src"
    )
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


if __name__ == "__main__":
    jpgfolder = "D:/11/"
    pdfFile = "D:/11/contract.pdf"
    url = "https://mp.weixin.qq.com/s/6IleHJNr8wxGGQAi4aAtbg"
    downloadJPG(jpgfolder, url)
    combine2Pdf(jpgfolder, pdfFile)