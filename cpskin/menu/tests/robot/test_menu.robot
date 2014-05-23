*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***


*** Test cases ***


Test menu
    Logged as owner
    Page Should Contain Link   LOISIRS
    Click Link                 LOISIRS
    Element Should Be Visible  css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Click Element              css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Element Should Be Visible  css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Click Element              css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Element Should Be Visible  css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Click Element              css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata

    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata

Test loading with 3 levels
    Logged as owner
    Page Should Contain Link  LOISIRS

    Click Link          LOISIRS
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-bibliotheques
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/bibliotheques

Test loading with 4 levels
    Logged as owner
    Page Should Contain Link  LOISIRS

    Click Link          LOISIRS
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata

Test begin on other page than root
    Logged as owner
    Go To  http://localhost:55001/plone/commune/services_communaux/finances

    Page Should Contain Link  LOISIRS

    Click Link          LOISIRS
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata

Test keyboard navigation
    Logged as owner
    Page Should Contain Link   LOISIRS
    Click Link                 LOISIRS
    Focus                      css=a#loisirs-art_et_culture
    Element Should Be Visible  css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Focus                      css=a#loisirs-art_et_culture-artistes
    Element Should Be Visible  css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Click Element              css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Location Should Be         http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata


Test level 5 not in menu
    Logged as owner
    Page Should Contain Link  LOISIRS

    Click Link          LOISIRS
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-rockers
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/rockers

Test fourth level navigation folder not working in wrong place
    Logged as owner
    Page Should Contain Link  LOISIRS

    Click Link          LOISIRS
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Element       css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-cinema
    # Menu not deployed
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/cinema

    Page Should Contain  Kinepolis


*** Keywords ***

Logged as owner
    Log in as site owner
