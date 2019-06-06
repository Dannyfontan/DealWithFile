import tkinter as tk
import SearchMenu

def main():
    MainMenu = tk.Tk()
    MainMenu.title('主菜单')
    MainMenu.geometry('480x320')

    Frame_Main = tk.Frame(MainMenu)
    Frame_Main.pack(expand='yes', side=tk.TOP)

    def WalkMenu():
        MainMenu.withdraw()
        SearchMenu.walkmenu()

    Button_Main_Walk = tk.Button(Frame_Main, font=('Arial', 16), text='遍历', width=20, command =WalkMenu)
    Button_Main_Walk.pack(side=tk.TOP, padx = 3, pady = 3)

    Button_Main_Search = tk.Button(Frame_Main, font=('Arial', 16), text='查找', width=20)
    Button_Main_Search.pack(side=tk.TOP)

    Button_Main_Compare = tk.Button(Frame_Main, font=('Arial', 16), text='对比', width=20)
    Button_Main_Compare.pack(side=tk.TOP)

    MainMenu.mainloop()

if __name__ == '__main__':
    main()