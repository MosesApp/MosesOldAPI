from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from MosesWebservice import settings
from MosesWebserviceApp import views
from django.conf.urls.static import static

urlpatterns = format_suffix_patterns(patterns('MosesWebserviceApp.views',
    url(r'^$', 'api_root'),

    # Users
    url(r'^users/$',
        views.UsersCRUD.as_view(),
        name='usersCRUD'),

    url(r'^users/byGroup/(?P<pk>[0-9]+)/$',
        views.GroupUserDetailByUser.as_view(),
        name='usersByGroup'),

    url(r'^getUser/(?P<pk>[0-9&]+)/$',
        views.UserDetails.as_view(),
        name='userByFacebookId'),

    # Groups
    url(r'^groups/$',
        views.GroupsCRUD.as_view(),
        name='groupsCRUD'),

    url(r'^groups/addUser/$',
        views.GroupUserCreate.as_view(),
        name='addGroupUser'),

    url(r'^groups/byUser/(?P<pk>[0-9]+)/$',
        views.GroupUserDetailByGroup.as_view(),
        name='groupsByUser'),

    # Bill
    url(r'^createBill/$',
        views.BillCreate.as_view(),
        name='billCreate'),

    # Expenses
    url(r'^expenses/$',
        views.ExpensesCRUD.as_view(),
        name='expensesCRUD'),

    url(r'^expenses/byUser/(?P<pk>[0-9]+)/$',
        views.ExpensesByUser.as_view(),
        name='expensesByUser'),

    # Currency
    url(r'^currencies/$',
        views.CurrenciesCRUD.as_view(),
        name='currenciesCRUD'),
        
)) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('', url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),)
