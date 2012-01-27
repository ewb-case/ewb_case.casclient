from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName


class CasLogOut(BrowserView):
    """
    """

    def __call__(self):
        portal = self.context.portal_url.getPortalObject()
        cas_client_plugin = self.portal.acl_users.anz_casclient
        
        mt = getToolByName(context, 'portal_membership')
        mt.logoutUser(REQUEST=self.request)
        
        self.request.RESPONSE.redirect(cas_client_plugin.casServerUrlPrefix + '/logout')

