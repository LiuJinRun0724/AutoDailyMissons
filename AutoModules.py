import cv2
import pyautogui as pag
import numpy as np
import time
import sys

# 判断目标对象是否存在
def img_exist(img,template):
    # 匹配目标对象和当前屏幕截图
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    # 返回匹配最大值和最大值位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # 设置阈值为0.8,匹配值大于0.8判定为匹配成功
    threshold = 0.8
    if max_val >= threshold:
        return True
    else:
        return False
    
# 获取目标对象坐标    
def Match(img_path):
    # 获取屏幕截图
    screenshot = pag.screenshot()
    # 二值化处理
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 加载识别对象
    template = cv2.imread(img_path) 
    
    # 确认识别对象存在
    exist = img_exist(screenshot, template)
    if exist:
        # 获取匹配图像位置
        res = cv2.matchTemplate(screenshot,template,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # 标记图像位置
        top_left     = max_loc
        bottom_right = [max_loc[0]+template.shape[0],max_loc[1]+template.shape[1]]
        cv2.rectangle(screenshot,top_left,bottom_right,(255,0,0),2)
        # 计算中心坐标
        Mid_loc      = ((top_left[0]+bottom_right[0])/2,(top_left[1]+bottom_right[1])/2)
        '''
        # 显示识别对象位置(调试用)
        cv2.imshow('Regtangle image',screenshot)
        # 按任意键取消页面
        cv2.waitKey(0)
        '''
        return Mid_loc
    else:
        print("没有找到目标对象，请确认当前桌面")

# 注册返回桌面事件
def desktop():
    pag.hotkey('win','d')


# 注册Esc键
def esc():
    pag.press('esc')

# 注册点击事件
def toClick(res):
    pag.click(x=int(res[0]),y=int(res[1]))

# 执行点击事件
def Click(img_path):
    res = waitUntil(img_path)
    toClick(res)


# 执行双击事件
def doubleClick(img_path):
    res = waitUntil(img_path)
    toClick(res)
    time.sleep(0.1)
    toClick(res)

# 设置超时保护，防死循环
def timeRecord(startTime,timeout):
    endTime = time.time()
    if(endTime-startTime>timeout):
        return False
    else:
        return True

# 轮询等待
def waitUntil(img_path):
    startTime = time.time()
    timeout = 60
    res = Match(img_path)
    while not(res):
        res = Match(img_path)
        if(res):
            return res
        if not(timeRecord(startTime,timeout)):
            sys.exit()      

