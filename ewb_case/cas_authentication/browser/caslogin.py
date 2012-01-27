from Products.Five.browser import BrowserView

class CasLogIn(BrowserView):
    """
    """

    def __call__(self):
        portal = self.context.portal_url.getPortalObject()
        plugin = self.portal.acl_users.anz_casclient
        
        if plugin.casServerUrlPrefix:
            url = plugin.getLoginURL() + '?service=' + plugin.getService()
            if plugin.renew:
                url += '&renew=true'
            if plugin.gateway:
                url += '&gateway=true'
        
            self.request.RESPONSE.redirect(url, lock=1)
        
