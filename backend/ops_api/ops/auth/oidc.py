from http import HTTPStatus

from authlib.integrations.django_client import OAuth
from authlib.jose import jwt
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


oauth = OAuth()
oauth.register("logingov")


class OidcController(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request: Request):
        print(f"request.data = {request.data}")

        callback_url = request.data["callbackUrl"]
        # state = request.data["state"]
        code = request.data.get("code")
        pkce_code_verifier = request.data["pkceCodeVerifier"]

        print(
            f"""Got an OIDC request with the callback URL of {callback_url}
            and code of {code} and pkceCodeVerifier of {pkce_code_verifier}"""
        )

        token = oauth.logingov.fetch_access_token(
            code_verifier=pkce_code_verifier,
            grant_type="authorization_code",
            code=code,
        )
        print(token)

        return Response({"jwt": "OPS-specific JWT"}, status=HTTPStatus.OK)

    @staticmethod
    def get(request: Request):

        key_path = (
            settings.BASE_DIR / ".." / "ops" / "management" / "key" / "dev_only.pem"
        )
        with key_path.open("rb") as f:
            key = f.read()

        header = {"alg": "RS256"}
        payload = {"iss": "HHS", "sub": "OPRE OPS superuser"}
        jws = jwt.encode(header, payload, key)

        return Response({"jws": jws}, status=HTTPStatus.OK)
