import re
b = '会议地点: Guimarães, Portugal'
a = re.findall(r'会议地点: (.*)', b)
print(a)