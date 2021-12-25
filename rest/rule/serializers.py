from django.db.models import fields
from rest_framework import serializers
from .models import Rule, Query, Config, Strategy, Order
# # , User
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"

class RuleSerializer(serializers.ModelSerializer):
    serialization_title = "Rule"
    """many should be false because each query related to one rule
       name should be 'query' as the same as related_name in OntoOneField
    """
    query = serializers.StringRelatedField(many=False)
    class Meta:
        model = Rule
        # depth = 1
        # fields = ['name', 'index_name', 'total']
        fields = "__all__"

    # def validate_name(self, value):
    #     filter_list = ["java"]
    #     for i in filter_list:
    #         if i in value:
    #             raise serializers.ValidationError("Do not use this word")

class QuerySerializer(serializers.ModelSerializer):
    rule = RuleSerializer()
    class Meta:
        model = Query
        fields = "__all__"

class ConfigSerializer(serializers.ModelSerializer):
    rule = RuleSerializer()
    class Meta:
        model = Config
        fields = "__all__"

class StrategySerializer(serializers.ModelSerializer):
    rules = RuleSerializer(many=True)
    class Meta:
        model = Strategy
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    strategy = StrategySerializer()
    rule = RuleSerializer()
    class Meta:
        model = Order
        fields = "__all__"

