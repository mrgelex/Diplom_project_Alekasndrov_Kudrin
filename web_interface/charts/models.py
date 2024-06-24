from django.db import models

class LogTimetab(models.Model):
    log_id=models.IntegerField(max_length=10, primary_key=True)
    device_id=models.IntegerField(max_length=10)
    timestamp_loc=models.DateTimeField()
    timestamp_dev=models.DateTimeField()
    GMT=models.CharField(max_length=50)
    status=models.IntegerField(max_length=10)
    depth=models.IntegerField(max_length=10)
    power=models.IntegerField(max_length=10)
    status_string=models.IntegerField(max_length=10)
    data=models.CharField(max_length=200)

    class Meta:
        managed=False
        db_table='LOG_TIME'

class LogEventtab(LogTimetab):

    class Meta:
        managed=False
        db_table='LOG_EVENT'
