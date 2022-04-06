from django.db import models
from django.db.models.fields import BooleanField
import requests
import random
import json
import yaml
from elasticsearch import Elasticsearch
from django.core.exceptions import ValidationError
from .config import es_url
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
    """
    This is the main model that connected to Query, Config, and Strategy. 
    total file would be completed after creating a rule. In fact, total is for final query.
    """
    name = models.CharField(max_length=200)
    index_name = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    CREATE_RULE = 'create_rule'
    STRATEGY = 'strategy'
    flag_fields = (
        (CREATE_RULE, "create_rule"),
        (STRATEGY, "strategy")
    )
    flag = models.CharField(max_length=250, blank=True, null=True, choices=flag_fields, default=CREATE_RULE)
    total = models.TextField(blank=True, null=True)
    # objects = CustomRuleManager()
    # default_manager = CustomRuleManager()

    @property
    def index_alias(self):
        """
        In this part, if we write more than one index name in the field of index, this property function 
        would create an alias for this rule and put all those indices in the alias.
        """
        indices_name = self.index_name.split(", ")
        index = []
        for indx in indices_name:
            index.append(indx)

        if len(index) >= 2:
            # print(len(index))
            print("you should define an alias")
            url = f'http://{es_url}/_aliases?pretty'
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
    
    
    def sequence(self):
        """
        if the sequence that defined in the Config model is true, it would use sequenced query.
        """
        config = self.config.all()
        try:
            if config.sequence == False:
                return False
            # elif self.flag == 'strategy':
            #     return True
            else:
                return True
        except:
            return 'has no conf'
    
    # @property
    def total_method(self):
        """
        This would combined queries to each other. If we use sequence in Config model we have a different total query.
        finally, this will fill the total field that we discussed before.
        """
        queries = self.queries.all()
        # if self.sequence == 'has no conf':
        #     return "has no conf"
        # else:
        if self.sequence == False:
            z = (f"{queries.event_category} where {queries.condition}")
        else:
            x=f""
            z = ""
            for i in range (len(queries)):
                c = f"[{queries[i].event_category} where {queries[i].condition}]\\n "
                x += c
            
            z = "sequence\\n " + str(x)
        self.total = z
        self.save(update_fields=["total"])

        return x, z
    
    def clean(self):
        """
        if the index that we write in the rule is not defined in the elasticsearch, it would not allow to 
        create the rule. You must first create the index then add the rule.
        """
        es = Elasticsearch([f'{es_url}'],)
        
        get_index_from_elastic = []
        for index in es.indices.get('*'):
            get_index_from_elastic.append(index)
        
        if self.index_name not in get_index_from_elastic:
            raise ValidationError("index not found")
        super(Rule, self).clean()
    
    # def handling_index(self):
        
    #     es = Elasticsearch(['192.168.250.123'],)
    #     get_index_from_elastic = []
    #     # k = 0
    #     for index in es.indices.get('*'):
    #         get_index_from_elastic.append(index)
        
    #     # for ii in get_index_from_elastic:
    #     if self.index_name not in get_index_from_elastic: 
    #         # k += 1
    #         self.index_name = ""
    #     else:
    #         self.index_name = self.index_name
        
    #     return self.index_name
        
    class Meta:
        verbose_name = 'Rule'
        verbose_name_plural = 'Rules'

    def __str__(self):
        return f"{self.name}"

class Query(models.Model):
    """
    we can have one query or more than that, but if you want to add more than one query
    you should activate the sequence boolean key. Only event_category and condition work.
    """
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

    # def save(self, *args, **kwargs):
    #     super(Query, self).save(*args, **kwargs)
    #     self.rule.total = self.rule.total_method

    class Meta:
        verbose_name = 'Query'
        verbose_name_plural = 'Queries'

    def __str__(self):
        return f"{self.rule}"  
       
class Config(models.Model):
    """
    Only sequence works.
    """
    rule = models.OneToOneField(Rule, on_delete=models.CASCADE, related_name='config')
    sequence = models.BooleanField(default=False)
    until = models.BooleanField(default=False)
    maxspan = models.BooleanField(default=False)
    size = models.BooleanField(default=False)
    
    # def sequence(self):
        
    #     # config = self.rule.config
    #     try:
    #         if self.sequence == False:
    #             return False
    #         # elif self.flag == 'strategy':
    #         #     return True
    #         else:
    #             return True
    #     except:
    #         return 'has no conf'
    
    def __str__(self):
        return f"{self.rule}"
    
class Strategy(models.Model):
    """
    When we want to combine some rule, strategy, rule and strategy together we use
    strategy.
    """
    rules = models.ManyToManyField("Rule", through='Order')
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
        es = Elasticsearch([f'{es_url}'],)
        if len(indices) > 1:
            url = f'http://{es_url}/_aliases?pretty'
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
                # try:
                """
                This is for handling errors. we send a request to Elasticsearch to get the list of all indices and if one of the indices does not 
                in the list, then alias should not be created.
                """
                get_index_from_elastic = []
                k = 0
                for index in es.indices.get('*'):
                    get_index_from_elastic.append(index)
                    
                for ii in indices:
                    if ii not in get_index_from_elastic: 
                        k += 1
                        
                if k == 0:
                    res1 = requests.post(url, headers=headers, data=data)
                    res = res1.json()
                    indices = alias_name
                    print("Response: ", res)
                    
                else:              
                    indices = ""
                                            
                # except:  
                #     print("####################################","ERROR stratey alias")
                #     return "raise error"
            self.strategy_alias = ' '.join(indices)
            # self.save()
        else:
            self.strategy_alias = ' '.join(indices)
            # self.save() 

        return indices
    
    def clean(self):
        """This is for handling errors in save method. 
            we cannot do handling errors in save because
            we confront 1000 errors.
        """
        if self.strategy_alias == '':
            raise ValidationError("index not found")
        super(Strategy, self).clean()
        
        
    def save(self, *args, **kwargs):
        
        # if self.strategy_alias=='':
        #     # print(self.id)
        #     # self.delete()
        #     return #prevent save
        #     # record = Strategy.objects.filter(id=self.id)
        #     # print(record)
        #     # record.clear()
        # else:
        #     # super(Strategy, self).save(*args, **kwargs)
        super(Strategy, self).save(*args, **kwargs)
        instance = Strategy.objects.last()
        
        dict_file = """
        ANPdata:
        - creation_date = "%s"
        - maturity = "production"
        - updated_date = "%s"
        
        ANPrule:
        - author= ["ANP"]
        - language= "eql"
        
        name: "%s"

        index: %s

        type: frequency
        num_events: 1
        timeframe:
        hours: 1
        
        eql:
         query: "%s"

        alert:
        - "slack"

        slack:
        slack_webhook_url: "https://hooks.slack.com/services/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"

        """%(instance.create_time, instance.modified_time, instance.strategy_name, instance.strategy_alias, instance.strategy_total)
                
        dict_file = yaml.safe_load(dict_file)          
        with open(f'D:\\Downloads\\VSCode\\elastalert\\rest\\Aras_strategy_{instance.strategy_name}.yaml', 'w') as file:
            yaml.dump(dict_file, file, width=1000)
        # except ValueError:
        #     print("error")
            
        
class Order(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name='stra')
    order = models.AutoField(primary_key=True)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, blank=True, null=True)
    add_from_another_strategy = models.BooleanField(default=False)
    add_strategy = models.ManyToManyField(Strategy, blank=True)
