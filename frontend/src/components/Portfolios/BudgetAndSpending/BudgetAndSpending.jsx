import { useOutletContext } from "react-router-dom";
import { useGetBudgetLineItemQuery } from "../../../api/opsAPI";
import CANBudgetLineTable from "../../CANs/CANBudgetLineTable";
import PortfolioBudgetSummary from "../PortfolioBudgetSummary/PortfolioBudgetSummary";
import DebugCode from "../../DebugCode";

const BudgetAndSpending = () => {
    // NOTE: Portfolio 1 with FY 2021 is a good example to test this component
    const { fiscalYear, budgetLineIds, portfolioFunding } = useOutletContext();
    const budgetLineItemQueries = budgetLineIds.map((id) => useGetBudgetLineItemQuery(id));

    const isLoading = budgetLineItemQueries.some((query) => query.isLoading);
    const budgetLineItems = budgetLineItemQueries.map((query) => query?.data);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <>
            <h2 className="font-sans-lg">Portfolio Budget & Spending Summary</h2>
            <p className="font-sans-sm">
                The summary below shows the budget and spending for this Portfolio for the selected fiscal year.
            </p>
            <PortfolioBudgetSummary
                fiscalYear={fiscalYear}
                portfolioFunding={portfolioFunding}
            />
            <section>
                <h2>Portfolio Budget Lines</h2>
                <p>
                    This is a list of all budget lines allocating funding from this Portfolio’s CANs for the selected
                    fiscal year.
                </p>
            </section>
            <CANBudgetLineTable
                budgetLines={budgetLineItems}
                totalFunding={portfolioFunding?.total_funding.amount}
            />
            <DebugCode data={portfolioFunding} />
        </>
    );
};

export default BudgetAndSpending;
