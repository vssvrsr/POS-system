from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
import json

from appFinal.views import isLogin
from appFinal.models import User, Shop, Employee
from .models import Message


def room(request):
    if not isLogin(request):    # 確認是否登入
        return redirect('/app')

    userNow = request.session['emp_name_ch']
    shopNow = request.session['user_shop_name']
    shopAll = Shop.objects.all()

    user_id_now = request.session['user_id']
    shop_id_now = request.session['user_shop']

    chat_messages = Message.objects.filter(
        group_name=shop_id_now).order_by("created")[:100]

    # 取得User中文名
    message_list = []
    for message_item in chat_messages:
        employee = Employee.objects.get(emp_id=message_item.user.user_emp_id)
        emp_name_ch = employee.emp_name_ch

        message_list.append({
            'user': message_item.user,
            'emp_name_ch': emp_name_ch,
            'group_name': message_item.group_name,
            'message': message_item.message,
            'created': message_item.created
        })

    return render(request, 'chat/room.html', locals())
