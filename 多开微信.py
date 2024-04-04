# -*- coding: utf-8 -*-
# newWX.py created by MoMingLog on 25/3/2024.
"""
【作者】MoMingLog
【创建时间】2024-03-25
【功能描述】
"""
import ctypes
import os

if __name__ == '__main__':
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "http"))

    if ctypes.sizeof(ctypes.c_void_p) == ctypes.sizeof(ctypes.c_ulonglong):
        filepath = os.path.join(root_dir, 'wxDriver64.dll')
        driver = ctypes.cdll.LoadLibrary(filepath)
    else:
        filepath = os.path.join(root_dir, 'wxDriver.dll')
        driver = ctypes.cdll.LoadLibrary(filepath)

    new_wechat = driver.new_wechat
    new_wechat.argtypes = None
    new_wechat.restype = ctypes.c_int
    new_wechat()
