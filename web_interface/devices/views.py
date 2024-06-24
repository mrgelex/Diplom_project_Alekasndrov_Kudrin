from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

webAcces=0

class Bush:
    def __init__(self, folder_id, name, rule_id, deviceSet):
        self.id=folder_id
        self.name=name
        self.rule=rule_id
        self.deviceSet=deviceSet
    def access(self, ruleCli):
        if self.rule > ruleCli:
            self.rule=ruleCli

class Device:
    def __init__(self,device_id, name_user):
        self.device_id=device_id
        self.name_user=name_user


def allFold(request):
    if not 'user' in request.session:
        print('нет пользователя')
        return redirect('login')
    if 'oneFold' in request.session:
        print('есть 1 вложенный каталог')
        return redirect('showbush')
    if 'manyFold' in request.session:
        print('есть вложенные каталоги')
        if not 'rootFold' in request.session:
            return redirect('showbush')
    user=request.session['user']
    allFold=Foldertab.objects.all()
    if not 'rootFold' in request.session:
        print('нет корневых')
        userPerm=UserPermtab.objects.filter(user_id=user.get('userid'))
        print('userPerm', userPerm)
        if len(userPerm) < 2:
            print('userPerm < 2')
            foldListOne=list(userPerm.values('folder_id', 'rule_id'))
            foldDataOne=allFold.get(folder_id=foldListOne[0].get('folder_id'))
            foldListOne[0]['name']=foldDataOne.name
            foldListOne[0]['root_folder']=foldDataOne.root_folder
            request.session['oneFold']=foldListOne
            print('foldListOne', foldListOne)
            return redirect('showbush')
        foldDictList=list(userPerm.values('folder_id', 'rule_id'))
        print('foldDictList', foldDictList)
        foldListMany=[]
        for i in foldDictList:
            foldDataMany=allFold.get(folder_id=i.get('folder_id'))
            print('foldDataMany', foldDataMany)
            i['name']=foldDataMany.name
            i['root_folder']=foldDataMany.root_folder
            foldListMany.append(i)
        print('foldListMany', foldListMany)
        request.session['manyFold']=foldListMany
        folIdList=[]
        for i in userPerm:
            folIdList.append(i.folder_id)
        rootFolList=[]
        for i in folIdList:
            rootFolList=rootFolList+list(allFold.filter(folder_id=i).values_list('root_folder', flat=True))
        rootFolList=list(set(rootFolList))
        if len(rootFolList) < 2:
            print('меньше двух корневых')
            return redirect('showbush')
        request.session['rootFold']=rootFolList
    rootFoldata=[]
    for i in rootFolList:
        rootFoldata=rootFoldata+list(allFold.filter(folder_id=i).values('folder_id', 'name'))
    return render(request, 'devices/fold-list.html', {'rootFoldata':rootFoldata, 'user':user})

def showBush():
    return HttpResponse("<h1>Нет ничего</h1>")

# def showBush(request, idFol):
#     if not 'user' in request.session:
#         return redirect('login')
#     if 'manyFold' in request.session:
#         foldData=request.session['manyFold']
#     elif 'oneFold' in request.session:
#         foldData=request.session['oneFold']
#     else:
#         print('нет каталогов')
#     user=request.session['user']
#     if not idFol in request.session['rootFold']:
#         return render(request, 'devices/warning.html', {'text':'Извините, у Вас нет доступа к такому ресурсу'})
#     selectFold=[]
#     for i in foldData:
#         if i.get('root_folder')==idFol:
#             devices=Devicetab.objects.filter(folder_id=i.get('folder_id'))
#             bushObj=Bush(i.get('folder_id'), i.get('name'), i.get('rule_id'), devices)
#             bushObj.access(user.get('clrule'))
#             if bushObj.rule > webAcces:
#                 selectFold.append(bushObj)
#     if not selectFold:
#         return render(request, 'devices/warning.html', {'text':'Извините, Ваш уровень просмотра ограничен'})
#     return render(request, 'devices/bushes.html', {'selectFold':selectFold,'user':user})