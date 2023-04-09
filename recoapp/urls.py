from django.urls import path
from .views import recommendViewset


urlpatterns=[
    path('recommend-products/', recommendViewset.as_view({'post':'get_new_user_recommendations'}), 
         name='recommend_products'),
]