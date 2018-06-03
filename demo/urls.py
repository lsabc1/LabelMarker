from django.conf.urls import url
from . import tagging_data_view, tagging_data_writefile_view

urlpatterns = [
    url(r'^$', tagging_data_writefile_view.tagging_push),       #这个页面不会存在，只会跳转到data页面
    url(r'^tagging_data', tagging_data_view.showtagging_data),  #主要的标记页面
    url(r'^tagging-get', tagging_data_writefile_view.tagging_push)  #标记后存在一瞬间就跳转到data页面
]
