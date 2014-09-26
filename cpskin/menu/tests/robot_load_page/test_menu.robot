*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***


*** Test Cases ***


Test menu
    Click LOISIRS Menu

    Element Should Be Visible  css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Click Element              css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Element Should Be Visible  css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Click Element              css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Element Should Be Visible  css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Click Element              css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata

    Wait Until Page Contains Element  xpath=//h1[contains(text(),'Tata')]
    Location Should Be                http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata

Test loading with 3 levels
    Click LOISIRS Menu

    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-bibliotheques
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/bibliotheques

Test loading with 4 levels
    Click LOISIRS Menu

    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata

Test begin on other page than root
    Go To  http://localhost:55001/plone/commune/services_communaux/finances

    Element Should Be Visible  css=li#portaltab-loisirs a
    Click Element              css=li#portaltab-loisirs a

    Wait Until Page Contains Element  xpath=//h1[contains(text(),'LOISIRS')]
    Location Should Be                http://localhost:55001/plone/loisirs


    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata

Test keyboard navigation
    Click LOISIRS Menu

    Focus                      css=a#loisirs-art_et_culture
    Element Should Be Visible  css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Focus                      css=a#loisirs-art_et_culture-artistes
    Element Should Be Visible  css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Click Element              css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Location Should Be         http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata


Test level 5 not in menu
    Click LOISIRS Menu

    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-rockers
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/rockers

Test fourth level navigation folder not working in wrong place
    Click LOISIRS Menu

    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-cinema
    # Menu not deployed
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/cinema

    Page Should Contain  Kinepolis

Test menu visible when location is subfolder
    Go To  http://localhost:55001/plone/loisirs/art_et_culture
    Element Should Be Visible  css=ul.navTreeLevel0 a#loisirs-art_et_culture


*** Keywords ***


Click LOISIRS menu
    Element Should Be Visible  css=li#portaltab-loisirs a
    Click Element              css=li#portaltab-loisirs a

    Wait Until Page Contains Element  xpath=//h1[contains(text(),'LOISIRS')]
    Location Should Be                http://localhost:55001/plone/loisirs
