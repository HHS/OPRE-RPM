"""initial db

Revision ID: f515d8d67b78
Revises:
Create Date: 2024-02-28 15:14:01.810646+00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f515d8d67b78"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("oidc_id", sa.UUID(), nullable=True),
        sa.Column("hhs_id", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column(
            "date_joined", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column("updated", sa.DateTime(), nullable=True),
        sa.Column("division", sa.Integer(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        # sa.ForeignKeyConstraint(["division"], ["division.id"], name="fk_user_division"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=False)
    op.create_index(op.f("ix_user_oidc_id"), "user", ["oidc_id"], unique=True)
    op.create_table(
        "division",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("abbreviation", sa.String(length=10), nullable=False),
        sa.Column("division_director_id", sa.Integer(), nullable=True),
        sa.Column("deputy_division_director_id", sa.Integer(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["deputy_division_director_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["division_director_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("abbreviation"),
        sa.UniqueConstraint("name"),
    )
    op.create_foreign_key("fk_user_division", "user", "division", ["division"], ["id"])
    op.create_table(
        "administrative_and_support_project_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_administrative_and_support_project_version_end_transaction_id"),
        "administrative_and_support_project_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_administrative_and_support_project_version_operation_type"),
        "administrative_and_support_project_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_administrative_and_support_project_version_transaction_id"),
        "administrative_and_support_project_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "agreement_team_members_version",
        sa.Column("user_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("agreement_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", "agreement_id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_agreement_team_members_version_end_transaction_id"),
        "agreement_team_members_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_agreement_team_members_version_operation_type"),
        "agreement_team_members_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_agreement_team_members_version_transaction_id"),
        "agreement_team_members_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "agreement_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "agreement_type",
            postgresql.ENUM(
                "CONTRACT",
                "GRANT",
                "DIRECT_ALLOCATION",
                "IAA",
                "IAA_AA",
                "MISCELLANEOUS",
                name="agreementtype",
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "name",
            sa.String(),
            autoincrement=False,
            nullable=True,
            comment="In MAPS this was PROJECT.PROJECT_TITLE",
        ),
        sa.Column("description", sa.String(), autoincrement=False, nullable=True),
        sa.Column(
            "product_service_code_id", sa.Integer(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "agreement_reason",
            postgresql.ENUM(
                "NEW_REQ", "RECOMPETE", "LOGICAL_FOLLOW_ON", name="agreementreason"
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "project_officer_id", sa.Integer(), autoincrement=False, nullable=True
        ),
        sa.Column("project_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "procurement_shop_id", sa.Integer(), autoincrement=False, nullable=True
        ),
        sa.Column("notes", sa.Text(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_agreement_version_end_transaction_id"),
        "agreement_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_agreement_version_operation_type"),
        "agreement_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_agreement_version_transaction_id"),
        "agreement_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "budget_line_item_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("line_description", sa.String(), autoincrement=False, nullable=True),
        sa.Column("comments", sa.Text(), autoincrement=False, nullable=True),
        sa.Column("agreement_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("can_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "services_component_id", sa.Integer(), autoincrement=False, nullable=True
        ),
        sa.Column("clin_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "amount",
            sa.Numeric(precision=12, scale=2),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "DRAFT",
                "PLANNED",
                "IN_EXECUTION",
                "OBLIGATED",
                name="budgetlineitemstatus",
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("date_needed", sa.Date(), autoincrement=False, nullable=True),
        sa.Column(
            "proc_shop_fee_percentage",
            sa.Numeric(precision=12, scale=5),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_budget_line_item_version_end_transaction_id"),
        "budget_line_item_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_budget_line_item_version_operation_type"),
        "budget_line_item_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_budget_line_item_version_transaction_id"),
        "budget_line_item_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "can_fiscal_year_carry_forward_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("can_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("from_fiscal_year", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("to_fiscal_year", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "received_amount",
            sa.Numeric(precision=12, scale=2),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "expected_amount",
            sa.Numeric(precision=12, scale=2),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("notes", sa.String(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_can_fiscal_year_carry_forward_version_end_transaction_id"),
        "can_fiscal_year_carry_forward_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_can_fiscal_year_carry_forward_version_operation_type"),
        "can_fiscal_year_carry_forward_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_can_fiscal_year_carry_forward_version_transaction_id"),
        "can_fiscal_year_carry_forward_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "can_fiscal_year_version",
        sa.Column("can_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("fiscal_year", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "total_fiscal_year_funding",
            sa.Numeric(precision=12, scale=2),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "received_funding",
            sa.Numeric(precision=12, scale=2),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "expected_funding",
            sa.Numeric(precision=12, scale=2),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "potential_additional_funding",
            sa.Numeric(precision=12, scale=2),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("can_lead", sa.String(), autoincrement=False, nullable=True),
        sa.Column("notes", sa.String(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("can_id", "fiscal_year", "transaction_id"),
    )
    op.create_index(
        op.f("ix_can_fiscal_year_version_end_transaction_id"),
        "can_fiscal_year_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_can_fiscal_year_version_operation_type"),
        "can_fiscal_year_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_can_fiscal_year_version_transaction_id"),
        "can_fiscal_year_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "can_funding_sources_version",
        sa.Column("can_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "funding_source_id", sa.Integer(), autoincrement=False, nullable=False
        ),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("can_id", "funding_source_id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_can_funding_sources_version_end_transaction_id"),
        "can_funding_sources_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_can_funding_sources_version_operation_type"),
        "can_funding_sources_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_can_funding_sources_version_transaction_id"),
        "can_funding_sources_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "can_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("number", sa.String(length=30), autoincrement=False, nullable=True),
        sa.Column("description", sa.String(), autoincrement=False, nullable=True),
        sa.Column("purpose", sa.String(), autoincrement=False, nullable=True),
        sa.Column("nickname", sa.String(length=30), autoincrement=False, nullable=True),
        sa.Column("expiration_date", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column(
            "appropriation_date", sa.DateTime(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "appropriation_term", sa.Integer(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "arrangement_type",
            sa.Enum(
                "OPRE_APPROPRIATION",
                "COST_SHARE",
                "IAA",
                "IDDA",
                "MOU",
                name="canarrangementtype",
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("authorizer_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "managing_portfolio_id", sa.Integer(), autoincrement=False, nullable=True
        ),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_can_version_end_transaction_id"),
        "can_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_can_version_operation_type"),
        "can_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_can_version_transaction_id"),
        "can_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "clin_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(length=256), autoincrement=False, nullable=True),
        sa.Column("source_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_clin_version_end_transaction_id"),
        "clin_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_clin_version_operation_type"),
        "clin_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_clin_version_transaction_id"),
        "clin_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "contact_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("first_name", sa.String(), autoincrement=False, nullable=True),
        sa.Column("last_name", sa.String(), autoincrement=False, nullable=True),
        sa.Column("middle_name", sa.String(), autoincrement=False, nullable=True),
        sa.Column("address", sa.String(), autoincrement=False, nullable=True),
        sa.Column("city", sa.String(), autoincrement=False, nullable=True),
        sa.Column("state", sa.String(), autoincrement=False, nullable=True),
        sa.Column("zip", sa.String(), autoincrement=False, nullable=True),
        sa.Column("phone_area_code", sa.String(), autoincrement=False, nullable=True),
        sa.Column("phone_number", sa.String(), autoincrement=False, nullable=True),
        sa.Column("email", sa.String(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_contact_version_end_transaction_id"),
        "contact_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_contact_version_operation_type"),
        "contact_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_contact_version_transaction_id"),
        "contact_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "contract_agreement_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("contract_number", sa.String(), autoincrement=False, nullable=True),
        sa.Column("incumbent_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("vendor_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("task_order_number", sa.String(), autoincrement=False, nullable=True),
        sa.Column("po_number", sa.String(), autoincrement=False, nullable=True),
        sa.Column(
            "acquisition_type",
            postgresql.ENUM(
                "GSA_SCHEDULE", "TASK_ORDER", "FULL_AND_OPEN", name="acquisitiontype"
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("delivered_status", sa.Boolean(), autoincrement=False, nullable=True),
        sa.Column(
            "contract_type",
            postgresql.ENUM(
                "FIRM_FIXED_PRICE",
                "TIME_AND_MATERIALS",
                "LABOR_HOUR",
                "COST_PLUS_FIXED_FEE",
                "COST_PLUS_AWARD_FEE",
                "HYBRID",
                name="contracttype",
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "service_requirement_type",
            postgresql.ENUM(
                "SEVERABLE", "NON_SEVERABLE", name="servicerequirementtype"
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_contract_agreement_version_end_transaction_id"),
        "contract_agreement_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_contract_agreement_version_operation_type"),
        "contract_agreement_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_contract_agreement_version_transaction_id"),
        "contract_agreement_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "contract_support_contacts_version",
        sa.Column("contract_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("users_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("contract_id", "users_id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_contract_support_contacts_version_end_transaction_id"),
        "contract_support_contacts_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_contract_support_contacts_version_operation_type"),
        "contract_support_contacts_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_contract_support_contacts_version_transaction_id"),
        "contract_support_contacts_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "direct_agreement_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("payee", sa.String(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_direct_agreement_version_end_transaction_id"),
        "direct_agreement_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_direct_agreement_version_operation_type"),
        "direct_agreement_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_direct_agreement_version_transaction_id"),
        "direct_agreement_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "division_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(length=100), autoincrement=False, nullable=True),
        sa.Column(
            "abbreviation", sa.String(length=10), autoincrement=False, nullable=True
        ),
        sa.Column(
            "division_director_id", sa.Integer(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "deputy_division_director_id",
            sa.Integer(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_division_version_end_transaction_id"),
        "division_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_division_version_operation_type"),
        "division_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_division_version_transaction_id"),
        "division_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "funding_partner_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(length=100), autoincrement=False, nullable=True),
        sa.Column(
            "nickname", sa.String(length=100), autoincrement=False, nullable=True
        ),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_funding_partner_version_end_transaction_id"),
        "funding_partner_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_funding_partner_version_operation_type"),
        "funding_partner_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_funding_partner_version_transaction_id"),
        "funding_partner_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "funding_source_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(length=100), autoincrement=False, nullable=True),
        sa.Column(
            "nickname", sa.String(length=100), autoincrement=False, nullable=True
        ),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_funding_source_version_end_transaction_id"),
        "funding_source_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_funding_source_version_operation_type"),
        "funding_source_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_funding_source_version_transaction_id"),
        "funding_source_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "grant_agreement_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("foa", sa.String(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_grant_agreement_version_end_transaction_id"),
        "grant_agreement_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_grant_agreement_version_operation_type"),
        "grant_agreement_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_grant_agreement_version_transaction_id"),
        "grant_agreement_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "group_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_group_version_end_transaction_id"),
        "group_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_group_version_name"), "group_version", ["name"], unique=False
    )
    op.create_index(
        op.f("ix_group_version_operation_type"),
        "group_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_group_version_transaction_id"),
        "group_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "iaa_aa_agreement_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("iaa_aa", sa.String(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_iaa_aa_agreement_version_end_transaction_id"),
        "iaa_aa_agreement_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_iaa_aa_agreement_version_operation_type"),
        "iaa_aa_agreement_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_iaa_aa_agreement_version_transaction_id"),
        "iaa_aa_agreement_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "iaa_agreement_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("iaa", sa.String(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_iaa_agreement_version_end_transaction_id"),
        "iaa_agreement_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_iaa_agreement_version_operation_type"),
        "iaa_agreement_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_iaa_agreement_version_transaction_id"),
        "iaa_agreement_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "notification_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("title", sa.String(), autoincrement=False, nullable=True),
        sa.Column("message", sa.String(), autoincrement=False, nullable=True),
        sa.Column("is_read", sa.Boolean(), autoincrement=False, nullable=True),
        sa.Column("expires", sa.Date(), autoincrement=False, nullable=True),
        sa.Column("recipient_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_notification_version_end_transaction_id"),
        "notification_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_notification_version_operation_type"),
        "notification_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_notification_version_transaction_id"),
        "notification_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "ops_db_history_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "event_type",
            sa.Enum("NEW", "UPDATED", "DELETED", "ERROR", name="opsdbhistorytype"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "event_details",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("class_name", sa.String(), autoincrement=False, nullable=True),
        sa.Column("row_key", sa.String(), autoincrement=False, nullable=True),
        sa.Column(
            "changes",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_ops_db_history_version_end_transaction_id"),
        "ops_db_history_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ops_db_history_version_operation_type"),
        "ops_db_history_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ops_db_history_version_transaction_id"),
        "ops_db_history_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "ops_event_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "event_type",
            sa.Enum(
                "LOGIN_ATTEMPT",
                "CREATE_BLI",
                "UPDATE_BLI",
                "CREATE_PROJECT",
                "CREATE_NEW_AGREEMENT",
                "UPDATE_AGREEMENT",
                "SEND_BLI_FOR_APPROVAL",
                "DELETE_AGREEMENT",
                "ACKNOWLEDGE_NOTIFICATION",
                "LOGOUT",
                "CREATE_USER",
                "UPDATE_USER",
                "DEACTIVATE_USER",
                "CREATE_BLI_PACKAGE",
                "UPDATE_BLI_PACKAGE",
                "CREATE_SERVICES_COMPONENT",
                "UPDATE_SERVICES_COMPONENT",
                "DELETE_SERVICES_COMPONENT",
                name="opseventtype",
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "event_status",
            sa.Enum("SUCCESS", "FAILED", "UNKNOWN", name="opseventstatus"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "event_details",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_ops_event_version_end_transaction_id"),
        "ops_event_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ops_event_version_operation_type"),
        "ops_event_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ops_event_version_transaction_id"),
        "ops_event_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "package_snapshot_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("package_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("version", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("bli_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_package_snapshot_version_end_transaction_id"),
        "package_snapshot_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_package_snapshot_version_operation_type"),
        "package_snapshot_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_package_snapshot_version_transaction_id"),
        "package_snapshot_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "package_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("submitter_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("workflow_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("notes", sa.String(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_package_version_end_transaction_id"),
        "package_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_package_version_operation_type"),
        "package_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_package_version_transaction_id"),
        "package_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "portfolio_team_leaders_version",
        sa.Column("portfolio_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("team_lead_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("portfolio_id", "team_lead_id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_portfolio_team_leaders_version_end_transaction_id"),
        "portfolio_team_leaders_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_portfolio_team_leaders_version_operation_type"),
        "portfolio_team_leaders_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_portfolio_team_leaders_version_transaction_id"),
        "portfolio_team_leaders_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "portfolio_url_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("portfolio_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("url", sa.String(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_portfolio_url_version_end_transaction_id"),
        "portfolio_url_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_portfolio_url_version_operation_type"),
        "portfolio_url_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_portfolio_url_version_transaction_id"),
        "portfolio_url_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "portfolio_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(), autoincrement=False, nullable=True),
        sa.Column("abbreviation", sa.String(), autoincrement=False, nullable=True),
        sa.Column(
            "status",
            sa.Enum("IN_PROCESS", "NOT_STARTED", "SANDBOX", name="portfoliostatus"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("division_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("description", sa.Text(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_portfolio_version_end_transaction_id"),
        "portfolio_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_portfolio_version_operation_type"),
        "portfolio_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_portfolio_version_transaction_id"),
        "portfolio_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "procurement_shop_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(), autoincrement=False, nullable=True),
        sa.Column("abbr", sa.String(), autoincrement=False, nullable=True),
        sa.Column("fee", sa.Float(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_procurement_shop_version_end_transaction_id"),
        "procurement_shop_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_procurement_shop_version_operation_type"),
        "procurement_shop_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_procurement_shop_version_transaction_id"),
        "procurement_shop_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "product_service_code_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(), autoincrement=False, nullable=True),
        sa.Column("naics", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("support_code", sa.String(), autoincrement=False, nullable=True),
        sa.Column("description", sa.String(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_product_service_code_version_end_transaction_id"),
        "product_service_code_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_service_code_version_operation_type"),
        "product_service_code_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_service_code_version_transaction_id"),
        "product_service_code_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "project_cans_version",
        sa.Column("project_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("can_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("project_id", "can_id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_project_cans_version_end_transaction_id"),
        "project_cans_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_cans_version_operation_type"),
        "project_cans_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_cans_version_transaction_id"),
        "project_cans_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "project_team_leaders_version",
        sa.Column("project_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("team_lead_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("project_id", "team_lead_id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_project_team_leaders_version_end_transaction_id"),
        "project_team_leaders_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_team_leaders_version_operation_type"),
        "project_team_leaders_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_team_leaders_version_transaction_id"),
        "project_team_leaders_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "project_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "project_type",
            postgresql.ENUM(
                "RESEARCH", "ADMINISTRATIVE_AND_SUPPORT", name="projecttype"
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("title", sa.String(), autoincrement=False, nullable=True),
        sa.Column("short_title", sa.String(), autoincrement=False, nullable=True),
        sa.Column("description", sa.Text(), autoincrement=False, nullable=True),
        sa.Column("url", sa.Text(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_project_version_end_transaction_id"),
        "project_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_version_operation_type"),
        "project_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_version_transaction_id"),
        "project_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "research_project_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("origination_date", sa.Date(), autoincrement=False, nullable=True),
        sa.Column(
            "methodologies",
            postgresql.ARRAY(
                sa.Enum(
                    "SURVEY",
                    "FIELD_RESEARCH",
                    "PARTICIPANT_OBSERVATION",
                    "ETHNOGRAPHY",
                    "EXPERIMENT",
                    "SECONDARY_DATA_ANALYSIS",
                    "CASE_STUDY",
                    name="methodologytype",
                )
            ),
            server_default="{}",
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "populations",
            postgresql.ARRAY(
                sa.Enum(
                    "POPULATION_1",
                    "POPULATION_2",
                    "POPULATION_3",
                    name="populationtype",
                )
            ),
            server_default="{}",
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_research_project_version_end_transaction_id"),
        "research_project_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_research_project_version_operation_type"),
        "research_project_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_research_project_version_transaction_id"),
        "research_project_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "role_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(), autoincrement=False, nullable=True),
        sa.Column("permissions", sa.String(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_role_version_end_transaction_id"),
        "role_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_role_version_name"), "role_version", ["name"], unique=False
    )
    op.create_index(
        op.f("ix_role_version_operation_type"),
        "role_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_role_version_transaction_id"),
        "role_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "services_component_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("number", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("optional", sa.Boolean(), autoincrement=False, nullable=True),
        sa.Column("description", sa.String(), autoincrement=False, nullable=True),
        sa.Column("period_start", sa.Date(), autoincrement=False, nullable=True),
        sa.Column("period_end", sa.Date(), autoincrement=False, nullable=True),
        sa.Column(
            "contract_agreement_id", sa.Integer(), autoincrement=False, nullable=True
        ),
        sa.Column("clin_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_services_component_version_end_transaction_id"),
        "services_component_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_services_component_version_operation_type"),
        "services_component_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_services_component_version_transaction_id"),
        "services_component_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "shared_portfolio_cans_version",
        sa.Column("portfolio_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("can_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("portfolio_id", "can_id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_shared_portfolio_cans_version_end_transaction_id"),
        "shared_portfolio_cans_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_shared_portfolio_cans_version_operation_type"),
        "shared_portfolio_cans_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_shared_portfolio_cans_version_transaction_id"),
        "shared_portfolio_cans_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "step_approvers_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "workflow_step_template_id",
            sa.Integer(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("user_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("role_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("group_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_step_approvers_version_end_transaction_id"),
        "step_approvers_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_step_approvers_version_operation_type"),
        "step_approvers_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_step_approvers_version_transaction_id"),
        "step_approvers_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "transaction",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("remote_addr", sa.String(length=50), nullable=True),
        sa.Column("issued_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_group_version",
        sa.Column("user_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("group_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", "group_id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_user_group_version_end_transaction_id"),
        "user_group_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_group_version_operation_type"),
        "user_group_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_group_version_transaction_id"),
        "user_group_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "user_role_version",
        sa.Column("user_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("role_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", "role_id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_user_role_version_end_transaction_id"),
        "user_role_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_role_version_operation_type"),
        "user_role_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_role_version_transaction_id"),
        "user_role_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "user_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("oidc_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column("hhs_id", sa.String(), autoincrement=False, nullable=True),
        sa.Column("email", sa.String(), autoincrement=False, nullable=True),
        sa.Column("first_name", sa.String(), autoincrement=False, nullable=True),
        sa.Column("last_name", sa.String(), autoincrement=False, nullable=True),
        sa.Column(
            "date_joined",
            sa.DateTime(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("updated", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("division", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_user_version_email"), "user_version", ["email"], unique=False
    )
    op.create_index(
        op.f("ix_user_version_end_transaction_id"),
        "user_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_version_oidc_id"), "user_version", ["oidc_id"], unique=False
    )
    op.create_index(
        op.f("ix_user_version_operation_type"),
        "user_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_version_transaction_id"),
        "user_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "vendor_contacts_version",
        sa.Column("vendor_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("contact_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("vendor_id", "contact_id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_vendor_contacts_version_end_transaction_id"),
        "vendor_contacts_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_vendor_contacts_version_operation_type"),
        "vendor_contacts_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_vendor_contacts_version_transaction_id"),
        "vendor_contacts_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "vendor_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(), autoincrement=False, nullable=True),
        sa.Column("duns", sa.String(), autoincrement=False, nullable=True),
        sa.Column("active", sa.Boolean(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_vendor_version_end_transaction_id"),
        "vendor_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_vendor_version_operation_type"),
        "vendor_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_vendor_version_transaction_id"),
        "vendor_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "workflow_instance_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("associated_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "associated_type",
            sa.Enum("CAN", "PROCUREMENT_SHOP", name="workflowtriggertype"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "workflow_template_id", sa.Integer(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "workflow_action",
            sa.Enum(
                "DRAFT_TO_PLANNED",
                "PLANNED_TO_EXECUTING",
                "GENERIC",
                name="workflowaction",
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "current_workflow_step_instance_id",
            sa.Integer(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_workflow_instance_version_end_transaction_id"),
        "workflow_instance_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_workflow_instance_version_operation_type"),
        "workflow_instance_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_workflow_instance_version_transaction_id"),
        "workflow_instance_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "workflow_step_dependency_version",
        sa.Column(
            "predecessor_step_id", sa.Integer(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "successor_step_id", sa.Integer(), autoincrement=False, nullable=False
        ),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "predecessor_step_id", "successor_step_id", "transaction_id"
        ),
    )
    op.create_index(
        op.f("ix_workflow_step_dependency_version_end_transaction_id"),
        "workflow_step_dependency_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_workflow_step_dependency_version_operation_type"),
        "workflow_step_dependency_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_workflow_step_dependency_version_transaction_id"),
        "workflow_step_dependency_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "workflow_step_instance_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "workflow_instance_id", sa.Integer(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "workflow_step_template_id",
            sa.Integer(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.Enum("REVIEW", "APPROVED", "REJECTED", "CHANGES", name="workflowstatus"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("notes", sa.String(), autoincrement=False, nullable=True),
        sa.Column("time_started", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("time_completed", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_workflow_step_instance_version_end_transaction_id"),
        "workflow_step_instance_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_workflow_step_instance_version_operation_type"),
        "workflow_step_instance_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_workflow_step_instance_version_transaction_id"),
        "workflow_step_instance_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "workflow_step_template_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(), autoincrement=False, nullable=True),
        sa.Column(
            "workflow_template_id", sa.Integer(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "workflow_type",
            sa.Enum(
                "APPROVAL",
                "DOCUMENT_MGMT",
                "VALIDATION",
                "PROCUREMENT",
                name="workflowsteptype",
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("index", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_workflow_step_template_version_end_transaction_id"),
        "workflow_step_template_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_workflow_step_template_version_operation_type"),
        "workflow_step_template_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_workflow_step_template_version_transaction_id"),
        "workflow_step_template_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "workflow_template_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(), autoincrement=False, nullable=True),
        sa.Column("created_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated_on", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("created_by", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", "transaction_id"),
    )
    op.create_index(
        op.f("ix_workflow_template_version_end_transaction_id"),
        "workflow_template_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_workflow_template_version_operation_type"),
        "workflow_template_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_workflow_template_version_transaction_id"),
        "workflow_template_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "clin",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "contact",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("middle_name", sa.String(), nullable=True),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("zip", sa.String(), nullable=True),
        sa.Column("phone_area_code", sa.String(), nullable=True),
        sa.Column("phone_number", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "funding_partner",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("nickname", sa.String(length=100), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "funding_source",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("nickname", sa.String(length=100), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "group",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_group_name"), "group", ["name"], unique=False)
    op.create_table(
        "notification",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("message", sa.String(), nullable=True),
        sa.Column("is_read", sa.Boolean(), nullable=True),
        sa.Column("expires", sa.Date(), nullable=True),
        sa.Column("recipient_id", sa.Integer(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["recipient_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ops_db_history",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "event_type",
            sa.Enum("NEW", "UPDATED", "DELETED", "ERROR", name="opsdbhistorytype"),
            nullable=True,
        ),
        sa.Column(
            "event_details", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("class_name", sa.String(), nullable=True),
        sa.Column("row_key", sa.String(), nullable=True),
        sa.Column("changes", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_ops_db_history_class_name_row_key_created_on",
        "ops_db_history",
        ["class_name", "row_key", sa.text("created_on DESC")],
        unique=False,
    )
    op.create_table(
        "ops_event",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "event_type",
            sa.Enum(
                "LOGIN_ATTEMPT",
                "CREATE_BLI",
                "UPDATE_BLI",
                "CREATE_PROJECT",
                "CREATE_NEW_AGREEMENT",
                "UPDATE_AGREEMENT",
                "SEND_BLI_FOR_APPROVAL",
                "DELETE_AGREEMENT",
                "ACKNOWLEDGE_NOTIFICATION",
                "LOGOUT",
                "CREATE_USER",
                "UPDATE_USER",
                "DEACTIVATE_USER",
                "CREATE_BLI_PACKAGE",
                "UPDATE_BLI_PACKAGE",
                "CREATE_SERVICES_COMPONENT",
                "UPDATE_SERVICES_COMPONENT",
                "DELETE_SERVICES_COMPONENT",
                name="opseventtype",
            ),
            nullable=True,
        ),
        sa.Column(
            "event_status",
            sa.Enum("SUCCESS", "FAILED", "UNKNOWN", name="opseventstatus"),
            nullable=True,
        ),
        sa.Column(
            "event_details", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "portfolio",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("abbreviation", sa.String(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("IN_PROCESS", "NOT_STARTED", "SANDBOX", name="portfoliostatus"),
            nullable=True,
        ),
        sa.Column("division_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["division_id"],
            ["division.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "procurement_shop",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("abbr", sa.String(), nullable=False),
        sa.Column("fee", sa.Float(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "product_service_code",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("naics", sa.Integer(), nullable=True),
        sa.Column("support_code", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "project_type",
            postgresql.ENUM(
                "RESEARCH", "ADMINISTRATIVE_AND_SUPPORT", name="projecttype"
            ),
            nullable=False,
        ),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("short_title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("short_title"),
    )
    op.create_table(
        "role",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("permissions", sa.String(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_role_name"), "role", ["name"], unique=False)
    op.create_table(
        "vendor",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("duns", sa.String(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "workflow_template",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "administrative_and_support_project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["project.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "agreement",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "agreement_type",
            postgresql.ENUM(
                "CONTRACT",
                "GRANT",
                "DIRECT_ALLOCATION",
                "IAA",
                "IAA_AA",
                "MISCELLANEOUS",
                name="agreementtype",
            ),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(),
            nullable=False,
            comment="In MAPS this was PROJECT.PROJECT_TITLE",
        ),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("product_service_code_id", sa.Integer(), nullable=True),
        sa.Column(
            "agreement_reason",
            postgresql.ENUM(
                "NEW_REQ", "RECOMPETE", "LOGICAL_FOLLOW_ON", name="agreementreason"
            ),
            nullable=True,
        ),
        sa.Column("project_officer_id", sa.Integer(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("procurement_shop_id", sa.Integer(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["procurement_shop_id"],
            ["procurement_shop.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_service_code_id"],
            ["product_service_code.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_officer_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "can",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("number", sa.String(length=30), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("purpose", sa.String(), nullable=True),
        sa.Column("nickname", sa.String(length=30), nullable=True),
        sa.Column("expiration_date", sa.DateTime(), nullable=True),
        sa.Column("appropriation_date", sa.DateTime(), nullable=True),
        sa.Column("appropriation_term", sa.Integer(), nullable=True),
        sa.Column(
            "arrangement_type",
            sa.Enum(
                "OPRE_APPROPRIATION",
                "COST_SHARE",
                "IAA",
                "IDDA",
                "MOU",
                name="canarrangementtype",
            ),
            nullable=True,
        ),
        sa.Column("authorizer_id", sa.Integer(), nullable=True),
        sa.Column("managing_portfolio_id", sa.Integer(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["authorizer_id"],
            ["funding_partner.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["managing_portfolio_id"],
            ["portfolio.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "portfolio_team_leaders",
        sa.Column("portfolio_id", sa.Integer(), nullable=False),
        sa.Column("team_lead_id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["portfolio_id"],
            ["portfolio.id"],
        ),
        sa.ForeignKeyConstraint(
            ["team_lead_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("portfolio_id", "team_lead_id"),
    )
    op.create_table(
        "portfolio_url",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("portfolio_id", sa.Integer(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["portfolio_id"],
            ["portfolio.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "project_team_leaders",
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("team_lead_id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
        ),
        sa.ForeignKeyConstraint(
            ["team_lead_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("project_id", "team_lead_id"),
    )
    op.create_table(
        "research_project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("origination_date", sa.Date(), nullable=True),
        sa.Column(
            "methodologies",
            postgresql.ARRAY(
                sa.Enum(
                    "SURVEY",
                    "FIELD_RESEARCH",
                    "PARTICIPANT_OBSERVATION",
                    "ETHNOGRAPHY",
                    "EXPERIMENT",
                    "SECONDARY_DATA_ANALYSIS",
                    "CASE_STUDY",
                    name="methodologytype",
                )
            ),
            server_default="{}",
            nullable=False,
        ),
        sa.Column(
            "populations",
            postgresql.ARRAY(
                sa.Enum(
                    "POPULATION_1",
                    "POPULATION_2",
                    "POPULATION_3",
                    name="populationtype",
                )
            ),
            server_default="{}",
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["project.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_group",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["group.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "group_id"),
    )
    op.create_table(
        "user_role",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["role.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
    )
    op.create_table(
        "vendor_contacts",
        sa.Column("vendor_id", sa.Integer(), nullable=False),
        sa.Column("contact_id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["vendor_id"],
            ["vendor.id"],
        ),
        sa.PrimaryKeyConstraint("vendor_id", "contact_id"),
    )
    op.create_table(
        "workflow_instance",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("associated_id", sa.Integer(), nullable=False),
        sa.Column(
            "associated_type",
            sa.Enum("CAN", "PROCUREMENT_SHOP", name="workflowtriggertype"),
            nullable=False,
        ),
        sa.Column("workflow_template_id", sa.Integer(), nullable=True),
        sa.Column(
            "workflow_action",
            sa.Enum(
                "DRAFT_TO_PLANNED",
                "PLANNED_TO_EXECUTING",
                "GENERIC",
                name="workflowaction",
            ),
            nullable=False,
        ),
        sa.Column("current_workflow_step_instance_id", sa.Integer(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["workflow_template_id"],
            ["workflow_template.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "workflow_step_template",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("workflow_template_id", sa.Integer(), nullable=True),
        sa.Column(
            "workflow_type",
            sa.Enum(
                "APPROVAL",
                "DOCUMENT_MGMT",
                "VALIDATION",
                "PROCUREMENT",
                name="workflowsteptype",
            ),
            nullable=False,
        ),
        sa.Column("index", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["workflow_template_id"],
            ["workflow_template.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "agreement_team_members",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("agreement_id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["agreement_id"],
            ["agreement.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "agreement_id"),
    )
    op.create_table(
        "can_fiscal_year",
        sa.Column("can_id", sa.Integer(), nullable=False),
        sa.Column("fiscal_year", sa.Integer(), nullable=False),
        sa.Column(
            "total_fiscal_year_funding",
            sa.Numeric(precision=12, scale=2),
            nullable=True,
        ),
        sa.Column("received_funding", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("expected_funding", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column(
            "potential_additional_funding",
            sa.Numeric(precision=12, scale=2),
            nullable=True,
        ),
        sa.Column("can_lead", sa.String(), nullable=True),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["can_id"],
            ["can.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("can_id", "fiscal_year"),
    )
    op.create_table(
        "can_fiscal_year_carry_forward",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("can_id", sa.Integer(), nullable=True),
        sa.Column("from_fiscal_year", sa.Integer(), nullable=True),
        sa.Column("to_fiscal_year", sa.Integer(), nullable=True),
        sa.Column("received_amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("expected_amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["can_id"],
            ["can.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "can_funding_sources",
        sa.Column("can_id", sa.Integer(), nullable=False),
        sa.Column("funding_source_id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["can_id"],
            ["can.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["funding_source_id"],
            ["funding_source.id"],
        ),
        sa.PrimaryKeyConstraint("can_id", "funding_source_id"),
    )
    op.create_table(
        "contract_agreement",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contract_number", sa.String(), nullable=True),
        sa.Column("incumbent_id", sa.Integer(), nullable=True),
        sa.Column("vendor_id", sa.Integer(), nullable=True),
        sa.Column("task_order_number", sa.String(), nullable=True),
        sa.Column("po_number", sa.String(), nullable=True),
        sa.Column(
            "acquisition_type",
            postgresql.ENUM(
                "GSA_SCHEDULE", "TASK_ORDER", "FULL_AND_OPEN", name="acquisitiontype"
            ),
            nullable=True,
        ),
        sa.Column("delivered_status", sa.Boolean(), nullable=False),
        sa.Column(
            "contract_type",
            postgresql.ENUM(
                "FIRM_FIXED_PRICE",
                "TIME_AND_MATERIALS",
                "LABOR_HOUR",
                "COST_PLUS_FIXED_FEE",
                "COST_PLUS_AWARD_FEE",
                "HYBRID",
                name="contracttype",
            ),
            nullable=True,
        ),
        sa.Column(
            "service_requirement_type",
            postgresql.ENUM(
                "SEVERABLE", "NON_SEVERABLE", name="servicerequirementtype"
            ),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["agreement.id"],
        ),
        sa.ForeignKeyConstraint(
            ["incumbent_id"],
            ["vendor.id"],
        ),
        sa.ForeignKeyConstraint(
            ["vendor_id"],
            ["vendor.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "direct_agreement",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("payee", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["agreement.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "grant_agreement",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("foa", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["agreement.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "iaa_aa_agreement",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("iaa_aa", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["agreement.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "iaa_agreement",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("iaa", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["agreement.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "package",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("submitter_id", sa.Integer(), nullable=True),
        sa.Column("workflow_id", sa.Integer(), nullable=True),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["submitter_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["workflow_id"],
            ["workflow_instance.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "project_cans",
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("can_id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["can_id"],
            ["can.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
        ),
        sa.PrimaryKeyConstraint("project_id", "can_id"),
    )
    op.create_table(
        "shared_portfolio_cans",
        sa.Column("portfolio_id", sa.Integer(), nullable=False),
        sa.Column("can_id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["can_id"],
            ["can.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["portfolio_id"],
            ["portfolio.id"],
        ),
        sa.PrimaryKeyConstraint("portfolio_id", "can_id"),
    )
    op.create_table(
        "step_approvers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("workflow_step_template_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.Column("group_id", sa.Integer(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["group.id"],
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["role.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["workflow_step_template_id"],
            ["workflow_step_template.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "workflow_step_instance",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("workflow_instance_id", sa.Integer(), nullable=True),
        sa.Column("workflow_step_template_id", sa.Integer(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("REVIEW", "APPROVED", "REJECTED", "CHANGES", name="workflowstatus"),
            nullable=False,
        ),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("time_started", sa.DateTime(), nullable=True),
        sa.Column("time_completed", sa.DateTime(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["updated_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["workflow_instance_id"],
            ["workflow_instance.id"],
        ),
        sa.ForeignKeyConstraint(
            ["workflow_step_template_id"],
            ["workflow_step_template.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "contract_support_contacts",
        sa.Column("contract_id", sa.Integer(), nullable=False),
        sa.Column("users_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["contract_id"],
            ["contract_agreement.id"],
        ),
        sa.ForeignKeyConstraint(
            ["users_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("contract_id", "users_id"),
    )
    op.create_table(
        "services_component",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("number", sa.Integer(), nullable=True),
        sa.Column("optional", sa.Boolean(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("period_start", sa.Date(), nullable=True),
        sa.Column("period_end", sa.Date(), nullable=True),
        sa.Column("contract_agreement_id", sa.Integer(), nullable=True),
        sa.Column("clin_id", sa.Integer(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["clin_id"],
            ["clin.id"],
        ),
        sa.ForeignKeyConstraint(
            ["contract_agreement_id"],
            ["contract_agreement.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "workflow_step_dependency",
        sa.Column("predecessor_step_id", sa.Integer(), nullable=False),
        sa.Column("successor_step_id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["predecessor_step_id"],
            ["workflow_step_instance.id"],
        ),
        sa.ForeignKeyConstraint(
            ["successor_step_id"],
            ["workflow_step_instance.id"],
        ),
        sa.PrimaryKeyConstraint("predecessor_step_id", "successor_step_id"),
    )
    op.create_table(
        "budget_line_item",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("line_description", sa.String(), nullable=True),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("agreement_id", sa.Integer(), nullable=True),
        sa.Column("can_id", sa.Integer(), nullable=True),
        sa.Column("services_component_id", sa.Integer(), nullable=True),
        sa.Column("clin_id", sa.Integer(), nullable=True),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "DRAFT",
                "PLANNED",
                "IN_EXECUTION",
                "OBLIGATED",
                name="budgetlineitemstatus",
            ),
            nullable=True,
        ),
        sa.Column("date_needed", sa.Date(), nullable=True),
        sa.Column(
            "proc_shop_fee_percentage", sa.Numeric(precision=12, scale=5), nullable=True
        ),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["agreement_id"],
            ["agreement.id"],
        ),
        sa.ForeignKeyConstraint(
            ["can_id"],
            ["can.id"],
        ),
        sa.ForeignKeyConstraint(
            ["clin_id"],
            ["clin.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["services_component_id"],
            ["services_component.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "package_snapshot",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("package_id", sa.Integer(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.Column("bli_id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["bli_id"], ["budget_line_item.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["package_id"],
            ["package.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("package_snapshot")
    op.drop_table("budget_line_item")
    op.drop_table("workflow_step_dependency")
    op.drop_table("services_component")
    op.drop_table("contract_support_contacts")
    op.drop_table("workflow_step_instance")
    op.drop_table("step_approvers")
    op.drop_table("shared_portfolio_cans")
    op.drop_table("project_cans")
    op.drop_table("package")
    op.drop_table("iaa_agreement")
    op.drop_table("iaa_aa_agreement")
    op.drop_table("grant_agreement")
    op.drop_table("direct_agreement")
    op.drop_table("contract_agreement")
    op.drop_table("can_funding_sources")
    op.drop_table("can_fiscal_year_carry_forward")
    op.drop_table("can_fiscal_year")
    op.drop_table("agreement_team_members")
    op.drop_table("workflow_step_template")
    op.drop_table("workflow_instance")
    op.drop_table("vendor_contacts")
    op.drop_table("user_role")
    op.drop_table("user_group")
    op.drop_table("research_project")
    op.drop_table("project_team_leaders")
    op.drop_table("portfolio_url")
    op.drop_table("portfolio_team_leaders")
    op.drop_table("can")
    op.drop_table("agreement")
    op.drop_table("administrative_and_support_project")
    op.drop_table("workflow_template")
    op.drop_table("vendor")
    op.drop_index(op.f("ix_role_name"), table_name="role")
    op.drop_table("role")
    op.drop_table("project")
    op.drop_table("product_service_code")
    op.drop_table("procurement_shop")
    op.drop_table("portfolio")
    op.drop_table("ops_event")
    op.drop_index(
        "idx_ops_db_history_class_name_row_key_created_on", table_name="ops_db_history"
    )
    op.drop_table("ops_db_history")
    op.drop_table("notification")
    op.drop_index(op.f("ix_group_name"), table_name="group")
    op.drop_table("group")
    op.drop_table("funding_source")
    op.drop_table("funding_partner")
    op.drop_table("contact")
    op.drop_table("clin")
    op.drop_index(
        op.f("ix_workflow_template_version_transaction_id"),
        table_name="workflow_template_version",
    )
    op.drop_index(
        op.f("ix_workflow_template_version_operation_type"),
        table_name="workflow_template_version",
    )
    op.drop_index(
        op.f("ix_workflow_template_version_end_transaction_id"),
        table_name="workflow_template_version",
    )
    op.drop_table("workflow_template_version")
    op.drop_index(
        op.f("ix_workflow_step_template_version_transaction_id"),
        table_name="workflow_step_template_version",
    )
    op.drop_index(
        op.f("ix_workflow_step_template_version_operation_type"),
        table_name="workflow_step_template_version",
    )
    op.drop_index(
        op.f("ix_workflow_step_template_version_end_transaction_id"),
        table_name="workflow_step_template_version",
    )
    op.drop_table("workflow_step_template_version")
    op.drop_index(
        op.f("ix_workflow_step_instance_version_transaction_id"),
        table_name="workflow_step_instance_version",
    )
    op.drop_index(
        op.f("ix_workflow_step_instance_version_operation_type"),
        table_name="workflow_step_instance_version",
    )
    op.drop_index(
        op.f("ix_workflow_step_instance_version_end_transaction_id"),
        table_name="workflow_step_instance_version",
    )
    op.drop_table("workflow_step_instance_version")
    op.drop_index(
        op.f("ix_workflow_step_dependency_version_transaction_id"),
        table_name="workflow_step_dependency_version",
    )
    op.drop_index(
        op.f("ix_workflow_step_dependency_version_operation_type"),
        table_name="workflow_step_dependency_version",
    )
    op.drop_index(
        op.f("ix_workflow_step_dependency_version_end_transaction_id"),
        table_name="workflow_step_dependency_version",
    )
    op.drop_table("workflow_step_dependency_version")
    op.drop_index(
        op.f("ix_workflow_instance_version_transaction_id"),
        table_name="workflow_instance_version",
    )
    op.drop_index(
        op.f("ix_workflow_instance_version_operation_type"),
        table_name="workflow_instance_version",
    )
    op.drop_index(
        op.f("ix_workflow_instance_version_end_transaction_id"),
        table_name="workflow_instance_version",
    )
    op.drop_table("workflow_instance_version")
    op.drop_index(op.f("ix_vendor_version_transaction_id"), table_name="vendor_version")
    op.drop_index(op.f("ix_vendor_version_operation_type"), table_name="vendor_version")
    op.drop_index(
        op.f("ix_vendor_version_end_transaction_id"), table_name="vendor_version"
    )
    op.drop_table("vendor_version")
    op.drop_index(
        op.f("ix_vendor_contacts_version_transaction_id"),
        table_name="vendor_contacts_version",
    )
    op.drop_index(
        op.f("ix_vendor_contacts_version_operation_type"),
        table_name="vendor_contacts_version",
    )
    op.drop_index(
        op.f("ix_vendor_contacts_version_end_transaction_id"),
        table_name="vendor_contacts_version",
    )
    op.drop_table("vendor_contacts_version")
    op.drop_index(op.f("ix_user_version_transaction_id"), table_name="user_version")
    op.drop_index(op.f("ix_user_version_operation_type"), table_name="user_version")
    op.drop_index(op.f("ix_user_version_oidc_id"), table_name="user_version")
    op.drop_index(op.f("ix_user_version_end_transaction_id"), table_name="user_version")
    op.drop_index(op.f("ix_user_version_email"), table_name="user_version")
    op.drop_table("user_version")
    op.drop_index(
        op.f("ix_user_role_version_transaction_id"), table_name="user_role_version"
    )
    op.drop_index(
        op.f("ix_user_role_version_operation_type"), table_name="user_role_version"
    )
    op.drop_index(
        op.f("ix_user_role_version_end_transaction_id"), table_name="user_role_version"
    )
    op.drop_table("user_role_version")
    op.drop_index(
        op.f("ix_user_group_version_transaction_id"), table_name="user_group_version"
    )
    op.drop_index(
        op.f("ix_user_group_version_operation_type"), table_name="user_group_version"
    )
    op.drop_index(
        op.f("ix_user_group_version_end_transaction_id"),
        table_name="user_group_version",
    )
    op.drop_table("user_group_version")
    op.drop_index(op.f("ix_user_oidc_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_table("transaction")
    op.drop_index(
        op.f("ix_step_approvers_version_transaction_id"),
        table_name="step_approvers_version",
    )
    op.drop_index(
        op.f("ix_step_approvers_version_operation_type"),
        table_name="step_approvers_version",
    )
    op.drop_index(
        op.f("ix_step_approvers_version_end_transaction_id"),
        table_name="step_approvers_version",
    )
    op.drop_table("step_approvers_version")
    op.drop_index(
        op.f("ix_shared_portfolio_cans_version_transaction_id"),
        table_name="shared_portfolio_cans_version",
    )
    op.drop_index(
        op.f("ix_shared_portfolio_cans_version_operation_type"),
        table_name="shared_portfolio_cans_version",
    )
    op.drop_index(
        op.f("ix_shared_portfolio_cans_version_end_transaction_id"),
        table_name="shared_portfolio_cans_version",
    )
    op.drop_table("shared_portfolio_cans_version")
    op.drop_index(
        op.f("ix_services_component_version_transaction_id"),
        table_name="services_component_version",
    )
    op.drop_index(
        op.f("ix_services_component_version_operation_type"),
        table_name="services_component_version",
    )
    op.drop_index(
        op.f("ix_services_component_version_end_transaction_id"),
        table_name="services_component_version",
    )
    op.drop_table("services_component_version")
    op.drop_index(op.f("ix_role_version_transaction_id"), table_name="role_version")
    op.drop_index(op.f("ix_role_version_operation_type"), table_name="role_version")
    op.drop_index(op.f("ix_role_version_name"), table_name="role_version")
    op.drop_index(op.f("ix_role_version_end_transaction_id"), table_name="role_version")
    op.drop_table("role_version")
    op.drop_index(
        op.f("ix_research_project_version_transaction_id"),
        table_name="research_project_version",
    )
    op.drop_index(
        op.f("ix_research_project_version_operation_type"),
        table_name="research_project_version",
    )
    op.drop_index(
        op.f("ix_research_project_version_end_transaction_id"),
        table_name="research_project_version",
    )
    op.drop_table("research_project_version")
    op.drop_index(
        op.f("ix_project_version_transaction_id"), table_name="project_version"
    )
    op.drop_index(
        op.f("ix_project_version_operation_type"), table_name="project_version"
    )
    op.drop_index(
        op.f("ix_project_version_end_transaction_id"), table_name="project_version"
    )
    op.drop_table("project_version")
    op.drop_index(
        op.f("ix_project_team_leaders_version_transaction_id"),
        table_name="project_team_leaders_version",
    )
    op.drop_index(
        op.f("ix_project_team_leaders_version_operation_type"),
        table_name="project_team_leaders_version",
    )
    op.drop_index(
        op.f("ix_project_team_leaders_version_end_transaction_id"),
        table_name="project_team_leaders_version",
    )
    op.drop_table("project_team_leaders_version")
    op.drop_index(
        op.f("ix_project_cans_version_transaction_id"),
        table_name="project_cans_version",
    )
    op.drop_index(
        op.f("ix_project_cans_version_operation_type"),
        table_name="project_cans_version",
    )
    op.drop_index(
        op.f("ix_project_cans_version_end_transaction_id"),
        table_name="project_cans_version",
    )
    op.drop_table("project_cans_version")
    op.drop_index(
        op.f("ix_product_service_code_version_transaction_id"),
        table_name="product_service_code_version",
    )
    op.drop_index(
        op.f("ix_product_service_code_version_operation_type"),
        table_name="product_service_code_version",
    )
    op.drop_index(
        op.f("ix_product_service_code_version_end_transaction_id"),
        table_name="product_service_code_version",
    )
    op.drop_table("product_service_code_version")
    op.drop_index(
        op.f("ix_procurement_shop_version_transaction_id"),
        table_name="procurement_shop_version",
    )
    op.drop_index(
        op.f("ix_procurement_shop_version_operation_type"),
        table_name="procurement_shop_version",
    )
    op.drop_index(
        op.f("ix_procurement_shop_version_end_transaction_id"),
        table_name="procurement_shop_version",
    )
    op.drop_table("procurement_shop_version")
    op.drop_index(
        op.f("ix_portfolio_version_transaction_id"), table_name="portfolio_version"
    )
    op.drop_index(
        op.f("ix_portfolio_version_operation_type"), table_name="portfolio_version"
    )
    op.drop_index(
        op.f("ix_portfolio_version_end_transaction_id"), table_name="portfolio_version"
    )
    op.drop_table("portfolio_version")
    op.drop_index(
        op.f("ix_portfolio_url_version_transaction_id"),
        table_name="portfolio_url_version",
    )
    op.drop_index(
        op.f("ix_portfolio_url_version_operation_type"),
        table_name="portfolio_url_version",
    )
    op.drop_index(
        op.f("ix_portfolio_url_version_end_transaction_id"),
        table_name="portfolio_url_version",
    )
    op.drop_table("portfolio_url_version")
    op.drop_index(
        op.f("ix_portfolio_team_leaders_version_transaction_id"),
        table_name="portfolio_team_leaders_version",
    )
    op.drop_index(
        op.f("ix_portfolio_team_leaders_version_operation_type"),
        table_name="portfolio_team_leaders_version",
    )
    op.drop_index(
        op.f("ix_portfolio_team_leaders_version_end_transaction_id"),
        table_name="portfolio_team_leaders_version",
    )
    op.drop_table("portfolio_team_leaders_version")
    op.drop_index(
        op.f("ix_package_version_transaction_id"), table_name="package_version"
    )
    op.drop_index(
        op.f("ix_package_version_operation_type"), table_name="package_version"
    )
    op.drop_index(
        op.f("ix_package_version_end_transaction_id"), table_name="package_version"
    )
    op.drop_table("package_version")
    op.drop_index(
        op.f("ix_package_snapshot_version_transaction_id"),
        table_name="package_snapshot_version",
    )
    op.drop_index(
        op.f("ix_package_snapshot_version_operation_type"),
        table_name="package_snapshot_version",
    )
    op.drop_index(
        op.f("ix_package_snapshot_version_end_transaction_id"),
        table_name="package_snapshot_version",
    )
    op.drop_table("package_snapshot_version")
    op.drop_index(
        op.f("ix_ops_event_version_transaction_id"), table_name="ops_event_version"
    )
    op.drop_index(
        op.f("ix_ops_event_version_operation_type"), table_name="ops_event_version"
    )
    op.drop_index(
        op.f("ix_ops_event_version_end_transaction_id"), table_name="ops_event_version"
    )
    op.drop_table("ops_event_version")
    op.drop_index(
        op.f("ix_ops_db_history_version_transaction_id"),
        table_name="ops_db_history_version",
    )
    op.drop_index(
        op.f("ix_ops_db_history_version_operation_type"),
        table_name="ops_db_history_version",
    )
    op.drop_index(
        op.f("ix_ops_db_history_version_end_transaction_id"),
        table_name="ops_db_history_version",
    )
    op.drop_table("ops_db_history_version")
    op.drop_index(
        op.f("ix_notification_version_transaction_id"),
        table_name="notification_version",
    )
    op.drop_index(
        op.f("ix_notification_version_operation_type"),
        table_name="notification_version",
    )
    op.drop_index(
        op.f("ix_notification_version_end_transaction_id"),
        table_name="notification_version",
    )
    op.drop_table("notification_version")
    op.drop_index(
        op.f("ix_iaa_agreement_version_transaction_id"),
        table_name="iaa_agreement_version",
    )
    op.drop_index(
        op.f("ix_iaa_agreement_version_operation_type"),
        table_name="iaa_agreement_version",
    )
    op.drop_index(
        op.f("ix_iaa_agreement_version_end_transaction_id"),
        table_name="iaa_agreement_version",
    )
    op.drop_table("iaa_agreement_version")
    op.drop_index(
        op.f("ix_iaa_aa_agreement_version_transaction_id"),
        table_name="iaa_aa_agreement_version",
    )
    op.drop_index(
        op.f("ix_iaa_aa_agreement_version_operation_type"),
        table_name="iaa_aa_agreement_version",
    )
    op.drop_index(
        op.f("ix_iaa_aa_agreement_version_end_transaction_id"),
        table_name="iaa_aa_agreement_version",
    )
    op.drop_table("iaa_aa_agreement_version")
    op.drop_index(op.f("ix_group_version_transaction_id"), table_name="group_version")
    op.drop_index(op.f("ix_group_version_operation_type"), table_name="group_version")
    op.drop_index(op.f("ix_group_version_name"), table_name="group_version")
    op.drop_index(
        op.f("ix_group_version_end_transaction_id"), table_name="group_version"
    )
    op.drop_table("group_version")
    op.drop_index(
        op.f("ix_grant_agreement_version_transaction_id"),
        table_name="grant_agreement_version",
    )
    op.drop_index(
        op.f("ix_grant_agreement_version_operation_type"),
        table_name="grant_agreement_version",
    )
    op.drop_index(
        op.f("ix_grant_agreement_version_end_transaction_id"),
        table_name="grant_agreement_version",
    )
    op.drop_table("grant_agreement_version")
    op.drop_index(
        op.f("ix_funding_source_version_transaction_id"),
        table_name="funding_source_version",
    )
    op.drop_index(
        op.f("ix_funding_source_version_operation_type"),
        table_name="funding_source_version",
    )
    op.drop_index(
        op.f("ix_funding_source_version_end_transaction_id"),
        table_name="funding_source_version",
    )
    op.drop_table("funding_source_version")
    op.drop_index(
        op.f("ix_funding_partner_version_transaction_id"),
        table_name="funding_partner_version",
    )
    op.drop_index(
        op.f("ix_funding_partner_version_operation_type"),
        table_name="funding_partner_version",
    )
    op.drop_index(
        op.f("ix_funding_partner_version_end_transaction_id"),
        table_name="funding_partner_version",
    )
    op.drop_table("funding_partner_version")
    op.drop_index(
        op.f("ix_division_version_transaction_id"), table_name="division_version"
    )
    op.drop_index(
        op.f("ix_division_version_operation_type"), table_name="division_version"
    )
    op.drop_index(
        op.f("ix_division_version_end_transaction_id"), table_name="division_version"
    )
    op.drop_table("division_version")
    op.drop_table("division")
    op.drop_index(
        op.f("ix_direct_agreement_version_transaction_id"),
        table_name="direct_agreement_version",
    )
    op.drop_index(
        op.f("ix_direct_agreement_version_operation_type"),
        table_name="direct_agreement_version",
    )
    op.drop_index(
        op.f("ix_direct_agreement_version_end_transaction_id"),
        table_name="direct_agreement_version",
    )
    op.drop_table("direct_agreement_version")
    op.drop_index(
        op.f("ix_contract_support_contacts_version_transaction_id"),
        table_name="contract_support_contacts_version",
    )
    op.drop_index(
        op.f("ix_contract_support_contacts_version_operation_type"),
        table_name="contract_support_contacts_version",
    )
    op.drop_index(
        op.f("ix_contract_support_contacts_version_end_transaction_id"),
        table_name="contract_support_contacts_version",
    )
    op.drop_table("contract_support_contacts_version")
    op.drop_index(
        op.f("ix_contract_agreement_version_transaction_id"),
        table_name="contract_agreement_version",
    )
    op.drop_index(
        op.f("ix_contract_agreement_version_operation_type"),
        table_name="contract_agreement_version",
    )
    op.drop_index(
        op.f("ix_contract_agreement_version_end_transaction_id"),
        table_name="contract_agreement_version",
    )
    op.drop_table("contract_agreement_version")
    op.drop_index(
        op.f("ix_contact_version_transaction_id"), table_name="contact_version"
    )
    op.drop_index(
        op.f("ix_contact_version_operation_type"), table_name="contact_version"
    )
    op.drop_index(
        op.f("ix_contact_version_end_transaction_id"), table_name="contact_version"
    )
    op.drop_table("contact_version")
    op.drop_index(op.f("ix_clin_version_transaction_id"), table_name="clin_version")
    op.drop_index(op.f("ix_clin_version_operation_type"), table_name="clin_version")
    op.drop_index(op.f("ix_clin_version_end_transaction_id"), table_name="clin_version")
    op.drop_table("clin_version")
    op.drop_index(op.f("ix_can_version_transaction_id"), table_name="can_version")
    op.drop_index(op.f("ix_can_version_operation_type"), table_name="can_version")
    op.drop_index(op.f("ix_can_version_end_transaction_id"), table_name="can_version")
    op.drop_table("can_version")
    op.drop_index(
        op.f("ix_can_funding_sources_version_transaction_id"),
        table_name="can_funding_sources_version",
    )
    op.drop_index(
        op.f("ix_can_funding_sources_version_operation_type"),
        table_name="can_funding_sources_version",
    )
    op.drop_index(
        op.f("ix_can_funding_sources_version_end_transaction_id"),
        table_name="can_funding_sources_version",
    )
    op.drop_table("can_funding_sources_version")
    op.drop_index(
        op.f("ix_can_fiscal_year_version_transaction_id"),
        table_name="can_fiscal_year_version",
    )
    op.drop_index(
        op.f("ix_can_fiscal_year_version_operation_type"),
        table_name="can_fiscal_year_version",
    )
    op.drop_index(
        op.f("ix_can_fiscal_year_version_end_transaction_id"),
        table_name="can_fiscal_year_version",
    )
    op.drop_table("can_fiscal_year_version")
    op.drop_index(
        op.f("ix_can_fiscal_year_carry_forward_version_transaction_id"),
        table_name="can_fiscal_year_carry_forward_version",
    )
    op.drop_index(
        op.f("ix_can_fiscal_year_carry_forward_version_operation_type"),
        table_name="can_fiscal_year_carry_forward_version",
    )
    op.drop_index(
        op.f("ix_can_fiscal_year_carry_forward_version_end_transaction_id"),
        table_name="can_fiscal_year_carry_forward_version",
    )
    op.drop_table("can_fiscal_year_carry_forward_version")
    op.drop_index(
        op.f("ix_budget_line_item_version_transaction_id"),
        table_name="budget_line_item_version",
    )
    op.drop_index(
        op.f("ix_budget_line_item_version_operation_type"),
        table_name="budget_line_item_version",
    )
    op.drop_index(
        op.f("ix_budget_line_item_version_end_transaction_id"),
        table_name="budget_line_item_version",
    )
    op.drop_table("budget_line_item_version")
    op.drop_index(
        op.f("ix_agreement_version_transaction_id"), table_name="agreement_version"
    )
    op.drop_index(
        op.f("ix_agreement_version_operation_type"), table_name="agreement_version"
    )
    op.drop_index(
        op.f("ix_agreement_version_end_transaction_id"), table_name="agreement_version"
    )
    op.drop_table("agreement_version")
    op.drop_index(
        op.f("ix_agreement_team_members_version_transaction_id"),
        table_name="agreement_team_members_version",
    )
    op.drop_index(
        op.f("ix_agreement_team_members_version_operation_type"),
        table_name="agreement_team_members_version",
    )
    op.drop_index(
        op.f("ix_agreement_team_members_version_end_transaction_id"),
        table_name="agreement_team_members_version",
    )
    op.drop_table("agreement_team_members_version")
    op.drop_index(
        op.f("ix_administrative_and_support_project_version_transaction_id"),
        table_name="administrative_and_support_project_version",
    )
    op.drop_index(
        op.f("ix_administrative_and_support_project_version_operation_type"),
        table_name="administrative_and_support_project_version",
    )
    op.drop_index(
        op.f("ix_administrative_and_support_project_version_end_transaction_id"),
        table_name="administrative_and_support_project_version",
    )
    op.drop_table("administrative_and_support_project_version")
    # ### end Alembic commands ###
