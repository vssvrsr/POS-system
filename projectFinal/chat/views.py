from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
import json

from appFinal.views import isLogin
from appFinal.models import User, Shop
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

    return render(request, 'chat/room.html', locals())
