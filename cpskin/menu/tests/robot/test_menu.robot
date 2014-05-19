*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***


*** Test cases ***

Scenario: Test menu
    Given logged as owner


*** Keywords ***

logged as owner
    Log in as site owner
