PROXY_URL = None #"http://xxx.xxx.xxx.xxx:xxxx" # or None
MODEL = 'gpt-3.5-turbo-0125' #gpt-4o-mini-2024-07-18' or 'gpt-3.5-turbo-0125'

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
