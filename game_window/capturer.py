import numpy as np
import win32gui, win32ui, win32con
import time
from pynput import mouse
import cv2
from PIL import Image


class Capturer:

    width_res = 1920
    height_res = 1080

    def __init__(self,ventana):
        self.ventana = ventana


    #Captura el escritorio y devuelve una imagen cv2
    @staticmethod
    def get_screenshot():
        #podría mejorarse capturando solo la ventana

        # get the window image data
        hdesktop = win32gui.GetDesktopWindow()
        wDC = win32gui.GetWindowDC(hdesktop)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, Capturer.width_res, Capturer.height_res)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (Capturer.width_res, Capturer.height_res), dcObj, (0, 0), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (Capturer.height_res, Capturer.width_res, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hdesktop, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel
        img = img[..., :3]

        img = np.ascontiguousarray(img)
        return img

    #Coge un objeto ventana y un screenshot (puede ser None para que saque captura) y devuelve el recorte
    @staticmethod
    def cut_window(clase_ventana, screenshot = None):
        screenshot = Capturer.get_screenshot() if not screenshot else screenshot
        return screenshot[clase_ventana.top:clase_ventana.bot, clase_ventana.left:clase_ventana.right]

    @property
    def window(self):
        return self.cut_window(self.ventana)

