import PySimpleGUI as sg
import time
import threading
from wlan_scan import get_signal_level


# 这些全局变量用来在主线程和后台线程之间共享数据
ssid='CMCC-student'
RED_THRESHHOLD = 3
ORANGE_THRESHHOLD = 15
backend_run = True
signal_level = 0
color = 'grey'
# base64编码的按钮图片
T_OFF = b'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'
T_ON = b'iVBORw0KGgoAAAANSUhEUgAAAFAAAAA8CAYAAADxJz2MAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAfWSURBVHhe7ZtfTNNXFMfPvS1toWUqEIf/wAzQLJmJZpnzwSXuTQX/JMsy5+u2d/dgIm5LTIzKnjTZ4172MLcl0wVFjUtMtjizmc1/y9TJKA4BARkWhFagwO/ufG9vuxaoVkS4uN8n1t7fvb+09vzOuefcc47k4uLi4uLi4uLyv0SY9ymzdc+JSiU824UQFfxhpcpxSpUUpYLEcnOLFShSLfxXj5CqSynqkko2C0Fn6w9WXzO3TIkpCbB676lXPEK8Qw7V8CesNtNzFBUWQtY7RMcbDmy+aCZz5okECG1zZN5+SWqHmSKPx0NFRUUUCgXJ7/eRz++ngM9P/oDf3GEHw0PDNDwSp/gwvw/HKRqNUW+kl0ZGR8wdDGukVFT7JFqZkwC37GsoEXG5n5R6n4TwSimodNEiKl6wgObNn8dTT70TzAqKbbl/YIAi9yPU1XmPRsdGzQp9KR35SX3dphZznZXH/vLte0+vdkg18K1LIaeFCxfS8uXl5PP5zB3PBxBeW2s7ddztIIcFy3/6pFJvn6irOWdumZRHCnDr3lM7+IM+Zw0LvVBYSJVVlRQMFpjV5xOYevj2ba2VLMVRRbS74VDNEbM8gawC3FJ7ahcL7jDG0LqqqgqSUuo121n4godWvJhHJSFJQb+kAn/iZw7GFcX4FYmOUbh7lO72pkw2A5h2y51Wam9rT0wIceTkgc0fJi4ymVSA0Dxe+poXVVl5mSgrW2ZW7MXLz3btSwFatTSPCgO5PWgI9PrdOF28DQfDujaOe/e6qampCeZMgp3LiUPVdWYpxQQBYs8bU+onmG15eRnNBeGtWuqj9VUB1rasBvVIIDwI8XLLMO9/ZtLQ3d1NjY1N2pxJiS0n66rPmiVNxjcmvK24ytNLYbYrV1aZFTvJ8wjatCqfVpTmmZmnoy0ySqd+f0ix4Uwp3mFzbm1tg2lHhRpbc7JuW9gsUYau61CFhQeHgT3PZqBt774enDbhgWVFXtq5LkRFwcwtAJZYUlyEcC1EHqn9QpLUnQiSWcTvI1SBt7XZYUDz3no1qJ3FdDMvX9LbrwUnbAcVlRV8aPByfCNrtn/csMFM/ydAnDAQJMN0bQ9VYLbPQnhJ4IS2rwkSnxdSIO5dsmSxnnEcwZaaQAsQZ1scz3DCQJBsM3AY02m22Vg030PrKgLmKsGyZUvMAUKs31J7ugZzWoA6McDgeGbzCQOhCrztTLH2JX+GKWNbW7J4kR7zVqdlljBhZFUYnG1tBnHeVEOVqTDZAysuKTYj2rhh3w9eqZ2HoNXIqiAxYDMIkmealxf7tNNKkp+fr19Mybyh2AaJZCiukJKyOasCp5HrCWM6gRaWl3jNVYJiDmmA8shtkoWmAz7k82wGZ9vZYvx3FxaGzEhVwlOXYohkqM0gMTBbjP9uJI01DpVK1DAwTk1aCrIqs8X470bGXSMhQCm0AFOTlpJMSc0G4z2/L2mtigXIS3qHtNmBgPRTgU1IpagLg6H4sJ6wlfEZkpkEecN04vG4GVGPRJ0UI1SrbAaZ5NkiFnfMKEFSgGwUXSkNRKnPZpCGny0i0UwBDhlZjaFAjwo9LmKxmJ60FdQwZotwd1rtmIlFo/qd9+UwB9KkU9SR+7160lZQABq/F80ESPE3/5P58O6jYscoJb6XiSq8CqNC/6C/Xy/Yys2Omd9mwvdGMgpOcTZfWCvS+wP+/LM6QkRvCN4jEbu18Ofmyatnzwpo3/m/hsxVgp6eHv0Oy/1x35tDWoBorMF7V0dXenuDdUB4v/49c9HC721x6nv4nwNBvbijU/tcoGWmBYiuJJb2uWR7g838xgJE9exZE4k5dL4xU/s6OzppcHAQ4cv1fl/wGOZShzyvoN14R28I2htsBWaF0uODwczQYjqBptdfidEIxylJtHK1J5TLUeITNl/9FFMChDNxSHyDxhr0hkBdbQWnkuOXYjQwNP1ChPC+u/JQa2A6LX/f4QAa4Yy60HBos/YZICVA4HVELcutD4016A2xGfzAL3+JUmff9AXY+MyjF6MTemY6ed/Di7VqlL1HRo9MRm3w1oWjfS+v33mZhzv7+wdkIBCwOtE6wrK7cTeuEyGl871TTjhgW7jGDqPh2sSuhL7ePmpsbNRjJcR7DQerz+gLw4TiauOFr26veGPnAP+jNvZGelUg4BfBoL1CxM9tZafyR3uc8n2CikKenAUJwTVxnFd/9SH92TGir9OB8G7cvMW7mRL8lI6w8D41SymyftXWj84cZpXdhTEajNDeMBdAAQg1jPT2tmQ+L9He5uizLY5nOGFkiythss3NzSwCXKlj7HXfTTqOdB75rLbVnt6jSOmOBfSGoL3heetMHQ+8LRyG3vMAa15/Xv7uyYQHHqvsW/ec3qiE+pZNOoTeELQ3oEI/V5otcwVRB+I8hCra26I7VYgP2Gy/MLdMSk67ha4de7yf8YazEdemT0SX90yNdM6Csy2OZzhhIEhOoC7A2548UH3JTGQlJwEmQVeSM0qHWP3WmSkqKCigIhZkIXvr5H9xSNUMLAOJULyQz0NKClmV9DQeC+M6guT0OO9xPJEAk6CxhiMH9IZAI0v05ByFTTdqUnrHcTzLttdlY0oCTILeELQ3oELP/5RK1ElR6kO1ytxiGz38g7t0JllQGPk8pKSQVTHrLi4uLi4uLi4uLjlA9C9TVjLI3KTNogAAAABJRU5ErkJggg=='


