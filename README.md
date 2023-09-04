# PyOrcid: An API client for ORCID API

**Overview**

PyOrcid is a Python library and API client designed to simplify interactions with the ORCID API. ORCID (Open Researcher and Contributor ID) is a nonprofit organization that provides unique identifiers to researchers, ensuring their work is accurately attributed and discoverable. PyOrcid enables developers to seamlessly integrate ORCID functionality into their software, allowing users to collect, track, and sync their publication materials, research activities, and other related information.

**Official ORCID documentation**

Check out the methods, scopes, and examples mentioned in [official documentation here](https://info.orcid.org/documentation/).

**Developer Authentication**

To access the ORCID API, you need to authenticate your ORCID ID. 

1. **Create an ORCID Account:** If you don't already have an ORCID account, you'll need to create one. Visit the ORCID website and sign up for an account.

2. **Access Developer Tools:** Once you've logged into your ORCID account, navigate to "Your Profile." From there, select "Developer Tools."

3. **Obtain Client Credentials:** In the Developer Tools section, you'll be able to generate your developer credentials:
   - **Client ID:** You will receive a `client_id` that uniquely identifies your application.
   - **Client Secret:** You'll also be provided with a `client_secret` for secure communication.

4. **Register Redirect URI:** Register a `redirect_uri` for your application. This URI is where users will be redirected after authorizing your application's access to their ORCID data. Make sure to specify these URIs in advance to prevent errors during integration. You can use your GitHub repository URL or any other URL under your control as the `redirect_uri`.

More detailed steps mentioned [here](https://info.orcid.org/ufaqs/how-do-i-register-a-public-api-client/).

Next:
```python
from pyorcid import OrcidAuthentication
# Load environment variables from .env
OrcidAuthentication(client_id="APP-xxxxxxxx", client_secret="xx-xx-xxxx-xxx", redirect_uri="https://github.com/user")

By executing this code, you will be redirected to your URI with a **code**. Copy and paste the full URL in the terminal input prompt. Then, you will obtain an **access_token** which will be auto-saved in `.env` file along with other credentials.

**After Authentication**

There are various methods available in the package. You will need ORCID IDs of the researchers/users to access their ORCID profiles. For example:

```python
from pyorcid import Orcid
orcid_id = 'xxxx-xxxx-xxxx-xxxx'
orcid = Orcid(orcid_id=orcid_id)
orcid.__dir__()
works_data = orcid.works()
for key, value in fundings_data.items():
    print(key, value)