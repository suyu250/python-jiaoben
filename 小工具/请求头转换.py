import re
import tkinter as tk

windows = tk.Tk()
windows.geometry('400x500+500+400')
windows.title('请求头转换')
headers = {}


def headers_change():
    c_dic = {}
    global headers
    headers_str = T1.get('1.0', tk.END)
    pattern = '^(.*?):(.*)$'
    for line in headers_str.splitlines():
        headers = re.sub(pattern, '\'\\1\':\'\\2\',', line).replace(' ', '')
        T2.insert('insert', headers + '\n')


def clear():
    T1.delete(0.1, tk.END)
    T2.delete(0.1, tk.END)


T1 = tk.Text(windows)
T1.place(x=10, y=10, height=220, width=380)
T2 = tk.Text(windows)
T2.place(x=10, y=270, height=220, width=380)

B1 = tk.Button(windows, text='转换', command=headers_change)
B1.place(x=310, y=235, height=30, width=80)
B1 = tk.Button(windows, text='清空', command=clear)
B1.place(x=220, y=235, height=30, width=80)

L1 = tk.Label(windows, text='运用re模块正则表达式拆分')
L1.place(x=10, y=235, height=30, width=200)
windows.mainloop()
