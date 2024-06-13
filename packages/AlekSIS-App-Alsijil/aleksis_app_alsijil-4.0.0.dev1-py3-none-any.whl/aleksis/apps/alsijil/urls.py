from django.urls import path

from . import views

urlpatterns = [
    path("extra_marks/", views.ExtraMarkListView.as_view(), name="extra_marks"),
    path(
        "extra_marks/create/",
        views.ExtraMarkCreateView.as_view(),
        name="create_extra_mark",
    ),
    path(
        "extra_marks/<int:pk>/edit/",
        views.ExtraMarkEditView.as_view(),
        name="edit_extra_mark",
    ),
    path(
        "extra_marks/<int:pk>/delete/",
        views.ExtraMarkDeleteView.as_view(),
        name="delete_extra_mark",
    ),
    path("group_roles/", views.GroupRoleListView.as_view(), name="group_roles"),
    path("group_roles/create/", views.GroupRoleCreateView.as_view(), name="create_group_role"),
    path(
        "group_roles/<int:pk>/edit/",
        views.GroupRoleEditView.as_view(),
        name="edit_group_role",
    ),
    path(
        "group_roles/<int:pk>/delete/",
        views.GroupRoleDeleteView.as_view(),
        name="delete_group_role",
    ),
    path(
        "groups/<int:pk>/group_roles/",
        views.AssignedGroupRolesView.as_view(),
        name="assigned_group_roles",
    ),
    path(
        "groups/<int:pk>/group_roles/assign/",
        views.AssignGroupRoleView.as_view(),
        name="assign_group_role",
    ),
    path(
        "groups/<int:pk>/group_roles/<int:role_pk>/assign/",
        views.AssignGroupRoleView.as_view(),
        name="assign_group_role",
    ),
    path(
        "group_roles/assignments/<int:pk>/edit/",
        views.GroupRoleAssignmentEditView.as_view(),
        name="edit_group_role_assignment",
    ),
    path(
        "group_roles/assignments/<int:pk>/stop/",
        views.GroupRoleAssignmentStopView.as_view(),
        name="stop_group_role_assignment",
    ),
    path(
        "group_roles/assignments/<int:pk>/delete/",
        views.GroupRoleAssignmentDeleteView.as_view(),
        name="delete_group_role_assignment",
    ),
    path(
        "group_roles/assignments/assign/",
        views.AssignGroupRoleMultipleView.as_view(),
        name="assign_group_role_multiple",
    ),
]
