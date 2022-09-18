import os
import sys
import time
import subprocess


def get_signal_level(ssid):
    '''
    执行iw dev wlan scan的输出
pi@raspberrypi:~/wlan_scan $ sudo iw dev wlan0 scan
BSS d0:79:80:1b:3c:71(on wlan0)
	last seen: 702.018s [boottime]
	TSF: 0 usec (0d, 00:00:00)
	freq: 2422
	beacon interval: 100 TUs
	capability: ESS Privacy ShortPreamble ShortSlotTime APSD RadioMeasure (0x1c31)
	signal: -25.00 dBm
	last seen: 0 ms ago
	SSID: CMCC-student
	Supported rates: 1.0* 2.0* 5.5* 11.0* 9.0 18.0 36.0 54.0 
	DS Parameter set: channel 3
	TIM: DTIM Count 0 DTIM Period 1 Bitmap Control 0x0 Bitmap[0] 0x0
	Country: CN	Environment: bogus
		Channels [1 - 13] @ 30 dBm
	Power constraint: 0 dB
	TPC report: TX power: 22 dBm
...
    '''
    # 获得无线网络信号强度的命令
    command = 'sudo iw dev wlan0 scan | grep -B 3 "SSID: {}" | grep signal'.format(ssid)

    while True:
        try:
            # 执行命令，当有多个同名的SSID时，结果是多行
            signal_lines = subprocess.check_output(command, shell=True).decode().split('\n')
        except:
            # 无线网卡忙时，命令可能出错，直接重试即可
            print('retry cmd...')
            continue

        signal_level = -99
        for signal_line in signal_lines: # 例如 signal: -28.00 dBm
            try:
                # 字符串处理得到数字部分的字符串
                signal_dBm = signal_line.split(' ')[1]
                # 将数字字符串转化为小数
                signal_dBm = float(signal_dBm)
    
                signal_level_new = signal_dBm
                # 四舍五入
                signal_level_new = round(signal_level_new)
    
                # 多个结果时，只保留最大值
                if signal_level_new > signal_level:
                    signal_level = signal_level_new
            # 如果某一行处理有格式错误，直接丢弃，继续处理后面的行
            except:
                print('skip this line...')
                continue

        print('signal_level: '+str(signal_level), flush=True)
        break
    return signal_level


if __name__ == '__main__':
    get_signal_level('CMCC-student')

