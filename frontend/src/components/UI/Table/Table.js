import PropTypes from "prop-types";
import styles from "./table.module.css";

/**
 * The Table component is a layout component that displays a table
 * @param {object} props - The component props.
 * @param {React.ReactNode} [props.children] - The children to render - optional.
 * @param {string[]} props.tableHeadings - The table headings to display.
 * @param {React.ReactNode} [props.checkBoxSlot] - The checkbox slot - optional.
 * @returns {React.JSX.Element} - The rendered component.
 * @example
 * <Table tableHeadings={["Heading 1", "Heading 2", "Heading 3"]}>
 **/
const Table = ({ children, tableHeadings, checkBoxSlot }) => {
    /**
     * Adds a width to the Status column
     * @param {string} heading - The heading to check
     * @returns {object | undefined} - The width to add if the heading is Status
     *
     */
    const addWidthIfStatus = (heading) => {
        if (heading === "Status") {
            return { width: "6.25rem" };
        }
        return undefined;
    };

    return (
        <table className={`usa-table usa-table--borderless width-full ${styles.tableHover}`}>
            <thead>
                <tr>
                    {checkBoxSlot && checkBoxSlot}
                    {tableHeadings.map((heading, index) => (
                        <th
                            key={index}
                            scope="col"
                            style={addWidthIfStatus(heading)}
                        >
                            {heading}
                        </th>
                    ))}
                </tr>
            </thead>
            <tbody>{children}</tbody>
        </table>
    );
};

Table.propTypes = {
    children: PropTypes.node.isRequired,
    tableHeadings: PropTypes.arrayOf(PropTypes.string).isRequired,
    checkBoxSlot: PropTypes.node
};

export default Table;
