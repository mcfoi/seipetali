__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


from cms.cms_toolbar import BasicToolbar,ADMIN_MENU_IDENTIFIER,get_user_sites_queryset,get_cms_setting,Site,_,ADMIN_SITES_BREAK,admin_reverse,USER_SETTINGS_BREAK




class CustomToolbar(BasicToolbar):

    def populate(self):
        self.init_from_request()

        self.add_admin_menu()
        self.add_language_menu()

    def add_admin_menu(self):
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, self.current_site.name)

        # Users button
        self.add_users_button(admin_menu)

        # sites menu
        if get_cms_setting('PERMISSION'):
            sites_queryset = get_user_sites_queryset(self.request.user)
        else:
            sites_queryset = Site.objects.all()

        if len(sites_queryset) > 1:
            sites_menu = admin_menu.get_or_create_menu('sites', _('Sites'))
            sites_menu.add_sideframe_item(_('Admin Sites'), url=admin_reverse('sites_site_changelist'))
            sites_menu.add_break(ADMIN_SITES_BREAK)
            for site in sites_queryset:
                sites_menu.add_link_item(site.name, url='http://%s' % site.domain,
                                         active=site.pk == self.current_site.pk)

        # # admin
        # admin_menu.add_sideframe_item(_('Administration'), url=admin_reverse('index'))
        # admin_menu.add_break(ADMINISTRATION_BREAK)

        # cms users
        admin_menu.add_sideframe_item(_('User settings'), url=admin_reverse('cms_usersettings_change'))
        admin_menu.add_break(USER_SETTINGS_BREAK)

        # logout
        self.add_logout_button(admin_menu)