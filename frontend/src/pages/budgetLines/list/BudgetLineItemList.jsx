import { useState } from "react";
// import { useSelector } from "react-redux";
import { useSearchParams } from "react-router-dom";
import _ from "lodash";
import App from "../../../App";
import { useGetAgreementsQuery, useGetBudgetLineItemsQuery, useGetCansQuery } from "../../../api/opsAPI";
import Breadcrumb from "../../../components/UI/Header/Breadcrumb";
import TablePageLayout from "../../../components/Layouts/TablePageLayout";
import AllBudgetLinesTable from "../../../components/BudgetLineItems/AllBudgetLinesTable";
import BLIFilterButton from "./BLIFilterButton";
import SummaryCardsSection from "../../../components/BudgetLineItems/SummaryCardsSection";
import BLIFilterTags from "./BLIFilterTags";

/**
 * Page for the Budget Line Item List.
 * @returns {React.JSX.Element} - The component JSX.
 */
export const BudgetLineItemList = () => {
    const [searchParams] = useSearchParams();
    // const activeUser = useSelector((state) => state?.auth?.activeUser);
    const [filters, setFilters] = useState({
        fiscalYears: [],
        portfolios: [],
        bliStatus: []
    });
    const {
        data: budgetLineItems,
        error: budgetLineItemsError,
        isLoading: budgetLineItemsIsLoading
    } = useGetBudgetLineItemsQuery();
    const { data: cans, error: cansError, isLoading: cansIsLoading } = useGetCansQuery();
    const { data: agreements, error: agreementsError, isLoading: agreementsAreError } = useGetAgreementsQuery();

    const myBudgetLineItemsUrl = searchParams.get("filter") === "my-budget-line-items";

    if (budgetLineItemsIsLoading || cansIsLoading || agreementsAreError) {
        return (
            <App>
                <h1>Loading...</h1>
            </App>
        );
    }
    if (budgetLineItemsError || cansError || agreementsError) {
        return (
            <App>
                <h1>Oops, an error occurred</h1>
            </App>
        );
    }

    // FILTERS
    let filteredBudgetLineItems = _.cloneDeep(budgetLineItems);

    // filter by fiscal year
    filteredBudgetLineItems = filteredBudgetLineItems.filter((bli) => {
        return (
            _.isNull(filters.fiscalYears) ||
            _.isEmpty(filters.fiscalYears) ||
            filters.fiscalYears.some((fy) => {
                return fy.id === bli.fiscal_year;
            })
        );
    });

    // filter by portfolio
    filteredBudgetLineItems = filteredBudgetLineItems.filter((bli) => {
        return (
            _.isNull(filters.portfolios) ||
            _.isEmpty(filters.portfolios) ||
            filters.portfolios.some((portfolio) => {
                return portfolio.id === bli.portfolio_id;
            })
        );
    });

    // filter by BLI status
    filteredBudgetLineItems = filteredBudgetLineItems.filter((bli) => {
        return (
            _.isNull(filters.bliStatus) ||
            _.isEmpty(filters.bliStatus) ||
            filters.bliStatus.some((bliStatus) => {
                return bliStatus.status === bli.status;
            })
        );
    });

    const sortBLIs = (blis) => {
        return blis.sort((a, b) => {
            return new Date(a.date_needed) - new Date(b.date_needed);
        });
    };

    let sortedBLIs = [];
    if (myBudgetLineItemsUrl) {
        const myBLIs = filteredBudgetLineItems.filter(() => {
            return true;
        });
        sortedBLIs = sortBLIs(myBLIs);
    } else {
        // all-budget-line-items
        sortedBLIs = sortBLIs(filteredBudgetLineItems);
    }

    // handy for debugging
    // console.log("filters", filters);
    // console.log("setFilters", setFilters);
    // console.log("activeUser", activeUser);
    // console.log("budgetLineItems", budgetLineItems);
    // console.log("filteredBudgetLineItems", filteredBudgetLineItems);
    // console.log("sortedBLIs", sortedBLIs);

    const budgetLinesWithCanAndAgreementName = sortedBLIs.map((budgetLine) => {
        const can = cans.find((can) => can.id === budgetLine.can_id);
        const agreement = agreements.find((agreement) => agreement.id === budgetLine.agreement_id);
        const procurementShopAbbr = agreement?.procurement_shop?.abbr;

        return {
            ...budgetLine,
            can_number: can?.number,
            agreement_name: agreement?.name,
            procShopCode: procurementShopAbbr
        };
    });

    return (
        <App>
            <Breadcrumb currentName={"Budget Lines"} />
            <TablePageLayout
                title="Budget Lines"
                subtitle={myBudgetLineItemsUrl ? "My Budget Lines" : "All Budget Lines"}
                details={
                    myBudgetLineItemsUrl
                        ? "This is a list of the budget lines you are listed as a Team Member on. Please select filter options to see budget lines by Portfolio, Status, or Fiscal Year."
                        : "This is a list of budget lines across all OPRE projects and agreements, including drafts. Please select filter options to see budget lines by Portfolio, Status, or Fiscal Year."
                }
                buttonText="Add Budget Lines"
                buttonLink="/budget-lines/create"
                FilterTags={
                    <BLIFilterTags
                        filters={filters}
                        setFilters={setFilters}
                    />
                }
                TableSection={<AllBudgetLinesTable budgetLines={budgetLinesWithCanAndAgreementName} />}
                FilterButton={
                    <BLIFilterButton
                        filters={filters}
                        setFilters={setFilters}
                    />
                }
                SummaryCardsSection={<SummaryCardsSection budgetLines={budgetLinesWithCanAndAgreementName} />}
            />
        </App>
    );
};
