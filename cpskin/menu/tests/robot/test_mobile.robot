*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***
${FF_PROFILE_DIR}  ${CURDIR}/firefoxmobileprofile


*** Test cases ***

Test desktop menu not visible
    Logged as owner
    Element Should Not Be Visible  css=ul#portal-globalnav li#portaltab-commune

Test menu
    Logged as owner
    Click Element       id=mobnav-btn
    Click Element       css=div#mobile-first-level-wrapper a#loisirs
    Click Element       css=ul.submenu-level-1 li:nth-child(2)
    Click Element       css=ul.submenu-level-2 li:nth-child(2)
    Click Element       css=ul.submenu-level-3 li:nth-child(1)
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata

Test loading with 3 levels
    Logged as owner
    Click Element       id=mobnav-btn
    Click Element       css=div#mobile-first-level-wrapper a#loisirs
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.submenu-level-1 li:nth-child(2)
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.submenu-level-2 li:nth-child(1)
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/bibliotheques

Test loading with 4 levels
    Logged as owner
    Click Element       id=mobnav-btn
    Click Element       css=div#mobile-first-level-wrapper a#loisirs
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.submenu-level-1 li:nth-child(2)
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.submenu-level-2 li:nth-child(2)
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.submenu-level-3 li:nth-child(1)
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata

Test direct access link
    Logged as owner
    Click Element  id=mobnav-btn
    Click Element  css=div#mobile-first-level-wrapper a#loisirs
    Click Element  css=ul.submenu-level-1 li:nth-child(2)
    Click Element  css=ul.submenu-level-2 li:nth-child(4)

    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/rockers/john_lennon

*** Keywords ***

Logged as owner
    Log in as site owner
