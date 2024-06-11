# Xray Library
Library responsible for sending execution results and updating the XrayTest definition.

## Usage Notices
- Cannot make use of Teardown
- You cannot create keywords in the same scope as the test
- Works in pipeline, to use locally it is necessary to use dotEnv

## Correct usage
```
# File: log_console_test.robot

*** Settings ***
Documentation    Test scenarios for log console.
Library    Xray
Resource    resources/kw.resource

*** Tasks ***
Log message to console
    Log Hello World

# File: resources/kw.resource

*** Keywords ***
Log Hello World
    Log To Console    message=Hello World
```

```
# File: search_google_test.robot

*** Settings ***
Documentation    Test scenarios for search google.
Library    SeleniumLibrary
Library    Xray

*** Tasks ***
Search for the sentence Worten in Google
    Open Browser    url=https://www.google.com    browser=chrome
    Input Text    locator=name:q    text=Worten
    Press Keys    None    ENTER
    Title Should Be    title=Worten - Pesquisa Google
    Close Browser
```

## Misuse
```
# File: log_console_test.robot

*** Settings ***
Documentation    Test scenarios for log console.
Library    Xray

*** Tasks ***
Log message to console
    Log Hello World

*** Keywords ***
Log Hello World
    Log To Console    message=Hello World
```

```
# File: search_google_test.robot

*** Settings ***
Documentation    Test scenarios for search google.
Library    SeleniumLibrary
Library    Xray

*** Tasks ***
Search for the sentence Worten in Google
    Open Browser    url=https://www.google.com    browser=chrome
    Input Text    locator=name:q    text=Worten
    Press Keys    None    ENTER
    Title Should Be    title=Worten - Pesquisa Google
    [Teardown]   Close Browser
```

## Local usage
Create an `.env` file using `.env.example` as a base.