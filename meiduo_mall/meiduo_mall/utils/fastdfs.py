"""
自定义文件存储后端，实现拼接完整图片链接
所谓的Django存储后端，决定了我们文件类型字段的新建保存和访问。
"""
# Storage是Django默认的存储后端
from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client
from rest_framework.exceptions import ValidationError


class FastDFSStorage(Storage):

    def __init__(self, fdfs_base_url=None):
        self.fdfs_base_url = fdfs_base_url or settings.FDFS_BASE_URL

    def _open(self, name, mode='rb'):
        # 功能：打开django本地文件 —— 文件保存在django本地
        pass

    def _save(self, name, content, max_length=None):
        # 功能：在ImageField类型字段被赋值为一个文件对象的时候触发调用保存文件数据
        # 参数: @name:文件名；@content:文件对象；
        # 返回值：返回值就是将来保存到数据库的值(返回文件id)
        # (1)、提取文件数据
        data = content.read()
        # (2)、上传到fdfs
        conn = Fdfs_client(settings.FDFS_PATH)
        res = conn.upload_by_buffer(data)
        if res['Status'] != 'Upload successed.':
            raise ValidationError('fdfs上传失败！')
        file_id = res['Remote file_id']
        # (3)、返回文件id
        return file_id

    def exists(self, name):
        # 功能：用于判断保存的文件是否重复
        # 参数：@name：本地保存的文件名
        # 返回值：True表示存在；False表示不存在；
        # 注意：此处如果返回True表示文件已保存则不会在调用_save方法保存。
        # 此处我们固定返回False，表示文件未保存，直接调用_save方法实现上传fdfs
        # 而fdfs服务器会自行判断文件是否存在不会重复保存。
        return False

    def url(self, name):
        # 功能：拼接返回完整的图片链接
        # 参数：name是文件索引标识(存储在mysql中文件id)
        return self.fdfs_base_url + name
