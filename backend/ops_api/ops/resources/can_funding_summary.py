from flask import Response, request

from models.base import BaseModel
from ops_api.ops.auth.auth_types import Permission, PermissionType
from ops_api.ops.auth.decorators import is_authorized
from ops_api.ops.base_views import BaseItemAPI
from ops_api.ops.utils.cans import aggregate_funding_summaries, get_can_funding_summary, get_filtered_cans
from ops_api.ops.utils.response import make_response_with_headers


class CANFundingSummaryItemAPI(BaseItemAPI):
    def __init__(self, model: BaseModel):
        super().__init__(model)

    @is_authorized(PermissionType.GET, Permission.CAN)
    def get(self) -> Response:
        # Get query parameters
        can_ids = request.args.getlist("can_ids")
        fiscal_year = request.args.get("fiscal_year")
        active_period = request.args.getlist("active_period", type=int)
        transfer = request.args.getlist("transfer")
        portfolio = request.args.getlist("portfolio")
        fy_budget = request.args.getlist("fy_budget", type=int)

        # Check if required 'can_ids' parameter is provided
        if not can_ids:
            return make_response_with_headers({"error": "'can_ids' parameter is required"}, 400)

        # Handle case when a single 'can_id' is provided with no additional filters
        if len(can_ids) == 1 and not (active_period or transfer or portfolio or fy_budget):
            return self._handle_single_can_no_filters(can_ids[0], fiscal_year)

        # If 'can_ids' is 0 or multiple ids are provided, filter and aggregate
        return self._handle_cans_with_filters(can_ids, fiscal_year, active_period, transfer, portfolio, fy_budget)

    def _handle_single_can_no_filters(self, can_id: str, fiscal_year: str = None) -> Response:
        """Helper method for handling a single 'can_id' with no filters."""
        can = self._get_item(can_id)
        can_funding_summary = get_can_funding_summary(can, int(fiscal_year) if fiscal_year else None)
        return make_response_with_headers(can_funding_summary)

    def _get_cans(self, can_ids: list) -> list:
        """Helper method to get CANS."""
        if can_ids == [0]:
            return self._get_all_items()
        return [self._get_item(can_id) for can_id in can_ids]

    def _handle_cans_with_filters(
        self,
        can_ids: list,
        fiscal_year: str = None,
        active_period: list = None,
        transfer: list = None,
        portfolio: list = None,
        fy_budget: list = None,
    ) -> Response:
        cans_with_filters = get_filtered_cans(self._get_cans(can_ids), active_period, transfer, portfolio, fy_budget)

        can_funding_summaries = [
            get_can_funding_summary(can, int(fiscal_year) if fiscal_year else None) for can in cans_with_filters
        ]

        aggregated_summary = aggregate_funding_summaries(can_funding_summaries)

        return make_response_with_headers(aggregated_summary)
