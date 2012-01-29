from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName


class CasClientCallback(BrowserView):
    """
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        if not self.portal_membership.isAnonymousUser():
            member = self.portal_membership.getAuthenticatedMember()
            login_time = member.getProperty('login_time', '2000/01/01 00:00:00 US/Eastern')
            initial_login = int(str(login_time) == '2000/01/01 00:00:00 US/Eastern')
            if initial_login:
                member.setMemberProperties(dict(must_change_password=True))
                self.request.RESPONSE.redirect('%s/login_password' % self.portal.absolute_url())
                return
        
        self.request.RESPONSE.redirect('%s' % self.portal.absolute_url())


    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
    
    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')