from django.db import models

class Ihrd(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(db_column='Full_Name', max_length=50) 
    nickname = models.CharField(max_length=50, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'IHRD' # Points directly to your MySQL table
       
