# django 库
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# 本地库
from blog.models import Blog
from .models import ReadNum
from .models import ReadDetail

def read_once(request,obj):
    '''
    阅读一次给阅读数量加一
    :param request:
    :param obj: 需要增加阅读数的对象,例如Blog
    :return: read_key，string 包含哪个对象已经阅读的信息
    '''
    ct = ContentType.objects.get_for_model(obj)
    read_key = "%s_%s_read" % (ct.model,obj.id)

    if not request.COOKIES.get(read_key):
        # 总的阅读量增加
        readnum,created = ReadNum.objects.get_or_create(content_type=ct,object_id= obj.id) # 方法返回一个元组第二参数无用
        # 阅读一次
        readnum.add_read_num() # 函数包含了保存操作
        # 当天阅读量增加
        today = timezone.now().date() # 获取现在时间的date部分，精确到日
        readdetail,created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.id, read_date =today)
        readdetail.add_read_num()
    return read_key

