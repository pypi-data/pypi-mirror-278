# REST client for UW IT Bill API

To use this client, you'll need these settings in your application or script:

    # Specifies whether requests should use live or mocked resources,
    # acceptable values are 'Live' or 'Mock' (default)
    RESTCLIENTS_ITBILL_DAO_CLASS='Live'

    # Values for authentication credentials
    RESTCLIENTS_ITBILL_BASIC_AUTH=<base64-encoded-credentials>

    # ITBill API hostname (test or production)
    RESTCLIENTS_ITBILL_HOST='https://server.washington.edu'
