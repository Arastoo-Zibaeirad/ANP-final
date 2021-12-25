# from .models import Rule, Query, Config, Strategy

# def change_my_name_plz (sender, instance, created, **kwargs):
#     if created:
#         Rule.objects.create(name='something', index_name='sth')



# from django.db.models.signals import post_save
# from django.contrib.auth.models import Strategy
# from django.dispatch import receiver
# from .models import Rule
 
 
# @receiver(post_save, sender=Strategy)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Rule.objects.create(strategy=instance)
  
# @receiver(post_save, sender=Strategy)
# def save_profile(sender, instance, **kwargs):
#         instance.rule.save()


from django.db.models.query_utils import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Rule, Strategy, Query, Order
import yaml
from django.db.models.signals import m2m_changed
import random
import json
import requests
##we say who is send signals to this function(create_rule)... @receiver myani daryaft konandeye in signal function create_rule ast
@receiver(post_save, sender=Rule)
def create_yaml(sender, instance, created, **kwargs):
    """
    after creating an object in rule, we want to create a yaml file 
    """
    if created:
        dict_file = """[{'ANPdata' : ['creation_date = %s', 'maturity = production', 'updated_date = %s']},
                        {'ANPrule' : [{'author': ["Elastic"]}, {'language': "eql"}, {'rule_id': "55"}, {'threat': 'ghgf'}]},
                        {'name': \" %s \"},
                        {'index': "%s"},
                        {'type': "any"},
                        {'query': [{'query': %s}]}]"""%(instance.create_time, instance.modified_time, instance.name, instance.index_name, instance.total_method()[1])
                
        dict_file = yaml.safe_load(dict_file)          
        with open(f'{instance.name}.yaml', 'w') as file:
            yaml.dump(dict_file, file)



@receiver(post_save, sender=Strategy)
def create_yaml_strategy(sender, instance, created, **kwargs):
    """
    after creating an object in strategy, we want to create a yaml file 
    """
    if created:
        print("created",created)
        dict_file = """[{'ANPdata' : ['creation_date = %s', 'maturity = production', 'updated_date = %s']},
                        {'ANPrule' : [{'author': ["Elastic"]}, {'language': "eql"}, {'rule_id': "55"}, {'threat': 'ghgf'}]},
                        {'name': \" %s \"},
                        {'index': "%s"},
                        {'type': "any"},
                        {'query': [{'query': %s}]}]"""%(instance.create_time, instance.modified_time, instance.strategy_name, instance.strategy_alias, instance.strategy_total)
                
        dict_file = yaml.safe_load(dict_file)          
        with open(f'{instance.strategy_name}.yaml', 'w') as file:
            yaml.dump(dict_file, file)
    else:
        Strategy.objects.update()
        # Strategy.objects.filter(pk=b.id).update()


# @receiver(post_save, sender=Query)
# def fill_total(sender, instance, created, **kwargs):
#     """
#     fill the field of total after create a rule
#     """
    # instance.rule.total = str(instance.id)
    # print(instance.id)
    # num = 0
  
    # rule = instance
    # queries = rule.queries.all()
    # rule.save()
    # queries.save()
    # print(queries)
    # f = instance.rule.queries.all()
    
    

    
    # num = []
    # if created:
    #     num += 1
        # print(len(instance.rule.queries.all()))
        # f = instance.rule.queries.all()
    
    # print(num)

    # x = ""
    # for i in range (len(f)):
    # c = (f"[{f[i].event_category} where {f[i].condition}]\\n  ")
    # x += c
    # z = "sequence\\n " + x     
    # print(z)
        
        
        
        
        
    #     x=""
    #     queries = instance.queries.all()
    #     if instance.sequence == 'has no conf':
    #         return "has no conf"
    #     else:
    
        
    #         if instance.sequence == False:
    #             z = (f"{queries.event_category} where {queries.condition}")
    #         elif instance.sequence == True:
    #             for i in range (len(queries)):
    #                 c = (f"[{queries[i].event_category} where {queries[i].condition}]\\n  ")
    #                 x = x + c
    #             z = "sequence\\n " + x 
    #         instance.total = instance.queries.all
    #         print(instance.total)
    # else:
    #     print("no")


# @receiver(m2m_changed, sender=Strategy.rules.through)
# def create_rule(sender, instance, **kwargs):
#     """
#     create a rule when an object from Strategy is created.
#     """   
#     rules = instance.rules.all()
#     if len(rules) != 0:
#         y = ""
#         indices = []
#         for rule in rules:
#             index = rule.index_name
#             indices.append(index)
#             queries = rule.queries.all()   
#             x = ""
#             for i in range (len(queries)):
#                 c = (f"[{queries[i].event_category} where {queries[i].condition}]\\n ")
#                 x +=  c
#             y += x
#         z = "sequence\\n " + y
#         url = 'http://192.168.250.123:9200/_aliases?pretty'
#         headers = {
#         'Content-Type': 'application/json'
#         }
#         alias_name = f"Strategy_alias{random.random()}"
#         data = '{"actions" : [ { "add" : { "indices" : %s, "alias" : "%s" } } ]}'%(json.dumps(indices), alias_name)
#         try:
#             res1 = requests.post(url, headers=headers, data=data)
#             res = res1.json()
#         except:
#             print("ERROR")
#         a = Rule.objects.create(name=instance.strategy_name, index_name=alias_name, total=z, flag='strategy')

#         a.total=z
#         return z    
#     else:
#         pass
    
# 
        
 