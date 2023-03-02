from drf_spectacular.extensions import OpenApiAuthenticationExtension


class JWTAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = 'authentication.backends.JWTAuthentication'
    name = 'JWTAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }


class JWTCookieAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = 'authentication.backends.JWTCookieAuthentication'
    name = 'JWTCookieAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'access',
        }
