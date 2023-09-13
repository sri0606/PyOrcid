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

## QuickStart
```python
pip install PyOrcid
```
## Two ways to access public ORCID data
1. [Access through Orcid API](#access-through-orcid-api)

   You can get read/update access if you use Orcid API (note: update feature available only with member API). This is the official and most trusted way to get access. There are public and member APIs.
   
   You will need:
     - Developer's Application details (for authorization)
     - Orcid ID and corresponding access token of any researcher/user (for reading data)
     - Member API has extra authentication [steps](https://info.orcid.org/documentation/integration-guide/registering-a-member-api-client/)

2. [Access through OrcidScrapper feature of PyOrcid](#access-through-orcidscrapper-feature-of-pyorcid)

   You will only get to read the public Orcid records. This is simplest way and an alternative to using API. Doesn't require any authorization.
   
   You will need:
     - Orcid ID of the reasearcher/user(for reading data)

## Access through ORCID API
### 1. Developer : Registering your application
**Skip this step if you already have details of client ID, client secret and a redirect uri of authorized application**

To access the Public ORCID API, you need to register and authenticate yourself by registering an applications. 

If you need access to other people's orcid profile, register your application and pass along your application details to them (they need to execute [step 2](#2.after-registering-your-application) to give you access).

1. **Create an ORCID Account:** If you don't already have an ORCID account, you'll need to create one. Visit the ORCID website and [sign up for an account](https://orcid.org/register).

2. **Access Developer Tools:** Once you've logged into your ORCID account, navigate to "Your Profile." From there, select "Developer Tools."

3. **Obtain Client Credentials:** In the Developer Tools section, you'll be able to generate your developer credentials:
   - **Client ID:** You will receive a `client_id` that uniquely identifies your application.
   - **Client Secret:** You'll also be provided with a `client_secret` for secure communication.

4. **Register Redirect URI:** Register a `redirect_uri` for your application. This URI is where users will be redirected after authorizing your application's access to their ORCID data. Make sure to specify these URIs in advance to prevent errors during integration. You can use your GitHub repository URL or any other URL under your control as the `redirect_uri`.

More detailed steps mentioned [here](https://info.orcid.org/ufaqs/how-do-i-register-a-public-api-client/) to access public API.

**To access the Member API, follow these [instructions](https://info.orcid.org/documentation/integration-guide/registering-a-member-api-client/).**

### 2. After registering your application

You need to get an access token. Getting an access-token depends on whether a method/scope require user authorization.

Get the `client_id`, `client_secret` and `redirect_uri` details from your [registered application](https://orcid.org/developer-tools).

#### a) For reading public-access data of a public profile 

By executing following code, you will get an access-token to read (publid-access) data of a public profile. This doesn't require user authorization. Don't need to provide any value for redirect_uri.

**You can use this token to access any number of public profiles.**
```python
from pyorcid import OrcidAuthentication

# redirect_uri  is not required
orcid_auth = OrcidAuthentication(client_id="APP-xxxxxxxx", client_secret="xx-xx-xxxx-xxx")

access_token = orcid_auth.get_public_access_token()
```

#### b) For Member API or reading limited-access data of public profile
By executing following code, the user will be redirected to orcid authorization page. Once the user authorizes your application, they will be redirected to "redirected_uri" you registered. Copy and paste the full URL of redirected page (contains special code) in terminal. Please save it for future use or else the application has to be authorized everytime.

**This token is exclusively for the user who granted access.**
```python
from pyorcid import OrcidAuthentication

# Authenticate your application 
# Any valid user can authorize your application by running the following command 
orcid_auth = OrcidAuthentication(client_id="APP-xxxxxxxx", client_secret="xx-xx-xxxx-xxx",      
                                 redirect_uri="https://github.com/user")

access_token = orcid_auth.get_private_access_token()
```

**Executing this line of code:**
- Click the URL as mentioned in output, which will redirect the user to orcid website.
- It will ask the user whether to authorize your application.
- After your application is authorized, user will be redirected to application's `redirect_uri` with a **code**. Copy and paste the full URL in the terminal input prompt. Then, you will obtain an **access_token**. Most probably, this token will not expire for around 20 years. So, make sure to save it, otherwise user have to re-authorize your application.

### 3.After Authentication

To utilize the functionalities offered by this package, you have access to a variety of methods. To get started, you'll require the ORCID IDs of the researchers or users whose data you intend to access, as well as the access token that is received after the user authorized your application to interact with their ORCID profiles. For instance

```python
from pyorcid import Orcid

#Orcid ID of the user
orcid_id = 'xxxx-xxxx-xxxx-xxxx'

#this is the access token obtained either of above auth methods
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

## Access through OrcidScrapper feature of PyOrcid
This is an alternative to Orcid API. You can only read the orcid profiles on public database. All you need is the Orcid ID of the researchers you wish to retrieve.
OrcidScrapper can access all methods of Orcid class as it is inherited from it.

```python
from src import pyorcid
orcid_id = '0000-0003-0666-9883'
orcid = pyorcid.OrcidScrapper(orcid_id=orcid_id)
orcid.__dir__()
```
```
works_data = orcid.works()[0]
for key, value in works_data.items():
    print(key, value)

orcid.record_summary()

```