*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***


*** Test cases ***

Test menu
    Logged as owner
    Page Should Contain Link  LOISIRS
    Click link  LOISIRS
    Page Should Contain Link  Art & Culture
    Click link  Art & Culture
    Page Should Contain Link  Artistes
    Click link  Artistes
    Page Should Contain Link  Tata
    Click link  Tata
    Location Should Contain   tata

Test level1
    Logged as owner
    Page Should Contain Link  LOISIRS
    Click link  LOISIRS



*** Keywords ***

Logged as owner
    Log in as site owner
