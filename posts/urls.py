from django.urls import path
from .views import CommentDetailView, CommentListView, PostFilterView, PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view()),
    path('by/<str:pk>/', PostFilterView.as_view()),
    path('comments/<int:comment_pk>/', CommentDetailView.as_view()),
    path('<int:pk>/comments/', CommentListView.as_view()),
    path('<int:pk>/', PostDetailView.as_view())
]
