from django.urls    import path
from .views         import CategoryView, SubCategoryView, ProductListView, DetailView, ProductTotalListView

urlpatterns = [
    path('/category', CategoryView.as_view()),
    path('/category/<int:main_id>', SubCategoryView.as_view()),
    path('/list/<int:sub_id>', ProductListView.as_view()),
    path('/list/total/<int:main_id>', ProductTotalListView.as_view()),
    path('/<int:product_id>', DetailView.as_view())
]
