*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***
${FF_PROFILE_DIR}  ${CURDIR}/firefoxmobileprofile


*** Test cases ***

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
    Click Element       css=ul.submenu-level-2 li:nth-child(2)
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes
    Click Element       css=ul.submenu-level-3 li:nth-child(1)
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata

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

*** Keywords ***

Logged as owner
    Log in as site owner
