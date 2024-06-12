from django.db import models

class LogTimetab(models.Model):
    log_id=models.IntegerField()
    device_id=models.IntegerField()
    timestamp_loc=models.DateTimeField()
    timestamp_dev=models.DateTimeField()
    GMT=models.CharField()
    status=models.IntegerField()
    depth=models.IntegerField()
    power=models.IntegerField()
    status_string=models.IntegerField()
    data=models.CharField()

    class Meta:
        managed=False
        db_table='LOG_TIME'

class LogEventtab(LogTimetab):

    class Meta:
        managed=False
        db_table='LOG_EVENT'
