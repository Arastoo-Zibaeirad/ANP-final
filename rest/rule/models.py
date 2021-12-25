from django.db import models
from django.db.models.fields import BooleanField
import requests
import random
import json
import yaml
from django.core.files.base import ContentFile, File
import time
from elasticsearch import Elasticsearch
# from django.db.models.signals import post_save

# class StrategyManager(models.Manager):
#     def get_value(self, queryset, **kwargs):
#         a = super().create(**kwargs)
#         y = ""
#         for i in queryset:
#             queries = i.queries.all()
#             print("index_name: ", i.index_name)
            
#             # for query in queries:
#             #     print("query: ",query)
#             x = ""
#             for i in range (len(queries)):
#                 c = (f"[{queries[i].event_category} where {queries[i].condition}]\\n ")
#                 x +=  c
#             y += x
#         z = "sequence\\n " + y
#         print("ZZZZZZZZ: ", z) 
#         a.total = z 
#         a.save()

# class QueryManager(models.Manager):
#     def create(self,**kwargs):
#         a = super().create(**kwargs)
#         print("2222222222", a)
#         queries = a.rule.queries.all()
#         sequence = a.rule.sequence
#         # print('-------', sequence)
#         if sequence == False:
#             # print('+++++++', sequence)
#             z = (f"{queries.event_category} where {queries.condition}")
        
#         elif sequence == True:
#             x = ""
#             for i in range (len(queries)):
#                 # print("$$$$$len", len(queries))
#                 c = (f"[{queries[i].event_category} where {queries[i].condition}]\\n  ")
#                 x +=  c
#                 z = "sequence\\n " + x 
        
        
#         a.total= "ss"
        
#         a.save()
#         # return z   
    
    
# class CustomRuleManager(models.Manager):    
#     def create(self, **kwargs):
#         q = super().create(**kwargs)
#         dict_file = """[{'ANPdata' : ['creation_date = %s', 'maturity = production', 'updated_date = %s']},
#                         {'ANPrule' : [{'author': ["Elastic"]}, {'language': "eql"}, {'rule_id': "55"}, {'threat': 'ghgf'}]},
#                         {'name': \" %s \"},
#                         {'index': "%s"},
#                         {'type': "any"}]"""%(q.create_time, q.modified_time, q.name, q.index_name)
                                       
#         dict_file = eval(dict_file)
#         with open(f'testyaml{random.random()}.yaml', 'w') as file:
#             documents = yaml.dump(dict_file, file)
        
#         return documents

# class CustomStrategyManager(models.Manager):
#     def create(self, *args, **kwargs):
#         s = super().create(*args, **kwargs)
#         rule = Rule.objects.create(name=s.strategy_name, index_name="sss")
#         rs = s.rules.all()
#         for r in rs:
            
#             print("@@@@@@@@@@@@@@",r)

#         print("#################done")

# class CustomStrategyManager(models.Manager):
#     def create(self, **kwargs):
#         strategy_rule_create_queryset = super().create(**kwargs)
#         print("##", strategy_rule_create_queryset)
        
#         rule = Rule.objects.create(name="ee", index_name="ee")
#         rule.save()
#         return rule
        
