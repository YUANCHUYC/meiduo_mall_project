# 自定工程项目中使用的常规转换器

class UsernameConverter:
    """自定义路由转换器去匹配用户名"""
    # 定义匹配用户名的正则表达式
    regex = '[a-zA-Z0-9_-]{5,20}'

    # 功能：把路径参数，转化成一个python类型，传入视图函数
    # value：路径中的原值
    # return：返回值就是转化之后的数据
    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)


class MobileConverter:
    """自定义路由转换器去匹配手机号"""
    # 定义匹配手机号的正则表达式
    regex = '1[3-9]\d{9}'

    # 功能：把路径参数，转化成一个python类型，传入视图函数
    # value：路径中的原值
    # return：返回值就是转化之后的数据
    def to_python(self, value):
        # to_python：将匹配结果传递到视图内部时使用
        return str(value)

    # 路由反解析
    def to_url(self, value):
        # to_url：将匹配结果用于反向解析传值时使用
        return str(value)
