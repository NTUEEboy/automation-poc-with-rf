*** Settings ***
Library           SeleniumLibrary       timeout=15s
Library           ../library/MachineInfo.py
Library           ../chromedriver_binary/

*** Variables ***
${binary_location}    C:\\Program Files\\NZXT CAM\\NZXT CAM.exe
${login_email}    ming.kuo@nzxt.com
${login_pwd}    Nzxt5566

*** Keywords ***
General settings
    Add chromedriver to PATH

Add chromedriver to PATH
    Evaluate    chromedriver_binary.add_chromedriver_to_path()     modules=chromedriver_binary

Open CAM
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys
    ${options.binary_location}=    Set Variable    ${binary_location}
    Create Webdriver    Chrome    options=${options}
    Focus on CAM window

Focus on CAM window
    Sleep    10s    # To make sure the prvious CAM program process is totally closed
    ${title}=    Wait Until Keyword Succeeds    20x    3s    Get Window Titles    browser=CURRENT
    Select Window    ${title}

Click "Log In" on the beginning page
    Wait Until Element Is Visible    xpath://button[contains(text(), "Log In")]
    Sleep    5s
    Click Element    xpath://button[contains(text(), "Log In")]

Log in and accept the policy
    Wait Until Element Is Visible    xpath://*[@id="app"]/div/div[2]/div/div/div[2]/form/div[1]/label/input
    Input Text    xpath://*[@id="app"]/div/div[2]/div/div/div[2]/form/div[1]/label/input    ${login_email}
    Input Text    xpath://*[@id="app"]/div/div[2]/div/div/div[2]/form/div[2]/label/input    ${login_pwd}
    Sleep    6s    # For Demo
    Click Element    xpath://button[contains(text(), "Log In")]
    Click Element    xpath:/html/body/div[3]/div/div/div/div[1]/div/div[2]/label/input
    Sleep    4s    # For Demo
    Click Element    xpath://button[contains(text(), "Confirm")]

NZXT user account should be logged in successfully
    Error message wrapper    No PC Monitoring section on the navbar    Wait Until Element Is Visible    xpath://a[contains(text(), "PC Monitoring")]
    ${pc_monitoring}=    Get Text    xpath://a[contains(text(), "PC Monitoring")]
    Sleep    6s    # For Demo
    Should Be Equal    ${pc_monitoring}    PC Monitoring    msg=The text on PC Monitoring section is not "PC Monitoring"

GPU should be detected by CAM
    Error message wrapper    No Spec section on the navbar    Wait Until Element Is Visible    xpath://a[contains(text(), "System Specs")]
    Click Element    xpath://a[contains(text(), "System Specs")]
    Error message wrapper  Can't find the GPU Section on Spec page    Wait Until Element Is Visible    xpath://*[@id="system-specs-gpu"]/div[2]/div
    ${gpu_actual}=    Get Text    xpath://*[@id="system-specs-gpu"]/div[2]/div
    ${gpu_expect}=    MachineInfo.gpu_info
    Should Be Equal    ${gpu_actual}    ${gpu_expect}    msg=The GPU name is wrong!

Close CAM
    Close Window

Error message wrapper
    [Arguments]    ${error_msg}    @{original_kw_args}
    ${status}=    Run Keyword And Return Status    @{original_kw_args}
    Run Keyword If    ${status} == ${FALSE}    
    ...    Fail    msg=${error_msg}

#change