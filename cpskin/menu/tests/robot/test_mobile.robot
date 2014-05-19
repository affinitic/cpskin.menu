*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***
${FF_PROFILE_DIR}  ${CURDIR}/firefoxmobileprofile


*** Test cases ***

Scenario: Test menu
    Given logged as owner
    Click Element  id=mobnav-btn


*** Keywords ***

logged as owner
    Log in as site owner
