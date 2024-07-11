import App from "../../../App";
import AgreementBLIAccordion from "../../../components/Agreements/AgreementBLIAccordion";
import AgreementCANReviewAccordion from "../../../components/Agreements/AgreementCANReviewAccordion";
import AgreementChangesAccordion from "../../../components/Agreements/AgreementChangesAccordion";
import AgreementMetaAccordion from "../../../components/Agreements/AgreementMetaAccordion";
import BudgetLinesTable from "../../../components/BudgetLineItems/BudgetLinesTable";
import ReviewChangeRequestAccordion from "../../../components/ChangeRequests/ReviewChangeRequestAccordion";
import ServicesComponentAccordion from "../../../components/ServicesComponents/ServicesComponentAccordion";
import TextArea from "../../../components/UI/Form/TextArea";
import ConfirmationModal from "../../../components/UI/Modals/ConfirmationModal";
import PageHeader from "../../../components/UI/PageHeader";
import { BLI_STATUS } from "../../../helpers/budgetLines.helpers";
import { findDescription, findPeriodEnd, findPeriodStart } from "../../../helpers/servicesComponent.helpers";
import { convertCodeForDisplay } from "../../../helpers/utils";
import useApproveAgreement from "./ApproveAgreement.hooks";

const ApproveAgreement = () => {
    const {
        agreement,
        projectOfficerName,
        servicesComponents,
        groupedBudgetLinesByServicesComponent,
        budgetLinesInReview,
        changeRequestsInReview,
        changeInCans,
        notes,
        setNotes,
        confirmation,
        setConfirmation,
        showModal,
        setShowModal,
        modalProps,
        checkBoxText,
        handleCancel,
        handleDecline,
        handleApprove,
        title,
        changeRequestTitle,
        afterApproval,
        setAfterApproval,
        submittersNotes,
        changeToStatus,
        statusForTitle
    } = useApproveAgreement();

    if (!agreement) {
        return <div>Loading...</div>;
    }

    return (
        <App breadCrumbName={`Approve BLI ${changeRequestTitle} ${statusForTitle}`}>
            {showModal && (
                <ConfirmationModal
                    heading={modalProps.heading}
                    setShowModal={setShowModal}
                    actionButtonText={modalProps.actionButtonText}
                    handleConfirm={modalProps.handleConfirm}
                    secondaryButtonText={modalProps.secondaryButtonText}
                />
            )}
            <PageHeader
                title={title}
                subTitle={agreement.name}
            />
            <ReviewChangeRequestAccordion
                changeType={changeRequestTitle}
                changeRequests={changeRequestsInReview}
                statusChangeTo={changeToStatus}
            />
            <AgreementMetaAccordion
                instructions="Please review the agreement details below to ensure all information is correct."
                agreement={agreement}
                projectOfficerName={projectOfficerName}
                convertCodeForDisplay={convertCodeForDisplay}
            />

            <AgreementBLIAccordion
                title="Review Budget Lines"
                instructions="This is a list of all budget lines within this agreement.  Changes are displayed with a blue underline. Use the toggle to see how your approval would change the budget lines."
                budgetLineItems={budgetLinesInReview}
                agreement={agreement}
                afterApproval={afterApproval}
                setAfterApproval={setAfterApproval}
                action={changeToStatus}
            >
                <section className="margin-top-4">
                    {groupedBudgetLinesByServicesComponent.map((group) => (
                        <ServicesComponentAccordion
                            key={group.servicesComponentId}
                            servicesComponentId={group.servicesComponentId}
                            withMetadata={true}
                            periodStart={findPeriodStart(servicesComponents, group.servicesComponentId)}
                            periodEnd={findPeriodEnd(servicesComponents, group.servicesComponentId)}
                            description={findDescription(servicesComponents, group.servicesComponentId)}
                        >
                            <BudgetLinesTable
                                budgetLines={group.budgetLines}
                                readOnly={true}
                            />
                        </ServicesComponentAccordion>
                    ))}
                </section>
            </AgreementBLIAccordion>
            <AgreementCANReviewAccordion
                instructions="The budget lines showing In Review Status have allocated funds from the CANs displayed below."
                selectedBudgetLines={budgetLinesInReview}
                afterApproval={afterApproval}
                setAfterApproval={setAfterApproval}
                action={changeToStatus}
            />
            {changeToStatus === BLI_STATUS.PLANNED && (
                <AgreementChangesAccordion
                    changeInBudgetLines={budgetLinesInReview.reduce((acc, { amount }) => acc + amount, 0)}
                    changeInCans={changeInCans}
                />
            )}
            <section>
                <h2 className="font-sans-lg text-semibold">Submitter&apos;s Notes</h2>
                <p
                    className="margin-top-3 text-semibold font-12px line-height-body-1"
                    style={{ maxWidth: "25rem" }}
                >
                    {submittersNotes}
                </p>
            </section>
            <section>
                <h2 className="font-sans-lg text-semibold margin-top-5">Reviewer&apos;s Notes</h2>
                <TextArea
                    name="submitter-notes"
                    label="Notes (optional)"
                    maxLength={150}
                    value={notes}
                    onChange={(name, value) => setNotes(value)}
                />
            </section>
            <div className="usa-checkbox padding-bottom-105 margin-top-4">
                <input
                    className="usa-checkbox__input"
                    id="approve-confirmation"
                    type="checkbox"
                    name="approve-confirmation"
                    value="approve-confirmation"
                    checked={confirmation}
                    onChange={() => setConfirmation(!confirmation)}
                />
                <label
                    className="usa-checkbox__label"
                    htmlFor="approve-confirmation"
                >
                    {checkBoxText}
                </label>
            </div>
            <div className="grid-row flex-justify-end flex-align-center margin-top-8">
                <button
                    name="cancel"
                    className={`usa-button usa-button--unstyled margin-right-2`}
                    data-cy="cancel-approval-btn"
                    onClick={handleCancel}
                >
                    Cancel
                </button>

                <button
                    className={`usa-button usa-button--outline margin-right-2`}
                    data-cy="decline-approval-btn"
                    onClick={handleDecline}
                >
                    Decline
                </button>
                <button
                    className="usa-button"
                    data-cy="send-to-approval-btn"
                    onClick={handleApprove}
                    disabled={!confirmation}
                >
                    Approve
                </button>
            </div>
        </App>
    );
};

export default ApproveAgreement;
