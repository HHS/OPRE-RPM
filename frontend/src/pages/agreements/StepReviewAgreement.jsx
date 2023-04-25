import { useSelector } from "react-redux";

export const StepReviewAgreement = () => {
    const selectedResearchProject = useSelector((state) => state.createAgreement.selected_project);
    const selectedAgreement = useSelector((state) => state.createAgreement.agreement);
    const { title } = selectedResearchProject;
    const {
        selected_agreement_type: agreementType,
        name: agreementName,
        description: agreementDescription,
        selected_product_service_code: productServiceCode,
        selected_agreement_reason: agreementReason,
        incumbent_entered: agreementIncumbent,
    } = selectedAgreement;
    const selectedProcurementShop = useSelector((state) => state.createAgreement.selected_procurement_shop);
    const { name: procurementShopName, fee } = selectedProcurementShop;
    const projectOfficer = useSelector((state) => state.createAgreement.agreement.project_officer.full_name);
    const teamMembers = useSelector((state) => state.createAgreement.agreement.team_members);
    const teamMembersFullNamesAndId = teamMembers.map((member) => {
        return { name: member.full_name, id: member.member_id };
    });

    // TODO: Replace with actual NAICS Code from Selected Product Service Code
    const NAICS_Code = "541690";
    const programSupportCode = "R410 - Research";
    return (
        <>
            <h1>Review and Send Agreement to Approval</h1>
            <p>
                Please review the agreement below or edit any information if necessary. Send to Approval will send the
                agreement to your Division Director to review for Planned Status.
            </p>
            <dl className="margin-0 padding-y-2 padding-x-105 font-12px">
                <dt className="margin-0 text-base-dark">Project</dt>
                <dd className="text-semibold margin-0">{title}</dd>
                <dt className="margin-0 text-base-dark">Agreement Type</dt>
                <dd className="text-semibold margin-0">{agreementType}</dd>
                <dt className="margin-0 text-base-dark">Agreement Name</dt>
                <dd className="text-semibold margin-0">{agreementName}</dd>
                <dt className="margin-0 text-base-dark">Description</dt>
                <dd className="text-semibold margin-0">{agreementDescription}</dd>
                <dt className="margin-0 text-base-dark">Product Service Code</dt>
                <dd className="text-semibold margin-0">{productServiceCode}</dd>
                <dt className="margin-0 text-base-dark">NAICS Code</dt>
                <dd className="text-semibold margin-0">{NAICS_Code}</dd>
                <dt className="margin-0 text-base-dark">Program Support Code</dt>
                <dd className="text-semibold margin-0">{programSupportCode}</dd>
                <dt className="margin-0 text-base-dark">Procurement Shop</dt>
                <dd className="text-semibold margin-0">{`${procurementShopName}-Fee Rate: ${fee}%`}</dd>
                <dt className="margin-0 text-base-dark">Reason for creating the agreement</dt>
                <dd className="text-semibold margin-0">{agreementReason}</dd>
                <dt className="margin-0 text-base-dark">Incumbent</dt>
                <dd className="text-semibold margin-0">{agreementIncumbent}</dd>
                <dt className="margin-0 text-base-dark">Project Officer</dt>
                <dd className="text-semibold margin-0">{projectOfficer}</dd>
                {teamMembersFullNamesAndId.length > 0 && (
                    <>
                        <dt className="margin-0 text-base-dark">Team Members</dt>
                        {teamMembersFullNamesAndId.map((member) => (
                            <dd key={member.id} className="text-semibold margin-0">
                                {member.name}
                            </dd>
                        ))}
                    </>
                )}
            </dl>
        </>
    );
};

export default StepReviewAgreement;
