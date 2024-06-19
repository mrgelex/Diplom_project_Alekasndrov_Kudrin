from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

class Bush:
    def __init__(self, folder_id, rule_id):
        self.id=folder_id
        self.tool=rule_id

def allFold(request):
    if not 'user' in request.session:
        return redirect('login')
    if 'oneFold' in request.session:
        return redirect('showbush')
    user=request.session['user']
    userPerm=UserPermtab.objects.filter(user.get('userid'))
    if userPerm.count() < 2:
        for i in userPerm:
            item1=i.folder_id
            item2=i.rule_id
        request.session['oneFold']={'onlyOne':item1, 'oneRule':item2}
        return redirect('showbush')
    request.session['manyFold']=list(userPerm.values_list('folder_id', 'rule_id'))
    folIdList=[]
    for i in userPerm:
        folIdList.append(i.folder_id)
    all=Foldertab.objects.all()
    rootFolList=[]
    for i in folIdList:
        rootFolList=rootFolList+list(all.filter(folder_id=i).values_list('root_folder', flat=True))
    rootFolList=list(set(rootFolList))
    if rootFolList < 2:
        return redirect('showbush')
    request.session['rootFold']=rootFolList
    

def showBush(request):
    if not 'user' in request.session:
        return redirect('login')
    if 'oneFold' in request.session:
        oneFold=request.session['oneFold']
        deviceData=Devicetab.objects.filter(folder_id=oneFold.get('onlyOne'))
        

    