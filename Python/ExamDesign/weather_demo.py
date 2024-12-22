import tkinter as tk
from tkinter import messagebox
import mysql.connector
import json
import requests
from datetime import datetime
from tkinter import ttk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

plt.rcParams['font.family'] = 'STsong'
plt.rcParams['font.style'] = 'normal'

CITY_CODES = {
    "广州": "59287",
    "深圳": "59493",
    "珠海": "59488",
    "北京": "54511",
    "上海": "58362",
    "杭州": "58457",
}


class LoginWindow:  # 登录窗口
    def __init__(self):  # 初始化登录窗口
        self.window = tk.Tk()
        self.window.title("登录系统")
        self.window.geometry("300x300")

        self.label_username = tk.Label(self.window, text="用户名:")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(self.window)
        # self.entry_username.insert(0, "test")
        self.entry_username.pack()

        self.label_password = tk.Label(self.window, text="密码:")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(self.window, show="*")
        # self.entry_password.insert(0, "123456")
        self.entry_password.pack()

        self.login_button = tk.Button(self.window, text="登录", command=self.login)
        self.login_button.pack(pady=20)

        self.register_button = tk.Button(self.window, text="注册新用户", command=self.open_register_window)
        self.register_button.pack(pady=5)

    def login(self):  # 连接数据库，进行登录
        username = self.entry_username.get()
        password = self.entry_password.get()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Mysql135!",
                database="py_db"
            )

            cursor = conn.cursor()

            # 执行查询
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))

            result = cursor.fetchone()

            if result:
                messagebox.showinfo("成功", "登录成功！")
                self.window.destroy()
                MainWindow(username)
            else:
                messagebox.showerror("错误", "用户名或密码错误！")

        except mysql.connector.Error as err:
            messagebox.showerror("数据库错误", f"发生错误: {err}")

        finally:
            if 'conn' in locals():
                conn.close()

    def open_register_window(self):  # 打开注册窗口
        RegisterWindow()

    def run(self):  # 运行登录窗口
        self.window.mainloop()


class RegisterWindow:  # 注册窗口
    def __init__(self):  # 初始化注册窗口
        self.window = tk.Toplevel()
        self.window.title("注册新用户")
        self.window.geometry("300x250")
        self.window.wm_minsize(300, 250)

        self.label_username = tk.Label(self.window, text="用户名:")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(self.window)
        self.entry_username.pack()

        self.label_password = tk.Label(self.window, text="密码:")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(self.window, show="*")
        self.entry_password.pack()

        self.label_confirm = tk.Label(self.window, text="确认密码:")
        self.label_confirm.pack(pady=10)
        self.entry_confirm = tk.Entry(self.window, show="*")
        self.entry_confirm.pack()

        self.register_button = tk.Button(self.window, text="注册", command=self.register)
        self.register_button.pack(pady=20)

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        confirm = self.entry_confirm.get()

        if not username or not password or not confirm:
            messagebox.showerror("错误", "所有字段都必须填写！")
            return

        if password != confirm:
            messagebox.showerror("错误", "两次输入的密码不一致！")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Mysql135!",
                database="py_db"
            )

            cursor = conn.cursor()

            check_query = "SELECT * FROM users WHERE username = %s"  # 检查用户名是否已存在
            cursor.execute(check_query, (username,))

            if cursor.fetchone():
                messagebox.showerror("错误", "用户名已存在！")
                return

            insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, password))
            conn.commit()

            messagebox.showinfo("成功", "注册成功！")
            self.window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("数据库错误", f"发生错误: {err}")

        finally:
            if 'conn' in locals():
                conn.close()


def get_city_weather(city_name):  # 获取指定城市的天气信息
    if city_name not in CITY_CODES:
        messagebox.showerror("错误", "不支持的城市")
        return None

    json_filename = f'{city_name}_weather.json'

    try:
        city_code = CITY_CODES[city_name]
        api_url = f'https://weather.cma.cn/api/weather/view?stationid={city_code}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': f'https://weather.cma.cn/web/weather/{city_code}.html',
            'Accept': 'application/json, text/plain, */*',
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        weather_data = {
            "城市": city_name,
            "获取时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "天气预报": []
        }

        if 'data' in data and 'daily' in data['data']:
            for day in data['data']['daily']:
                day_data = {
                    "日期": day.get('date', ''),
                    "白天": {
                        "天气状况": day.get('dayText', ''),
                        "温度": f"{day.get('high', '')}℃",
                        "风况": f"{day.get('dayWindDirection', '')} {day.get('dayWindScale', '')}"
                    },
                    "夜间": {
                        "天气状况": day.get('nightText', ''),
                        "温度": f"{day.get('low', '')}℃",
                        "风况": f"{day.get('nightWindDirection', '')} {day.get('nightWindScale', '')}"
                    }
                }
                weather_data["天气预报"].append(day_data)

        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)

        return weather_data, json_filename

    except Exception as e:  # 直接尝试读取本地数据，不显示警告
        if os.path.exists(json_filename):
            with open(json_filename, 'r', encoding='utf-8') as f:
                weather_data = json.load(f)
            return weather_data, json_filename
        else:
            messagebox.showerror("错误", "本地没有可用的天气数据")
            return None, None


