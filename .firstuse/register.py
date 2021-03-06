#FlyOS Panel By:XingYuJie
#Use Under License GPL - V3
"""flyos用户注册程序"""
import os
import sqlite3

import pywebio.input
from pywebio.output import put_html, popup, put_text
from pywebio import start_server
from pywebio.session import set_env

import termux_auth

FLYOS_ROOT = os.getenv('FLYOS')
HOME = os.getenv("HOME")

#Tips
print("______________________________________")
print("欢迎使用FlyOS!")
print("请使用本机浏览器访问:http://127.0.0.1:5005 来初始化FlyOS")
#FlyOS 激活main
def main():
    """主方法"""
    if not os.path.exists(FLYOS_ROOT+"/.firstuse/lock"):
        set_env(title="欢迎使用FlyOS", auto_scroll_bottom=True)
        put_html("<h1>欢迎使用！ -- FlyOS 初始化向导</h1>")
        put_text('欢迎使用FlyOS!开始初始化您的FlyOS吧！')
        popup('Hi,There！欢迎使用FlyOS！让我们来初始化FlyOS吧！')
        password = pywebio.input.input("设置您的系统开机密码:", type="password")
        vpwd = pywebio.input.input("请再次输入密码验证:", type="password")
        if password != vpwd:
            popup('错误', "两次输入密码不一致，请刷新页面重试")
            return
        put_text('初始化完成！请进入termuxAPP开始体验FlyOS吧！')
        termux_auth.change_passwd(password)
    try:
        os.mkdir(f"{HOME}/.flyos")
    except FileExistsError:
        pass
    conn = sqlite3.connect(f'{HOME}/.flyos/service.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE boot (
        ID INTEGER PRIMARY KEY NOT NULL,
        command           TEXT    NOT NULL,
        status            INT     NOT NULL
        );''')
    cur.execute('''CREATE TABLE login (
        ID INTEGER PRIMARY KEY NOT NULL,
        command           TEXT    NOT NULL,
        status            INT     NOT NULL
        );''')
    cur.execute('''INSERT INTO boot (command, status) VALUES (
        "ttyd pwlogin", 1
    )''')
    cur.execute(f'''INSERT INTO boot (command, status) VALUES (
        "python {FLYOS_ROOT}/panel/server.py", 1
    )''')
    cur.execute('''INSERT INTO boot (command, status) VALUES (
        "apachectl start", 1
    )''')
    cur.execute(f'''INSERT INTO boot (command, status) VALUES (
        "python {FLYOS_ROOT}/virtualmachine/web.py", 1
    )''')
    cur.execute('''INSERT INTO boot (command, status) VALUES (
        "nginx", 1
    )''')
    cur.execute('''INSERT INTO boot (command, status) VALUES (
        "php-fpm", 1
    )''')
    cur.execute('''INSERT INTO boot (command, status) VALUES (
        "http-server", 1
    )''')
    cur.execute(f'''INSERT INTO boot (command, status) VALUES (
        "python {FLYOS_ROOT}/phone/web.py", 1
    )''')
    cur.execute(f'''INSERT INTO boot (command, status) VALUES (
        "python {FLYOS_ROOT}/api/web.py", 1
    )''')
    cur.execute('''INSERT INTO boot (command, status) VALUES (
        "sshd", 1
    )''')
    cur.execute('''INSERT INTO boot (command, status) VALUES(
        "jupyter notebook --ip='0.0.0.0' --port=2000 --NotebookApp.token='' --no-browser", 1
    )''')
    cur.execute('''INSERT INTO boot (command, status) VALUES(
        "termux-wake-lock", 1
    )''')
    cur.execute('''INSERT INTO boot (command, status) VALUES(
        "code-server --bind-addr 0.0.0.0:2001", 1
    )''')
    conn.commit()
    conn.close()

    os.kill(os.getpid(), 9)

#Server Port 关于服务器的配置信息
if __name__ == '__main__':
    start_server(main, debug=True, host='0.0.0.0', port=5005)
