/// <reference types="cypress" />

import { terminalLog, testLogin } from "./utils";

const testAgreement = {
    agreement_type: "CONTRACT",
    agreement_reason: "NEW_REQ",
    name: "Test Contract",
    number: "TEST001",
    description: "Test Description",
    research_project_id: 1,
    product_service_code_id: 1,
    procurement_shop_id: 1,
    incumbent: "Test Vendor",
    project_officer: 1,
    team_members: [
        {
            id: 3,
        },
        {
            id: 5,
        },
    ],
    notes: "Test Notes",
};

beforeEach(() => {
    testLogin("admin");
    cy.visit(`/`);
});

afterEach(() => {
    cy.injectAxe();
    cy.checkA11y(null, null, terminalLog);
});

it("edit an agreement", () => {
    expect(localStorage.getItem("access_token")).to.exist;

    // create test agreement
    const bearer_token = `Bearer ${window.localStorage.getItem("access_token")}`;
    cy.request({
        method: "POST",
        url: "http://localhost:8080/api/v1/agreements/",
        body: testAgreement,
        headers: {
            Authorization: bearer_token,
            "Content-Type": "application/json",
            Accept: "application/json",
        },
    }).then((response) => {
        expect(response.status).to.eq(201);
        expect(response.body.id).to.exist;
        const agreementId = response.body.id;

        cy.intercept("PATCH", "**/agreements/**").as("patchAgreement");
        cy.visit(`/agreements/${agreementId}`);
        cy.get('#edit').click();
        cy.get('#edit').should("not.exist");
        cy.get('[data-cy="continue-btn"]').should("exist");
        cy.get("h1").should("have.text", "Test Contract");
        // test validation
        cy.get("#name").clear();
        cy.get("#name").blur();
        cy.get("#input-error-message").should("contain", "This is required information");
        cy.get("[data-cy='continue-btn']").should("be.disabled");
        cy.get("#name").type("Test Edit Title");
        cy.get("#input-error-message").should("not.exist");
        cy.get("[data-cy='continue-btn']").should("not.be.disabled");
        cy.get("#description").type(" more text");
        cy.get("#agreementNotes").type("test edit notes");

        cy.get("[data-cy='continue-btn']").click();

        cy.wait("@patchAgreement")
            .then((interception) => {
                const { statusCode, body } = interception.response;
                expect(statusCode).to.equal(200);
                expect(body.message).to.equal("Agreement updated");
            })
            .then(cy.log);

        cy.get("h1").should("have.text", "Test Edit Title");
        cy.get('#edit').should("exist");

        cy.request({
            method: "DELETE",
            url: `http://localhost:8080/api/v1/agreements/${agreementId}`,
            headers: {
                Authorization: bearer_token,
                Accept: "application/json",
            },
        }).then((response) => {
            expect(response.status).to.eq(200);
        });
    });
});
