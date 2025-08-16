# Django Blog Project - Blog Post Features

## Overview
This project includes a fully functional blog system where users can create, read, update, and delete posts (CRUD). Features are built using Django class-based views and forms.

## Features

1. **List Posts**
   - URL: `/posts/`
   - Displays all blog posts.
   - Accessible to all users (authenticated or not).

2. **View Post Detail**
   - URL: `/posts/<id>/`
   - Shows full post content.
   - Accessible to all users.

3. **Create Post**
   - URL: `/posts/new/`
   - Only logged-in users can create posts.
   - Form includes `title` and `content`.
   - Author is automatically set to the logged-in user.

4. **Update Post**
   - URL: `/posts/<id>/edit/`
   - Only the author of the post can edit.
   - Users cannot edit posts created by others.

5. **Delete Post**
   - URL: `/posts/<id>/delete/`
   - Only the author can delete.
   - Redirects to `/posts/` after deletion.

## Permissions
- **Public Access:** View list and detail of posts.
- **Authenticated Access:** Create posts.
- **Author Only:** Update and delete posts.

## Usage Notes
- Make sure users are logged in to create, edit, or delete posts.
- All templates should extend `base.html` to maintain consistent layout and navigation.
- The Post model automatically sets the `published_date` on creation.

