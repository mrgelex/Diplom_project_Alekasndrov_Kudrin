from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
import socket_mod as s
import perm_for_web as p

webAcces=p.web
lvlbutSP=p.viewSP
lvlbutChart=p.shart

class Bush:
    def __init__(self, folder_id, name, rule_id, deviceDicts=None):
        self.id=folder_id
        self.name=name
        self.rule=rule_id
        self.deviceDicts=deviceDicts
    def access(self, ruleCli):
        if self.rule > ruleCli:
            self.rule=ruleCli

class Dev:
    def __init__(self, dbData, operData):
        pass

def allFold(request):

    def addnestFold(dictFold, foldId):
        DataList=[]
        nestFold=list(allFold.filter(root_folder=foldId).values('folder_id', 'root_folder', 'name')) # каталог 1 и он корневой; найти вложенные каталоги в лист
        for i in nestFold:
            i['rule_id']=dictFold.get('rule_id') # каждой группе добавиить роль корневого каталога
            DataList.append(i)
        return DataList
    
    def addFold(dictFold, foldId):
        foldData=allFold.get(folder_id=foldId) # выбрать данные по одному каталогу
        dictFold['name']=foldData.name # добавить имя каталога к правам
        dictFold['root_folder']=foldData.root_folder # добавить id корневого каталога к правам
        return dictFold

    if not 'user' in request.session:
        # print('нет пользователя')
        return redirect('login')
    if 'oneFold' in request.session:
        # print('есть 1 вложенный каталог')
        idFol=request.session['rootOne']
        # return redirect('onlyBush')
        return redirect(reverse('showbush', args=[idFol]))
    if 'manyFold' in request.session:
        # print('есть вложенные каталоги')
        if 'rootOne' in request.session:
            idFol=request.session['rootOne']
        # return redirect('onlyBush')
            return redirect(reverse('showbush', args=[idFol]))
    user=request.session['user']
    if user.get('clrule') < webAcces:
        return render(request, 'devices/warning.html', {'text':'Извините, Ваш уровень доступа ограничен', 'user':user})
    allFold=Foldertab.objects.all()
    if not 'rootOne' or not 'rootMany' in request.session:
        # print('нет корневых')
        userPerm=UserPermtab.objects.filter(user_id=user.get('userid'))# это все права пользователя в querySet
        foldList=list(userPerm.values('folder_id', 'rule_id')) # это лист со словорями права для каталогов
        folDataList=[]
        if len(foldList) < 2: # 1 каталог?
            # print('foldList < 2')
            oneFoldId=foldList[0].get('folder_id')# id этого каталога
            dictFold=addFold(foldList[0], oneFoldId)
            if dictFold.get('root_folder'): # этот каталог не корневой?
                # print('один каталог группа с устройствами')
                request.session['oneFold']=dictFold
                request.session['rootOne']=dictFold.get('root_folder')
                # return redirect('onlyBush')
                return redirect(reverse('showbush', args=[dictFold.get('root_folder')]))
            request.session['manyFold']=addnestFold(foldList[0], oneFoldId) # пользователь имеет доступ ко всем группа в одном корневом
            request.session['rootOne']=oneFoldId
            # return redirect('onlyBush')
            return redirect(reverse('showbush', args=[oneFoldId]))
        rootFolList=[]
        for i in foldList:
            rootValid=list(allFold.filter(folder_id=i.get('folder_id')).values_list('root_folder', flat=True)) # выбрать все корневые по id
            if not rootValid[0]: # это корневой
                # print(rootValid[0])
                folDataList=folDataList+addnestFold(i, i.get('folder_id'))
                rootFolList.append(i.get('folder_id'))
            else:
                folDataList.append(addFold(i, i.get('folder_id')))
                rootFolList=rootFolList+rootValid
        request.session['manyFold']=folDataList
        rootFolList=list(set(rootFolList))
        if len(rootFolList) < 2:
            # print('меньше двух корневых')
            request.session['rootOne']=rootFolList
            # return redirect('onlyBush')
            return redirect(reverse('showbush', args=[rootFolList[0]]))
        request.session['rootMany']=rootFolList
    rootFolList=request.session['rootMany']
    rootFoldata=[]
    for i in rootFolList:
        rootFoldata=rootFoldata+list(allFold.filter(folder_id=i).values('folder_id', 'name'))
    return render(request, 'devices/fold-list.html', {'rootFoldata':rootFoldata, 'user':user})


def showBush(request, idFol):
    # print(idFol)
    if not 'user' in request.session:
        return redirect('login')
    if 'manyFold' in request.session:
        foldData=request.session['manyFold']
    elif 'oneFold' in request.session:
        foldData=[request.session['oneFold']]
        # print(foldData)
    else:
        pass
        # print('нет каталогов')
    user=request.session['user']
    if 'rootMany' in request.session:
        rootSession=request.session['rootMany']
    if 'rootOne' in request.session:
        rootSession=[request.session['rootOne']]
    # print(rootSession)
    if not idFol in rootSession:
        return render(request, 'devices/warning.html', {'text':'Извините, у Вас нет доступа к такому ресурсу<br/>Пожалуйста, используйте графический интерфейс для доступа к Вашим ресурсам', 'user':user})
    
    selectFold=[]
    for i in foldData:
        if i.get('root_folder')==idFol:
            bushObj=Bush(i.get('folder_id'), i.get('name'), i.get('rule_id'))
            bushObj.access(user.get('clrule'))
            if bushObj.rule >= webAcces:
                deviceSet=Devicetab.objects.filter(folder_id=i.get('folder_id'), enable=True)
                if deviceSet:
                    print('yes')
                    dDev=deviceSet.values('device_id', 'name_user','description')
                    for f in dDev:
                        f.update(s.operData(f.get('device_id'), True))
                    print(dDev)
                        
                    bushObj.deviceDicts=dDev
                    devlist=list(deviceSet.values_list('device_id', flat=True))
                    dictDev={}

                    if 'validF' in request.session:
                        # print('данные в сессии есть')
                        validF=request.session['validF']
                        if not isinstance(validF, list):
                            validF=[validF]
                            #  print('преобразован в список', validF)
                        if not i.get('folder_id') in validF:
                            # print('каталога в сессии нет')
                            # print('исследуемый каталог',i.get('folder_id'))
                            validF.append(i.get('folder_id'))
                            request.session['validF']=validF
                            # print('список до записи', validF)
                            # print('каталог записан', request.session['validF'])
                            if 'accesD' in request.session:
                                accesD=request.session['accesD']
                                # print('yes', accesD)
                            else:
                                accesD={}
                                # print('no', accesD)
                            for i in devlist:
                                dictDev[str(i)]=bushObj.rule
                            accesD.update(dictDev)
                            # print('полученный словарь устройств', accesD)
                            request.session['accesD']=accesD
                        pass
                    else:
                        request.session['validF']=i.get('folder_id')

                        # print('каталог не проверен и вообще нет данных в сессии', 'первый записан', request.session['validF'])
                        for i in devlist:
                            dictDev[str(i)]=bushObj.rule
                        request.session['accesD']=dictDev
                        # print('словарь записан', request.session['accesD'])
                    selectFold.append(bushObj)
                else:
                    text='Отображение устройств отключено'
            else:
                text='Извините, Ваш уровень доступа ограничен'

    if not selectFold:
        return render(request, 'devices/warning.html', {'text':text, 'user':user})
    return render(request, 'devices/bushes.html', {'selectFold':selectFold,'user':user, 'lvlbutSP':lvlbutSP, 'lvlbutChart':lvlbutChart})