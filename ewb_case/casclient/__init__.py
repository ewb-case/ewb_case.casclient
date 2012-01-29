from AccessControl import Permissions

from Products.PluggableAuthService.PluggableAuthService import registerMultiPlugin

from ewb_case.casclient.casclient import CasClient, manage_addAnzCASClient, addAnzCASClientForm


# register plugins with pas
try:
    registerMultiPlugin(CasClient.meta_type)
except RuntimeError:
    pass

def initialize(context):
    context.registerClass(AnzCASClient,
        permission=Permissions.manage_users,
        constructors=(
            add_cas_client_form,
            addCasClient
        ),
        visibility=None
    )
