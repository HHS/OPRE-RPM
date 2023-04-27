import { Link } from "react-router-dom";
import { CheckAuth } from "../../Auth/auth";

export const Menu = () => {
    const isAuthorized = CheckAuth();
    return (
        <div id="nav-menu">
            <button type="button" className="usa-nav__close">
                <img src="/assets/img/usa-icons/close.svg" alt="Close" />
            </button>
            <ul className="usa-nav__primary usa-accordion">
                {isAuthorized ? (
                    <li className="usa-nav__primary-item">
                        <Link to="/portfolios/">Portfolios</Link>
                    </li>
                ) : (
                    <li>
                        <span></span>
                    </li>
                )}
                <li className="usa-nav__primary-item">
                    <Link to="/cans/">CANs</Link>
                </li>
                <li className="usa-nav__primary-item">
                    <Link to="/budget-lines/create">Create Budget Line</Link>
                </li>
                <li className="usa-nav__primary-item">
                    <Link to="/agreements/create">Create Agreement</Link>
                </li>
                <li className="usa-nav__primary-item">
                    <Link to="/agreements/">Agreement List</Link>
                    <Link to="/projects/create">Create Project</Link>
                </li>
            </ul>
        </div>
    );
};
