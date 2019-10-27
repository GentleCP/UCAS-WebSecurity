from MyWebSite.settings import LIMIT_TIME,LIMIT_COUNT
from .models import HostInfo
from .models import LoginError
from django.contrib.auth.models import User
from django.contrib import auth
from MyWebSite.settings import ACCOUNT_LIMIT_TIME, MAX_ERR_LOGIN_TIMES


import pytz
import datetime
import time


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
            if ret.count >= LIMIT_COUNT:
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


def check_account_state(request):
    """
    检查账户是否在封禁状态
    Args:
        request: request对象
    Returns:
        state: 1表示该账户状态正常，0表示该账户还在被封禁状态，-1表示用户名或密码错误
    """
    state = 1
    username = request.POST.get('username', "")
    password = request.POST.get('password', "")
    auth_res = auth.authenticate(username=username, password=password)
    default_first_err_time = datetime.datetime(2019, 10, 24, 12, 30, 11).replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    default_first_err_time = timestamp_to_1970(default_first_err_time)
    curr_time = datetime.datetime.now().replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    curr_time = timestamp_to_1970(curr_time)

    # auth_user表中查找该用户
    user_obj = User.objects.filter(username=username).first()
    if not user_obj:  # 该用户不存在
        state = -1
        return state  # 直接返回True，交给Form进一步判断

    # 据user id查询login_err表
    login_err = LoginError.objects.filter(user=user_obj).first()
    if (not login_err) and (not auth_res):  # login_err表中没有该账户的记录并且登录失败
        err_login_times = 1
        block_state = False
        login_err_obj = LoginError(user=user_obj, first_err_time=curr_time, err_login_times=err_login_times, block_state=block_state)
        login_err_obj.save()
    elif login_err:  # login_err表中存在该账户的记录
        first_err_time = login_err.first_err_time
        err_login_times = login_err.err_login_times
        block_state = login_err.block_state

        time_interval = curr_time - first_err_time

        if time_interval > ACCOUNT_LIMIT_TIME:  # 超过10min
            if not auth_res:  # 用户名密码错误，重置login_err对象，并将错误次数置为1
                login_err = set_login_err(login_err, curr_time, 1, False)
                login_err.save()
            else:  # 用户名密码正确，登录成功
                login_err = set_login_err(login_err, default_first_err_time, 0, False)
                login_err.save()
        elif (time_interval <= ACCOUNT_LIMIT_TIME) and block_state:  # 10min内，并且账户已被封禁
            state = 0
            return state
        elif (time_interval <= ACCOUNT_LIMIT_TIME) and (not block_state):  # 10min内，并且账户未被封禁
            if not auth_res:  # 用户名和密码错误
                err_login_times = err_login_times + 1
                login_err = set_login_err(login_err, first_err_time, err_login_times, False)
                if err_login_times == MAX_ERR_LOGIN_TIMES:
                    login_err = set_login_err(login_err, first_err_time, 0, True)  # 这里的时间必须是数据库中取出来的第一次登录失败的时间
                login_err.save()
            else:  # 用户名和密码正确
                login_err = set_login_err(login_err, default_first_err_time, 0, False)
                login_err.save()
    elif auth_res:
        return state

    return state


def set_login_err(login_err, first_err_time, err_login_times, block_state):
    """
    更新 login_err 对象
    """
    login_err.first_err_time = first_err_time
    login_err.err_login_times = err_login_times
    login_err.block_state = block_state

    return login_err


def timestamp_to_1970(timestamp):
    """
    当前时间距离1970的秒数
    """
    return time.mktime(timestamp.timetuple())



