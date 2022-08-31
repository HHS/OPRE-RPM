import { useDispatch, useSelector } from "react-redux";
import { getPortfolio } from "./getPortfolio";
import { useEffect } from "react";
import { useParams, Link } from "react-router-dom";

const CanList = (props) => {
    return (
        <li>
            <Link to={`/cans/${props.id}`}>{props.name}</Link>
        </li>
    );
};

const PortfolioDetail = () => {
    const dispatch = useDispatch();
    const portfolio = useSelector((state) => state.portfolioDetail.portfolio);
    const urlPathParams = useParams();

    useEffect(() => {
        dispatch(getPortfolio(urlPathParams.id));
    }, [dispatch, urlPathParams.id]);

    return (
        <main>
            <section className="flex">
                <div className="one-flex">
                    <div className="rounded-box">
                        <div className="info-unit">
                            <h2>Portfolio Information</h2>
                        </div>
                        <div className="info-unit">
                            <h3>Portfolio description</h3>
                            {portfolio.description}
                        </div>
                        <div className="info-unit">
                            <h3>Status</h3>
                            {portfolio.status}
                        </div>
                        <div className="info-unit">
                            <h3>Fiscal Year Funding</h3>
                            {portfolio.current_fiscal_year_funding}
                        </div>
                        <div className="info-unit">
                            <h3>CANs</h3>
                            <ul>
                                {portfolio.cans?.map((can) => (
                                    <CanList key={can.id} id={can.id} name={can.number} />
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    );
};

export default PortfolioDetail;
