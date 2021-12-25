
from django.urls import path, include
# from .views import RuleDetail, RuleList, query_total, test, UserList, UserDetail

from .views import UserViewSet, RuleViewSet, QueryViewSet, ConfigViewSet, StrategyViewSet, OrderViewSet
from rest_framework import routers

app_name = "rule"

router = routers.SimpleRouter()
router.register('users', UserViewSet)
router.register('rule', RuleViewSet)
router.register('query', QueryViewSet)
router.register('config', ConfigViewSet)
router.register('strategy', StrategyViewSet)
router.register('order', OrderViewSet)
# urlpatterns = router.urls

#or
urlpatterns = [
    path("", include(router.urls)),
    
    
]

# urlpatterns = [
#     path("", RuleList.as_view(), name="list"),
#     path("<int:pk>", RuleDetail.as_view(), name="detail"),    
#     path("users/", UserList.as_view(), name="user-list"),
#     path("users/<int:pk>", UserDetail.as_view(), name="user-detail"),

# ]











# router = DefaultRouter()
# router.register(r'rule', RuleViewSets, basename='rule')
# urlpatterns = router.urls

# urlpatterns = [
#     # path("rule_list", rule_list),
#     # path("rule_detail/<pk>", rule_detail),
#     # path("rule_save", rule_save),
#     # path("rule_update/<pk>", rule_update),
#     # path("rule_delete/<pk>", rule_delete),

#     # path("rulelist/", RuleList.as_view()),
      
#     # path("", include(router.urls)),


#     path("query/", query_total),
#     path("test/<id>", test),
#     # path("yaml/", rule_yaml),
#     # path("detail/<int:pk>/", query_total_detail),
#     # path("get_rule_id/<int:pk>/", get_rule_id),
    




# ]
