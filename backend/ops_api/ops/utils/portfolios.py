from decimal import Decimal
from typing import TypedDict

from models.cans import CAN, CANFiscalYear, CANFiscalYearCarryOver
from ops_api.ops import db
from sqlalchemy import select
from sqlalchemy.sql.functions import coalesce, sum


class FundingLineItem(TypedDict):
    """Dict type hint for line items in total funding."""

    amount: float
    label: str


class TotalFunding(TypedDict):
    """Dict type hint for total finding"""

    total_funding: FundingLineItem
    planned_funding: FundingLineItem
    obligated_funding: FundingLineItem
    in_execution_funding: FundingLineItem
    available_funding: FundingLineItem


def _get_total_fiscal_year_funding(portfolio_id: int, fiscal_year: int) -> Decimal:
    # N.B. BudgetLineItem isn't needed here but will be needed in the other calcs.
    stmt = (
        select(coalesce(sum(CANFiscalYear.total_fiscal_year_funding), 0))
        .join(CAN)
        # .join(
        #     BudgetLineItem,
        #     and_(
        #         BudgetLineItem.can_fiscal_year_can_id == CANFiscalYear.can_id,
        #         BudgetLineItem.can_fiscal_year_fiscal_year == CANFiscalYear.fiscal_year,
        #     ),
        # )
        .where(CAN.managing_portfolio_id == portfolio_id)
        .where(CANFiscalYear.fiscal_year == fiscal_year)
    )

    return db.session.execute(stmt).scalar()


def _get_carry_forward_total(portfolio_id: int, fiscal_year: int) -> Decimal:
    stmt = (
        select(coalesce(sum(CANFiscalYearCarryOver.amount), 0))
        .join(CAN)
        .where(CAN.managing_portfolio_id == portfolio_id)
        .where(CANFiscalYearCarryOver.to_fiscal_year == fiscal_year)
    )

    return db.session.execute(stmt).scalar()


def _get_budget_line_item_total_planned(portfolio_id: int, fiscal_year: int) -> Decimal:
    ...


# def get_total_funding(portfolio: Portfolio, fiscal_year: Optional[int] = None) -> TotalFunding:
# can_fiscal_year_query = CANFiscalYear.query.filter(CANFiscalYear.can.has(CAN.managing_portfolio == portfolio))
#
# can_fiscal_year_carry_over_query = CANFiscalYearCarryOver.query.filter(
#     CANFiscalYearCarryOver.can.has(CAN.managing_portfolio == portfolio)
# )
#
# if fiscal_year:
#     can_fiscal_year_query = can_fiscal_year_query.filter(CANFiscalYear.fiscal_year == fiscal_year).all()
#
#     can_fiscal_year_carry_over_query = can_fiscal_year_carry_over_query.filter(
#         CANFiscalYearCarryOver.to_fiscal_year == fiscal_year
#     ).all()

# total_funding = sum([c.total_fiscal_year_funding for c in can_fiscal_year_query]) or 0
# total_funding = _get_total_fiscal_year_funding(portfolio_id=portfolio.id, fiscal_year=fiscal_year)
#
# carry_over_funding = _get_carry_forward_total(portfolio_id=portfolio.id, fiscal_year=fiscal_year)

# Amount available to a Portfolio budget is the sum of the BLI minus the Portfolio total (above)
# budget_line_items = BudgetLineItem.query.filter(
#     BudgetLineItem.can_fiscal_year.has(
#         CANFiscalYear.can.managing_portfolio == portfolio
#     )
# )
#
# if fiscal_year:
#     budget_line_items = budget_line_items.filter(
#         BudgetLineItem.can_fiscal_year.fiscal_year == fiscal_year
#     )
#
# planned_budget_line_items = budget_line_items.filter(
#     BudgetLineItem.status.has(BudgetLineItemStatus.Planned)
# ).all()
# planned_funding = sum([b.funding for b in planned_budget_line_items]) or 0
#
# obligated_budget_line_items = budget_line_items.filter(
#     BudgetLineItem.status.has(BudgetLineItemStatus.Obligated)
# ).all()
# obligated_funding = sum([b.funding for b in obligated_budget_line_items]) or 0
#
# in_execution_budget_line_items = budget_line_items.filter(
#     BudgetLineItem.status.has(BudgetLineItemStatus.In_Execution)
# ).all()
# in_execution_funding = sum([b.funding for b in in_execution_budget_line_items]) or 0
#
# total_accounted_for = sum(
#     (
#         planned_funding,
#         obligated_funding,
#         in_execution_funding,
#     )
# )
#
# available_funding = float(total_funding) - float(total_accounted_for)
#
# return {
#     "total_funding": {
#         "amount": float(total_funding),
#         "percent": "Total",
#     },
#     "carry_over_funding": {
#         "amount": float(carry_over_funding),
#         "percent": "Carry Over",
#     },
#     "planned_funding": {
#         "amount": float(planned_funding),
#         "percent": get_percentage(total_funding, planned_funding),
#     },
#     "obligated_funding": {
#         "amount": float(obligated_funding),
#         "percent": get_percentage(total_funding, obligated_funding),
#     },
#     "in_execution_funding": {
#         "amount": float(in_execution_funding),
#         "percent": get_percentage(total_funding, in_execution_funding),
#     },
#     "available_funding": {
#         "amount": float(available_funding),
#         "percent": get_percentage(total_funding, available_funding),
#     },
# }


def get_percentage(total_funding: float, specific_funding: float) -> float:
    return 0 if total_funding == 0 else f"{round(float(specific_funding) / float(total_funding), 2) * 100}"
