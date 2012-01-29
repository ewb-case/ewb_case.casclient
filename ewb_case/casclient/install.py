from AccessControl import Permissions

from Products.PluggableAuthService.PluggableAuthService import registerMultiPlugin

from ewb_case.casclient.plugins.casclient import CasClient, manage_add_cas_client, add_cas_client_form


def register_casclient_plugin():
    """register plugin with pas
    """
    try:
        registerMultiPlugin(CasClient.meta_type)
    except RuntimeError:
        #    make refresh users happy
        pass

def register_casclient_plugin_class(context):
    context.registerClass(CasClient,
        permission=Permissions.manage_users,
        constructors=(
            add_cas_client_form,
            manage_add_cas_client
        ),
        visibility=None
    )
