
from django import http
from django.db.models import query
from django.db.models.query import QuerySet
from django.http import response
from django.shortcuts import render
from rest_framework import HTTP_HEADER_ENCODING, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .models import Rule, Query, Config, Strategy, Order
from rest_framework import viewsets



from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from django.views.generic import ListView, DetailView
from .serializers import RuleSerializer, UserSerializer, QuerySerializer, ConfigSerializer, StrategySerializer, OrderSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework import routers
from django_filters.rest_framework import DjangoFilterBackend 

class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class RuleViewSet(ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    filterset_fields= ['name', 'index_name']
    search_fields = ['name', 'index_name', 'total']
    ordering_fields = ['id']
    # ['name', 'index_name', 'rule__queries']
    # def get_queryset(self):
    #     queryset = Rule.objects.all()
        
    #     index_name = self.request.query_params.get('index_name')
    #     if index_name is not None:
    #         queryset = queryset.filter(index_name=index_name) 
        
    #     name = self.request.query_params.get('name')
    #     if name is not None:
    #         queryset = queryset.filter(name=name)
    #     return queryset

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [IsAdminUser]
        else: 
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class QueryViewSet(ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

class ConfigViewSet(ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = ConfigSerializer

class StrategyViewSet(ModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer














###apiview
# class RuleList(ListCreateAPIView):
#     queryset = Rule.objects.all()
#     serializer_class = RuleSerializer
    
# class RuleDetail(RetrieveAPIView):
#     queryset = Rule.objects.all()
#     serializer_class = RuleSerializer

# class UserList(ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     """just admin users can see UerList"""
#     permission_classes = (IsAdminUser,)
# class UserDetail(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAdminUser,)

    
    
    

    





























# Create your views here.
# ############################################################
# class RuleList(generics.ListCreateAPIView):
#     queryset = Rule.objects.all()
#     serializer_class = RuleSerializer
#     pass

# class RuleViewSets(viewsets.ModelViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     serializer_class = RuleSerializer
#     def get_queryset(self):
#         rule = Rule.objects.all()
#         return rule

#     def list(self, request):
#         """
#         List of all rules
#         """
#         queryset = Rule.objects.all()
#         serializer = RuleSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, *args, **kwargs):
#         """
#         retrieve the rule base on the name
#         """
#         params = kwargs
#         print(params['pk'])
#         name = Rule.objects.filter(name=params['pk'])
#         serializer = RuleSerializer(name, many=True)
#         return Response(serializer.data)

############################################

    # def retrieve(self, request, *args, **kwargs):
    #     """
    #     retrieve the rules based on index name
    #     """
    #     params = kwargs
    #     print(params['pk'])
    #     index_name = Rule.objects.filter(index_name=params['pk'])
    #     serializer = RuleSerializer(index_name, many=True)
    #     return Response(serializer.data)
        
    # def create(self, request, *args, **kwargs):

    #     """
    #     create a new rule 
    #     """

    #     rule_data = request.data
    #     new_rule = Rule.objects.create(name=rule_data["name"], index_name=rule_data["index_name"])
    #     new_rule.save()
    #     serializer = RuleSerializer(new_rule)
    #     return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     logedin_user = request.user
    #     if(logedin_user == "admin"):
    #         rule = self.get_object()
    #         rule.delete()
    #         response_message = {"message": "item has been deleted"}
    #     else:
    #         response_message = {"message": "not allowed"}

    #     return Response(response_message)


    # def get(self, request, *args, **kwargs):
    #     try:
    #         id = request.query_params["id"]
    #         if id != None:
    #                 rule = Rule.objects.get(id=id)
    #                 serializer = RuleSerializer(rule)
    #     except:    
    #         rule = self.get_queryset()
    #         serializer = RuleSerializer(rule, many=True)
        
    #     return Response(serializer.data)




    # def post(self, request, *args, **kwargs):    
        
    #     rule_data = request.data
    #     new_rule = Rule.objects.create(name=rule_data["name"], index_name=rule_data["index_name"])
    #     new_rule.save()
    #     serializer = RuleSerializer(new_rule)
    #     return Response(serializer.data)


# @api_view(["GET"])
# def rule_list(request):
#     rule = Rule.objects.all()
#     rule_serialize = RuleSerializer(rule, many=True)
#     return Response(rule_serialize.data)

# @api_view(["GET"])
# def rule_detail(request, pk):
#     try:
#         rule = Rule.objects.get(id=pk)
#     except:
#         return response.HttpResponse(status=404)
#     rule_serialize = RuleSerializer(rule, many=False)
#     return Response(rule_serialize.data)
    
# @api_view(["POST"])
# def rule_save(request):
#     rule = RuleSerializer(data=request.data)
    
#     if rule.is_valid():
#         rule.save()
#         return Response(rule.data, status=201)
#     return Response()

# @api_view(["POST"])
# def rule_update(request, pk):
#     instance = Rule.objects.get(id=pk)
#     rule = RuleSerializer(instance=instance, data=request.data)
#     if rule.is_valid():
#         rule.save()
    
#     return Response()

# @api_view(["DELETE"])
# def rule_delete(request, pk):
#     instance = Rule.objects.get(id=pk)
#     # rule = RuleSerializer(instance=instance, data=request.data)
#     # if rule.is_valid():
#     #     rule.save()
#     instance.delete()
#     return Response("Rule Deleted")