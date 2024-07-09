from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *

webAcces=10

class Bush:
    def __init__(self, folder_id, name, rule_id, deviceSet=None):
        self.id=folder_id
        self.name=name
        self.rule=rule_id
        self.deviceSet=deviceSet
    def access(self, ruleCli):
        if self.rule > ruleCli:
            self.rule=ruleCli


def allFold(request):

    def addnestFold():
        pass

    if not 'user' in request.session:
        print('нет пользователя')
        return redirect('login')
    if 'oneFold' in request.session:
        print('есть 1 вложенный каталог')
        # idFol=request.session['rootOne']
        return redirect('onlyBush')
        # return redirect(reverse('showbush', args=[idFol[0].get('root_folder')]))
    if 'manyFold' in request.session:
        print('есть вложенные каталоги')
        # if 'rootOne' in request.session:
            # idFol=request.session['rootOne']
        return redirect('onlyBush')
            # return redirect(reverse('showbush', args=[idFol[0]]))
    user=request.session['user']
    allFold=Foldertab.objects.all()
    if not 'rootFold' in request.session:
        print('нет корневых')
        userPerm=UserPermtab.objects.filter(user_id=user.get('userid'))# это все права пользователя в querySet
        foldList=list(userPerm.values('folder_id', 'rule_id')) # это лист со словорями права для каталогов
        foldListMany=[]
        if len(foldList) < 2: # 1 каталог?
            print('foldList < 2')
            oneFoldId=foldList[0].get('folder_id')# id этого каталога
            foldDataOne=allFold.get(folder_id=oneFoldId) # выбрать данные по одному каталогу
            foldList[0]['name']=foldDataOne.name # добавить имя каталога к правам
            foldList[0]['root_folder']=foldDataOne.root_folder # добавить id корневого каталога к правам
            if foldDataOne.root_folder: # этот каталог не корневой?
                print('один каталог группа с устройствами')
                request.session['oneFold']=foldList
                return redirect('onlyBush')
                # return redirect(reverse('showbush', args=[foldDataOne.root_folder]))
            nestFold=list(allFold.filter(root_folder=oneFoldId).values('folder_id', 'root_folder', 'name')) # каталог 1 и он корневой; найти вложенные каталоги в лист
            for i in nestFold:
                i['rule_id']=foldList[0].get('rule_id') # каждой группе добавиить роль корневого каталога
                foldListMany.append(i)
            request.session['manyFold']=foldListMany # пользователь имеет доступ ко всем группа в одном корневом
            return redirect('onlyBush')
            # return redirect(reverse('showbush', args=[foldDataOne.root_folder]))
            
        # for i in foldList:
        #     foldDataMany=allFold.get(folder_id=i.get('folder_id'))
        #     i['name']=foldDataMany.name
        #     i['root_folder']=foldDataMany.root_folder
        #     foldListMany.append(i)
        # request.session['manyFold']=foldListMany # добавить в сессию каталоги (с данными) доступные пользователю
        folIdList=[]
        for i in userPerm:
            folIdList.append(i.folder_id) # собрать все id
        rootFolList=[]
        for i in folIdList:
            listFol=list(allFold.filter(folder_id=i).values_list('root_folder', flat=True)) # выбрать все корневые по id
            if not listFol[0]: # это корневой
                pass #найти вложенные в лист, присвоить роль, записать с сессию, записать каталог root
                rootFolList=rootFolList+listFol
            else:
                pass
        rootFolList=list(set(rootFolList))
        if len(rootFolList) < 2:
            print('меньше двух корневых')
            request.session['rootOne']=rootFolList
            return redirect('onlyBush')
            # return redirect(reverse('showbush', args=[rootFolList[0]]))
        request.session['rootFold']=rootFolList
    rootFolList=request.session['rootFold']
    rootFoldata=[]
    for i in rootFolList:
        rootFoldata=rootFoldata+list(allFold.filter(folder_id=i).values('folder_id', 'name'))
    return render(request, 'devices/fold-list.html', {'rootFoldata':rootFoldata, 'user':user})


def showBush(request, idFol):
    if not 'user' in request.session:
        return redirect('login')
    if 'manyFold' in request.session:
        foldData=request.session['manyFold']
    # elif 'oneFold' in request.session:
    #     foldData=request.session['oneFold']
    else:
        print('нет каталогов')
    user=request.session['user']
    if not idFol in request.session['rootFold']:
        return render(request, 'devices/warning.html', {'text':'Извините, у Вас нет доступа к такому ресурсу'})
    selectFold=[]
    for i in foldData:
        if i.get('root_folder')==idFol:
            bushObj=Bush(i.get('folder_id'), i.get('name'), i.get('rule_id'))
            bushObj.access(user.get('clrule'))
            if bushObj.rule >= webAcces:
                bushObj.deviceSet=Devicetab.objects.filter(folder_id=i.get('folder_id'))
                selectFold.append(bushObj)
    if not selectFold:
        return render(request, 'devices/warning.html', {'text':'Извините, Ваш уровень просмотра ограничен'})
    return render(request, 'devices/bushes.html', {'selectFold':selectFold,'user':user})


def onlyBush(request):
    user=request.session['user']
    if 'manyFold' in request.session:
        foldData=request.session['manyFold']
    if 'oneFold' in request.session:
        foldData=request.session['oneFold']

    selectFold=[]
    for i in foldData:
        bushObj=Bush(i.get('folder_id'), i.get('name'), i.get('rule_id'))#1
        bushObj.access(user.get('clrule'))#2
        devices=Devicetab.objects.filter(folder_id=i.get('folder_id'))#4 
        if bushObj.rule >= webAcces:#3
            selectFold.append(bushObj)#5
    if not selectFold:
        return render(request, 'devices/warning.html', {'text':'Извините, Ваш уровень просмотра ограничен'})
    return render(request, 'devices/bushes.html', {'selectFold':selectFold,'user':user})
