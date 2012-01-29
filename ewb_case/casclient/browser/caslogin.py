from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName


class CasLogIn(BrowserView):
    """
    """

    def __call__(self):
        portal = self.context.portal_url.getPortalObject()
        acl = getToolByName(portal, "acl_users")
        plugin = acl.anz_casclient

        if plugin.casServerUrlPrefix:
            url = plugin.getLoginURL() + '?service=' + plugin.getService()
            if plugin.renew:
                url += '&renew=true'
            if plugin.gateway:
                url += '&gateway=true'
        
            self.request.RESPONSE.redirect(url, lock=1)
        
