# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET,require_POST
from django.http import StreamingHttpResponse
import json
from PIL import Image,ImageDraw,ImageFont
import time
import sys
import os
import md5
import requests
from corelib.decorators import json_view

reload(sys)
sys.setdefaultencoding('utf-8')

def getRandomString():
    num = int(time.time())%10
    random = os.urandom(num)
    m1 = md5.new()
    m1.update(random)
    return m1.hexdigest()

@json_view
@require_POST
def get_image_mask(request):
    return_word = ''
    words_str = request.POST.get('words')
    image = request.FILES.get('image')
    filename = "upload_files/" +getRandomString()+ str(time.time()) + '.jpeg'
    with open(filename,'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)
    destination.close
    width = 532
    height = 742
    baseImage = Image.open(filename)
    if baseImage.size[0] > width or baseImage.size[1] > height:
        x = 0
        y = 0
        if baseImage.size[0] > width:
            x = (baseImage.size[0] - width)/2
        if baseImage.size[1] > height:
            y = (baseImage.size[1] - height)/2
        box = (x,y,width+x,height+y)
        baseImage = baseImage.crop(box)
    baseImage = baseImage.convert('L').convert("RGB")
    draw = ImageDraw.Draw(baseImage)
    hwzfnt = ImageFont.truetype('hwzs.TTF', 60)
    first_word = unicode("妈妈是个美人儿")
    second_word = unicode("我想对你说")
    third_word = unicode("母亲节快乐！")
    color = (255, 144, 0, 128)
    draw.text((30,411), first_word,font=hwzfnt,fill=color)
    fnt = ImageFont.truetype('FZLTHJW.TTF', 40)
    draw = ImageDraw.Draw(baseImage)
    draw.text((30,490), second_word,font=fnt,fill=color)
    row_height = 50
    total_height = 530
    if words_str:
        words_arr = json.loads(words_str)
        for word in words_arr:
            total_height += row_height
            return_word =  return_word + word + '\n'
        draw = ImageDraw.Draw(baseImage)
        draw.text((30,total_height-row_height), return_word,font=fnt,fill=color)
        draw = ImageDraw.Draw(baseImage)
        draw.text((30,total_height),third_word,font=fnt,fill=color)
        del draw
        filename = "image_files/" +getRandomString()+ str(int(time.time())) + ".jpg"
        return_file = baseImage.save(filename)
        file_object = open(filename)
        images_data = upload_image_to_restfulali(file_object.read())
    return images_data

def upload_image_to_restfulali(image_data):
        url = 'http://upload.media.aliyun.com/api/proxy/upload'
        data = {'dir':'/portrait','name':getRandomString()+'.jpg','size':str(int(len(image_data)))}
        token = "UPLOAD_AK_TOP MjMzMDQxMjM6ZXlKcGJuTmxjblJQYm14NUlqb2lNQ0lzSW01aGJXVnpjR0ZqWlNJNkluQnZjM1JsY2lJc0ltVjRjR2x5WVhScGIyNGlPaUl0TVNJc0ltUnBjaUk2SW5CdmNuUnlZV2wwSW4wOjVmMjE3ZTFkYjE2ZmY1ZGFjYWJiYmFjNWJiN2Q0NWRiMDJlNjc5ZTA"
        headers = {'Authorization': token}
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
