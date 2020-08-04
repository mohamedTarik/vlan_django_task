from django.shortcuts import render
from .models import Vlans
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import VlanSerializer
from netmiko import ConnectHandler
import requests

# Create your views here.

class Vlans_APIS(viewsets.ViewSet):

	serializer_class = VlanSerializer
	#switch={'ip':'10.10.20.100','user':'developer','pass':'C1sco12345','port':'443'}
	switch={'ip':'209.73.216.56','user':'root','pass':'J3llyfish1','port':'443'}

	conn=ConnectHandler(ip=switch['ip'],username=switch['user'],password=switch['pass'],device_type='juniper')


	def list(self,request):
		"""Sync from DB to switch"""

		queryset = Vlans.objects.all()
		serializer = self.serializer_class(queryset, many=True)
		for v_object in serializer.data:

			config_comands = ['set vlans ' + v_object['vlan_name'] + ' vlan-id ' + v_object['vlan_id']]
			self.conn.send_config_set(config_comands,exit_config_mode=False)
			print(config_comands)

			''' RESTconf/Netconf/SNMP is not Working With this Juniper Switch (SYNC)'''
			'''SNMP is not working because of VPN tunnel i think'''

		return Response(serializer.data)


	def create(self,request):
		vlan_data=request.data
		config_comands = ['set vlans ' + vlan_data['vlan_name'] + ' vlan-id ' + vlan_data['vlan_id']]
		self.conn.send_config_set(config_comands, exit_config_mode=False)
		try:
			data=Vlans.objects.create(vlan_id=vlan_data['vlan_id'] , vlan_name=vlan_data['vlan_name'], description=vlan_data['description'])
			data.save()
			si = self.serializer_class(data)
		except:
			return Response({'Error':'Duplicate entry vlan '+str(vlan_data['vlan_id'])+' for key PRIMARY'})

		return Response(si.data)


	def retrieve(self, request, pk=None):
		try:
			obj=Vlans.objects.get(vlan_id=pk)
			serializer = self.serializer_class(obj)
		except:
			return Response({"Error": "vlan "+pk+" doesn't exsists"})


		return Response(serializer.data)


	def update(self, request, pk=None):
		#config_comands = ['set vlans ' + request.data['vlan_name'] + ' vlan-id ' + pk]
		obj = Vlans.objects.get(vlan_id=pk)
		si = self.serializer_class(obj)

		config_comands = ['rename' +' vlans '+si.data['vlan_name']+ ' to '+request.data['vlan_name']]

		self.conn.send_config_set(config_comands, exit_config_mode=False)
		Vlans.objects.filter(vlan_id=pk).update(vlan_name=request.data['vlan_name'],description=request.data['description'])

		obj = Vlans.objects.get(vlan_id=pk)
		si=self.serializer_class(obj)

		return Response(si.data)


	def partial_update(self, request, pk=None):
		return Response({"msg":"update"})


	def destroy(self, request, pk=None):

		try:
			obj = Vlans.objects.get(vlan_id=pk)
		except:
			return Response({'Error': 'vlan '+pk+' already deleted'})

		serializer = self.serializer_class(obj)
		config_comands = ['delete vlans ' + serializer.data['vlan_name']]
		self.conn.send_config_set(config_comands,exit_config_mode=False)

		try:
			obj = Vlans.objects.get(vlan_id=pk)
			obj.delete()

		except:
			return Response({'Error': 'vlan '+pk+' already deleted'})

		return Response({'msg':'vlan '+pk+ ' deleted'})