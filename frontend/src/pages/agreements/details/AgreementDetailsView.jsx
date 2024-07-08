import PropTypes from "prop-types";
import AgreementHistoryPanel from "../../../components/Agreements/AgreementDetails/AgreementHistoryPanel";
import Tag from "../../../components/UI/Tag/Tag";
import { convertCodeForDisplay } from "../../../helpers/utils";

/**
 * Renders the details of an agreement
 * @component
 * @param {Object} props - The component props.
 * @param {Object} props.agreement - The agreement object to display details for.
 * @param {Object} props.projectOfficer - The project officer object for the agreement.
 * @returns {JSX.Element} - The rendered component.
 */
const AgreementDetailsView = ({ agreement, projectOfficer }) => {
    const MISSING_VALUE_TEXT = "TBD";

    return (
        <section>
            <div className="grid-row margin-top-2">
                <div
                    className="grid-col-6 padding-right-1"
                    data-cy="details-left-col"
                >
                    {/* // NOTE: Left Column */}
                    <dl className="margin-0 font-12px">
                        <dt className="margin-0 text-base-dark margin-top-3">Description</dt>
                        <dd className="margin-0 margin-top-05 text-semibold">
                            {agreement?.description ? agreement.description : MISSING_VALUE_TEXT}
                        </dd>
                    </dl>
                    <h3 className="text-base-dark margin-top-3 text-normal font-12px">Notes</h3>
                    {agreement.notes ? (
                        <div
                            className="font-12px overflow-y-scroll force-show-scrollbars"
                            style={{ height: "11.375rem" }}
                            data-cy="details-notes"
                            role="region"
                            aria-live="polite"
                            aria-label="Agreement Notes"
                        >
                            {agreement.notes}
                        </div>
                    ) : (
                        <p className="font-12px">There are currently no notes for this agreement.</p>
                    )}
                    <h3 className="text-base-dark margin-top-3 text-normal font-12px">History</h3>
                    <AgreementHistoryPanel agreementId={agreement.id} />
                </div>
                <div
                    className="grid-col-6 padding-left-2"
                    data-cy="details-right-col"
                >
                    {/* // NOTE: Right Column */}
                    <dl className="margin-0 font-12px">
                        <dt className="margin-0 text-base-dark margin-top-3">Agreement Type</dt>
                        <dd className="margin-0 margin-top-1">
                            <Tag
                                tagStyle="primaryDarkTextLightBackground"
                                text={convertCodeForDisplay("agreementType", agreement?.agreement_type)}
                            />
                        </dd>
                        <dt className="margin-0 text-base-dark margin-top-3">Product Service Code</dt>
                        <dd className="margin-0 margin-top-1">
                            <Tag
                                tagStyle="primaryDarkTextLightBackground"
                                text={
                                    agreement?.product_service_code?.name
                                        ? agreement.product_service_code.name
                                        : MISSING_VALUE_TEXT
                                }
                            />
                        </dd>
                    </dl>
                    <div className="display-flex">
                        <dl className="grid-col-4 margin-0 font-12px">
                            <dt className="margin-0 text-base-dark margin-top-3">NAICS Code</dt>
                            <dd className="margin-0 margin-top-1">
                                <Tag
                                    tagStyle="primaryDarkTextLightBackground"
                                    text={
                                        agreement?.product_service_code?.naics
                                            ? `${agreement.product_service_code.naics}`
                                            : MISSING_VALUE_TEXT
                                    }
                                />
                            </dd>
                        </dl>
                        <dl className="grid-col-4 margin-0 margin-left-2 font-12px">
                            <dt className="margin-0 text-base-dark margin-top-3">Program Support Code</dt>
                            <dd className="margin-0 margin-top-1">
                                <Tag
                                    tagStyle="primaryDarkTextLightBackground"
                                    text={
                                        agreement?.product_service_code?.support_code
                                            ? agreement?.product_service_code?.support_code
                                            : MISSING_VALUE_TEXT
                                    }
                                />
                            </dd>
                        </dl>
                    </div>
                    <dl className="margin-0 font-12px">
                        <dt className="margin-0 text-base-dark margin-top-3">Procurement Shop</dt>
                        <dd className="margin-0 margin-top-1">
                            <Tag
                                tagStyle="primaryDarkTextLightBackground"
                                text={`${agreement?.procurement_shop?.abbr} - Fee Rate: ${
                                    agreement?.procurement_shop?.fee * 100
                                }%`}
                            />
                        </dd>
                    </dl>
                    <div className="display-flex">
                        <dl className="grid-col-4 margin-0 font-12px">
                            <dt className="margin-0 text-base-dark margin-top-3">Agreement Reason</dt>
                            <dd className="margin-0 margin-top-1">
                                <Tag
                                    tagStyle="primaryDarkTextLightBackground"
                                    text={
                                        agreement?.agreement_reason
                                            ? convertCodeForDisplay("agreementReason", agreement?.agreement_reason)
                                            : MISSING_VALUE_TEXT
                                    }
                                />
                            </dd>
                        </dl>
                        {agreement?.incumbent && (
                            <dl className="grid-col-4 margin-0 margin-left-2 font-12px">
                                <dt className="margin-0 text-base-dark margin-top-3">Incumbent</dt>
                                <dd className="margin-0 margin-top-1">
                                    <Tag
                                        tagStyle="primaryDarkTextLightBackground"
                                        text={agreement?.incumbent}
                                    />
                                </dd>
                            </dl>
                        )}
                    </div>
                    <dl className="margin-0 font-12px">
                        <dt className="margin-0 text-base-dark margin-top-3">Project Officer</dt>
                        <dd className="margin-0 margin-top-1">
                            <Tag
                                tagStyle="primaryDarkTextLightBackground"
                                text={
                                    projectOfficer && Object.keys(projectOfficer).length !== 0
                                        ? projectOfficer?.full_name
                                        : MISSING_VALUE_TEXT
                                }
                            />
                        </dd>
                    </dl>
                    <dl className="margin-0 font-12px">
                        <dt className="margin-0 text-base-dark margin-top-3">Team Members</dt>
                        {agreement?.team_members?.length > 0 ? (
                            <>
                                {agreement?.team_members.map((member) => (
                                    <dd
                                        key={member.id}
                                        className="margin-0 margin-top-1 margin-bottom-2"
                                    >
                                        <Tag
                                            tagStyle="primaryDarkTextLightBackground"
                                            text={member.full_name}
                                        />
                                    </dd>
                                ))}
                            </>
                        ) : (
                            <dd className="margin-0 margin-top-1 margin-bottom-2">
                                <Tag
                                    tagStyle="primaryDarkTextLightBackground"
                                    text={MISSING_VALUE_TEXT}
                                />
                            </dd>
                        )}
                    </dl>
                </div>
            </div>
        </section>
    );
};

AgreementDetailsView.propTypes = {
    agreement: PropTypes.object.isRequired,
    projectOfficer: PropTypes.object
};

export default AgreementDetailsView;
