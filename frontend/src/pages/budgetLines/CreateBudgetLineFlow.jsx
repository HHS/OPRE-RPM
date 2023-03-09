import React from "react";

export const CreateBudgetLineFlow = ({ children, onFinish }) => {
    const [formData, setFormData] = React.useState({});
    const [currentIndex, setCurrentIndex] = React.useState(0);

    const goToNext = (stepData) => {
        const nextIndex = currentIndex + 1;
        const updatedData = {
            ...formData,
            ...stepData,
        };
        console.log(updatedData);

        if (nextIndex < children.length) {
            setCurrentIndex(nextIndex);
        } else {
            onFinish(updatedData);
        }
        setFormData(updatedData);
    };

    const currentChild = React.Children.toArray(children)[currentIndex];

    if (React.isValidElement(currentChild)) {
        return React.cloneElement(currentChild, {
            goToNext,
        });
    }

    return currentChild;
};