def backend_task():
    global signal_level
    seconds = 0.5

    while backend_run is True:
        # 调用wlan_scan的函数取得信号强度
        signal_level = get_signal_level(ssid)
        # 暂停0.5，不要给系统带来太大的负担
        time.sleep(seconds)
    print('backend task completes')


def main():
    global backend_run
    global color

    # 设置GUI窗口元素的大小和排列
    sg.theme('light grey')
    layout = [[sg.Col([[sg.T('SSID: '+ssid, font=("Arial", 15))],
                       [sg.T(font=("Arial", 30))],
                       [sg.T(str(0), key='-OUTPUT-', size=(2, 1), font=("Arial", 170))],
                       [sg.T(font=("Arial", 10))],
                       [sg.B(image_data=T_ON, k='-TOGGLE-', button_color=sg.theme_background_color(), metadata=True)]],
                       element_justification='center', k='-TOP COL-')]]
    window = sg.Window('无线信号检测器', layout, location=(0,0), size=(320,480))

    # 开始后台线程,更新信号强度signal_level
    threading.Thread(target=backend_task).start()

    while True:
        # 每500ms更新一次窗口
        event, values = window.read(timeout=500)

        # 窗口关闭
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        # 暂停/恢复按钮
        if event.startswith('-TOGGLE'):
            # 保存按钮的状态到metadata
            state = window[event].metadata = not window[event].metadata
            # 更新按钮的显示
            window[event].update(image_data=T_ON if state else T_OFF)
            if state:
                # 再次启动后台更新线程
                backend_run = True
                threading.Thread(target=backend_task).start()
                continue
            else:
                # 设置backend_run，让后台线程自己退出
                backend_run = False

        # 设置信号强度的颜色
        if backend_run == False:
            color='grey'
        elif signal_level < RED_THRESHHOLD:
            color='red'
        elif signal_level < ORANGE_THRESHHOLD:
            color='orange'
        else:
            color='green'
        window['-OUTPUT-'].update(str(signal_level), text_color=color)

    # 窗口关闭，结束后台线程
    backend_run = False
    window.close()
    print('main completes')


if __name__ == '__main__':
    main()

