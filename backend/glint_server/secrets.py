def default_secrets() -> dict[str, dict[str, str]]:
    # return {}
    return {
        "gitlab_personal_access_token": {
            "patternName": "GitLab Personal Access Token",
            "regex": "/glpat-[0-9a-zA-Z\\-]{20}/",
        },
        "AWS": {
            "patternName": "AWS Access Token",
            "regex": "/AKIA[0-9A-Z]{16}/",
        },
        "PKCS8 private key": {
            "patternName": "PKCS8 private key",
            "regex": "/-----BEGIN PRIVATE KEY-----/",
        },
        "RSA private key": {
            "patternName": "RSA private key",
            "regex": "/-----BEGIN RSA PRIVATE KEY-----/",
        },
        "SSH private key": {
            "patternName": "SSH private key",
            "regex": "/-----BEGIN OPENSSH PRIVATE KEY-----/",
        },
        "PGP private key": {
            "patternName": "PGP private key",
            "regex": "/-----BEGIN PGP PRIVATE KEY BLOCK-----/",
        },
        "Github Personal Access Token": {
            "patternName": "Github Personal Access Token",
            "regex": "/ghp_[0-9a-zA-Z]{36}/",
        },
        "Github OAuth Access Token": {
            "patternName": "Github OAuth Access Token",
            "regex": "/gho_[0-9a-zA-Z]{36}/",
        },
        "SSH (DSA) private key": {
            "patternName": "SSH (DSA) private key",
            "regex": "/-----BEGIN DSA PRIVATE KEY-----/",
        },
        "SSH (EC) private key": {
            "patternName": "SSH (EC) private key",
            "regex": "/-----BEGIN EC PRIVATE KEY-----/",
        },
        "Github App Token": {
            "patternName": "Github App Token",
            "regex": "/(ghu|ghs)_[0-9a-zA-Z]{36}/",
        },
        "Github Refresh Token": {
            "patternName": "Github Refresh Token",
            "regex": "/ghr_[0-9a-zA-Z]{76}/",
        },
        "Shopify shared secret": {
            "patternName": "Shopify shared secret",
            "regex": "/shpss_[a-fA-F0-9]{32}/",
        },
        "Shopify access token": {
            "patternName": "Shopify access token",
            "regex": "/shpat_[a-fA-F0-9]{32}/",
        },
        "Shopify custom app access token": {
            "patternName": "Shopify custom app access token",
            "regex": "/shpca_[a-fA-F0-9]{32}/",
        },
        "Shopify private app access token": {
            "patternName": "Shopify private app access token",
            "regex": "/shppa_[a-fA-F0-9]{32}/",
        },
        "Slack token": {
            "patternName": "Slack token",
            "regex": "/xox[baprs]-([0-9a-zA-Z]{10,48})?/",
        },
        "Stripe": {
            "patternName": "Stripe",
            "regex": "/(sk|pk)_(test|live)_[0-9a-z]{10,32}/i",
        },
        "PyPI upload token": {
            "patternName": "PyPI upload token",
            "regex": "/pypi-AgEIcHlwaS5vcmc[A-Za-z0-9-_]{50,1000}/",
        },
        "Google (GCP) Service-account": {
            "patternName": "Google (GCP) Service-account",
            "regex": '/"type": "service_account"/',
        },
        "Password in URL": {
            "patternName": "Password in URL",
            "regex": "/[a-zA-Z]{3,10}:\\/\\/[^$][^:@]{3,20}:[^$][^:@]{3,40}@.{1,100}/",
        },
        "Heroku API Key": {
            "patternName": "Heroku API Key",
            "regex": "/ (heroku[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12})['\"]/i",
        },
        "Slack Webhook": {
            "patternName": "Slack Webhook",
            "regex": "/https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}/",
        },
        "Twilio API Key": {
            "patternName": "Twilio API Key",
            "regex": "/SK[0-9a-fA-F]{32}/",
        },
        "Age secret key": {
            "patternName": "Age secret key",
            "regex": "/AGE-SECRET-KEY-1[QPZRY9X8GF2TVDW0S3JN54KHCE6MUA7L]{58}/",
        },
        "Facebook token": {
            "patternName": "Facebook token",
            "regex": "/(facebook[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-f0-9]{32})['\"]/i",
        },
        "Twitter token": {
            "patternName": "Twitter token",
            "regex": "/(twitter[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-f0-9]{35,44})['\"]/i",
        },
        "Adobe Client ID (Oauth Web)": {
            "patternName": "Adobe Client ID (Oauth Web)",
            "regex": "/(adobe[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-f0-9]{32})['\"]/i",
        },
        "Adobe Client Secret": {
            "patternName": "Adobe Client Secret",
            "regex": "/(p8e-)[a-z0-9]{32}/i",
        },
        "Alibaba AccessKey ID": {
            "patternName": "Alibaba AccessKey ID",
            "regex": "/(LTAI)[a-z0-9]{20}/i",
        },
        "Alibaba Secret Key": {
            "patternName": "Alibaba Secret Key",
            "regex": "/(alibaba[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{30})['\"]/i",
        },
        "Asana Client ID": {
            "patternName": "Asana Client ID",
            "regex": "/(asana[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([0-9]{16})['\"]/i",
        },
        "Asana Client Secret": {
            "patternName": "Asana Client Secret",
            "regex": "/(asana[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{32})['\"]/i",
        },
        "Atlassian API token": {
            "patternName": "Atlassian API token",
            "regex": "/(atlassian[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{24})['\"]/i",
        },
        "Bitbucket client ID": {
            "patternName": "Bitbucket client ID",
            "regex": "/(bitbucket[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{32})['\"]/i",
        },
        "Bitbucket client secret": {
            "patternName": "Bitbucket client secret",
            "regex": "/(bitbucket[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9_\\-]{64})['\"]/i",
        },
        "Beamer API token": {
            "patternName": "Beamer API token",
            "regex": "/(beamer[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"](b_[a-z0-9=_\\-]{44})['\"]/i",
        },
        "Clojars API token": {
            "patternName": "Clojars API token",
            "regex": "/(CLOJARS_)[a-z0-9]{60}/i",
        },
        "Contentful delivery API token": {
            "patternName": "Contentful delivery API token",
            "regex": "/(contentful[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9\\-=_]{43})['\"]/i",
        },
        "Contentful preview API token": {
            "patternName": "Contentful preview API token",
            "regex": "/(contentful[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9\\-=_]{43})['\"]/i",
        },
        "Databricks API token": {
            "patternName": "Databricks API token",
            "regex": "/dapi[a-h0-9]{32}/",
        },
        "Discord API key": {
            "patternName": "Discord API key",
            "regex": "/(discord[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-h0-9]{64})['\"]/i",
        },
        "Discord client ID": {
            "patternName": "Discord client ID",
            "regex": "/(discord[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([0-9]{18})['\"]/i",
        },
        "Discord client secret": {
            "patternName": "Discord client secret",
            "regex": "/(discord[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9=_\\-]{32})['\"]/i",
        },
        "Doppler API token": {
            "patternName": "Doppler API token",
            "regex": "/['\"](dp\\.pt\\.)[a-z0-9]{43}['\"]/i",
        },
        "Dropbox API secret/key": {
            "patternName": "Dropbox API secret/key",
            "regex": "/(dropbox[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{15})['\"]/i",
        },
        "Dropbox short lived API token": {
            "patternName": "Dropbox short lived API token",
            "regex": "/(dropbox[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"](sl\\.[a-z0-9\\-=_]{135})['\"]/i",
        },
        "Dropbox long lived API token": {
            "patternName": "Dropbox long lived API token",
            "regex": "/(dropbox[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"][a-z0-9]{11}(AAAAAAAAAA)[a-z0-9\\-_=]{43}['\"]/i",
        },
        "Duffel API token": {
            "patternName": "Duffel API token",
            "regex": "/['\"]duffel_(test|live)_[a-z0-9_-]{43}['\"]/i",
        },
        "Dynatrace API token": {
            "patternName": "Dynatrace API token",
            "regex": "/['\"]dt0c01\\.[a-z0-9]{24}\\.[a-z0-9]{64}['\"]/i",
        },
        "EasyPost API token": {
            "patternName": "EasyPost API token",
            "regex": "/['\"]EZAK[a-z0-9]{54}['\"]/i",
        },
        "EasyPost test API token": {
            "patternName": "EasyPost test API token",
            "regex": "/['\"]EZTK[a-z0-9]{54}['\"]/i",
        },
        "Fastly API token": {
            "patternName": "Fastly API token",
            "regex": "/(fastly[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9\\-=_]{32})['\"]/i",
        },
        "Finicity client secret": {
            "patternName": "Finicity client secret",
            "regex": "/(finicity[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{20})['\"]/i",
        },
        "Finicity API token": {
            "patternName": "Finicity API token",
            "regex": "/(finicity[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-f0-9]{32})['\"]/i",
        },
        "Flutterweave public key": {
            "patternName": "Flutterweave public key",
            "regex": "/FLWPUBK_TEST-[a-h0-9]{32}-X/i",
        },
        "Flutterweave secret key": {
            "patternName": "Flutterweave secret key",
            "regex": "/FLWSECK_TEST-[a-h0-9]{32}-X/i",
        },
        "Flutterweave encrypted key": {
            "patternName": "Flutterweave encrypted key",
            "regex": "/FLWSECK_TEST[a-h0-9]{12}/",
        },
        "Frame.io API token": {
            "patternName": "Frame.io API token",
            "regex": "/fio-u-[a-z0-9-_=]{64}/i",
        },
        "GoCardless API token": {
            "patternName": "GoCardless API token",
            "regex": "/['\"]live_[a-z0-9-_=]{40}['\"]/i",
        },
        "Grafana API token": {
            "patternName": "Grafana API token",
            "regex": "/['\"]eyJrIjoi[a-z0-9-_=]{72,92}['\"]/i",
        },
        "Hashicorp Terraform user/org API token": {
            "patternName": "Hashicorp Terraform user/org API token",
            "regex": "/['\"][a-z0-9]{14}\\.atlasv1\\.[a-z0-9-_=]{60,70}['\"]/i",
        },
        "Hubspot API token": {
            "patternName": "Hubspot API token",
            "regex": "/(hubspot[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-h0-9]{8}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{12})['\"]/i",
        },
        "Intercom API token": {
            "patternName": "Intercom API token",
            "regex": "/(intercom[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9=_]{60})['\"]/i",
        },
        "Intercom client secret/ID": {
            "patternName": "Intercom client secret/ID",
            "regex": "/(intercom[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-h0-9]{8}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{12})['\"]/i",
        },
        "Ionic API token": {
            "patternName": "Ionic API token",
            "regex": "/ion_[a-z0-9]{42}/i",
        },
        "Linear API token": {
            "patternName": "Linear API token",
            "regex": "/lin_api_[a-z0-9]{40}/i",
        },
        "Linear client secret/ID": {
            "patternName": "Linear client secret/ID",
            "regex": "/(linear[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-f0-9]{32})['\"]/i",
        },
        "Lob API Key": {
            "patternName": "Lob API Key",
            "regex": "/(lob[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]((live|test)_[a-f0-9]{35})['\"]/i",
        },
        "Lob Publishable API Key": {
            "patternName": "Lob Publishable API Key",
            "regex": "/(lob[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]((test|live)_pub_[a-f0-9]{31})['\"]/i",
        },
        "Mailchimp API key": {
            "patternName": "Mailchimp API key",
            "regex": "/(mailchimp[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-f0-9]{32}-us20)['\"]/i",
        },
        "Mailgun private API token": {
            "patternName": "Mailgun private API token",
            "regex": "/(mailgun[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"](key-[a-f0-9]{32})['\"]/i",
        },
        "Mailgun public validation key": {
            "patternName": "Mailgun public validation key",
            "regex": "/(mailgun[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"](pubkey-[a-f0-9]{32})['\"]/i",
        },
        "Mailgun webhook signing key": {
            "patternName": "Mailgun webhook signing key",
            "regex": "/(mailgun[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-h0-9]{32}-[a-h0-9]{8}-[a-h0-9]{8})['\"]/i",
        },
        "Mapbox API token": {
            "patternName": "Mapbox API token",
            "regex": "/(pk\\.[a-z0-9]{60}\\.[a-z0-9]{22})/i",
        },
        "messagebird-api-token": {
            "patternName": "MessageBird API token",
            "regex": "/(messagebird[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{25})['\"]/i",
        },
        "MessageBird API client ID": {
            "patternName": "MessageBird API client ID",
            "regex": "/(messagebird[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-h0-9]{8}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{12})['\"]/i",
        },
        "New Relic user API Key": {
            "patternName": "New Relic user API Key",
            "regex": "/['\"](NRAK-[A-Z0-9]{27})['\"]/",
        },
        "New Relic user API ID": {
            "patternName": "New Relic user API ID",
            "regex": "/(newrelic[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([A-Z0-9]{64})['\"]/i",
        },
        "New Relic ingest browser API token": {
            "patternName": "New Relic ingest browser API token",
            "regex": "/['\"](NRJS-[a-f0-9]{19})['\"]/",
        },
        "npm access token": {
            "patternName": "npm access token",
            "regex": "/['\"](npm_[a-z0-9]{36})['\"]/i",
        },
        "Planetscale password": {
            "patternName": "Planetscale password",
            "regex": "/pscale_pw_[a-z0-9\\-_\\.]{43}/i",
        },
        "Planetscale API token": {
            "patternName": "Planetscale API token",
            "regex": "/pscale_tkn_[a-z0-9\\-_\\.]{43}/i",
        },
        "Postman API token": {
            "patternName": "Postman API token",
            "regex": "/PMAK-[a-f0-9]{24}\\-[a-f0-9]{34}/i",
        },
        "Pulumi API token": {
            "patternName": "Pulumi API token",
            "regex": "/pul-[a-f0-9]{40}/",
        },
        "Rubygem API token": {
            "patternName": "Rubygem API token",
            "regex": "/rubygems_[a-f0-9]{48}/",
        },
        "Sendgrid API token": {
            "patternName": "Sendgrid API token",
            "regex": "/SG\\.[a-z0-9_\\-\\.]{66}/i",
        },
        "Sendinblue API token": {
            "patternName": "Sendinblue API token",
            "regex": "/xkeysib-[a-f0-9]{64}\\-[a-z0-9]{16}/i",
        },
        "Shippo API token": {
            "patternName": "Shippo API token",
            "regex": "/shippo_(live|test)_[a-f0-9]{40}/",
        },
        "Linkedin Client secret": {
            "patternName": "Linkedin Client secret",
            "regex": "/(linkedin[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z]{16})['\"]/i",
        },
        "Linkedin Client ID": {
            "patternName": "Linkedin Client ID",
            "regex": "/(linkedin[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{14})['\"]/i",
        },
        "Twitch API token": {
            "patternName": "Twitch API token",
            "regex": "/(twitch[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\"]([a-z0-9]{30})['\"]/i",
        },
        "Typeform API token": {
            "patternName": "Typeform API token",
            "regex": "/(typeform[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}(tfp_[a-z0-9\\-_\\.=]{59})/i",
        },
        "Social Security Number": {
            "patternName": "Social Security Number",
            "regex": "/\\d{3}-\\d{2}-\\d{4}/",
        },
    }
