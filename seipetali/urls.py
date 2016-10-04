from django.conf.urls import patterns, include, url
from django.contrib import admin
import urls_api

from photologue.views import PhotoDetailView
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns



photologue = patterns('',
                      url(r'^photo/(?P<slug>[\-\d\w]+)/$',
                           PhotoDetailView.as_view(),
                           name='pl-photo',),
                       )





urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),


    # Examples:
    url(r'^$', 'seipetali.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Admin panel of django

    # allauth urls login,logout,password/reset,confirm
    url(r'^accounts/', include('allauth.urls')),

    url(r'^search/map/', 'alloggio.views.search_map', name='alloggio_search_map' ),
    url(r'^search/', 'alloggio.views.search_start', name='alloggio_search' ),


    url(r'^alloggio/list/', 'alloggio.views.list', name='alloggio_list' ),
    url(r'^alloggio/create', 'alloggio.views.create', name='alloggio_create' ),
    url(r'^alloggio/edit/(?P<pk>\d+)/$', 'alloggio.views.edit', name='alloggio_edit' ),
    url(r'^alloggio/detail/(?P<pk>\d+)$', 'alloggio.views.detail', name='alloggio_detail' ),

    url(r'^reservation/detail/(?P<pk>\d+)$', 'reservation.views.detail', name='reservation_detail' ),

    url(r'^gallery/', include(photologue, namespace='photologue')),

    url(r'^faq/list/(?P<gruppo>\w+)$', 'faq.views.list', name='faq_listagruppo' ),
    url(r'^faq/list', 'faq.views.list', name='faq_list' ),
    url(r'^faq/create', 'faq.views.create', name='faq_create' ),
    url(r'^faq/edit/(?P<pk>\d+)$', 'faq.views.edit', name='faq_edit' ),

    url(r'^user/locatore_registration', 'user.views.registra_locatore', name='registra_locatore' ),


    url(r'^dashboard/callcenter/$', 'seipetali.views.dashboard_call_center', name='dashboard_call_center' ),

    url(r'^seipetali/card/$', 'seipetali.views.seipetali_card', name='seipetali_card' ),

)

# Tutto il resto lo cerca come pagina statica... da tenere come ultima regola
urlpatterns += patterns('',
        url(r'^ng-template/(?P<page>.*)$', 'common.views.reverse_staticView',name='static_view'),
)



urlpatterns += i18n_patterns('',
    url(r'^cms/', include('cms.urls',None,'cms')),
)


urlpatterns += patterns('',
    (r'^i18n/', include('django.conf.urls.i18n')),
    # url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
)


# Add API Urls
urlpatterns += urls_api.get_urls()
urlpatterns += patterns('',
     url(r'api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
)



if settings.DEBUG :

    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

    # if settings.FORCE_PRODUCTION:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    )