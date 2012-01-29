from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName


class CasLogOut(BrowserView):
    """
    """

    def __call__(self):
        portal = self.context.portal_url.getPortalObject()
        acl = getToolByName(portal, "acl_users")
        cas_client_plugin = acl.casclient
        
        mt = getToolByName(self.context, 'portal_membership')
        mt.logoutUser(REQUEST=self.request)
        
        self.request.RESPONSE.redirect(cas_client_plugin.casServerUrlPrefix + '/logout')
