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
    Click Element  css=div#mobile-first-level-wrapper a#loisirs
    Click Element  css=ul.submenu-level-1 li:nth-child(2)
    Click Element  css=ul.submenu-level-2 li:nth-child(2)
    Click link  Tata
    Location Should Contain   tata


*** Keywords ***

logged as owner
    Log in as site owner
