from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from MosesWebservice import settings
from MosesWebserviceApp import views
from django.conf.urls.static import static

urlpatterns = format_suffix_patterns(patterns('MosesWebserviceApp.views',
    url(r'^$', 'api_root'),

    url(r'^users/$',
        views.UserList.as_view(),
        name='user-crud'),
    url(r'^user/(?P<facebook_id>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail'),

    url(r'^groups/$',
        views.GroupList.as_view(),
        name='group-read'),
    url(r'^group/$',
        views.GroupCreate.as_view(),
        name='group-create'),

    url(r'^bill/$',
        views.BillCreate.as_view(),
        name='bill-create'),

    url(r'^bill_users/$',
        views.BillUserList.as_view(),
        name='bill_user-crud'),
    url(r'^bill_user/(?P<pk>[0-9]+)/$',
        views.BillUserDetail.as_view(),
        name='bill_user-detail'),

    url(r'^group_user/$',
        views.GroupUserCreate.as_view(),
        name='group_user-create'),
    url(r'^group_user_user/(?P<pk>[0-9]+)/$',
        views.GroupUserDetailUser.as_view(),
        name='group_user-detail_user'),
    url(r'^group_user_group/(?P<pk>[0-9]+)/$',
        views.GroupUserDetailGroup.as_view(),
        name='group_user-detail_group'),

)) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('', url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),)

