# Permissions & Groups Setup

## Overview
This project uses Django's groups and permissions system to restrict access.

### Permissions Added
- `can_view`: Allows viewing books
- `can_create`: Allows adding new books
- `can_edit`: Allows editing books
- `can_delete`: Allows deleting books

### Groups
- **Viewers** → `can_view`
- **Editors** → `can_view`, `can_edit`, `can_create`
- **Admins** → `can_view`, `can_edit`, `can_create`, `can_delete`

### Enforcement
Views are protected using `@permission_required` decorator.

### Setup Steps
1. Run `python manage.py makemigrations && python manage.py migrate`.
2. Go to admin → Groups and confirm groups & permissions.
3. Assign users to groups.
4. Test with different user roles.
