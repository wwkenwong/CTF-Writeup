import json
from io import BytesIO
import os
from cnnlib.recognition_object import Recognizer

import time
from PIL import Image

import requests
import base64
import string 
import copy

global MAX_ID 


class Challenge:
  def __init__(self):
    self.s = requests.Session()

  def get(self):
    r = self.s.get('https://captcha.chal.uiuc.tf/')
    try:
      header = r.text.split('<h2>')[1].split('</h2>')[0]
    except:
      header = None
    try:
      im = base64.b64decode(r.text.split('<img class="captcha" src="data:image/png;base64,')[1].split('"/>')[0])
    except:
      im = None
    return header, im

  def submit(self, answer):
    r = self.s.post('https://captcha.chal.uiuc.tf/', data={ 'captcha': answer })
    try:
      header = r.text.split('<h2>')[1].split('</h2>')[0]
    except:
      header = None
    try:
      im = base64.b64decode(r.text.split('<img class="captcha" src="data:image/png;base64,')[1].split('"/>')[0])
    except:
      im = None
    return header, im



os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

with open("conf/sample_config.json", "r") as f:
    sample_conf = json.load(f)

image_height = sample_conf["image_height"]
image_width = sample_conf["image_width"]
max_captcha = sample_conf["max_captcha"]
api_image_dir = sample_conf["api_image_dir"]
model_save_dir = sample_conf["model_save_dir"]
image_suffix = sample_conf["image_suffix"]  
char_set = sample_conf["char_set"]

basedir = os.path.abspath(os.path.dirname(__file__))
R = Recognizer(image_height, image_width, max_captcha, char_set, "model_v8/")
R2 = Recognizer(image_height, image_width, max_captcha, char_set, "model_v7/")
R3 = Recognizer(image_height, image_width, max_captcha, char_set, "model_v6/")
R4 = Recognizer(image_height, image_width, max_captcha, char_set, "model_v5/")
R5 = Recognizer(image_height, image_width, max_captcha, char_set, "model_v4/")
R6 = Recognizer(image_height, image_width, max_captcha, char_set, "model_v3/")
R7 = Recognizer(image_height, image_width, max_captcha, char_set, "model_gen2/")
R8 = Recognizer(image_height, image_width, max_captcha, char_set, "model_old/")


def response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def main():
  c = Challenge()
  header, im = c.get()
  print(header)
  with open('captcha.png', 'wb') as f: f.write(im)

  while True:
    im_bak = copy.copy(im)
    img = BytesIO(im)
    img = Image.open(img, mode="r")
    answer = R.rec_image(img)
    header, im = c.submit(answer)
    print(header)
    org_ans = answer
    if "Invalid" in header :
        ans_list = []
        ans_list.append(answer)
        answer_r2 = R2.rec_image(img)
        header, im = c.submit(answer_r2)
        print(header)
        if "Invalid" not in header :
            with open("./recycle/"+answer_r2+'.png', 'wb') as f: f.write(im_bak)
        else:
            ans_list.append(answer_r2)
            answer_r3 = R3.rec_image(img)
            header, im = c.submit(answer_r3)
            print(header)
            if "Invalid" not in header :
                with open("./recycle/"+answer_r3+'.png', 'wb') as f: f.write(im_bak)
            else:
                ans_list.append(answer_r3)
                answer_r4 = R4.rec_image(img)
                header, im = c.submit(answer_r4)
                print(header)
                if "Invalid" not in header :
                    with open("./recycle/"+answer_r4+'.png', 'wb') as f: f.write(im_bak)
                else:
                  ans_list.append(answer_r4)
                  answer_r5 = R5.rec_image(img)
                  header, im = c.submit(answer_r5)
                  print(header)
                  if "Invalid" not in header :
                      with open("./recycle/"+answer_r5+'.png', 'wb') as f: f.write(im_bak)
                  else:
                    ans_list.append(answer_r5)
                    answer_r6 = R6.rec_image(img)
                    header, im = c.submit(answer_r6)
                    print(header)
                    if "Invalid" not in header :
                        with open("./recycle/"+answer_r6+'.png', 'wb') as f: f.write(im_bak)
                    else:
                      ans_list.append(answer_r6)
                      answer_r7 = R7.rec_image(img)
                      header, im = c.submit(answer_r7)
                      print(header)
                      if "Invalid" not in header :
                          with open("./recycle/"+answer_r7+'.png', 'wb') as f: f.write(im_bak)
                      else:
                          ans_list.append(answer_r7)
                          answer_r8 = R8.rec_image(img)
                          header, im = c.submit(answer_r8)
                          print(header)
                          if "Invalid" not in header :
                              with open("./recycle/"+answer_r8+'.png', 'wb') as f: f.write(im_bak)
                          else:
                              ans_list.append(answer_r8)
                              print(ans_list)
                              with open("/tmp/tt/check.png", 'wb') as f: f.write(im_bak)
                              answer_ppl = input('> ').strip()
                              header, im = c.submit(answer_ppl)
                              print(header)
                              if "Invalid" not in header :
                                  with open("./recycle/"+answer_ppl+'.png', 'wb') as f: f.write(im_bak)
                              else:
                                  answer_ppl = input('> ').strip()
                                  header, im = c.submit(answer_ppl)
                                  if "Invalid" not in header :
                                      with open("./recycle/"+answer_ppl+'.png', 'wb') as f: f.write(im_bak)
                                  else:
                                      return 0 
    else:
        with open("./caught/"+answer+'.png', 'wb') as f: f.write(im_bak)
        lv = int(header.split(" ")[1])
        global MAX_ID
        MAX_ID = max(MAX_ID,lv)


if __name__ == '__main__':
    MAX_ID = 0 
    ID = 0 
    while True:
        main()
        ID +=1 
        print("[+] Tried : "+str(ID)+" Max lv "+str(MAX_ID))

