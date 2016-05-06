# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET,require_POST
from django.http import StreamingHttpResponse
import json
from PIL import Image,ImageDraw,ImageFont,ImageEnhance
import time
import sys
import os
import md5
import requests
from corelib.decorators import json_view

reload(sys)
sys.setdefaultencoding('utf-8')

first_word = unicode("妈妈是个美人儿")
second_word = unicode("我想对你说")
third_word = unicode("母亲节快乐！")
color = (255, 100, 0, 255)
<<<<<<< HEAD
hwzfnt = ImageFont.truetype('hwzs.TTF', 50)
fnt = ImageFont.truetype('FZLTHJW.TTF', 30)
=======
hwzfnt = ImageFont.truetype('fzqkbys.TTF', 50)
fnt = ImageFont.truetype('sxsl.ttf', 30)
>>>>>>> 3428ed2bc5bfcf11742e26fe5965f934c3cbe805
width = 529.0
height = 742.0
row_height = 33
word1_y = 525


def getRandomString():
    num = int(time.time())%10
    random = os.urandom(num)
    m1 = md5.new()
    random = random+str(time.time())
    m1.update(random)
    return m1.hexdigest()

def resize(baseImage):
    f1 = width / baseImage.size[0]
    f2 = height / baseImage.size[1]
    factor = f2
    new_width = int(baseImage.size[0] * factor)
    new_height = int(baseImage.size[1] * factor)
    baseImage = baseImage.resize((new_width,new_height),Image.ANTIALIAS)
    baseImage = crop(baseImage)
    return baseImage

def crop( baseImage):
    if baseImage.size[0] > width or baseImage.size[1] > height:
        x = 0
        y = 0
        if baseImage.size[0] > width:
            x = (baseImage.size[0] - width)/2
        if baseImage.size[1] > height:
            y = (baseImage.size[1] - height)/2
        box = (x,y,width+x,height+y)
        baseImage = baseImage.crop(box)
    return baseImage

@json_view
@require_POST
def get_image_mask(request):
    return_word = ''
    word1 = request.POST.get('word1')
    word2 = request.POST.get('word2')
    word3 = request.POST.get('word3')
    word4 = request.POST.get('word4')
    image = request.FILES.get('image')

    if image == None:
        return {"error":"no image"}
    upload_filename = "upload_files/" +getRandomString()+ str(time.time()) + '.jpeg'
    with open(upload_filename,'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)
    destination.close
    baseImage = Image.open(upload_filename)
    baseImage = resize(baseImage)   #图片缩放、裁剪
 #   baseImage = baseImage.convert('L').convert("RGB")
    baseImage = ImageEnhance.Color(baseImage).enhance(0.2)
    draw = ImageDraw.Draw(baseImage)
    draw.text((30,411), first_word,font=hwzfnt,fill=color)
    draw = ImageDraw.Draw(baseImage)
    draw.text((30,490), second_word,font=fnt,fill=color)
    filename = "image_files/" +getRandomString()+ str(int(time.time())) + ".jpg"
    words_arr = []
    if word1 != None:
        words_arr.append(word1)
    if word2 != None:
        words_arr.append(word2)
    if word3 != None:
        words_arr.append(word3)
    if word4 != None:
        words_arr.append(word4)
    if len(words_arr) > 0:
	total_height = word1_y
        for word in words_arr:
            total_height += row_height
            return_word =  return_word + word + '\n'
        draw = ImageDraw.Draw(baseImage)
        draw.text((30,word1_y), return_word,font=fnt,fill=color)
        draw = ImageDraw.Draw(baseImage)
        draw.text((30,total_height),third_word,font=fnt,fill=color)
        del draw
        return_file = baseImage.save(filename)
        file_object = open(filename)
        images_data = upload_image_to_restfulali(file_object.read())
    else:
        return_file = baseImage.save(filename)
        file_object = open(filename)
        images_data = upload_image_to_restfulali(file_object.read())
    os.remove(upload_filename)
    os.remove(filename)
    return images_data

def upload_image_to_restfulali(image_data):
        url = 'http://upload.media.aliyun.com/api/proxy/upload'
        data = {'dir':'/portrait','name':getRandomString()+'.jpg','size':str(int(len(image_data)))}
        token = "UPLOAD_AK_TOP MjMzMDQxMjM6ZXlKcGJuTmxjblJQYm14NUlqb2lNQ0lzSW01aGJXVnpjR0ZqWlNJNkluQnZjM1JsY2lJc0ltVjRjR2x5WVhScGIyNGlPaUl0TVNJc0ltUnBjaUk2SW5CdmNuUnlZV2wwSW4wOjVmMjE3ZTFkYjE2ZmY1ZGFjYWJiYmFjNWJiN2Q0NWRiMDJlNjc5ZTA"
        headers = {'Authorization': token}
        try:
            return_data =  requests.post(url,data=data,headers=headers,files={'content':image_data}).json()
        except:
            return_data =  requests.post(url,data=data,headers=headers,files={'content':image_data}).json()
        return return_data


def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
