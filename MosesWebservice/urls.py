from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from MosesWebservice import settings
from MosesWebserviceApp import views
from django.conf.urls.static import static

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
    url(r'^bill_receiver/(?P<pk>[0-9]+)/$',
        views.BillDetailReceiver.as_view(),
        name='bill-receiver-detail'),
    url(r'^bill_debtor/(?P<pk>[0-9]+)/$',
        views.BillDetailDebtor.as_view(),
        name='bill-debtor-detail'),

    url(r'^group_users/$',
        views.GroupUserList.as_view(),
        name='group_user-list'),
    url(r'^group_user/$',
        views.GroupUserCreate.as_view(),
        name='group_user-create'),
    url(r'^group_user/(?P<pk>[0-9]+)/$',
        views.GroupUserDetail.as_view(),
        name='group_user-detail'),

)) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('', url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),)

