from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)


class SchemaAPIView(SpectacularAPIView):
    pass


class SchemaSwaggerView(SpectacularSwaggerView):
    pass


class SchemaRedocView(SpectacularRedocView):
    pass
