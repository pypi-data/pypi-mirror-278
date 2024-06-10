# My Django Permissions

A custom Django permissions package.

## Installation

```bash
pip install aclvl_permissions
```

## Usage
In your Django project, you can use the custom permission as follows:

```bash
from my_django_permissions.permissions import AccessLevelPermission

class MyView(APIView):
    permission_classes = [AccessLevelPermission]
    required_access_levels = ['view_all_model', 'view_owner_model', 'create_all_model']
    view_key = 'model'
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

