import React from "react";
import PropTypes from "prop-types";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faClock } from "@fortawesome/free-regular-svg-icons";
import CurrencyFormat from "react-currency-format";
import TableTag from "../../UI/TableTag";
import ChangeIcons from "../ChangeIcons";
import TableRowExpandable from "../../UI/TableRowExpandable";
import {
    fiscalYearFromDate,
    formatDateNeeded,
    formatDateToMonthDayYear,
    totalBudgetLineFeeAmount,
    totalBudgetLineAmountPlusFees
} from "../../../helpers/utils";
import useGetUserFullNameFromId from "../../../hooks/user.hooks";
import { useIsBudgetLineEditableByStatus, useIsBudgetLineCreator } from "../../../hooks/budget-line.hooks";
import { useIsUserAllowedToEditAgreement } from "../../../hooks/agreement.hooks";

/**
 * BLIRow component that represents a single row in the Budget Lines table.
 * @param {Object} props - The props for the BLIRow component.
 * @param {Object} props.bl - The budget line object.
 * @param {boolean} [props.isReviewMode] - Whether the user is in review mode.
 * @param {Function} [props.handleSetBudgetLineForEditing] - The function to set the budget line for editing.
 * @param {Function} [props.handleDeleteBudgetLine] - The function to delete the budget line.
 * @param {Function} [props.handleDuplicateBudgetLine] - The function to duplicate the budget line.
 * @param {boolean} [props.readOnly] - Whether the user is in read only mode.
 * @returns {React.JSX.Element} The BLIRow component.
 **/
