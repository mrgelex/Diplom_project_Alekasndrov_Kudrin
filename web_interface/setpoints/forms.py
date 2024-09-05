from django import forms

class Setpoints(forms.Form):
    Username1=forms.CharField(required=False, label='Имя:', min_length=1, max_length=10, strip=True, disabled=True)
    Username2=forms.CharField(required=False, min_length=1, max_length=10, strip=True, disabled=True)
    NWires=forms.IntegerField(label='Количество проволоки, м:', min_value=0)
    WorkDepth=forms.IntegerField(label='Рабочая глубина, м:', min_value=0)
    WorkSpeed=forms.FloatField(label='Скорость движения, м/мин:', min_value=0)
    TmClearDelta=forms.IntegerField(label='Периодичность чистки, ч:', min_value=0)
    TmClearAbs=forms.IntegerField(label='Время первого старта, ч:', min_value=0)
    TmWaitWorkDepth=forms.IntegerField(label='Время ожидания на рабочей глубине, мин:', min_value=0)
    TmWaitLubr=forms.IntegerField(label='Время ожидания в лубрикаторе, мин:', min_value=0)
    ManualSpeed=forms.FloatField(label='Скорость в ручном, м/мин:', min_value=0)
    LimPlugDown=forms.IntegerField(label='Лимит на пробивку пробки вниз, м:', min_value=0)
    TmWaitDatPro=forms.IntegerField(label='Время ожидания до пробивки вниз, сек:', min_value=0)
    DepthClearUst=forms.IntegerField(label='Глубина чистки устья, м:', min_value=0)
    TmClearUst=forms.IntegerField(label='Периодичность чистки устья, мин:', min_value=0)
    TmWaitECN=forms.IntegerField(label='Время ожидания ЭЦН, мин:', min_value=0)
    EnUpECN=forms.BooleanField(label='Разрешение на подъем по ЭЦН', required=False, widget=forms.CheckboxInput())
    CollarSpeed=forms.FloatField(label='Скорость в лубрикаторе, м/мин:', min_value=0)
    CollarDepth=forms.IntegerField(label='Глубина снижения скорости, м:', min_value=0)

    def disable(self):
            for j in ['NWires', 'WorkDepth', 'WorkSpeed', 'TmClearDelta',
                      'TmClearAbs', 'TmWaitWorkDepth', 'TmWaitLubr', 'ManualSpeed',
                      'LimPlugDown', 'TmWaitDatPro', 'DepthClearUst', 'TmClearUst',
                      'TmWaitECN', 'EnUpECN', 'CollarSpeed', 'CollarDepth']:
                self.fields[j].disabled=True
