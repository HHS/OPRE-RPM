import CurrencyWithSmallCents from "../CurrencyWithSmallCents/CurrencyWithSmallCents";
import RoundedBox from "../RoundedBox/RoundedBox";

const CurrencySummaryCard = ({ headerText, amount, children }) => {
    return (
        <RoundedBox className="padding-y-205 padding-x-4 padding-right-9 display-inline-block">
            <div className="">
                <h3 className="margin-0 margin-bottom-3 font-12px text-brand-neutral text-normal">{headerText}</h3>
                <CurrencyWithSmallCents dollarsClasses="font-sans-xl" centsClasses="font-sans-3xs" amount={amount} />
                <div className="">{children}</div>
            </div>
        </RoundedBox>
    );
};

export default CurrencySummaryCard;
