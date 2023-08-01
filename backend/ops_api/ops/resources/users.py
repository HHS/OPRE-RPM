from flask import Response, current_app, request
from models.base import BaseModel
from ops_api.ops.base_views import BaseItemAPI, BaseListAPI
from ops_api.ops.utils.auth import Permission, PermissionType, is_authorized
from ops_api.ops.utils.response import make_response_with_headers
from typing_extensions import override


class UsersItemAPI(BaseItemAPI):
    def __init__(self, model: BaseModel):
        super().__init__(model)

    @override
    @is_authorized(PermissionType.GET, Permission.USER)
    def get(self, id: int) -> Response:
        # token = verify_jwt_in_request()
        # Get the user from the token to see who's making the request
        # sub = str(token[1]["sub"])
        oidc_id = request.args.get("oidc_id", type=str)

        # Grab the user, based on which ID is being queried (id or oidc_id)
        if oidc_id:
            response = self._get_item_by_oidc_with_try(oidc_id)
        else:
            response = self._get_item_with_try(id)

        # Users can only see their own user details
        # Update this authZ checks once we determine additional
        # roles that can view other users details.
        # TODO: Need to be able to do user lookup without OIDC
        # if sub == str(response.json["oidc_id"]):
        return response
        # else:
        #    response = make_response({}, 401)  # nosemgrep
        #    return response


class UsersListAPI(BaseListAPI):
    def __init__(self, model: BaseModel):
        super().__init__(model)

    @override
    @is_authorized(PermissionType.GET, Permission.USER)
    def get(self) -> Response:
        oidc_id = request.args.get("oidc_id", type=str)

        if oidc_id:
            response = self._get_item_by_oidc_with_try(oidc_id)
        else:
            items = self.model.query.all()
            response = make_response_with_headers([item.to_dict() for item in items])

        return response

    @override
    @is_authorized(PermissionType.PUT, Permission.USER)
    def put(self, id: int) -> Response:
        # Get the user to update
        user = self._get_item_with_try(id)

        # Update the user with the request data
        user.update(request.json)

        # Save the changes to the database
        current_app.db_session.add(user)
        current_app.db_session.commit()

        # Return the updated user as a response
        return make_response_with_headers(user.to_dict())
