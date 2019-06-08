#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk
from fuzzywuzzy import fuzz

#需要描述的对象就是页面
#基类就是一个框架
#派生类继承基类

class ListPage():
    def __init__(self, title):
        self.page = tk.Toplevel()
        ws = self.page.winfo_screenwidth()
        hs = self.page.winfo_screenheight()
        x = (ws / 2) - (1920 / 2)
        y = (hs / 2) - (1080 / 2)
        self.page.geometry('%dx%d+%d+%d' % (1920, 1080, x, y))
        self.page.title(title)

    def ret(self):
        self.page.destroy()
        mp = MainPage.mainpage(self)
        mp.create()

    def create(self):
        self.SelectFrame = tk.Frame(self.page)
        self.SelectFrame.pack(side = tk.TOP, fill = 'x')

        self.ReturnButton = tk.Button(self.SelectFrame, font = ('Arial', 15), text = '返回', command = self.ret)
        self.ReturnButton.pack(side = tk.LEFT, fill='x')

        self.SelectLabel = tk.Label(self.SelectFrame, font=('Arial', 15), text='输入或选择路径')
        self.SelectLabel.pack(side=tk.LEFT, fill='x')

        self.DirEntry = tk.Entry(self.SelectFrame, show=None, font=('Arial', 15))
        self.DirEntry.pack(side=tk.LEFT, fill='x', expand='yes')

        def dir_select():
            self.DirEntry.delete(0, 'end')
            DefaultDir = '/home/danny/'
            options = {}
            options['parent'] = self.page
            SelectedDir = tk.filedialog.askdirectory(title='选择文件', initialdir=(os.path.expanduser(DefaultDir)), **options)
            self.DirEntry.insert(0, SelectedDir)

        self.SelectButton = tk.Button(self.SelectFrame, font=('Arial', 15), text='选择', command=dir_select)
        self.SelectButton.pack(side=tk.LEFT)

        def walk():
            InputDir = self.DirEntry.get()
            if(InputDir == ''):
                tkinter.messagebox.showwarning(title='错误', message='请输入或选择路径')
                return [], [], []
            if(os.path.exists(InputDir) == False):
                tkinter.messagebox.showwarning(title = '错误', message = '路径不存在')
                return [], [], []

            for MainDir, SubDir, FileNameList in os.walk(InputDir):
                return MainDir, SubDir, FileNameList

        self.OutputFrame = tk.Frame(self.page)
        self.OutputFrame.pack(expand='yes', fill='both')
        self.OutputText = tk.ttk.Treeview(self.OutputFrame)
        self.OutputText.pack(expand='yes', fill='both')
        self.OutputText['show'] = 'headings'

        self.OutputText['columns'] = ('路径', '名称', '类型')
        self.OutputText.column('路径', width=250)
        self.OutputText.column('名称', width=150)
        self.OutputText.column('类型', width=100)

        self.OutputText.heading('路径', text='路径')
        self.OutputText.heading('名称', text='名称')
        self.OutputText.heading('类型', text='类型')

        def confirm():

            maindir, subdirs, files = walk()

            for child in self.OutputText.get_children():
                self.OutputText.delete(child)

            for subdir in subdirs:
                self.OutputText.insert('', 0, values=(maindir + '/' + subdir, subdir, '子目录'))

            for file in files:
                self.OutputText.insert('', 0, values=(maindir + '/' + file, file, '文件'))

        self.ConfirmButton = tk.Button(self.SelectFrame, font=('Arial', 15), text='确认', command = confirm)
        self.ConfirmButton.pack(side=tk.LEFT)
        self.page.mainloop()

