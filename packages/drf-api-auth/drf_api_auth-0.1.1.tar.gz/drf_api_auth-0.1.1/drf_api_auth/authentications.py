from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class ApikeyAuthentication(BaseAuthentication):
    """
    API-Key Authentication.

    Users or Services should authenticate by passing the api key in the "x-api-key"
    HTTP header.  For example:

        x-api-key: nXHnS60s1vKi6MvGbQ5VFMFnr5Y2hMdCCT07dE02PnkkZwjmZ8E3eTxVZvp73Pes
    """

    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from drf_api_auth.models import ApiAuth

        return ApiAuth

    """
    A custom api auth model may be used, but must have the following properties.

    * api_key -- The string to identify user
    * user -- The user to which the api_key belongs
    """

    def authenticate(self, request):
        api_key = request.META.get("X_API_KEY", "")

        if not api_key:
            return None

        model = self.get_model()

        try:
            api_auth = model.objects.select_related("user").get(api_key=api_key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid api key.")

        if not api_auth.user.is_active:
            raise exceptions.AuthenticationFailed("Invalid api key.")

        return api_auth.user, api_key
