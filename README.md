# PyOrcid: An API client for ORCID API

[![Python3](https://img.shields.io/badge/Python3-%233776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![dotenv](https://img.shields.io/badge/dotenv-%230a9e0a.svg?style=flat-square)](https://pypi.org/project/python-dotenv/)
[![urllib](https://img.shields.io/badge/urllib-%233776AB.svg?style=flat-square&logo=python&logoColor=white)](https://docs.python.org/3/library/urllib.html)
[![requests](https://img.shields.io/badge/requests-%233776AB.svg?style=flat-square&logo=python&logoColor=white)](https://docs.python-requests.org/en/master/)
![Tests](https://github.com/sri0606/PyOrcid/actions/workflows/tests.yml/badge.svg)


## Overview

PyOrcid is a Python library and API client designed to simplify interactions with the ORCID API. ORCID (Open Researcher and Contributor ID) is a nonprofit organization that provides unique identifiers to researchers, ensuring their work is accurately attributed and discoverable. PyOrcid enables developers to seamlessly integrate ORCID functionality into their software, allowing users to collect, track, and sync their publication materials, research activities, and other related information.

## Official ORCID documentation

Check out the methods, scopes, and examples mentioned in [official documentation here](https://info.orcid.org/documentation/).

## Developer Authentication : Registering your application

To access the Public ORCID API, you need to register and authenticate your ORCID ID. 

1. **Create an ORCID Account:** If you don't already have an ORCID account, you'll need to create one. Visit the ORCID website and [sign up for an account](https://orcid.org/register).

2. **Access Developer Tools:** Once you've logged into your ORCID account, navigate to "Your Profile." From there, select "Developer Tools."

3. **Obtain Client Credentials:** In the Developer Tools section, you'll be able to generate your developer credentials:
   - **Client ID:** You will receive a `client_id` that uniquely identifies your application.
   - **Client Secret:** You'll also be provided with a `client_secret` for secure communication.

4. **Register Redirect URI:** Register a `redirect_uri` for your application. This URI is where users will be redirected after authorizing your application's access to their ORCID data. Make sure to specify these URIs in advance to prevent errors during integration. You can use your GitHub repository URL or any other URL under your control as the `redirect_uri`.

More detailed steps mentioned [here](https://info.orcid.org/ufaqs/how-do-i-register-a-public-api-client/) to access public API.

**To access the Member API, follow these [instructions](https://info.orcid.org/documentation/integration-guide/registering-a-member-api-client/).**

## After registering your application

Get the `client_id`, `client_secret` and `redirect_uri` details from your [registered application](https://orcid.org/developer-tools).

```python
from pyorcid import OrcidAuthentication

# Authenticate your application 
# Any valid user can authorize your application by running the following command 
OrcidAuthentication(client_id="APP-xxxxxxxx", client_secret="xx-xx-xxxx-xxx", redirect_uri="https://github.com/user")
```

**Executing this line of code:**
- Click the URL as mentioned in output, which will redirect the user to orcid website.
- It will ask the user whether to authorize your application.
- After your application is authorized, user will be redirected to application's `redirect_uri` with a **code**. Copy and paste the full URL in the terminal input prompt. Then, you will obtain an **access_token**. Most probably, this token will not expire for around 20 years. So, make sure to save it, otherwise user have to re-authorize your application.

## After Authentication

To utilize the functionalities offered by this package, you have access to a variety of methods. To get started, you'll require the ORCID IDs of the researchers or users whose data you intend to access, as well as the access token that is received after the user authorized your application to interact with their ORCID profiles. For instance

```python
from pyorcid import Orcid

#Orcid ID of the user
orcid_id = 'xxxx-xxxx-xxxx-xxxx'
access_token = "xxxx-xxxxxxxxxxx-xxxxxxx-xxx"
#create an instance of the Orcid class
# state defines which ORCID API you want to use: public or member
orcid = Orcid(orcid_id=orcid_id, orcid_access_token=access_token, state = "public")
orcid.__dir__()
```
```python
# Get the information of user's works from their ORCID profile
works_data = orcid.works()[0]
for key, value in works_data.items():
    print(key, value)
```
```python

# Generate a markdown file with the summary of various section's data
orcid.generate_markdown_file(output_file = "md_generator_example.md")
```
