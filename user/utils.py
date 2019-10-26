from MyWebSite.settings import LIMIT_TIME,LIMIT_COUNT
from .models import HostInfo

import pytz
import datetime


def limit_ip(request):
    now_time = datetime.datetime.now().replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    host = request.META.get('REMOTE_ADDR')
    ret = HostInfo.objects.filter(host=host).first()  # 找到对应ip
    if ret:
        d_value = now_time-ret.start_time
        if d_value.seconds < LIMIT_TIME and ret.is_lock:
            # 访问太频繁,已被限制
            return True
        elif d_value.seconds >=LIMIT_TIME:
            # 距离上次访问超过限定时间，重置时间
            ret.count = 1
            ret.start_time = now_time
            ret.is_lock = 0
            ret.save()
            return False

        else:
            # 60秒内还没被限制的
            if ret.count >=LIMIT_COUNT:
                ret.is_lock = 1
                ret.count = 0
                ret.save()
                return True
            else:
                ret.count +=1
                ret.start_time = now_time
                ret.save()
                return False

    else:
        HostInfo.objects.create(host=host, start_time=now_time, count=1)
        return False