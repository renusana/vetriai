from django.urls import path

from .views import (
    ApprovalListView,
    ApprovalPreviewView,
    ApprovalDetailView,
    ApprovalApproveView,
    ApprovalEditView,
    ApprovalCancelView,
)

urlpatterns = [
    path(
        "",
        ApprovalListView.as_view(),
        name="approval-list",
    ),
    path(
        "preview/",
        ApprovalPreviewView.as_view(),
        name="approval-preview",
    ),
    path(
        "<int:action_id>/",
        ApprovalDetailView.as_view(),
        name="approval-detail",
    ),
    path(
        "<int:action_id>/approve/",
        ApprovalApproveView.as_view(),
        name="approval-approve",
    ),
    path(
        "<int:action_id>/edit/",
        ApprovalEditView.as_view(),
        name="approval-edit",
    ),
    path(
        "<int:action_id>/cancel/",
        ApprovalCancelView.as_view(),
        name="approval-cancel",
    ),
]
