"""
    用于生成随机User-Agent字符串

    Attributes:
    -----------
    platforms : dict
        包含不同操作系统的版本号信息
    browsers : list
        包含不同的浏览器标识符
    user_agents : dict
        包含不同操作系统和浏览器组合的User-Agent字符串列表
    get_random(platform=None)
        生成一个随机的User-Agent字符串
    get_random_windows_ua()
        生成一个随机的Windows操作系统的User-Agent字符串
    get_random_mac_ua()
        生成一个随机的Mac操作系统的User-Agent字符串
    get_random_ios_ua()
        生成一个随机的iOS操作系统的User-Agent字符串
    get_random_android_ua()
        生成一个随机的Android操作系统的User-Agent字符串
"""
from random import choice

# 定义各个操作系统的版本号信息
platforms = {
    'Windows': ['Windows NT 10.0', 'Windows NT 6.3', 'Windows NT 6.2',
                'Windows NT 6.1', 'Windows NT 6.0',
                'Windows NT 5.1', 'Windows NT 5.0'],
    'Mac': ['Macintosh; Intel Mac OS X 10_14_6', 'Macintosh; Intel Mac OS X 10_13_6',
            'Macintosh; Intel Mac OS X 10_12_6', 'Macintosh; Intel Mac OS X 10_11_6',
            'Macintosh; Intel Mac OS X 10_10_5'],
    'iOS': ['iPad; CPU OS 13_3 like Mac OS X',
            'iPad; CPU OS 12_4_4 like Mac OS X',
            'iPhone; CPU iPhone OS 13_3 like Mac OS X',
            'iPhone; CPU iPhone OS 12_4_4 like Mac OS X'],
    'Android': ['Linux; Android 9.0; SM-G965F Build/PPR1.180610.011',
                'Linux; Android 8.0.0; SM-G950F Build/R16NW',
                'Linux; Android 7.0; SAMSUNG SM-G930F Build/NRD90M',
                'Linux; Android 6.0.1; SAMSUNG SM-G920F Build/MMB29K']
}
# 定义不同浏览器的标识符
browsers = ['Chrome/80.0.3987.149', 'Firefox/74.0',
            'Safari/537.36', 'Edge/18.17763', 'Opera/66.0.3515.115',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)']


def __get_ua(version, browser):
    return f'Mozilla/5.0 ({version}) {browser}'


def get_random(platform=None):
    """

    :param platform: 随机ua字符串
    :return:
    """
    if platform:
        return __get_ua(choice(platforms[platform]), choice(browsers))
    return __get_ua(choice(sum(platforms.values(), [])), choice(browsers))


def get_random_windows_ua():
    """

    :return: windows ua字符串
    """
    return get_random('Windows')


# 生成一个随机的Mac操作系统的User-Agent字符串
def get_random_mac_ua():
    """

    :return: mac ua字符串
    """
    return get_random('Mac')


def get_random_ios_ua():
    """

    :return: ios ua字符串
    """
    return get_random('iOS')


def get_random_android_ua():
    """
    :return: 安卓 ua字符串
    """
    return get_random('Android')
