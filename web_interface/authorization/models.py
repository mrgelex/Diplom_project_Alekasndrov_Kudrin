from django.db import models

class Usertab(models.Model):
    user_id=models.IntegerField(max_length=10, primary_key=True)
    client_id=models.IntegerField(max_length=10)
    name=models.CharField(max_length=50)
    login=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    tg_id=models.CharField(max_length=50)

    class Meta:
        managed=False
        db_table='USER'

class Clienttab(models.Model):
    client_id=models.IntegerField(max_length=10, primary_key=True)
    name=models.CharField(max_length=30)
    rule_id=models.IntegerField(max_length=10)

    class Meta:
        managed=False
        db_table='CLIENT'

class Rulestab(models.Model):
    rule_id=models.IntegerField(max_length=10, primary_key=True)
    name=models.CharField(max_length=30)
    web=models.BooleanField(max_length=10)
    setting=models.BooleanField(max_length=10)
    control=models.BooleanField(max_length=10)
    report=models.BooleanField(max_length=10)
    bot=models.BooleanField(max_length=10)

    class Meta:
        managed=False
        db_table='RULES'