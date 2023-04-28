import React from "react";
import App from "../../App";
import { useSelector, useDispatch } from "react-redux";
import ProjectTypeSelect from "./ProjectTypeSelect";
import { setProjectId, setProjectShortTitle, setProjectTitle, setProjectDescription } from "./createProjectSlice";
import { useAddResearchProjectsMutation } from "../../api/opsAPI";

export const CreateProject = () => {
    const [currentIndex, setCurrentIndex] = React.useState(0);
    const dispatch = useDispatch();
    const projectShortTitle = useSelector((state) => state.createProject.project.short_title);
    const projectTitle = useSelector((state) => state.createProject.project.title);
    const projectDescription = useSelector((state) => state.createProject.project.description);
    const project = useSelector((state) => state.createProject.project);

    const [addResearchProject, results] = useAddResearchProjectsMutation();

    // if (errorAgreement) {
    //     return <div>Oops, an error occurred</div>;
    // }

    const handleCreateProject = async () => {
        // Save Project to DB
        const newProject = { ...project };
        delete newProject.id;
        delete newProject.selected_project_type;

        if (project) addResearchProject(newProject);
        // const response = await postProject(project);
        const newProjectId = results.id;
        console.log(`New Project Created: ${newProjectId}`);
        dispatch(setProjectId(newProjectId));
        alert("New Project Created!");
    };
    const handleCancel = () => {
        // TODO: Add cancel stuff
        // TODO: Clear createProject State
        goBack();
    };
    const goBack = () => {
        const previousIndex = currentIndex - 1;
        if (previousIndex >= 0) {
            setCurrentIndex(previousIndex);
        }
    };

    return (
        <App>
            <h1 className="font-sans-lg">Create New Project</h1>

            <h2 className="font-sans-lg">Select the Project Type</h2>
            <p>Select the type of project you are creating.</p>
            <ProjectTypeSelect />

            <h2 className="font-sans-lg">Project Details</h2>

            <label className="usa-label" htmlFor="project-abbr">
                Project Nickname or Acronym
            </label>
            <input
                className="usa-input"
                id="project-abbr"
                name="project-abbr"
                type="text"
                value={projectShortTitle || ""}
                onChange={(e) => dispatch(setProjectShortTitle(e.target.value))}
                required
            />

            <label className="usa-label" htmlFor="project-name">
                Project Title
            </label>
            <input
                className="usa-input"
                id="project-name"
                name="project-name"
                type="text"
                value={projectTitle || ""}
                onChange={(e) => dispatch(setProjectTitle(e.target.value))}
                required
            />

            <label className="usa-label" htmlFor="project-description">
                Description
            </label>
            <span id="with-hint-textarea-hint" className="usa-hint">
                Brief Description for internal purposes, not for the OPRE website.
            </span>
            <textarea
                className="usa-textarea"
                id="project-description"
                name="project-description"
                rows="5"
                style={{ height: "7rem" }}
                value={projectDescription || ""}
                onChange={(e) => dispatch(setProjectDescription(e.target.value))}
            ></textarea>

            <div className="grid-row flex-justify-end margin-top-8">
                <button className="usa-button usa-button--unstyled margin-right-2" onClick={handleCancel}>
                    Cancel
                </button>
                <button className="usa-button" onClick={handleCreateProject}>
                    Create Project
                </button>
            </div>
        </App>
    );
};