class SearchPage():
    def __init__(self, title):
        self.page = tk.Toplevel()
        ws = self.page.winfo_screenwidth()
        hs = self.page.winfo_screenheight()
        x = (ws / 2) - (720 / 2)
        y = (hs / 2) - (480 / 2)
        self.page.geometry('%dx%d+%d+%d' % (720, 480, x, y))
        self.page.title(title)

    def ret(self):
        self.page.destroy()
        mp = MainPage.mainpage(self)
        mp.create()

    def output(self):
        searchop = self.SearchOption.get()
        filename = self.FileEntry.get()
        inputdir = self.DirSelectEntry.get()

        for child in self.OutputText.get_children():
            self.OutputText.delete(child)

        if(filename == ''):
            tkinter.messagebox.showwarning(title='错误', message='请输入文件名')
            return
        if(inputdir == ''):
            tkinter.messagebox.showwarning(title='错误', message='请选择路径')
            return

        if(searchop == '精确搜索'):
            havefind = False
            for MainDir, SubDir, FileNameList in os.walk(inputdir):
                for file in FileNameList:
                    if (fuzz.ratio(filename, file) == 100):
                        self.OutputText.insert('', 0, text=MainDir  + file, values=(file, MainDir + '/' + file))
                        havefind = True
            if(havefind == False):
                tkinter.messagebox.showwarning(title='错误', message='未找到该文件')

        elif(searchop == '模糊搜索'):
            havefind = False
            for MainDir, SubDir, FileNameList in os.walk(inputdir):
                for file in FileNameList:
                    if (fuzz.partial_ratio(filename, file)  >= 90):
                        self.OutputText.insert('', 0, text=MainDir + file, values=(file, MainDir + '/' + file))
                        havefind = True
            if (havefind == False):
                tkinter.messagebox.showwarning(title='错误', message='未找到类似文件')

        else:
            print('error!')

    def reset(self):
        self.DirSelectEntry.delete(0, 'end')
        self.FileEntry.delete(0, 'end')
        self.SearchOption.current(0)
        for child in self.OutputText.get_children():
            self.OutputText.delete(child)

    def dir_select(self):
        self.DirSelectEntry.delete(0, 'end')
        DefaultDir = '/home/danny/'
        options = {}
        options['parent'] = self.page
        SelectedDir = tk.filedialog.askdirectory(title='选择文件', initialdir=(os.path.expanduser(DefaultDir)), **options)
        self.DirSelectEntry.insert(0, SelectedDir)


    def create(self):
        self.SearchFrame = tk.Frame(self.page)
        self.SearchFrame.pack(side = tk.TOP, fill = 'x')

        self.SearchLabel = tk.Label(self.SearchFrame, font=('Arial', 15), text='输入文件名')
        self.SearchLabel.pack(side=tk.LEFT, fill='x')

        self.FileEntry = tk.Entry(self.SearchFrame, show=None, font=('Arial', 15))
        self.FileEntry.pack(side=tk.LEFT, fill='x', expand='yes')

        self.SearchOption = tk.ttk.Combobox(self.SearchFrame, values = ['精确搜索', '模糊搜索'], state = 'readonly')
        self.SearchOption.pack(side=tk.LEFT, fill='x', expand='yes')
        self.SearchOption.current(0)

        self.DirSelectFrame = tk.Frame(self.page)
        self.DirSelectFrame.pack(side=tk.TOP, fill='x')

        self.DirSelectLabel = tk.Label(self.DirSelectFrame, font = ('Arial', 15), text = '选择范围路径')
        self.DirSelectLabel.pack(side = tk.LEFT, fill = 'x')

        self.DirSelectEntry = tk.Entry(self.DirSelectFrame, show=None, font=('Arial', 15))
        self.DirSelectEntry.pack(side=tk.LEFT, fill='x', expand = 'yes')

        self.DirSelectButton = tk.Button(self.DirSelectFrame, font = ('Arial', 15), text = '选择', command = self.dir_select)
        self.DirSelectButton.pack(side = tk.LEFT, fill = 'x')

        self.SelectButton = tk.Button(self.DirSelectFrame, font=('Arial', 15), text='开始查找', command = self.output)
        self.SelectButton.pack(side=tk.LEFT)

        self.OutputFrame = tk.Frame(self.page)
        self.OutputFrame.pack(expand='yes', fill='both')
        self.OutputText = tk.ttk.Treeview(self.OutputFrame)
        self.OutputText.pack(expand='yes', fill='both')
        self.OutputText['show'] = 'headings'

        self.OutputText['columns'] = ('文件名', '路径')
        self.OutputText.column('文件名', width=150)
        self.OutputText.column('路径', width=250)
        self.OutputText.heading('文件名', text='文件名')
        self.OutputText.heading('路径', text='路径')

        self.ReturnFrame = tk.Frame(self.page)
        self.ReturnFrame.pack(side = tk.TOP, anchor = 's')

        self.ReturnButton = tk.Button(self.ReturnFrame, font = ('Arial', 15), text = '返回', command = self.ret)
        self.ReturnButton.pack(side = tk.LEFT, fill='x')

        self.ResetButton = tk.Button(self.ReturnFrame, font = ('Arial', 15), text = '重置', command =self.reset)
        self.ResetButton.pack(side = tk.LEFT, fill = 'x')

        self.page.mainloop()

