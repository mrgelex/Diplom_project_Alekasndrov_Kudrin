from django import forms

class Setpoints(forms.Form):
    Username2=forms.CharField(label='Имя:', min_length=2, max_length=8, strip=True)
    NWires=forms.IntegerField(label='Количество проволоки, м:', min_value=1)
    WorkDepth=forms.IntegerField(label='Рабочая глубина, м:', min_value=1)
    WorkSpeed=forms.FloatField(label='Скорость движения, м/мин:', min_value=1)
    TmClearDelta=forms.IntegerField(label='Периодичность чистки, ч:', min_value=1)
    TmClearAbs=forms.IntegerField(label='Время первого старта, ч:', min_value=1)
    TmWaitWorkDepth=forms.IntegerField(label='Время ожидания на рабочей глубине, мин:', min_value=1)
    TmWaitLubr=forms.IntegerField(label='Время ожидания в лубрикаторе, мин:', min_value=1)
    ManualSpeed=forms.FloatField(label='Скорость в ручном, м/мин:', min_value=1)
    LimPlugDown=forms.IntegerField(label='Лимит на пробивку пробки вниз, м:', min_value=1)
    TmWaitDatPro=forms.IntegerField(label='Время ожидания до пробивки вниз, сек:', min_value=1)
    DepthClearUst=forms.IntegerField(label='Глубина чистки устья, м:', min_value=1)
    TmClearUst=forms.IntegerField(label='Периодичность чистки устья, мин:', min_value=1)
    TmWaitECN=forms.IntegerField(label='Время ожидания ЭЦН, мин:', min_value=1)
    EnUpECN=forms.BooleanField(label='Разрешение на подъем по ЭЦН', required=False, widget=forms.CheckboxInput())
    CollarSpeed=forms.FloatField(label='Скорость в лубрикаторе, м/мин:', min_value=1)
    CollarDepth=forms.IntegerField(label='Глубина снижения скорости, м:', min_value=1)

    def disable(self):
        self.Username2.disabled=True
        self.NWires.disabled=True
        self.WorkDepth.disabled=True
        self.WorkSpeed.disabled=True
        self.TmClearDelta.disabled=True
        self.TmClearAbs.disabled=True
        self.TmWaitWorkDepth.disabled=True
        self.TmWaitLubr.disabled=True
        self.ManualSpeed.disabled=True
        self.LimPlugDown.disabled=True
        self.TmWaitDatPro.disabled=True
        self.DepthClearUst.disabled=True
        self.TmClearUst.disabled=True
        self.TmWaitECN.disabled=True
        self.EnUpECN.disabled=True
        self.CollarSpeed.disabled=True
        self.CollarDepth.disabled=True