const BLIRow = ({
    bl: budgetLine,
    isReviewMode = false,
    handleSetBudgetLineForEditing = () => {},
    handleDeleteBudgetLine = () => {},
    handleDuplicateBudgetLine = () => {},
    readOnly = false
}) => {
    const [isExpanded, setIsExpanded] = React.useState(false);
    const [isRowActive, setIsRowActive] = React.useState(false);
    const budgetLineCreatorName = useGetUserFullNameFromId(budgetLine?.created_by);
    let feeTotal = totalBudgetLineFeeAmount(budgetLine?.amount, budgetLine?.proc_shop_fee_percentage);
    let budgetLineTotalPlusFees = totalBudgetLineAmountPlusFees(budgetLine?.amount, feeTotal);
    const isBudgetLineEditableFromStatus = useIsBudgetLineEditableByStatus(budgetLine);
    const isUserBudgetLineCreator = useIsBudgetLineCreator(budgetLine);
    const canUserEditAgreement = useIsUserAllowedToEditAgreement(budgetLine?.agreement_id);
    const isBudgetLineEditable = (canUserEditAgreement || isUserBudgetLineCreator) && isBudgetLineEditableFromStatus;
    const changeIcons = (
        <ChangeIcons
            item={budgetLine}
            handleDeleteItem={handleDeleteBudgetLine}
            handleDuplicateItem={handleDuplicateBudgetLine}
            handleSetItemForEditing={handleSetBudgetLineForEditing}
            isItemEditable={isBudgetLineEditable}
            duplicateIcon={true}
        />
    );
    // styles for the table row
    const removeBorderBottomIfExpanded = isExpanded ? "border-bottom-none" : "";
    const changeBgColorIfExpanded = { backgroundColor: isExpanded && "var(--neutral-lightest)" };

    const addErrorClassIfNotFound = (item) => {
        if (isReviewMode && !item) {
            return "table-item-error";
        } else {
            return "";
        }
    };
    // error class for need_by_date to be in the future
    const futureDateErrorClass = (item) => {
        const today = new Date().valueOf();
        const dateNeeded = new Date(item).valueOf();

        if (isReviewMode && dateNeeded < today) {
            return "table-item-error";
        } else {
            return "";
        }
    };

    const TableRowData = (
        <>
            <th
                scope="row"
                className={`${addErrorClassIfNotFound(budgetLine?.line_description)} ${removeBorderBottomIfExpanded}`}
                style={changeBgColorIfExpanded}
            >
                {budgetLine?.line_description}
            </th>
            <td
                className={`${futureDateErrorClass(
                    formatDateNeeded(budgetLine?.date_needed)
                )} ${addErrorClassIfNotFound(
                    formatDateNeeded(budgetLine?.date_needed)
                )} ${removeBorderBottomIfExpanded}`}
                style={changeBgColorIfExpanded}
            >
                {formatDateNeeded(budgetLine?.date_needed)}
            </td>
            <td
                className={`${addErrorClassIfNotFound(
                    fiscalYearFromDate(budgetLine?.date_needed)
                )} ${removeBorderBottomIfExpanded}`}
                style={changeBgColorIfExpanded}
            >
                {fiscalYearFromDate(budgetLine?.date_needed)}
            </td>
            <td
                className={`${addErrorClassIfNotFound(budgetLine?.can?.number)} ${removeBorderBottomIfExpanded}`}
                style={changeBgColorIfExpanded}
            >
                {budgetLine?.can?.number}
            </td>
            <td
                className={`${addErrorClassIfNotFound(budgetLine?.amount)} ${removeBorderBottomIfExpanded}`}
                style={changeBgColorIfExpanded}
            >
                <CurrencyFormat
                    value={budgetLine?.amount || 0}
                    displayType={"text"}
                    thousandSeparator={true}
                    prefix={"$"}
                    decimalScale={2}
                    fixedDecimalScale={true}
                    renderText={(value) => value}
                />
            </td>
            <td
                className={removeBorderBottomIfExpanded}
                style={changeBgColorIfExpanded}
            >
                {feeTotal === 0 ? (
                    0
                ) : (
                    <CurrencyFormat
                        value={feeTotal}
                        displayType={"text"}
                        thousandSeparator={true}
                        prefix={"$"}
                        decimalScale={2}
                        fixedDecimalScale={true}
                        renderText={(value) => value}
                    />
                )}
            </td>
            <td
                className={removeBorderBottomIfExpanded}
                style={changeBgColorIfExpanded}
            >
                {budgetLineTotalPlusFees === 0 ? (
                    0
                ) : (
                    <CurrencyFormat
                        value={budgetLineTotalPlusFees}
                        displayType={"text"}
                        thousandSeparator={true}
                        prefix={"$"}
                        decimalScale={2}
                        fixedDecimalScale={true}
                        renderText={(value) => value}
                    />
                )}
            </td>
            <td
                className={removeBorderBottomIfExpanded}
                style={changeBgColorIfExpanded}
            >
                {isRowActive && !isExpanded && !readOnly ? (
                    <div>{changeIcons}</div>
                ) : (
                    <TableTag status={budgetLine.status} />
                )}
            </td>
        </>
    );

    const ExpandedData = (
        <>
            <td
                colSpan={9}
                className="border-top-none"
                style={{ backgroundColor: "var(--neutral-lightest)" }}
            >
                <div className="display-flex padding-right-9">
                    <dl className="font-12px">
                        <dt className="margin-0 text-base-dark">Created By</dt>
                        <dd
                            id={`created-by-name-${budgetLine?.id}`}
                            className="margin-0"
                        >
                            {budgetLineCreatorName}
                        </dd>
                        <dt className="margin-0 text-base-dark display-flex flex-align-center margin-top-2">
                            <FontAwesomeIcon
                                icon={faClock}
                                className="height-2 width-2 margin-right-1"
                            />
                            {formatDateToMonthDayYear(budgetLine?.created_on)}
                        </dt>
                    </dl>
                    <dl
                        className="font-12px"
                        style={{ marginLeft: "9.0625rem" }}
                    >
                        <dt className="margin-0 text-base-dark">Notes</dt>
                        <dd
                            className="margin-0"
                            style={{ maxWidth: "400px" }}
                        >
                            {budgetLine?.comments ? budgetLine.comments : "No notes added."}
                        </dd>
                    </dl>
                    <div className="flex-align-self-end margin-left-auto margin-bottom-1">
                        {!readOnly && changeIcons}
                    </div>
                </div>
            </td>
        </>
    );
    return (
        <TableRowExpandable
            tableRowData={TableRowData}
            expandedData={ExpandedData}
            isExpanded={isExpanded}
            isRowActive={isRowActive}
            setIsExpanded={setIsExpanded}
            setIsRowActive={setIsRowActive}
        />
    );
};

BLIRow.propTypes = {
    bl: PropTypes.object.isRequired,
    canUserEditBudgetLines: PropTypes.bool,
    isReviewMode: PropTypes.bool,
    handleSetBudgetLineForEditing: PropTypes.func,
    handleDeleteBudgetLine: PropTypes.func,
    handleDuplicateBudgetLine: PropTypes.func,
    readOnly: PropTypes.bool
};

export default BLIRow;
