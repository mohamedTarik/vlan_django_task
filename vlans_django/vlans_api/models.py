from django.db import models

# Create your models here.

class Vlans(models.Model):
	vlan_id = models.CharField(primary_key=True,max_length=100)
	vlan_name = models.CharField(max_length=10)
	description = models.CharField(max_length=10)
	date = models.DateTimeField(auto_now_add=True)


