from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName


class CasLogIn(BrowserView):
    """
    """

    def __call__(self):
        portal = self.context.portal_url.getPortalObject()
        acl = getToolByName(portal, "acl_users")
        cas_client_plugin = acl.casclient

        if cas_client_plugin.casServerUrlPrefix:
            url = "%s?service=%s" % (cas_client_plugin.getLoginURL(), cas_client_plugin.getService())
            if cas_client_plugin.renew:
                url += '&renew=true'
            if cas_client_plugin.gateway:
                url += '&gateway=true'
        
            self.request.RESPONSE.redirect(url, lock=1)
        
