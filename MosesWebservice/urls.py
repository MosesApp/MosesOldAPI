from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from MosesWebserviceApp import views

urlpatterns = format_suffix_patterns(patterns('MosesWebserviceApp.views',
    url(r'^$', 'api_root'),

    url(r'^users/$',
        views.UserList.as_view(),
        name='user-list'),
    url(r'^user/(?P<facebook_id>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail'),

    url(r'^groups/$',
        views.GroupList.as_view(),
        name='group-list'),
    url(r'^group/(?P<pk>[0-9]+)/$',
        views.GroupDetail.as_view(),
        name='group-detail'),

    url(r'^bills/$',
        views.BillList.as_view(),
        name='bill-list'),
    url(r'^bill/(?P<pk>[0-9]+)/$',
        views.BillDetail.as_view(),
        name='bill-detail'),

    url(r'^group_users/$',
        views.GroupUserList.as_view(),
        name='group_user-list'),
    url(r'^group_user/(?P<pk>[0-9]+)/$',
        views.GroupUserDetail.as_view(),
        name='group_user-detail'),

))

urlpatterns += patterns('', url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),)