class Md5Page():
    def __init__(self, title):
        self.page = tk.Toplevel()
        ws = self.page.winfo_screenwidth()
        hs = self.page.winfo_screenheight()
        x = (ws / 2) - (1920 / 2)
        y = (hs / 2) - (1080 / 2)
        self.page.geometry('%dx%d+%d+%d' % (1920, 1080, x, y))
        self.page.title(title)


    def ret(self):
        self.page.destroy()
        mp = MainPage.mainpage(self)
        mp.create()

    def dir_output(self):
        dirname = self.DirEntry.get()
        if(dirname == ''):
            tkinter.messagebox.showwarning(title='错误', message='请输入或选择路径')
            return
        if (os.path.exists(dirname) == False):
            tkinter.messagebox.showwarning(title='错误', message='路径不存在')
            return

        def walk(dir):
            for MainDir, SubDir, FileNameList in os.walk(dir):
                return MainDir, SubDir, FileNameList

        maindir, subdirs, files = walk(dirname)
        self.DirSelectFrame.pack(side = tk.TOP, fill = 'x')
        self.FileSelectFrame.pack(side = tk.TOP, fill = 'x')
        '''self.OutputFrame = tk.Frame(self.page)
        self.OutputFrame.pack(expand='yes', fill='both')
        self.OutputText = tk.ttk.Treeview(self.OutputFrame)
        self.OutputText.pack(expand='yes', fill='both')
        self.OutputText['show'] = 'headings'

        self.OutputText['columns'] = ('文件名', '路径')
        self.OutputText.column('文件名', width=150)
        self.OutputText.column('路径', width=250)
        self.OutputText.heading('文件名', text='文件名')
        self.OutputText.heading('路径', text='路径')'''


    def create(self):
        self.MeunFrame = tk.Frame(self.page)
        self.MeunFrame.pack(side = tk.TOP, anchor = 'center', fill = 'x')

        self.DirSelectFrame = tk.Frame(self.MeunFrame)
        self.DirSelectFrame.pack(anchor = 'n')
        self.DirSelectLabel = tk.Label(self.DirSelectFrame, font = ('Arial', 15), text = '选择整个目录')
        self.DirSelectLabel.pack(side = tk.LEFT, fill = 'x')
        self.DirEntry = tk.Entry(self.DirSelectFrame, show=None, font=('Arial', 15))
        self.DirEntry.pack(side=tk.LEFT, fill='x', expand='yes')

        def dir_select():
            self.DirEntry.delete(0, 'end')
            DefaultDir = '/home/danny/'
            options = {}
            options['parent'] = self.page
            SelectedDir = tk.filedialog.askdirectory(title='选择文件', initialdir=(os.path.expanduser(DefaultDir)), **options)
            self.DirEntry.insert(0, SelectedDir)

        self.DirSelectButton = tk.Button(self.DirSelectFrame, font=('Arial', 15), text='选择', command=dir_select)
        self.DirSelectButton.pack(side=tk.LEFT)
        self.DirConfirmButton = tk.Button(self.DirSelectFrame, font=('Arial', 15), text='确认', command = self.dir_output)
        self.DirConfirmButton.pack(side = tk.LEFT)

        self.FileSelectFrame = tk.Frame(self.MeunFrame)
        self.FileSelectFrame.pack(anchor = 's')
        self.FileSelectLabel = tk.Label(self.FileSelectFrame, font = ('Arial', 15), text = '选择单个文件')
        self.FileSelectLabel.pack(side = tk.LEFT, fill = 'x')

        self.page.mainloop()

class MainPage():
    def __init__(self, title):
        self.page = tk.Tk()
        ws = self.page.winfo_screenwidth()
        hs = self.page.winfo_screenheight()
        x = (ws / 2) - (480 / 2)
        y = (hs / 2) - (320 / 2)
        self.page.geometry('%dx%d+%d+%d' % (480, 320, x, y))
        self.page.title(title)


    def list(self):
        self.page.withdraw()
        listpage = ListPage('遍历')
        listpage.create()

    def search(self):
        self.page.withdraw()
        searchpage = SearchPage('查找')
        searchpage.create()

    def md5(self):
        self.page.withdraw()
        md5page = Md5Page('Md5')
        md5page.create()

    def mainpage(self):
        mp = MainPage('test')
        return mp

    def create(self):
        self.MainFrame = tk.Frame(self.page)
        self.MainFrame.pack(expand = 'yes', side = tk.TOP)

        self.ListButton = tk.Button(self.MainFrame, font=('Arial', 16), text='遍历', width=20, command = self.list)
        self.ListButton.pack(side=tk.TOP)

        self.SearchButton = tk.Button(self.MainFrame, font=('Arial', 16), text='查找', width=20, command = self.search)
        self.SearchButton.pack(side = tk.TOP)

        self.MD5Button = tk.Button(self.MainFrame, font=('Arial', 16), text='MD5', width=20, command = self.md5)
        self.MD5Button.pack(side=tk.TOP)

        self.CompareButton = tk.Button(self.MainFrame, font=('Arial', 16), text='对比', width=20)
        self.CompareButton.pack(side = tk.TOP)

        self.page.mainloop()

def main():
    MAIN = MainPage('File System')
    MAIN.create()

if __name__ == '__main__':
    main()