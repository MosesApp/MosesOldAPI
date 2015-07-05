from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from MosesWebservice import settings
from MosesWebserviceApp import views
from django.conf.urls.static import static

urlpatterns = format_suffix_patterns(patterns('MosesWebserviceApp.views',
    url(r'^$', 'api_root'),

    # User
    url(r'^listUsers/$',
        views.UserList.as_view(),
        name='user-list'),

    url(r'^createUser/$',
        views.UserCreate.as_view(),
        name='user-create'),

    url(r'^getUser/(?P<pk>[0-9&]+)/$',
        views.UserDetails.as_view(),
        name='user-details-filter-facebookid'),

    # Group
    url(r'^createGroup/$',
        views.GroupCreate.as_view(),
        name='group-create'),

    url(r'^listGroups/$',
        views.GroupList.as_view(),
        name='group-list'),

    # Group_User
    url(r'^createGroupUserRelation/$',
        views.GroupUserCreate.as_view(),
        name='group_user-create'),

    url(r'^getUserGroupRelation/Group/(?P<pk>[0-9]+)/$',
        views.GroupUserDetailGroup.as_view(),
        name='group_user-details-filter-groupid'),

    url(r'^getUserGroupRelation/User/(?P<pk>[0-9]+)/$',
        views.GroupUserDetailUser.as_view(),
        name='group_user-details-filter-userid'),

    # Bill
    url(r'^createBill/$',
        views.BillCreate.as_view(),
        name='bill-create'),

    # Bill User
    url(r'^listBillUsers/$',
        views.BillUserList.as_view(),
        name='bill_user-list'),

    url(r'^createBillUser/$',
        views.BillUserCreate.as_view(),
        name='bill_user-create'),

    url(r'^getBillUser/(?P<pk>[0-9]+)/$',
        views.BillUserDetail.as_view(),
        name='bill_user-details'),

    # Currency
    url(r'^listCurrencies/$',
        views.CurrencyList.as_view(),
        name='currency-list'),

    url(r'^createCurrency/$',
        views.CurrencyCreate.as_view(),
        name='currency-create'),

)) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('', url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),)

