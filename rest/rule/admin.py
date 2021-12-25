from os import name
from django.contrib import admin
from .models import Rule, Query, Config, Strategy, Order#, CustomStrategyManager

# Register your models here.

# @admin.action(description='strategy')
# def strategy(modeladmin, request, queryset):

#     # queryset.update(flag='strategy')
#     strategy_name = ""
#     for rule in queryset:
#         a = str(rule)
#         strategy_name += f"{a} "    
    
#     indexname = ""
#     for rule in queryset:
#         a = str(rule)
#         indexname += f"{rule.index_name}, "
    
#     rule = Rule.objects.get_value(queryset, name=strategy_name, index_name=indexname, flag='strategy')
    
    # b = rule.create_total(queryset)
    
    # print(b)
    # a = print("^^^^^^^^^^^", queryset)
    
    # # rule.flag = str(queryset[0])
    # # print("##################", queryset[0])

    #     # print("!!!!!!!!!!!!!!!", rule)
    # # print("@@@@@@@@@@@", strategy_name)
    # rule.save()
    # for rule in queryset:
    #     queries = rule.queries.all()
    #     # print("#########################queries", queries)
    #     rule.query_sum = f""
        # print("##################a", d)
        # for query in a:
        #     zz += str(query.event_category)
    # rule.query_sum = 
   
    # rule.save()       
        
    # print("##########", queryset)
    # print("##########", request)
    # Rule.objects.create(name='test_strategy',index_name = 'test_index')
    
    
 


class StrategyInline(admin.TabularInline):
    model = Strategy
    extra = 1

class QueryInline(admin.TabularInline):
    model = Query
    extra = 1

class ConfigInline(admin.TabularInline):
    model = Config
    
class StrategyInline(admin.TabularInline):
    model = Strategy.rules.through
    extra = 1
class OrderInline(admin.StackedInline):
    model = Order
    extra = 1
    # readonly_fields = ['get_author_name']
    # def get_author_name(self, st):
    #     return st.strategy

class RuleAdmin(admin.ModelAdmin):
    # class Meta:
    #     model = Rule
    list_display = ['id', 'name', 'index_name', 'sequence','create_time', 'modified_time', 'total', 'total_method']
    search_fields = ['name', 'index_name']
    list_display_links = ['name']
    inlines = [
        QueryInline,
        ConfigInline,
        
        ]
    # def total_method(self,instance):
    #     a = instance.total_method()
    #     return instance.total
    # def save_model(self, request, obj, form, change):
    #     # obj.user = request.user
    #     # super().save_model(request, obj, form, change)

    #     Rule.objects.create(name=obj.name,index_name=obj.index_name, create_time=obj.create_time, modified_time=obj.modified_time)
        # return rule
    # actions = [strategy]
    
class QueryAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_category', 'condition',]
    # list_editable = ['sequence']
    search_field = ['event_category', 'condition']
    

class StrategyAdmin(admin.ModelAdmin):

    # strategy = Strategy.objects.get(id=25)
    # y, z = strategy.final()
    # def ff(self):
    #     return self.z
        
    # print(y,z)
    list_display = ['id', 'strategy_name', 'strategy_index','create_time','modified_time','final_query']
    # list_editable = ['sequence']
    list_display_links = ['strategy_name']
    search_field = ['strategy_name']
    inlines = [
        StrategyInline,
        
        
        ]
    # ordering = ('order',)
    exclude = ('rules',)

    # def save_model(self, request, obj, form, change):
    #     print('form.cleaned_data')
        # Strategy.objects.create(strategy_name=obj., rules)

admin.site.register(Rule, RuleAdmin)
admin.site.register(Query, QueryAdmin)
admin.site.register(Strategy, StrategyAdmin)
admin.site.register(Order)
# admin.site.register(Query) 