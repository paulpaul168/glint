def default_secrets() -> dict[str, dict[str, str]]:
    return {
        "gitlab_personal_access_token": {
            "name": "GitLab Personal Access Token",
            "regex": r"/glpat-[0-9a-zA-Z\\-]{20}/",
        },
        "AWS": {"name": "AWS Access Token", "regex": r"/AKIA[0-9A-Z]{16}/"},
        "PKCS8 private key": {
            "name": "PKCS8 private key",
            "regex": r"/-----BEGIN PRIVATE KEY-----/",
        },
        "RSA private key": {
            "name": "RSA private key",
            "regex": r"/-----BEGIN RSA PRIVATE KEY-----/",
        },
        "SSH private key": {
            "name": "SSH private key",
            "regex": r"/-----BEGIN OPENSSH PRIVATE KEY-----/",
        },
        "PGP private key": {
            "name": "PGP private key",
            "regex": r"/-----BEGIN PGP PRIVATE KEY BLOCK-----/",
        },
        "Github Personal Access Token": {
            "name": "Github Personal Access Token",
            "regex": r"/ghp_[0-9a-zA-Z]{36}/",
        },
        "Github OAuth Access Token": {
            "name": "Github OAuth Access Token",
            "regex": r"/gho_[0-9a-zA-Z]{36}/",
        },
        "SSH (DSA) private key": {
            "name": "SSH (DSA) private key",
            "regex": r"/-----BEGIN DSA PRIVATE KEY-----/",
        },
        "SSH (EC) private key": {
            "name": "SSH (EC) private key",
            "regex": r"/-----BEGIN EC PRIVATE KEY-----/",
        },
        "Github App Token": {
            "name": "Github App Token",
            "regex": r"/(ghu|ghs)_[0-9a-zA-Z]{36}/",
        },
        "Github Refresh Token": {
            "name": "Github Refresh Token",
            "regex": r"/ghr_[0-9a-zA-Z]{76}/",
        },
        "Shopify shared secret": {
            "name": "Shopify shared secret",
            "regex": r"/shpss_[a-fA-F0-9]{32}/",
        },
        "Shopify access token": {
            "name": "Shopify access token",
            "regex": r"/shpat_[a-fA-F0-9]{32}/",
        },
        "Shopify custom app access token": {
            "name": "Shopify custom app access token",
            "regex": r"/shpca_[a-fA-F0-9]{32}/",
        },
        "Shopify private app access token": {
            "name": "Shopify private app access token",
            "regex": r"/shppa_[a-fA-F0-9]{32}/",
        },
        "Slack token": {
            "name": "Slack token",
            "regex": r"/xox[baprs]-([0-9a-zA-Z]{10,48})?/",
        },
        "Stripe": {
            "name": "Stripe",
            "regex": r"/(?i)(sk|pk)_(test|live)_[0-9a-z]{10,32}/",
        },
        "PyPI upload token": {
            "name": "PyPI upload token",
            "regex": r"/pypi-AgEIcHlwaS5vcmc[A-Za-z0-9-_]{50,1000}/",
        },
        "Google (GCP) Service-account": {
            "name": "Google (GCP) Service-account",
            "regex": r'/\\"type\\": \\"service_account\\"/',
        },
        "Password in URL": {
            "name": "Password in URL",
            "regex": r"/[a-zA-Z]{3,10}:\\/\\/[^$][^:@]{3,20}:[^$][^:@]{3,40}@.{1,100}/",
        },
        "Heroku API Key": {
            "name": "Heroku API Key",
            "regex": r"/ (?i)(heroku[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12})['\\\"]/",
        },
        "Slack Webhook": {
            "name": "Slack Webhook",
            "regex": r"/https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}/",
        },
        "Twilio API Key": {
            "name": "Twilio API Key",
            "regex": r"/SK[0-9a-fA-F]{32}/",
        },
        "Age secret key": {
            "name": "Age secret key",
            "regex": r"/AGE-SECRET-KEY-1[QPZRY9X8GF2TVDW0S3JN54KHCE6MUA7L]{58}/",
        },
        "Facebook token": {
            "name": "Facebook token",
            "regex": r"/(?i)(facebook[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-f0-9]{32})['\\\"]/",
        },
        "Twitter token": {
            "name": "Twitter token",
            "regex": r"/(?i)(twitter[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-f0-9]{35,44})['\\\"]/",
        },
        "Adobe Client ID (Oauth Web)": {
            "name": "Adobe Client ID (Oauth Web)",
            "regex": r"/(?i)(adobe[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-f0-9]{32})['\\\"]/",
        },
        "Adobe Client Secret": {
            "name": "Adobe Client Secret",
            "regex": r"/(p8e-)(?i)[a-z0-9]{32}/",
        },
        "Alibaba AccessKey ID": {
            "name": "Alibaba AccessKey ID",
            "regex": r"/(LTAI)(?i)[a-z0-9]{20}/",
        },
        "Alibaba Secret Key": {
            "name": "Alibaba Secret Key",
            "regex": r"/(?i)(alibaba[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9]{30})['\\\"]/",
        },
        "Asana Client ID": {
            "name": "Asana Client ID",
            "regex": r"/(?i)(asana[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([0-9]{16})['\\\"]/",
        },
        "Asana Client Secret": {
            "name": "Asana Client Secret",
            "regex": r"/(?i)(asana[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9]{32})['\\\"]/",
        },
        "Atlassian API token": {
            "name": "Atlassian API token",
            "regex": r"/(?i)(atlassian[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9]{24})['\\\"]/",
        },
        "Bitbucket client ID": {
            "name": "Bitbucket client ID",
            "regex": r"/(?i)(bitbucket[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9]{32})['\\\"]/",
        },
        "Bitbucket client secret": {
            "name": "Bitbucket client secret",
            "regex": r"/(?i)(bitbucket[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9_\\-]{64})['\\\"]/",
        },
        "Beamer API token": {
            "name": "Beamer API token",
            "regex": r"/(?i)(beamer[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"](b_[a-z0-9=_\\-]{44})['\\\"]/",
        },
        "Clojars API token": {
            "name": "Clojars API token",
            "regex": r"/(CLOJARS_)(?i)[a-z0-9]{60}/",
        },
        "Contentful delivery API token": {
            "name": "Contentful delivery API token",
            "regex": r"/(?i)(contentful[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9\\-=_]{43})['\\\"]/",
        },
        "Contentful preview API token": {
            "name": "Contentful preview API token",
            "regex": r"/(?i)(contentful[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9\\-=_]{43})['\\\"]/",
        },
        "Databricks API token": {
            "name": "Databricks API token",
            "regex": r"/dapi[a-h0-9]{32}/",
        },
        "Discord API key": {
            "name": "Discord API key",
            "regex": r"/(?i)(discord[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-h0-9]{64})['\\\"]/",
        },
        "Discord client ID": {
            "name": "Discord client ID",
            "regex": r"/(?i)(discord[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([0-9]{18})['\\\"]/",
        },
        "Discord client secret": {
            "name": "Discord client secret",
            "regex": r"/(?i)(discord[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9=_\\-]{32})['\\\"]/",
        },
        "Doppler API token": {
            "name": "Doppler API token",
            "regex": r"/['\\\"](dp\\.pt\\.)(?i)[a-z0-9]{43}['\\\"]/",
        },
        "Dropbox API secret/key": {
            "name": "Dropbox API secret/key",
            "regex": r"/(?i)(dropbox[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9]{15})['\\\"]/",
        },
        "Dropbox short lived API token": {
            "name": "Dropbox short lived API token",
            "regex": r"/(?i)(dropbox[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"](sl\\.[a-z0-9\\-=_]{135})['\\\"]/",
        },
        "Dropbox long lived API token": {
            "name": "Dropbox long lived API token",
            "regex": r"/(?i)(dropbox[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"][a-z0-9]{11}(AAAAAAAAAA)[a-z0-9\\-_=]{43}['\\\"]/",
        },
        "Duffel API token": {
            "name": "Duffel API token",
            "regex": r"/['\\\"]duffel_(test|live)_(?i)[a-z0-9_-]{43}['\\\"]/",
        },
        "Dynatrace API token": {
            "name": "Dynatrace API token",
            "regex": r"/['\\\"]dt0c01\\.(?i)[a-z0-9]{24}\\.[a-z0-9]{64}['\\\"]/",
        },
        "EasyPost API token": {
            "name": "EasyPost API token",
            "regex": r"/['\\\"]EZAK(?i)[a-z0-9]{54}['\\\"]/",
        },
        "EasyPost test API token": {
            "name": "EasyPost test API token",
            "regex": r"/['\\\"]EZTK(?i)[a-z0-9]{54}['\\\"]/",
        },
        "Fastly API token": {
            "name": "Fastly API token",
            "regex": r"/(?i)(fastly[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9\\-=_]{32})['\\\"]/",
        },
        "Finicity client secret": {
            "name": "Finicity client secret",
            "regex": r"/(?i)(finicity[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9]{20})['\\\"]/",
        },
        "Finicity API token": {
            "name": "Finicity API token",
            "regex": r"/(?i)(finicity[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-f0-9]{32})['\\\"]/",
        },
        "Flutterweave public key": {
            "name": "Flutterweave public key",
            "regex": r"/FLWPUBK_TEST-(?i)[a-h0-9]{32}-X/",
        },
        "Flutterweave secret key": {
            "name": "Flutterweave secret key",
            "regex": r"/FLWSECK_TEST-(?i)[a-h0-9]{32}-X/",
        },
        "Flutterweave encrypted key": {
            "name": "Flutterweave encrypted key",
            "regex": r"/FLWSECK_TEST[a-h0-9]{12}/",
        },
        "Frame.io API token": {
            "name": "Frame.io API token",
            "regex": r"/fio-u-(?i)[a-z0-9-_=]{64}/",
        },
        "GoCardless API token": {
            "name": "GoCardless API token",
            "regex": r"/['\\\"]live_(?i)[a-z0-9-_=]{40}['\\\"]/",
        },
        "Grafana API token": {
            "name": "Grafana API token",
            "regex": r"/['\\\"]eyJrIjoi(?i)[a-z0-9-_=]{72,92}['\\\"]/",
        },
        "Hashicorp Terraform user/org API token": {
            "name": "Hashicorp Terraform user/org API token",
            "regex": r"/['\\\"](?i)[a-z0-9]{14}\\.atlasv1\\.[a-z0-9-_=]{60,70}['\\\"]/",
        },
        "Hubspot API token": {
            "name": "Hubspot API token",
            "regex": r"/(?i)(hubspot[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-h0-9]{8}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{12})['\\\"]/",
        },
        "Intercom API token": {
            "name": "Intercom API token",
            "regex": r"/(?i)(intercom[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9=_]{60})['\\\"]/",
        },
        "Intercom client secret/ID": {
            "name": "Intercom client secret/ID",
            "regex": r"/(?i)(intercom[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-h0-9]{8}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{12})['\\\"]/",
        },
        "Ionic API token": {
            "name": "Ionic API token",
            "regex": r"/ion_(?i)[a-z0-9]{42}/",
        },
        "Linear API token": {
            "name": "Linear API token",
            "regex": r"/lin_api_(?i)[a-z0-9]{40}/",
        },
        "Linear client secret/ID": {
            "name": "Linear client secret/ID",
            "regex": r"/(?i)(linear[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-f0-9]{32})['\\\"]/",
        },
        "Lob API Key": {
            "name": "Lob API Key",
            "regex": r"/(?i)(lob[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]((live|test)_[a-f0-9]{35})['\\\"]/",
        },
        "Lob Publishable API Key": {
            "name": "Lob Publishable API Key",
            "regex": r"/(?i)(lob[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]((test|live)_pub_[a-f0-9]{31})['\\\"]/",
        },
        "Mailchimp API key": {
            "name": "Mailchimp API key",
            "regex": r"/(?i)(mailchimp[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-f0-9]{32}-us20)['\\\"]/",
        },
        "Mailgun private API token": {
            "name": "Mailgun private API token",
            "regex": r"/(?i)(mailgun[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"](key-[a-f0-9]{32})['\\\"]/",
        },
        "Mailgun public validation key": {
            "name": "Mailgun public validation key",
            "regex": r"/(?i)(mailgun[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"](pubkey-[a-f0-9]{32})['\\\"]/",
        },
        "Mailgun webhook signing key": {
            "name": "Mailgun webhook signing key",
            "regex": r"/(?i)(mailgun[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-h0-9]{32}-[a-h0-9]{8}-[a-h0-9]{8})['\\\"]/",
        },
        "Mapbox API token": {
            "name": "Mapbox API token",
            "regex": r"/(?i)(pk\\.[a-z0-9]{60}\\.[a-z0-9]{22})/",
        },
        "messagebird-api-token": {
            "name": "MessageBird API token",
            "regex": r"/(?i)(messagebird[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9]{25})['\\\"]/",
        },
        "MessageBird API client ID": {
            "name": "MessageBird API client ID",
            "regex": r"/(?i)(messagebird[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-h0-9]{8}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{4}-[a-h0-9]{12})['\\\"]/",
        },
        "New Relic user API Key": {
            "name": "New Relic user API Key",
            "regex": r"/['\\\"](NRAK-[A-Z0-9]{27})['\\\"]/",
        },
        "New Relic user API ID": {
            "name": "New Relic user API ID",
            "regex": r"/(?i)(newrelic[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([A-Z0-9]{64})['\\\"]/",
        },
        "New Relic ingest browser API token": {
            "name": "New Relic ingest browser API token",
            "regex": r"/['\\\"](NRJS-[a-f0-9]{19})['\\\"]/",
        },
        "npm access token": {
            "name": "npm access token",
            "regex": r"/['\\\"](npm_(?i)[a-z0-9]{36})['\\\"]/",
        },
        "Planetscale password": {
            "name": "Planetscale password",
            "regex": r"/pscale_pw_(?i)[a-z0-9\\-_\\.]{43}/",
        },
        "Planetscale API token": {
            "name": "Planetscale API token",
            "regex": r"/pscale_tkn_(?i)[a-z0-9\\-_\\.]{43}/",
        },
        "Postman API token": {
            "name": "Postman API token",
            "regex": r"/PMAK-(?i)[a-f0-9]{24}\\-[a-f0-9]{34}/",
        },
        "Pulumi API token": {
            "name": "Pulumi API token",
            "regex": r"/pul-[a-f0-9]{40}/",
        },
        "Rubygem API token": {
            "name": "Rubygem API token",
            "regex": r"/rubygems_[a-f0-9]{48}/",
        },
        "Sendgrid API token": {
            "name": "Sendgrid API token",
            "regex": r"/SG\\.(?i)[a-z0-9_\\-\\.]{66}/",
        },
        "Sendinblue API token": {
            "name": "Sendinblue API token",
            "regex": r"/xkeysib-[a-f0-9]{64}\\-(?i)[a-z0-9]{16}/",
        },
        "Shippo API token": {
            "name": "Shippo API token",
            "regex": r"/shippo_(live|test)_[a-f0-9]{40}/",
        },
        "Linkedin Client secret": {
            "name": "Linkedin Client secret",
            "regex": r"/(?i)(linkedin[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z]{16})['\\\"]/",
        },
        "Linkedin Client ID": {
            "name": "Linkedin Client ID",
            "regex": r"/(?i)(linkedin[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9]{14})['\\\"]/",
        },
        "Twitch API token": {
            "name": "Twitch API token",
            "regex": r"/(?i)(twitch[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}['\\\"]([a-z0-9]{30})['\\\"]/",
        },
        "Typeform API token": {
            "name": "Typeform API token",
            "regex": r"/(?i)(typeform[a-z0-9_ .\\-,]{0,25})(=|>|:=|\\|\\|:|<=|=>|:).{0,5}(tfp_[a-z0-9\\-_\\.=]{59})/",
        },
        "Social Security Number": {
            "name": "Social Security Number",
            "regex": r"/\\d{3}-\\d{2}-\\d{4}/",
        },
    }