class MainWindow:  # 主界面
    def __init__(self, username):  # 初始化主界面
        self.window = tk.Tk()
        self.window.title("主界面")
        self.window.geometry("400x300")
        self.window.wm_minsize(400, 300)

        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        welcome_text = f"欢迎您，这是您的专属天气预报系统，{username}!"
        self.label_welcome = tk.Label(self.main_frame, text=welcome_text, font=("Arial", 12))
        self.label_welcome.pack(pady=30)

        self.weather_button = tk.Button(self.main_frame, text="天气预报", command=self.open_weather)
        self.weather_button.pack(pady=10)

        self.logout_button = tk.Button(self.main_frame, text="退出登录", command=self.logout)
        self.logout_button.pack(pady=20)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.mainloop()

    def open_weather(self):  # 切换到天气预报界面
        self.window.geometry("950x700")
        self.window.wm_minsize(950, 700)

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        weather_data, json_file = get_city_weather("广州")
        if weather_data and weather_data["天气预报"]:
            button_frame = tk.Frame(self.main_frame)
            button_frame.pack(pady=10)

            back_button = tk.Button(button_frame, text="返回主界面", command=self.return_to_main)
            back_button.pack()

            WeatherWindow("广州", self.main_frame)
        else:
            messagebox.showerror("错误", "未能获取到天气数据，请检查网络连接或API是否可用")
            self.return_to_main()

    def return_to_main(self):  # 返回主界面
        self.window.geometry("400x300")
        self.window.wm_minsize(400, 300)

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        welcome_text = "欢迎您！"
        self.label_welcome = tk.Label(self.main_frame, text=welcome_text, font=("Arial", 14))
        self.label_welcome.pack(pady=30)

        self.weather_button = tk.Button(self.main_frame, text="天气预报", command=self.open_weather)
        self.weather_button.pack(pady=10)

        self.logout_button = tk.Button(self.main_frame, text="退出登录", command=self.logout)
        self.logout_button.pack(pady=20)

    def on_closing(self):  # 主窗口关闭时不删除JSON文件
        self.window.destroy()

    def logout(self):  # 退出登录时不删除JSON文件
        self.window.destroy()
        LoginWindow().run()


