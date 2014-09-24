*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***


*** Test cases ***


Test direct access visibility
    Click LOISIRS menu

    Click Element  css=ul.navTreeLevel0 a#loisirs-art_et_culture

    # Direct access visible
    Element Should Be Visible  css=ul.direct_access a#loisirs-art_et_culture-artistes-abba
    Element Should Be Visible  css=ul.direct_access a#loisirs-art_et_culture-artistes-rockers-john_lennon

    # Direct access non visible from another folder
    Element Should Not Be Visible  css=ul.direct_access a#loisirs-tourisme-promenades

Test direct access link
    Click LOISIRS menu

    Click Element  css=ul.navTreeLevel0 a#loisirs-art_et_culture

    Click Element       css=ul.direct_access a#loisirs-art_et_culture-artistes-rockers-john_lennon
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/rockers/john_lennon


*** Keywords ***


Click LOISIRS menu
    Element Should Be Visible  css=li#portaltab-loisirs a
    Click Element              css=li#portaltab-loisirs a
    Location Should Be         http://localhost:55001/plone
