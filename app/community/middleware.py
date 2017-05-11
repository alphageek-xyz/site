from machina.apps.forum_permission.middleware import ForumPermissionMiddleware


class BetterForumPermissionMiddleware(ForumPermissionMiddleware):
    def process_request(self, request):
        if '/community/' in request.META.get('PATH_INFO', ''):
            super(BetterForumPermissionMiddleware, self).process_request(request)
