PROXY_URL = "http://xxx.xxx.xxx.xxx:xxxx" # or None
MODEL = "gpt-3.5-turbo-0125"
# for ModelAccesser_V2
# api key & base url for openai
# better have more than one account to avoid the rate limit
ACCOUNTS = [
    {
        "api_key": "sk-xxxx",
        "base_url": "https://your.gpt.proxy.base_url" # or None
    },
    {
        "api_key": "sk-xxxx",
        "base_url": "https://your.gpt.proxy.base_url"

    }
]

# for ModelAccesser_V1
# cookie: __Secure-next-auth.session-token available from https://chat.openai.com/
# better have more than one account to avoid the rate limit
SESSION_TOKEN = ["",""]