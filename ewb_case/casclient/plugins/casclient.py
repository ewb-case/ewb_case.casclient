import logging

from AccessControl import ClassSecurityInfo

from Globals import InitializeClass

from zope.i18nmessageid import MessageFactory

from ZODB.POSException import ConflictError

from Products.CMFCore.utils import getToolByName
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import \
    IExtractionPlugin, IChallengePlugin, IAuthenticationPlugin, \
    ICredentialsResetPlugin, ICredentialsUpdatePlugin

from anz.casclient.casclient import AnzCASClient
from anz.casclient.proxygrantingticketstorage import ProxyGrantingTicketStorage
from anz.casclient.sessionmappingstorage import SessionMappingStorage


_ = MessageFactory('ewb_case.casclient')


add_cas_client_form = PageTemplateFile(
    '../browser/templates/add_cas_client_form.pt', globals()
)

def manage_add_cas_client(self, id, title=None, REQUEST=None):
    """ Add an instance of cas client to PAS.
    """
    obj = CasClient(id, title)
    self._setObject(obj.getId(), obj)
    
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
            '%s/manage_workspace'
            '?manage_tabs_message='
            'AnzCentralAuthService+added.'
            % self.absolute_url()
        )


class CasClient(AnzCASClient):
    meta_type = 'EWB Case CAS Client'

    email_format_string = "%s"

    _properties = getattr(AnzCASClient, '_properties', ()) + ({
        'id': 'email_format_string',
        'lable': 'Email Format String',
        'type': 'string',
        'mode': 'w',
    },)

    security = ClassSecurityInfo()

    def __init__(self, id, title, **kwargs):
        self._id = self.id = id
        self.title = title
        self._pgtStorage = ProxyGrantingTicketStorage()
        self._sessionStorage = SessionMappingStorage()
    
    
    security.declarePrivate('_addMember')
    def _addMember(self, username, password=None, **kwargs):
        if password is None:
            regtool = getToolByName(self, 'portal_registration')
            password = regtool.generatePassword()
            
        regtool.addMember(username, password, **kwargs)
        
        portal = getToolByName(self, 'portal_url').getPortalObject()
        return self._notifyPassword(username, portal.validate_email)


    security.declarePrivate('_notifyPassword')
    def _notifyPassword(self, username, validate_email):
        """ Based on logic in plonesocial.auth.rpx
        """
        try:
            portal_registration = getToolByName(self, 'portal_registration')
            portal_registration.registeredNotify(username)
            return True
        except ConflictError:
            raise
        except Exception, err:
            msg = None
            success = False
            if validate_email:
                portal_membership = getToolByName(self, 'portal_membership')
                portal_membership.logoutUser()
                self._getPAS()._doDelUser(username)
                msg = _(u'status_fatal_password_mail',
                        default=u'Failed to create your account: unable to send your password to your email address: ${address}',
                        mapping={u'address' : str(err)})
            else:
                msg = _(u'status_nonfatal_password_mail',
                        default=u'You account has been created, but we were unable to send your password to your email address: ${address}',
                        mapping={u'address' : str(err)})
                success = True
            plone_utils = getToolByName(self, 'plone_utils')
            plone_utils.addPortalMessage(msg, 'error')
            return success
    
             
    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        if credentials['extractor'] != self.getId():
            return None
        
        login = credentials['login']
        acl_users = getToolByName(self, 'acl_users')
        if login is not None and acl_users.getUserById(login) is None:
            if not self._addMember(login, roles={'Member': True}, properties={
              'username' : login,
              'email' : self.email_format_string % login,}):
                return None
        return (login, login)

    

classImplements(
    CasClient,
    IExtractionPlugin,
    IChallengePlugin,
    ICredentialsResetPlugin,
    IAuthenticationPlugin)

InitializeClass(CasClient)