class WeatherWindow:  # 天气预报窗口
    def __init__(self, city_name="广州", parent_frame=None):
        self.current_city = city_name
        self.json_file = f'{city_name}_weather.json'

        with open(self.json_file, 'r', encoding='utf-8') as f:  # 读取JSON文件
            self.weather_data = json.load(f)

        self.parent_frame = parent_frame  # 使用传入的父框架

        city_frame = tk.Frame(self.parent_frame)  # 创建城市选择框架
        city_frame.pack(pady=10)

        # 添加城市选择下拉菜单
        self.city_var = tk.StringVar(value=city_name)
        city_label = tk.Label(city_frame, text="选择城市:", font=("Arial", 18))
        city_label.pack(side=tk.LEFT, padx=5)

        city_combo = ttk.Combobox(city_frame, textvariable=self.city_var, values=list(CITY_CODES.keys()))
        city_combo.pack(side=tk.LEFT, padx=5)
        city_combo.bind('<<ComboboxSelected>>', self.on_city_change)

        # 创建Canvas和Scrollbar
        self.canvas = tk.Canvas(self.parent_frame)
        self.scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.display_weather_info()  # 显示天气信息

        self.add_weather_charts()  # 在显示天气信息之后添加图表

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def display_weather_info(self):
        # 清除现有的天气信息
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 创建一个居中的容器框架
        center_frame = tk.Frame(self.scrollable_frame)
        center_frame.pack(expand=True)

        # 显示获取时间
        time_label = tk.Label(center_frame, text=f"获取时间: {self.weather_data['获取时间']}", font=("Arial", 12))
        time_label.pack(pady=10)

        # 添加天气提示文本区域
        weather_tips_frame = tk.Frame(center_frame, bg="#F0F0F0", padx=10, pady=5)
        weather_tips_frame.pack(fill=tk.X, pady=(0, 10))

        weather_tips_text = tk.Label(
            weather_tips_frame,
            text="          今天是" + self.weather_data['天气预报'][0]['日期'] + ","
                 + self.weather_data['天气预报'][0]['白天']['天气状况'] + ","
                 + self.weather_data['天气预报'][0]['白天']['温度'] + ","
                 + self.weather_data['天气预报'][0]['白天']['风况'] + "\n" + "\n" +
                 "       银河有迹可循，快乐后会有期，千万别回头呀，往后的日子都是崭新的,快乐是需要自己去追寻的！！！",
            wraplength=600,  # 文本自动换行宽度
            justify=tk.LEFT,
            bg="#F0F0F0",
            font=("Arial", 16)
        )
        weather_tips_text.pack()

        # 创建一个Frame来水平排列天气信息
        weather_frame = tk.Frame(center_frame)
        weather_frame.pack(pady=10)

        # 显示每天天气预报
        for day in self.weather_data['天气预报']:
            # 为每天创建一个垂直Frame
            day_frame = tk.Frame(weather_frame, bg="#4A90E2", padx=8, pady=5)  # 稍微减小内边距
            day_frame.pack(side=tk.LEFT, padx=3)  # 减小卡片间距

            # 日期标签
            date_label = tk.Label(day_frame, text=day['日期'],
                                  bg="#4A90E2", fg="white",
                                  font=("Arial", 11, "bold"))  # 稍微减小字体
            date_label.pack()

            # 白天天气
            day_weather = f"白天: {day['白天']['天气状况']}\n温度: {day['白天']['温度']}\n{day['白天']['风况']}"
            day_label = tk.Label(day_frame, text=day_weather,
                                 bg="#4A90E2", fg="white",
                                 justify=tk.LEFT,
                                 font=("Arial", 10))  # 设置字体大小
            day_label.pack(pady=2)

            # 夜间天气
            night_weather = f"夜间: {day['夜间']['天气状况']}\n温度: {day['夜间']['温度']}\n{day['夜间']['风况']}"
            night_label = tk.Label(day_frame, text=night_weather,
                                   bg="#4A90E2", fg="white",
                                   justify=tk.LEFT,
                                   font=("Arial", 10))  # 设置字体大小
            night_label.pack(pady=2)

    def add_weather_charts(self):
        """添加天气数据可视化图表"""
        # 创建图表框架
        chart_frame = ttk.Frame(self.scrollable_frame)
        chart_frame.pack(fill=tk.X, padx=20, pady=10)

        # 创建图表，缩小整体大小
        fig = Figure(figsize=(9, 4))  # 减小图表尺寸

        # 创建两个子图并排放置
        gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1])
        ax1 = fig.add_subplot(gs[0])  # 温度趋势图
        ax2 = fig.add_subplot(gs[1])  # 天气状况统计

        # 提取数据
        dates = [day['日期'] for day in self.weather_data['天气预报']]
        high_temps = [float(day['白天']['温度'].replace('℃', ''))
                      for day in self.weather_data['天气预报']]
        low_temps = [float(day['夜间']['温度'].replace('℃', ''))
                     for day in self.weather_data['天气预报']]

        # 绘制温度趋势图
        ax1.plot(dates, high_temps, 'ro-', label='日间温度', linewidth=2)
        ax1.plot(dates, low_temps, 'bo-', label='夜间温度', linewidth=2)
        ax1.set_title('温度变化趋势', pad=15, fontsize=11)  # 减小标题字体
        ax1.set_xlabel('日期', fontsize=9)
        ax1.set_ylabel('温度 (℃)', fontsize=9)
        ax1.legend(fontsize=9)
        ax1.grid(True, linestyle='--', alpha=0.7)

        # 调整x轴标签
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=8)  # 减小刻度字体

        # 统计天气状况
        day_weather_types = [day['白天']['天气状况']
                             for day in self.weather_data['天气预报']]
        weather_counts = {}
        for weather in day_weather_types:
            weather_counts[weather] = weather_counts.get(weather, 0) + 1

        # 绘制天气状况饼图
        if weather_counts:
            patches, texts, autotexts = ax2.pie(
                weather_counts.values(),
                labels=weather_counts.keys(),
                autopct='%1.1f%%',
                startangle=90
            )
            ax2.set_title('天气状况分布', pad=15, fontsize=11)  # 减小标题字体

            # 调整饼图文本大小
            plt.setp(autotexts, size=8)
            plt.setp(texts, size=8)

        # 调整布局
        fig.tight_layout()

        # 创建canvas并添加到窗口
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_city_change(self, event):
        """城市选择改变时的处理函数"""
        new_city = self.city_var.get()
        if new_city != self.current_city:
            weather_data, json_file = get_city_weather(new_city)
            if weather_data:
                self.current_city = new_city
                self.json_file = json_file
                self.weather_data = weather_data
                self.display_weather_info()
                self.add_weather_charts()


if __name__ == "__main__":
    app = LoginWindow()
    app.run()
