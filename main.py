#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk
import hashlib
import time
from fuzzywuzzy import fuzz
from pathlib import PureWindowsPath, Path

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
            danny = '/home/danny'
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

        self.OutputText['columns'] = ('路径', '名称', '类型', '大小', '修改时间')
        self.OutputText.column('路径', width=150)
        self.OutputText.column('名称', width=50)
        self.OutputText.column('类型', width=50)
        self.OutputText.column('大小', width=50)
        self.OutputText.column('修改时间', width=50)
        self.OutputText.heading('路径', text='路径')
        self.OutputText.heading('名称', text='名称')
        self.OutputText.heading('类型', text='类型')
        self.OutputText.heading('大小', text='大小')
        self.OutputText.heading('修改时间', text='修改时间')

        def confirm():

            maindir, subdirs, files = walk()

            for child in self.OutputText.get_children():
                self.OutputText.delete(child)

            def formatSize(bytes):
                try:
                    bytes = float(bytes)
                    kb = bytes / 1024
                except:
                    print("传入的字节格式不对")
                    return "Error"

                if kb >= 1024:
                    M = round(kb / 1024, 3)
                    if M >= 1024:
                        G = round(M / 1024, 3)
                        return "%.3fG" % (G)
                    else:
                        return "%.3fM" % (M)
                else:
                    kb = round(kb, 3)
                    return "%.3fkb" % (kb)



            for subdir in subdirs:
                subdir_addr = os.path.join(maindir, subdir)
                subdir_size = os.path.getsize(subdir_addr)
                timestamp = os.path.getmtime(subdir_addr)
                subdir_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp))
                self.OutputText.insert('', 'end', values=(subdir_addr, subdir, '子目录', formatSize(subdir_size), subdir_time))

            for file in files:
                file_addr = os.path.join(maindir, file)
                file_size = os.path.getsize(file_addr)
                timestamp = os.path.getmtime(file_addr)
                file_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp))
                self.OutputText.insert('', 'end', values=(file_addr, file, '文件', formatSize(file_size), file_time))

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
                        self.OutputText.insert('', 'end', text=MainDir  + file, values=(file, MainDir + '/' + file))
                        havefind = True
            if(havefind == False):
                tkinter.messagebox.showwarning(title='错误', message='未找到该文件')

        elif(searchop == '模糊搜索'):
            havefind = False
            for MainDir, SubDir, FileNameList in os.walk(inputdir):
                for file in FileNameList:
                    if (fuzz.partial_ratio(filename, file)  >= 90):
                        self.OutputText.insert('', 'end', text=MainDir + file, values=(file, MainDir + '/' + file))
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
        DefaultDir = '/home/danny'
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

    def reset(self):
        self.FileEntry.delete(0, 'end')
        self.DirEntry.delete(0, 'end')
        self.FileEntry.config(state='normal')
        self.FileConfirm.config(state='normal')
        self.DirEntry.config(state='normal')
        self.DirConfirm.config(state='normal')
        for child in self.OutputText.get_children():
            self.OutputText.delete(child)

    def dir_overwatch(self):
        self.FileEntry.delete(0, 'end')
        self.FileEntry.config(state = 'readonly')
        self.FileConfirm.config(state = 'disable')

    def file_overwatch(self):
        self.DirEntry.delete(0, 'end')
        self.DirEntry.config(state='readonly')
        self.DirConfirm.config(state = 'disable')

    def getmd5(self, file_addr):
        with open(file_addr, "rb") as f:
            md5 = hashlib.md5()
            md5.update(f.read())
            hash = md5.hexdigest()
            return hash

    def file_select(self):
        self.FileEntry.config(state = 'normal')
        self.FileConfirm.config(state = 'normal')
        self.file_overwatch()
        self.FileEntry.delete(0, 'end')
        for child in self.OutputText.get_children():
            self.OutputText.delete(child)

        DefaultDir = '/home/danny/'
        SelectedFiles = tk.filedialog.askopenfilenames(initialdir=DefaultDir, title="选择文件", filetypes=(("all files", "*.*"), ("all files", "*.*")))
        for SelectedFile in SelectedFiles:
            self.FileEntry.insert(0, SelectedFile + ' ')
        self.Files = SelectedFiles

    def file_output(self):
        self.file_overwatch()

        for child in self.OutputText.get_children():
            self.OutputText.delete(child)

        files_addr = self.FileEntry.get()
        if(not files_addr):
            tkinter.messagebox.showwarning(title = '警告', message = '请选择文件')
            self.DirEntry.config(state='normal')
            self.DirConfirm.config(state='normal')
            return

        for file_addr in self.Files:
            file = os.path.basename(file_addr)
            self.OutputText.insert('', 'end', values=(file, self.getmd5(file_addr), file_addr))

    def dir_select(self):
        self.DirEntry.config(state='normal')
        self.DirConfirm.config(state='normal')
        self.dir_overwatch()
        self.DirEntry.delete(0, 'end')
        DefaultDir = '/home/danny/'
        options = {}
        options['parent'] = self.page
        SelectedDir = tk.filedialog.askdirectory(title='选择路径', initialdir=(os.path.expanduser(DefaultDir)), **options)
        self.DirEntry.insert(0, SelectedDir)

    def dir_output(self):
        self.dir_overwatch()

        for child in self.OutputText.get_children():
            self.OutputText.delete(child)

        dirname = self.DirEntry.get()
        if(dirname == ''):
            tkinter.messagebox.showwarning(title='错误', message='请输入或选择路径')
            self.FileEntry.config(state='normal')
            self.FileConfirm.config(state='normal')
            return
        if (os.path.exists(dirname) == False):
            tkinter.messagebox.showwarning(title='错误', message='路径不存在')
            return

        def walk(dir):
            for MainDir, SubDir, FileNameList in os.walk(dir):
                return MainDir, SubDir, FileNameList

        maindir, subdirs, files = walk(dirname)

        for file in files:
            file_addr = os.path.join(maindir, file)
            self.OutputText.insert('', 'end', values=(file, self.getmd5(file_addr), file_addr))

    def text_save(self):
        f = tkinter.filedialog.asksaveasfile(title = '选择保存路径', mode='w', filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        if f is None:
            return

        for line in self.OutputText.get_children():
            res = ''
            for info in self.OutputText.item(line)['values']:
                res = res + str(info) + ' '
            res.rstrip()
            f.write(res + '\n')

        f.close()

    def create(self):
        self.MenuBar = tk.Menu(self.page)
        self.OptionMenu = tk.Menu(self.MenuBar, tearoff = 0)
        self.MenuBar.add_cascade(label = '选项', font = ('Arial', 15), menu = self.OptionMenu)
        self.OptionMenu.add_command(label = '保存', font = ('Arial', 15), command = self.text_save)
        self.OptionMenu.add_command(label = '退出', font = ('Arial', 15), command = self.page.quit)
        self.page.config(menu = self.MenuBar)

        self.OptionFrame = tk.Frame(self.page)
        self.OptionFrame.pack(side = tk.TOP, fill ='x')
        self.DirSelectFrame = tk.Frame(self.OptionFrame)
        self.DirSelectFrame.pack(side = tk.TOP, fill = 'x')
        self.ReturnButton = tk.Button(self.DirSelectFrame, font = ('Arial', 15), text ='返回', command = self.ret)
        self.ReturnButton.pack(side = tk.LEFT, fill ='x')
        self.DirSelectLabel = tk.Label(self.DirSelectFrame, font = ('Arial', 15), text = '输入或选择路径')
        self.DirSelectLabel.pack(side = tk.LEFT, fill = 'x')
        self.DirEntry = tk.Entry(self.DirSelectFrame, show = None, font = ('Arial', 15))
        self.DirEntry.pack(side = tk.LEFT, expand = 'yes', fill = 'x')
        self.DirSelectButton = tk.Button(self.DirSelectFrame, font=('Arial', 15), text='选择', command = self.dir_select)
        self.DirSelectButton.pack(side=tk.LEFT, fill ='x')
        self.DirConfirm = tk.Button(self.DirSelectFrame, font=('Arial', 15), text='确认', command=self.dir_output)
        self.DirConfirm.pack(side=tk.LEFT, fill ='x')

        self.FileSelectFrame = tk.Frame(self.OptionFrame)
        self.FileSelectFrame.pack(side = tk.TOP, fill = 'x')
        self.ResetButton = tk.Button(self.FileSelectFrame, font = ('Arial', 15), text ='置零', command = self.reset)
        self.ResetButton.pack(side = tk.LEFT, fill ='x')
        self.FileSelectLabel = tk.Label(self.FileSelectFrame, font = ('Arial', 15), text = '输入或选择文件')
        self.FileSelectLabel.pack(side = tk.LEFT, fill = 'x')
        self.FileEntry = tk.Entry(self.FileSelectFrame, show = None, font = ('Arial', 15))
        self.FileEntry.pack(side = tk.LEFT, expand = 'yes', fill = 'x')
        self.FileSelectButton = tk.Button(self.FileSelectFrame, font=('Arial', 15), text='选择', command=self.file_select)
        self.FileSelectButton.pack(side=tk.LEFT, fill='x')
        self.FileConfirm = tk.Button(self.FileSelectFrame, font=('Arial', 15), text='确认', command=self.file_output)
        self.FileConfirm.pack(side=tk.LEFT, fill='x')

        self.OutputFrame = tk.Frame(self.page)
        self.OutputFrame.pack(expand='yes', fill='both')
        self.OutputText = tk.ttk.Treeview(self.OutputFrame)
        self.OutputText.pack(expand='yes', fill='both')
        self.OutputText['show'] = 'headings'

        self.OutputText['columns'] = ('文件名', 'Md5', '路径')
        self.OutputText.column('文件名', width=150)
        self.OutputText.column('Md5', width=200)
        self.OutputText.column('路径', width=250)
        self.OutputText.heading('文件名', text='文件名')
        self.OutputText.heading('Md5', text='Md5')
        self.OutputText.heading('路径', text='路径')

        self.page.mainloop()

class ComparePage():
    def __init__(self, title):
        self.page = tk.Toplevel()
        ws = self.page.winfo_screenwidth()
        hs = self.page.winfo_screenheight()
        x = (ws / 2) - (1920 / 2)
        y = (hs / 2) - (1080 / 2)
        self.page.geometry('%dx%d+%d+%d' % (1920, 1080, x, y))
        self.page.title(title)
        self.Files = []
    def ret(self):
        self.page.destroy()
        mp = MainPage.mainpage(self)
        mp.create()

    def file_select(self):
        self.SelectEntry.delete(0, 'end')
        DefaultDir = '/home/danny/'
        SelectedFiles = tk.filedialog.askopenfilenames(initialdir=DefaultDir, title="选择文件",
                                                       filetypes=(("all files", "*.*"), ("all files", "*.*")))
        for SelectedFile in SelectedFiles:
            self.SelectEntry.insert(0, SelectedFile + ' ')
        self.Files = SelectedFiles

    def getmd5(self, file_addr):
        with open(file_addr, "rb") as f:
            md5 = hashlib.md5()
            md5.update(f.read())
            hash = md5.hexdigest()
            return hash

    def add(self):
        files_addr = self.SelectEntry.get()
        self.SelectEntry.delete(0, 'end')
        if (not files_addr):
            tkinter.messagebox.showwarning(title='警告', message='请选择文件')
            return

        def formatSize(bytes):
            try:
                bytes = float(bytes)
                kb = bytes / 1024
            except:
                print("传入的字节格式不对")
                return "Error"

            if kb >= 1024:
                M = round(kb / 1024, 3)
                if M >= 1024:
                    G = round(M / 1024, 3)
                    return "%.3fG" % (G)
                else:
                    return "%.3fM" % (M)
            else:
                kb = round(kb, 3)
                return "%.3fkb" % (kb)

        for file_addr in self.Files:
            file = os.path.basename(file_addr)
            timestamp = os.path.getmtime(file_addr)
            file_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp))
            file_size = os.path.getsize(file_addr)
            self.OutputText.insert('', 'end', values=(file_addr, file, self.getmd5(file_addr), file_time, formatSize(file_size)))

    def reset(self):
        self.SelectEntry.delete(0, 'end')
        for child in self.OutputText.get_children():
            self.OutputText.delete(child)

    def delete(self):
        for line in self.OutputText.get_children():
             print(self.OutputText.item(line)['values'][1])
        child = self.OutputText.get_children()
        size = len(child)
        if(size > 0):
            self.OutputText.delete(child[size-1])
        else:
            tkinter.messagebox.showwarning(title = '警告', message = '列表为空')
            return


    def create(self):
        self.OutputFrame = tk.Frame(self.page)
        self.OutputFrame.pack(expand='yes', fill='both')
        self.OutputText = tk.ttk.Treeview(self.OutputFrame)
        self.OutputText.pack(expand='yes', fill='both')
        self.OutputText['show'] = 'headings'

        self.OutputText['columns'] = ('路径', '文件名', 'Md5', '修改时间', '大小')
        self.OutputText.column('路径', width=250)
        self.OutputText.column('文件名', width=150)
        self.OutputText.column('Md5', width=100)
        self.OutputText.column('修改时间', width=100)
        self.OutputText.column('大小', width=50)

        self.OutputText.heading('路径', text='路径')
        self.OutputText.heading('文件名', text='文件名')
        self.OutputText.heading('Md5', text='Md5')
        self.OutputText.heading('修改时间', text='修改时间')
        self.OutputText.heading('大小', text='大小')

        self.MenuFrame = tk.Frame(self.page)
        self.MenuFrame.pack(side = tk.BOTTOM)
        self.SelectFrame = tk.Frame(self.MenuFrame)
        self.SelectFrame.pack(side = tk.TOP, fill = 'x')
        self.OptionFrame = tk.Frame(self.MenuFrame)
        self.OptionFrame.pack(side = tk.TOP, fill = 'x')

        self.SelectLabel = tk.Label(self.SelectFrame, font = ('Arial', 15), text = '选择文件')
        self.SelectLabel.pack(side = tk.LEFT, fill = 'x')
        self.SelectEntry = tk.Entry(self.SelectFrame, show = None, font = ('Arial', 15))
        self.SelectEntry.pack(side = tk.LEFT, fill = 'x')
        self.SelectButton = tk.Button(self.SelectFrame, font = ('Arial', 15), text = '选择', command = self.file_select)
        self.SelectButton.pack(side = tk.LEFT, fill = 'x')
        self.AddButton = tk.Button(self.SelectFrame, font = ('Arial', 15), text = '增加', command = self.add)
        self.AddButton.pack(side = tk.LEFT, fill = 'x')
        self.ReturnButton = tk.Button(self.OptionFrame, font = ('Arial', 15), text = '返回', command = self.ret)
        self.ReturnButton.pack(side = tk.LEFT, fill = 'x', expand = 'yes')
        self.ResetButton = tk.Button(self.OptionFrame, font = ('Arial', 15), text = '置零', command = self.reset)
        self.ResetButton.pack(side = tk.LEFT, fill = 'x', expand = 'yes')
        self.DeleteButton = tk.Button(self.OptionFrame, font = ('Arial', 15), text = '删除', command = self.delete)
        self.DeleteButton.pack(side = tk.LEFT, fill = 'x', expand = 'yes')

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

    def compare(self):
        self.page.withdraw()
        comparepage = ComparePage('对比')
        comparepage.create()

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

        self.CompareButton = tk.Button(self.MainFrame, font=('Arial', 16), text='对比', width=20, command = self.compare)
        self.CompareButton.pack(side = tk.TOP)

        self.ExitButton = tk.Button(self.MainFrame, font=('Arial', 16), text='退出', width=20, command = self.page.quit)
        self.ExitButton.pack(side = tk.TOP)

        self.page.mainloop()

def main():
    MAIN = MainPage('File System')
    MAIN.create()

if __name__ == '__main__':
    main()