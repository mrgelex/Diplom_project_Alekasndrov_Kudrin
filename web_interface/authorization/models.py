from django.db import models

class Usertab(models.Model):
    user_id=models.IntegerField()
    client_id=models.IntegerField()
    name=models.CharField()
    login=models.CharField()
    password=models.CharField()
    tg_id=models.CharField()

    class Meta:
        managed=False
        db_table='USER'

class Clienttab(models.Model):
    client_id=models.IntegerField()
    name=models.CharField()
    rule_id=models.IntegerField()

    class Meta:
        managed=False
        db_table='CLIENT'

class Rulestab(models.Model):
    rule_id=models.IntegerField()
    web=models.BooleanField()
    setting=models.BooleanField()
    control=models.BooleanField()
    report=models.BooleanField()
    bot=models.BooleanField()

    class Meta:
        managed=False
        db_table='RULES'