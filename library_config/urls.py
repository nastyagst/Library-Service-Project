from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("users.urls", namespace="users")),
    path("api/books/", include("books.urls", namespace="books")),
    path(
        "api/borrowings/",
        include("borrowings.urls", namespace="borrowings")
    ),
    path("api/payments/", include("payments.urls", namespace="payments")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
