from django import forms

class Setpoints(forms.Form):
    nameDev=forms.CharField(label='Имя:', min_length=2, max_length=8, strip=True)
    quanWire=forms.IntegerField(label='Количество проволоки, м:', min_value=1)
    workDepth=forms.IntegerField(label='Рабочая глубина, м:', min_value=1)
    speedMove=forms.FloatField(label='Скорость движения, м/мин:', min_value=1)
    perClean=forms.IntegerField(label='Периодичность чистки, ч:', min_value=1)
    timeStart=forms.IntegerField(label='Время первого старта, ч:', min_value=1)
    waitTimeDepth=forms.IntegerField(label='Время ожидания на рабочей глубине, мин:', min_value=1)
    waitTimeLub=forms.IntegerField(label='Время ожидания в лубрикаторе, мин:', min_value=1)
    speedManCont=forms.FloatField(label='Скорость в ручном, м/мин:', min_value=1)
    limPunch=forms.IntegerField(label='Лимит на пробивку пробки вниз, м:', min_value=1)
    waitTimePunch=forms.IntegerField(label='Время ожидания до пробивки вниз, сек:', min_value=1)
    depthClean=forms.IntegerField(label='Глубина чистки устья, м:', min_value=1)
    perCleanMouth=forms.IntegerField(label='Периодичность чистки устья, мин:', min_value=1)
    waitTimeESP=forms.IntegerField(label='Время ожидания ЭЦН, мин:', min_value=1)
    permLift=forms.BooleanField(label='Разрешение на подъем по ЭЦН', required=False, widget=forms.CheckboxInput())
    speedLub=forms.FloatField(label='Скорость в лубрикаторе, м/мин:', min_value=1)
    depthBrake=forms.IntegerField(label='Глубина снижения скорости, м:', min_value=1)

    def disable(self):
        self.nameDev.disabled=True
        self.quanWire.disabled=True
        self.workDepth.disabled=True
        self.speedMove.disabled=True
        self.perClean.disabled=True
        self.timeStart.disabled=True
        self.waitTimeDepth.disabled=True
        self.waitTimeLub.disabled=True
        self.speedManCont.disabled=True
        self.limPunch.disabled=True
        self.waitTimePunch.disabled=True
        self.depthClean.disabled=True
        self.perCleanMouth.disabled=True
        self.waitTimeESP.disabled=True
        self.permLift.disabled=True
        self.speedLub.disabled=True
        self.depthBrake.disabled=True
