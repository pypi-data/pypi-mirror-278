from rest_framework.permissions import BasePermission


def query_set_filter_key(view_key, user_access_levels, required_access_levels, request_method):
    if required_access_levels is None:
        return 'all'

    user_access_levels = user_access_levels.values_list('access_key', flat=True)
    methods = {"GET": "view", "POST": "create", "PUT": "update", "PATCH": "update", "DELETE": "delete"}

    required_access_levels_filter = [al for al in required_access_levels if al.startswith(methods[request_method])]
    user_access_levels_filter = [
        al for al in user_access_levels if al.split('_')[2] == view_key and al.startswith(methods[request_method])
    ]

    if any(level in user_access_levels_filter for level in required_access_levels_filter):
        query_filters = [x.split('_')[1] for x in user_access_levels_filter]
        if 'all' in query_filters:
            return 'all'
        elif 'owner' in query_filters:
            return 'owner'

    return None


class AccessLevelPermission(BasePermission):
    """
    Custom permission to allow access based on user's access levels.
    """

    def has_permission(self, request, view):
        required_access_levels = getattr(view, 'required_access_levels', None)
        view_key = getattr(view, 'view_key', None)

        if required_access_levels is None:
            return True
        if not request.user.is_authenticated:
            return False

        user_access_levels = request.user.get_access_levels().values_list('access_key', flat=True)
        method_access_prefix = {
            'GET': 'view',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete'
        }

        required_access_levels_filtered = [
            al for al in required_access_levels if al.startswith(method_access_prefix[request.method])
        ]
        user_access_levels_filtered = [
            al for al in user_access_levels if
            al.split('_')[2] == view_key and al.startswith(method_access_prefix[request.method])
        ]

        return any(level in user_access_levels_filtered for level in required_access_levels_filtered)

    def has_object_permission(self, request, view, obj):
        required_access_levels = getattr(view, 'required_access_levels', None)
        view_key = getattr(view, 'view_key', None)

        if required_access_levels is None:
            return True
        if not request.user.is_authenticated:
            return False

        user_access_levels = request.user.get_access_levels().values_list('access_key', flat=True)
        filter_key = query_set_filter_key(view_key, request.user.get_access_levels(), required_access_levels,
                                          request.method)

        method_access_prefix = {
            'GET': 'view',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete'
        }

        required_access_levels_filtered = [
            al for al in required_access_levels if al.startswith(method_access_prefix[request.method])
        ]
        user_access_levels_filtered = [
            al for al in user_access_levels if
            al.split('_')[2] == view_key and al.startswith(method_access_prefix[request.method])
        ]

        if filter_key in ['all', 'receptor']:
            return any(level in user_access_levels_filtered for level in required_access_levels_filtered)
        elif filter_key in ['owner', 'operator']:
            return request.user in obj.owners() and any(
                level in user_access_levels_filtered for level in required_access_levels_filtered
            )

        return False
