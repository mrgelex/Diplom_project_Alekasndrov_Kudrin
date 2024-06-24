from django.db import models

class UserPermtab(models.Model):
    perm_id=models.IntegerField(max_length=10, primary_key=True)
    user_id=models.IntegerField(max_length=10)
    folder_id=models.IntegerField(max_length=10)
    rule_id=models.IntegerField(max_length=10)

    class Meta:
        managed=False
        db_table='USER_PERM'

class Foldertab(models.Model):
    folder_id=models.IntegerField(max_length=10, primary_key=True)
    client_id=models.IntegerField(max_length=10)
    root_folder=models.IntegerField(max_length=10)
    name=models.CharField(max_length=30)

    class Meta:
        managed=False
        db_table='FOLDER'

class Devicetab(models.Model):
    device_id=models.IntegerField(max_length=10, primary_key=True)
    folder_id=models.IntegerField(max_length=10)
    name_user=models.CharField(max_length=50)
    IMEI=models.CharField(max_length=50)
    description=models.CharField(max_length=50)
    IP=models.CharField(max_length=50)
    port=models.IntegerField(max_length=10)
    modbus_over_tcp=models.BooleanField(max_length=10)
    add_pr200=models.IntegerField(max_length=10)
    add_tr16=models.IntegerField(max_length=10)
    add_inv=models.IntegerField(max_length=10)
    type_inv=models.CharField(max_length=50)
    GMT=models.CharField(max_length=50)

    class Meta:
        managed=False
        db_table='DEVICE'
