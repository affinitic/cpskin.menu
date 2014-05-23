*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***


*** Test cases ***


Test menu
    Logged as owner
    Page Should Contain Link  LOISIRS
    Click Link                LOISIRS
    Page Should Contain Link  Art & Culture
    Click Link                Art & Culture
    Page Should Contain Link  Artistes
    Click Link                Artistes
    Page Should Contain Link  Tata
    Click Link                Tata

    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata

    Location Should Contain   tata

Test loading with 3 levels
    Logged as owner
    Page Should Contain Link  LOISIRS

    Click Link          LOISIRS
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Link          Art & Culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Link          Bibliothèques
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/bibliotheques

Test loading with 4 levels
    Logged as owner
    Page Should Contain Link  LOISIRS

    Click Link          LOISIRS
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Link          Art & Culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Link          Artistes
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Link          Tata
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata

Test begin on other page than root
    Logged as owner
    Go To  http://localhost:55001/plone/commune/services_communaux/finances

    Page Should Contain Link  LOISIRS

    Click Link          LOISIRS
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Link          Art & Culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Link          Artistes
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Link          Tata
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata

Test keyboard navigation
    Logged as owner
    Page Should Contain Link  LOISIRS
    Click Link                LOISIRS
    Focus                     css=a#loisirs-art_et_culture
    Page Should Contain Link  Artistes
    Focus                     css=a#loisirs-art_et_culture-artistes
    Page Should Contain Link  Tata
    Click Link                Tata
    Location Should Be        http://localhost:55001/plone/loisirs/art_et_culture/artistes/tata


Test level 5 not in menu
    Logged as owner
    Pause
    Page Should Contain Link  LOISIRS

    Click Link          LOISIRS
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Link          Art & Culture
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Link          Artistes
    Location Should Be  http://localhost:55001/plone/loisirs
    Click Link          Rockers
    Location Should Be  http://localhost:55001/plone/loisirs/art_et_culture/artistes/rockers

*** Keywords ***

Logged as owner
    Log in as site owner
