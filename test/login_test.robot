*** Settings ***
Resource          ../resource/common.robot

*** Test Cases ***
User can open CAM and login
    [Setup]    General settings
    Open CAM
    Click "Log In" on the beginning page
    Log in and accept the policy
    NZXT user account should be logged in successfully
    [Teardown]    Close CAM