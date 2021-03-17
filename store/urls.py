from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path
from store import views
from cart import views as cart_views
from store.models import Comment, LikeDislike, Review

urlpatterns = [
    path('', views.index, name='home'),
    url(r'^$', views.product_list, name='product_list'),
    path('search/', views.search, name='search_products'),
    url(r'^ajax_calls/search/', views.autocompleteModel),
    path('cart_update/', cart_views.cart_update, name='cart_update'),

    url(r'^category/(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),

    url(r'^brend/(?P<company_slug>[-\w]+)/$',
        views.product_list_by_company,
        name='product_list_by_company'),

    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),

    path('comment/<int:pk>/', views.add_comment, name="add-comment"),
    path('comment/delete/<int:id>/', views.delete_comment, name='delete-comment'),
    path('review/<int:pk>/', views.add_review, name="add-review"),
    path('review/delete/<int:id>/', views.delete_review, name='delete-review'),

    url(r'^comment/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Comment, vote_type=LikeDislike.LIKE)),
        name='comment_like'),
    url(r'^comment/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Comment, vote_type=LikeDislike.DISLIKE)),
        name='comment_dislike'),
    url(r'^review/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Review, vote_type=LikeDislike.LIKE)),
        name='review_like'),
    url(r'^review/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Review, vote_type=LikeDislike.DISLIKE)),
        name='review_dislike'),

    url(r'^lazy_load_posts/(?P<pk>\d+)/$', views.lazy_load_posts, name='lazy_load_posts'),

]
