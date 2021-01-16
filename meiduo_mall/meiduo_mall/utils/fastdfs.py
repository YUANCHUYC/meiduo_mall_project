"""
自定义文件存储后端，实现拼接完整图片链接
所谓的Django存储后端，决定了我们文件类型字段的新建保存和访问。
"""
# Storage是Django默认的存储后端
from django.core.files.storage import Storage
from django.conf import settings


class FastDFSStorage(Storage):

    def __init__(self, fdfs_base_url=None):
        self.fdfs_base_url = fdfs_base_url or settings.FDFS_BASE_URL

    def _open(self, name, mode='rb'):
        # 功能：打开django本地文件
        pass

    def _save(self, name, content, max_length=None):
        # 功能：保存文件 —— 项目二实现
        pass

    def url(self, name):
        # 功能：拼接返回完整的图片链接
        # 参数：name是文件索引标识(存储在mysql中文件id)
        return self.fdfs_base_url + name
