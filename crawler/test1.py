a = int(input("请输入a的值："))
b = int(input("请输入b的值："))
if a > 0 and b > 0:
    x = int(input("请输入x的值："))
    if x > 0 and x <= 1:
        if a > 5000 and b < 1000 and x > 0.5:
            y = (a-b) * x * 0.9
        else:
            y = (a - b) * x
        print(y)
    else:
        print("输入出错")
else:
    print("输入出错")