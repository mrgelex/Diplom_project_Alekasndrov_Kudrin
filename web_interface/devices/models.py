from django.db import models

class UserPermtab(models.Model):
    perm_id=models.IntegerField()
    user_id=models.IntegerField()
    folder_id=models.IntegerField()
    rule_id=models.IntegerField()

    class Meta:
        managed=False
        db_table='USER_PERM'

class Foldertab(models.Model):
    folder_id=models.IntegerField()
    client_id=models.IntegerField()
    root_folder=models.IntegerField()
    name=models.CharField()

    class Meta:
        managed=False
        db_table='USER_PERM'

class Devicetab(models.Model):
    device_id=models.IntegerField()
    folder_id=models.IntegerField()
    name_user=models.CharField()
    IMEI=models.CharField()
    description=models.CharField()
    IP=models.CharField()
    port=models.IntegerField()
    modbus_over_tcp=models.BooleanField()
    add_pr200=models.IntegerField()
    add_tr16=models.IntegerField()
    add_inv=models.IntegerField()
    type_inv=models.CharField()
    GMT=models.CharField()

    class Meta:
        managed=False
        db_table='DEVICE'
