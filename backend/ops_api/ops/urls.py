from ops.portfolio.models import Portfolio
from ops.resources.portfolio import PortfolioItemAPI
from ops.resources.portfolio import PortfolioListAPI
from ops.resources.portfolio_calculate_funding import PortfolioCalculateFundingAPI

# Ideas from Flask docs: https://flask.palletsprojects.com/en/2.2.x/views/#method-dispatching-and-apis


def register_api(api_bp):
    api_bp.add_url_rule(
        "/portfolios/<int:id>/calcFunding/",
        view_func=PortfolioCalculateFundingAPI.as_view(
            "portfolio-calculate-funding", Portfolio
        ),
    )

    api_bp.add_url_rule(
        "/portfolios/<int:id>",
        view_func=PortfolioItemAPI.as_view("portfolio-item", Portfolio),
    )
    api_bp.add_url_rule(
        "/portfolios/",
        view_func=PortfolioListAPI.as_view("portfolio-group", Portfolio),
    )
