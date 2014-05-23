*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***


*** Test cases ***


Test direct access visibility
    Logged as owner
    Page Should Contain Link  LOISIRS
    Click Link                LOISIRS
    Page Should Contain Link  Art & Culture
    Click Link                Art & Culture

    # Direct access visible
    Element Should Be Visible    css=ul.direct_access a#loisirs-art_et_culture-artistes-abba
    Element Should Be Visible    css=ul.direct_access a#loisirs-art_et_culture-artistes-rockers-john_lennon

    # Direct access non visible from another folder
    Element Should Not Be Visible  css=ul.direct_access a#loisirs-tourisme-promenades

Test direct access link
    Logged as owner
    Page Should Contain Link  LOISIRS
    Click Link                LOISIRS
    Page Should Contain Link  Art & Culture
    Click Link                Art & Culture

    Click Element       css=ul.direct_access a#loisirs-art_et_culture-artistes-rockers-john_lennon
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/rockers/john_lennon

*** Keywords ***

Logged as owner
    Log in as site owner