class Rule(models.Model):
    name = models.CharField(max_length=200)
    index_name = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    # rule_file = models.FileField(blank=True, upload_to='')
    CREATE_RULE = 'create_rule'
    STRATEGY = 'strategy'
    flag_fields = (
        (CREATE_RULE, "create_rule"),
        (STRATEGY, "strategy")
    )
    flag = models.CharField(max_length=250, blank=True, null=True, choices=flag_fields, default=CREATE_RULE)
    total = models.TextField(blank=True, null=True)
    # DisplayFields = ['id', 'name', 'index_name', 'sequence' ,'flag','create_time', 'modified_time','total', 'total_property']

    # objects = CustomRuleManager()
    # default_manager = CustomRuleManager()

    # def save(self, *args, **kwargs):
        # x=""
        # queries = self.queries.all()
        # if self.sequence == 'has no conf':
        #     return "has no conf"
        # else:
        #     if self.sequence == False:
        #         z = (f"{queries.event_category} where {queries.condition}")
        #     elif self.sequence == True:
        #         for i in range (len(queries)):
        #             print(i)
        #             c = (f"[{queries[i].event_category} where {queries[i].condition}]\\n  ")
        #             x +=  c
        #         z = "sequence\\n " + x
        #     self.total = queries
            
          # super().save(*args, **kwargs)   
            
            
        # if self.flag == 'create_rule':
        #     if self.sequence == False:
        #         z = (f"{queries.event_category} where {queries.condition}")
        #         self.total = z
        #     elif self.sequence == True:
        #         for i in range (len(queries)):
        #             c = (f"[{queries[i].event_category} where {queries[i].condition}]\\n  ")
        #             x +=  c
        #         z = "sequence\\n " + x
        #         self.total = z
        
    @property
    def index_alias(self):
        indices_name = self.index_name.split(", ")
        index = []
        for indx in indices_name:
            index.append(indx)

        if len(index) >= 2:
            print(len(index))
            print("you should define an alias")
            url = 'http://192.168.250.123:9200/_aliases?pretty'
            headers = {
            'Content-Type': 'application/json'
            }
            alias_name = f"alias{random.random()}"
            data = '{"actions" : [ { "add" : { "indices" : %s, "alias" : "%s" } } ]}'%(json.dumps(index), alias_name)
            # data = json.dumps(data)
            print(data)
            try:
                res1 = requests.post(url, headers=headers, data=data)
                res = res1.json()
                print("RESPONSE: ",res)
                rule = Rule.objects.get(id=self.id)
                rule.index_name = alias_name
                # self.index_name= alias_name
                # indices_name = alias_name
                rule.save()            
            except:
                print("ERROR")
        return indices_name

    def total_method(self):
        
        queries = self.queries.all()
        if self.sequence == 'has no conf':
            return "has no conf"
        else:
            if self.sequence == False:
                z = (f"{queries.event_category} where {queries.condition}")
            elif self.sequence == True:
                x=f""
                z = ""
                for i in range (len(queries)):
                    # b = "sequence\\n "
                    c = f"[{queries[i].event_category} where {queries[i].condition}]\\n "
                    x += c
                print("XXX",x)
                z = "sequence\\n" + str(x)
                print("ZZZZZZZZZZZZZZZZZZZZ: ",z)
        self.total = z
        self.save()
        return x, z
            
    @property
    def sequence(self):
        try:
            if self.config.sequence == False:
                return False
            elif self.flag == 'strategy':
                return True
            else:
                return True
        except:
            return 'has no conf'    

    class Meta:
        verbose_name = 'Rule'
        verbose_name_plural = 'Rules'

    def __str__(self):
        return f"{self.name}"


class Query(models.Model):
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='queries')
    
    ANY = 'any'
    PROCESS = 'process'
    NETWORK = 'network'
    FILE = 'file'
    REGISTRY = 'registry'
    AUTHENTICATION = 'authentication'
    CONFIGURATION = 'configuration'
    DATABASE = 'database'
    DRIVER = 'driver'
    HOST = 'host'
    IAM = 'iam'
    INTRUSION_DETECTION = 'intrusion_detection'
    MALWARE = 'malware'
    PACKAGE = 'package'
    SESSION = 'session'
    THREAT = 'threat'
    WEB = 'web'

    event_category_fields = (
        (ANY, "any"),
        (PROCESS, "process"),
        (NETWORK, "network"),
        (FILE, "file"),
        (REGISTRY, "registry"),
        (AUTHENTICATION, "authentication"),
        (CONFIGURATION, "configuration"),
        (DATABASE, "database"),
        (DRIVER, "driver"),
        (HOST, "host"),
        (IAM, "iam"),
        (INTRUSION_DETECTION, "intrusion_detection"),
        (MALWARE, "malware"),
        (PACKAGE, "package"),
        (SESSION, "session"),
        (THREAT, "threat"),
        (WEB, "web"),
    )
   
    event_category = models.CharField(max_length=32, default=ANY, choices=event_category_fields)
    condition = models.CharField(max_length=200)
    by = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    # default_manager = QueryManager()
    # objects = QueryManager()

    class Meta:
        verbose_name = 'Query'
        verbose_name_plural = 'Queries'

    def __str__(self):
        return f"{self.rule}"  
       
class Config(models.Model):
    rule = models.OneToOneField(Rule, on_delete=models.CASCADE, related_name='config')
    sequence = models.BooleanField(default=False)
    until = models.BooleanField(default=False)
    maxspan = models.BooleanField(default=False)
    size = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.rule}"
    
