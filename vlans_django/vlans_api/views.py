from django.shortcuts import render
from .models import Vlans
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import VlanSerializer
from netmiko import ConnectHandler
# Create your views here.



class Vlans_APIS(viewsets.ViewSet):

	serializer_class = VlanSerializer
	#switch={'ip':'10.10.10.1','user':'uanme','pass':'password'}
	#conn=ConnectHandler(ip=switch['ip'],username=switch['user'],password=switch['pass'],device_type='cisco_ios')


	def list(self,request):
		queryset = Vlans.objects.all()

		serializer = self.serializer_class(queryset, many=True)
		for v_object in serializer.data:
			print(v_object['vlan_id'])
			#config_comands = ['vlan ' + v_object['vlan_id'],'name '+v_object['vlan_name']]
			#cli=self.conn.send_config_set(config_comands)
		return Response(serializer.data)

	def create(self,request):
		vlan_data=request.data
		data=Vlans.objects.create(vlan_id=vlan_data['vlan_id'] , vlan_name=vlan_data['vlan_name'], description=vlan_data['description'])
		data.save()
		si=self.serializer_class(data)
		return Response(si.data)




