/// <reference types="cypress" />
import { testLogin } from "./utils";

beforeEach(() => {
    cy.visit("/");
});

it("Notification Center appears when you click the bell icon and has 1 item in list", () => {
    cy.visit("/");
    testLogin("admin");
    cy.visit("/");
    cy.get("#notification-center-bell").click();
    cy.contains("Notifications");
    cy.get("#notification-center-list").its("length").should("eq", 1);

    // notifications not visible after clicking clear button
    cy.get("#clear-all-button").click();
    cy.get("#notification-center-list").its("length").should("eq", 0);
});
