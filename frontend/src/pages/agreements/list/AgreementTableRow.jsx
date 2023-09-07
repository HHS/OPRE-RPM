import { Fragment, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import { useDispatch, useSelector } from "react-redux";
import CurrencyFormat from "react-currency-format";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronDown, faChevronUp, faPen, faTrash } from "@fortawesome/free-solid-svg-icons";
import { faClock } from "@fortawesome/free-regular-svg-icons";
import { convertCodeForDisplay, formatDate } from "../../../helpers/utils";
import TableTag from "../../../components/UI/TableTag";
import { useDeleteAgreementMutation } from "../../../api/opsAPI";
import { setAlert } from "../../../components/UI/Alert/alertSlice";
import icons from "../../../uswds/img/sprite.svg";
import ConfirmationModal from "../../../components/UI/Modals/ConfirmationModal";
import useGetUserFullNameFromId from "../../../helpers/useGetUserFullNameFromId";

/**
 * Renders a row in the agreements table.
 *
 * @param {Object} props - The component props.
 * @param {Object} props.agreement - The agreement object to display.
 * @returns {React.JSX.Element} - The rendered component.
 */
export const AgreementTableRow = ({ agreement }) => {
    const navigate = useNavigate();
    const globalDispatch = useDispatch();
    const loggedInUserId = useSelector((state) => state.auth.activeUser.id);
    const [deleteAgreement] = useDeleteAgreementMutation();
    const [isExpanded, setIsExpanded] = useState(false);
    const [isRowActive, setIsRowActive] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [modalProps, setModalProps] = useState({});

    const agreementName = agreement?.name;
    const researchProjectName = agreement?.research_project?.title;

    let agreementType;
    agreementType = convertCodeForDisplay("agreementType", agreement?.agreement_type);

    const agreementSubTotal = agreement?.budget_line_items?.reduce((n, { amount }) => n + amount, 0);
    const procurementShopSubTotal = agreement?.budget_line_items?.reduce(
        (n, { amount }) => n + amount * (agreement.procurement_shop ? agreement.procurement_shop.fee : 0),
        0
    );
    const agreementTotal = agreementSubTotal + procurementShopSubTotal;

    // find the min(date_needed) of the BLIs
    let nextNeedBy = agreement?.budget_line_items?.reduce(
        (n, { date_needed }) => (n < date_needed ? n : date_needed),
        0
    );

    nextNeedBy = nextNeedBy ? formatDate(new Date(nextNeedBy)) : "";
    const agreementCreatedBy = useGetUserFullNameFromId(agreement?.created_by);
    const agreementNotes = agreement?.notes;
    const formatted_today = new Date().toLocaleString("en-US", { month: "long", day: "numeric", year: "numeric" });
    const agreementCreatedOn = agreement?.created_on
        ? new Date(agreement.created_on).toLocaleString("en-US", { month: "long", day: "numeric", year: "numeric" })
        : formatted_today;

    const handleExpandRow = () => {
        setIsExpanded(!isExpanded);
        setIsRowActive(true);
    };
    // styles for the expanded row
    const removeBorderBottomIfExpanded = isExpanded ? "border-bottom-none" : undefined;
    const changeBgColorIfExpanded = { backgroundColor: isRowActive ? "var(--neutral-lightest)" : undefined };

    // Validations for deleting an agreement
    const isLoggedInUserTheProjectOfficer = loggedInUserId === agreement?.project_officer;
    const isLoggedInUserTheAgreementCreator = loggedInUserId === agreement?.created_by;
    const isLoggedInUserATeamMember = agreement?.team_members?.find((tm) => tm.id === loggedInUserId);
    const areAllBudgetLinesInDraftStatus = agreement?.budget_line_items?.every((bli) => bli.status === "DRAFT");
    const areThereAnyBudgetLines = agreement?.budget_line_items?.length > 0;

    const canUserDeleteAgreement =
        (isLoggedInUserTheAgreementCreator || isLoggedInUserTheProjectOfficer || isLoggedInUserATeamMember) &&
        (areAllBudgetLinesInDraftStatus || !areThereAnyBudgetLines);

    const handleEditAgreement = (event) => {
        navigate(`/agreements/${event}?mode=edit`);
    };

    /**
     * Deletes an agreement.
     * @param {number} id - The id of the agreement to delete.
     * @returns {void}
     */
    const handleDeleteAgreement = (id) => {
        setShowModal(true);
        setModalProps({
            heading: "Are you sure you want to delete this agreement?",
            actionButtonText: "Delete",
            handleConfirm: () => {
                deleteAgreement(id)
                    .unwrap()
                    .then((fulfilled) => {
                        console.log(`DELETE agreement success: ${JSON.stringify(fulfilled, null, 2)}`);
                        globalDispatch(
                            setAlert({
                                type: "success",
                                heading: "Agreement deleted",
                                message: `Agreement ${agreementName} has been successfully deleted.`,
                            })
                        );
                    })
                    .catch((rejected) => {
                        console.error(`DELETE agreement rejected: ${JSON.stringify(rejected, null, 2)}`);
                        globalDispatch(
                            setAlert({
                                type: "error",
                                heading: "Error",
                                message: "An error occurred while deleting the agreement.",
                            })
                        );
                        navigate("/error");
                    });
            },
        });
    };
    const handleSubmitAgreementForApproval = (event) => {
        navigate(`/agreements/approve/${event}`);
    };

    const agreementStatus = agreement?.budget_line_items?.find((bli) => bli.status === "UNDER_REVIEW")
        ? "In Review"
        : "Draft";

    /**
     * Renders the edit, delete, and submit for approval icons.
     *
     * @param {Object} props - The component props.
     * @param {Object} props.agreement - The agreement object to display.
     * @param {string} props.status - The status of the agreement.
     * @returns {React.JSX.Element} - The rendered component.
     */
    const ChangeIcons = ({ agreement, status }) => {
        return (
            <>
                {(status === "Draft" || status === "In Review") && (
                    <div className="display-flex flex-align-center">
                        <FontAwesomeIcon
                            icon={faPen}
                            className="text-primary height-2 width-2 margin-right-1 cursor-pointer usa-tooltip"
                            title="edit"
                            data-position="top"
                            onClick={() => handleEditAgreement(agreement.id)}
                        />

                        <FontAwesomeIcon
                            icon={faTrash}
                            title={`${canUserDeleteAgreement ? "delete" : "user does not have permissions to delete"}`}
                            data-position="top"
                            className={`text-primary height-2 width-2 margin-right-1 cursor-pointer usa-tooltip ${
                                !canUserDeleteAgreement ? "opacity-30 cursor-not-allowed" : null
                            }`}
                            onClick={() => canUserDeleteAgreement && handleDeleteAgreement(agreement.id)}
                            data-cy="delete-agreement"
                        />

                        <svg
                            className="usa-icon text-primary height-205 width-205 cursor-pointer usa-tooltip"
                            onClick={() => handleSubmitAgreementForApproval(agreement.id)}
                            id={`submit-for-approval-${agreement.id}`}
                        >
                            <use xlinkHref={`${icons}#send`}></use>
                        </svg>
                    </div>
                )}
            </>
        );
    };
    return (
        <Fragment key={agreement?.id}>
            {showModal && (
                <ConfirmationModal
                    heading={modalProps.heading}
                    setShowModal={setShowModal}
                    actionButtonText={modalProps.actionButtonText}
                    handleConfirm={modalProps.handleConfirm}
                />
            )}
            <tr onMouseEnter={() => setIsRowActive(true)} onMouseLeave={() => !isExpanded && setIsRowActive(false)}>
                <th scope="row" className={removeBorderBottomIfExpanded} style={changeBgColorIfExpanded}>
                    <Link className="text-ink text-no-underline" to={"/agreements/" + agreement.id}>
                        {agreementName}
                    </Link>
                </th>
                <td className={removeBorderBottomIfExpanded} style={changeBgColorIfExpanded}>
                    {researchProjectName}
                </td>
                <td className={removeBorderBottomIfExpanded} style={changeBgColorIfExpanded}>
                    {agreementType || ""}
                </td>
                <td className={removeBorderBottomIfExpanded} style={changeBgColorIfExpanded}>
                    <CurrencyFormat
                        value={agreementTotal}
                        displayType={"text"}
                        thousandSeparator={true}
                        prefix={"$"}
                        decimalScale={2}
                        fixedDecimalScale={true}
                        renderText={(value) => value}
                    />
                </td>
                <td className={removeBorderBottomIfExpanded} style={changeBgColorIfExpanded}>
                    {nextNeedBy}
                </td>
                <td className={removeBorderBottomIfExpanded} style={changeBgColorIfExpanded}>
                    {isRowActive && !isExpanded ? (
                        <div>
                            <ChangeIcons agreement={agreement} status={agreementStatus} />
                        </div>
                    ) : (
                        <TableTag status={agreementStatus} />
                    )}
                </td>
                <td className={removeBorderBottomIfExpanded} style={changeBgColorIfExpanded}>
                    <FontAwesomeIcon
                        icon={isExpanded ? faChevronUp : faChevronDown}
                        className="height-2 width-2 padding-right-1 hover: cursor-pointer"
                        onClick={() => handleExpandRow()}
                        data-cy="expand-row"
                    />
                </td>
            </tr>

            {isExpanded && (
                <tr>
                    <td colSpan={9} className="border-top-none" style={{ backgroundColor: "var(--neutral-lightest)" }}>
                        <div className="display-flex padding-right-9">
                            <dl className="font-12px">
                                <dt className="margin-0 text-base-dark">Created By</dt>
                                <dd className="margin-0">{agreementCreatedBy}</dd>
                                <dt className="margin-0 text-base-dark display-flex flex-align-center margin-top-2">
                                    <FontAwesomeIcon icon={faClock} className="height-2 width-2 margin-right-1" />
                                    {agreementCreatedOn}
                                </dt>
                            </dl>
                            <dl className="font-12px" style={{ marginLeft: "9.0625rem" }}>
                                <dt className="margin-0 text-base-dark">Notes</dt>
                                <dd className="margin-0" style={{ maxWidth: "400px" }}>
                                    {agreementNotes ? agreementNotes : "No notes added."}
                                </dd>
                            </dl>
                            <div className="flex-align-self-end margin-left-auto margin-bottom-1">
                                <ChangeIcons agreement={agreement} status={agreementStatus} />
                            </div>
                        </div>
                    </td>
                </tr>
            )}
        </Fragment>
    );
};

AgreementTableRow.propTypes = {
    agreement: PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        research_project: PropTypes.shape({
            title: PropTypes.string.isRequired,
        }),
        agreement_type: PropTypes.string.isRequired,
        budget_line_items: PropTypes.arrayOf(
            PropTypes.shape({
                amount: PropTypes.number.isRequired,
                date_needed: PropTypes.string.isRequired,
                status: PropTypes.string.isRequired,
            })
        ).isRequired,
        procurement_shop: PropTypes.shape({
            fee: PropTypes.number.isRequired,
        }),
        created_by: PropTypes.number.isRequired,
        notes: PropTypes.string,
        created_on: PropTypes.string,
        project_officer: PropTypes.number.isRequired,
        team_members: PropTypes.arrayOf(
            PropTypes.shape({
                id: PropTypes.number.isRequired,
            })
        ).isRequired,
    }).isRequired,
};
