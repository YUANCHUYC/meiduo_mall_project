"""
自定义加密模块，使用itsdangrous来加解密数据
"""
from itsdangerous import TimedJSONWebSignatureSerializer
from django.conf import settings


class SecretOauth(object):

    def __init__(self):
        self.serializer = TimedJSONWebSignatureSerializer(
            settings.SECRET_KEY,
            expires_in=3600  # 秒
        )

    # 加密
    def dumps(self, content_dict):
        result = self.serializer.dumps(content_dict)
        return result.decode()

    # 解密
    def loads(self, access_token):
        # access_token秘文
        try:
            content_dict = self.serializer.loads(access_token)
        except Exception as e:
            # 解密错误
            return None
        return content_dict
