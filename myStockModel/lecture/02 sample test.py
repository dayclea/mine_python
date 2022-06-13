import FinanceDataReader as web
from datetime import date, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import platform

from matplotlib import font_manager, rc
if platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
elif platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
else:
    pass

today = date.today()
startday = date.today() - timedelta(720)
yesterday = date.today() - timedelta(1)
print(yesterday)

SEC = web.DataReader("USD/KRW", startday, yesterday)
print(type(SEC))
print(SEC.tail(10))
# SEC['Close'].plot(figsize=(16,4))

plt.subplot(211)
plt.title("USD/KRW_Open")
# plt.ylim([30000000, 50000000]) # y축의 범위 설정용. 안하면 전체 범위로 출력
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))

SEC[str(startday):str(yesterday)]['Open'].plot(figsize=(16, 10), style='b', xlabel='Date', ylabel='종가')
plt.subplots_adjust(hspace=0.5)

plt.subplot(212)
plt.title("USD/KRW_Close")
SEC[str(startday):str(yesterday)]["Close"].plot(figsize=(16, 10), style='g')

plt.show()