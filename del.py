# coding=utf-8  
import os  
import time  
  
def change():
    for i in os.listdir("tmp"):
        os.remove(os.path.join("tmp",i))
    if os.path.exists('/www/wwwroot/diary_jeffscode_com/posts.txt'):
        os.remove('/www/wwwroot/diary_jeffscode_com/posts.txt')  
    time.sleep(86400)  

def loop():  
    n=1  
    while(n>0):  
        change()  
  
loop()  