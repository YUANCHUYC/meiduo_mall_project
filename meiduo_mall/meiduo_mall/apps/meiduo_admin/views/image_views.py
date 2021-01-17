"""
图片管理的视图
"""
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.image_serializers import *
from meiduo_admin.paginations import MyPage
from django.conf import settings
from fdfs_client.client import Fdfs_client


class ImageViewSet(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = ImageModelSerializer
    pagination_class = MyPage

    # 自定义视图函数，新建图片可选sku视图
    def simple(self, request):
        # 1、获取目标查询集
        skus = SKU.objects.all()
        # 2、获取序列化器对象
        serializer = SKUSimpleModelSerializer(instance=skus, many=True)
        # 3、构建响应返回
        return Response(serializer.data)

    # # 拓展类CreateModelMixin提取的视图函数create，无法使用序列化器完成图片上传fdfs操作
    # def create(self, request, *args, **kwargs):
    #     # 我们重写了create视图函数，来实现图片上传
    #     # 1、获取图片数据
    #     # request.FILES --> 字典类型，{"image": <文件对象>}
    #     # django后端把前端传来的image字段的图片数据，封装成了文件对象
    #     f = request.FILES.get('image')
    #     data = f.read()  # 读取图片数据
    #
    #     # 2、使用fdfs客户端接口上传图片
    #     conn = Fdfs_client(settings.FDFS_PATH)
    #     res = conn.upload_by_buffer(data)
    #     if res['Status'] != 'Upload successed.':
    #         return Response({'code': 400, 'errmsg': '图片上传失败'})
    #     file_id = res['Remote file_id']
    #
    #     # 3、新建SKUImage对象保存数据库
    #     sku_id = request.POST.get('sku')
    #     image = SKUImage.objects.create(
    #         sku_id=sku_id,
    #         image=file_id  # 新建模型类对象ImageField类型字段赋值为一个字符串文件id
    #     )
    #
    #     # 4、构建响应
    #     return Response({
    #         'id': image.id,
    #         'sku': image.sku.id,
    #         'image': image.image.url
    #     })
