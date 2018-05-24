
def stringNotContainsChinese(string: str)->bool:
    """
    判断字符串是否不包含中文
    :param string: 待检测字符串
    :return: string含有中文则返回False，不含中文则返回True
    """
    if string is None:
        return False
    for i in range(len(string)):
        if ord(string[i]) > 255:
            return False
    return True
