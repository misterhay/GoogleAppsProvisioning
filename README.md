GoogleAppsProvisioning
======================

This can automate actions across multiple Google Apps domains, for example provisioning Google Apps user accounts from a CSV file generated by PowerSchool.

Setup:
pip install --upgrade google-api-python-client
pip install pyopenssl

Requires a p12 file from https://console.developers.google.com/project with some or all of the following APIs enabled:
Admin SDK
Google Classroom API
Apps Activity API (perhaps)
Drive API (perhaps)

You'll also need the Client ID from the Credentials screen. See https://developers.google.com/api-client-library/python/start/get_started for more information.
