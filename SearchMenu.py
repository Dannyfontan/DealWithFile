#!/usr/bin/python3

# -*- coding: utf-8 -*-

import os

import tkinter as tk

import tkinter.filedialog

import tkinter.ttk

def walkmenu():
    top = tk.Tk()
    top.title('遍历')
    top.geometry('1080x720')

    Frame_Dir_Select = tk.Frame(top)
    Frame_Dir_Select.pack(side=tk.TOP)
    Frame_Dir_Select.pack(fill='x')
    Label_Dir_Select = tk.Label(Frame_Dir_Select, font=('Arial', 15), text='输入或选择路径')  # 标签
    Label_Dir_Select.pack(side=tk.LEFT, fill='x')
    Entry_Dir_Select = tk.Entry(Frame_Dir_Select, show=None, font=('Arial', 15))  # 输入框
    Entry_Dir_Select.pack(side=tk.LEFT, fill='x', expand='yes')

    Frame_Options = tk.Frame(top)
    Frame_Options.pack(fill='x')

    def file_select():
        Entry_Dir_Select.delete(0, 'end')
        Default_Dir = '/home/danny/'
        options = {}
        options['parent'] = top
        Selected_Dir = tk.filedialog.askdirectory(title='选择文件', initialdir=(os.path.expanduser(Default_Dir)), **options)
        Entry_Dir_Select.insert(0, Selected_Dir)

    Button_Dir_Select = tk.Button(Frame_Dir_Select, font=('Arial', 15), text='选择', command=file_select)
    Button_Dir_Select.pack(side=tk.LEFT)

    def walk():
        Selected_Dir = Entry_Dir_Select.get()
        for maindir, subdir, file_name_list in os.walk(Selected_Dir):
            return maindir, subdir, file_name_list

    Frame_File_Output = tk.Frame(top)
    Frame_File_Output.pack(expand='yes', fill='both')
    Text_File_Output = tk.ttk.Treeview(Frame_File_Output)
    Text_File_Output.pack(expand='yes', fill='both')
    Text_File_Output['show'] = 'headings'

    Text_File_Output['columns'] = ('路径', '名称', '类型')
    Text_File_Output.column('路径', width=250)
    Text_File_Output.column('名称', width=150)
    Text_File_Output.column('类型', width=100)

    Text_File_Output.heading('路径', text='路径')
    Text_File_Output.heading('名称', text='名称')
    Text_File_Output.heading('类型', text='类型')

    def click():
        maindir, subdirs, files = walk()

        for subdir in subdirs:
            Text_File_Output.insert('', 0, text=maindir + subdir, values=(maindir + subdir, subdir, '子目录', '0'))

        for file in files:
            Text_File_Output.insert('', 0, text=maindir + file, values=(maindir + file, file, '文件', '0'))

    Button_File_Out = tk.Button(Frame_Dir_Select, font=('Arial', 15), text='确认', command=click)
    Button_File_Out.pack(side=tk.LEFT)

    top.mainloop()


