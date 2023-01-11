from ops.models.cans import BudgetLineItemStatus
import pytest


@pytest.mark.usefixtures("app_ctx")
def test_budget_line_item_status_retrieve_all(loaded_db_with_cans):
    bli_status = loaded_db_with_cans.session.query(BudgetLineItemStatus).all()
    assert len(bli_status) == 3


@pytest.mark.parametrize(
    "id,status", [(1, "Planned"), (2, "In Execution"), (3, "Obligated")]
)
@pytest.mark.usefixtures("app_ctx")
def test_budget_line_item_status_lookup(loaded_db_with_cans, id, status):
    bli_status = loaded_db_with_cans.session.query(BudgetLineItemStatus).get(id)
    assert bli_status.status == status