class Strategy(models.Model):
    rules = models.ManyToManyField(Rule, related_name='strategies', through='Order')
    strategy_name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    strategy_alias = models.TextField(blank=True, null=True)
    strategy_total = models.TextField(blank=True, null=True)
    # objects = CustomStrategyManager()
    # default_manager = models.Manager()
    
    class Meta:
        verbose_name = 'Strategy'
        verbose_name_plural = 'Strategies'
        # unique_together = [['rules']]
    
    def __str__(self):
        return f"{self.strategy_name}"
    "**************************************************************"
    # def total_method_strategy(self):
    #     rules = self.rules.all()
    #     if len(rules) != 0:
    #         y = ""
    #         for rule in rules:
    #             queries = rule.queries.all()   
    #             x = ""
    #             for i in range (len(queries)):
    #                 c = (f"[{queries[i].event_category} where {queries[i].condition}]\\n ")
    #                 x +=  c
    #             y += x
    #         z = "sequence\\n " + y
        # return (z,y)
        
    def final_query(self):
        strategies = self.stra.all()
        rules = self.rules.all()
        
        # for j in range(len(strategies)):
        x = ""
        for obj in strategies:
            '##########################This is for rule##########################'
            if obj.add_from_another_strategy == False:
                r = obj.rule
                q = r.total_method()[0]
                x += q
                '##########################This is for strategy##########################'
            if obj.add_from_another_strategy == True:
                for get_each_strategy in obj.add_strategy.all():
                    for rule_of_each_strategy in get_each_strategy.rules.all():
                        before_final_query = rule_of_each_strategy.total_method()[0]
                        x += before_final_query

        final_query = f"sequence\\n {x}"
        self.strategy_total = final_query
        self.save()
        return final_query
    
    def strategy_index(self):
        strategies = self.stra.all()
        rules = self.rules.all()
        strategy_indx_name_list = []
        for obj in strategies:
            if obj.add_from_another_strategy == False:
                r = obj.rule
                i = r.index_name
                strategy_indx_name_list.append(i)
            if obj.add_from_another_strategy == True:
                for get_each_strategy in obj.add_strategy.all():
                    for rule_of_each_strategy in get_each_strategy.rules.all():
                        i_name = rule_of_each_strategy.index_name
                        strategy_indx_name_list.append(i_name)
        # print("strategy_indx_name_list: ", strategy_indx_name_list)
        """the indices list has unique items"""
        indices = []
        for x in strategy_indx_name_list:
            if x not in indices:
                indices.append(x)
        indices.sort()
        collect_index_name = ""
        for i in indices:
            collect_index_name += i
        es = Elasticsearch(['192.168.250.123'],)
        if len(indices) >= 1:
            url = 'http://192.168.250.123:9200/_aliases?pretty'
            headers = {
            'Content-Type': 'application/json'
            }
            alias_name = f"Strategy_alias({collect_index_name})"
            data = '{"actions" : [ { "add" : { "indices" : %s, "alias" : "%s" } } ]}'%(json.dumps(indices), alias_name)
            try:
                alias = es.indices.get_alias(f"{alias_name}")
                alias = "Exist"
            except:
                alias = "Not Exist"
            if alias == "Exist":
                indices = alias_name
            else:
                try:
                    """
                    This is for handling errors. we send a request to Elasticsearch to get the list of all indices and if one of the indices does not in 
                    in the list, then alias should not be created.
                    """
                    get_index_from_elastic = []
                    k = 0
                    for index in es.indices.get('*'):
                        get_index_from_elastic.append(index)
                    for ii in indices:
                        if ii not in get_index_from_elastic: 
                            k += 1
                    print(k)
                    if k == 0:
                        res1 = requests.post(url, headers=headers, data=data)
                        res = res1.json()
                        indices = alias_name
                        print("Response: ", res)

                    else:                        
                        self.final_query = "error"
                        raise "error"
                        
                except:
                    print("ERROR stratey alias")
                    return None
      
            self.strategy_alias = indices
            self.save()
            return indices
        
    # def save(self, *args, **kwargs):
    #     if self.strategy_index() == "error":
    #         Strategy.objects.all() == None
            
    #     return super(Strategy, self).save(*args, **kwargs)   
    
    # def get():
    #     """do not create an object if an index is not exist
    #     """

class Order(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name='stra')
    order = models.AutoField(primary_key=True)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, blank=True, null=True)
    add_from_another_strategy = models.BooleanField(default=False)
    add_strategy = models.ManyToManyField(Strategy, blank=True)
