import os

try:
    from circle.web3 import configurations
except:
    configurations = None
try:
    from circle.web3 import developer_controlled_wallets
except:
    developer_controlled_wallets = None
try:
    from circle.web3 import user_controlled_wallets
except:
    user_controlled_wallets = None
try:
    from circle.web3 import smart_contract_platform
except:
    smart_contract_platform = None

CIRCLE_PUBLIC_KEY = None
API_KEY = None
ENTITY_SECRET = None
CONF_CLIENT = None


def init_configurations_client(user_agent=None, **kwargs):
    global CONF_CLIENT
    global API_KEY
    if not CONF_CLIENT:
        if 'api_key' in kwargs:
            API_KEY = kwargs['api_key']
        conf = configurations.Configuration(access_token=API_KEY, **kwargs)
        client = configurations.ApiClient(configuration=conf, user_agent=user_agent)
        CONF_CLIENT = client
        load_public_key()


def init_developer_controlled_wallets_client(api_key=None, entity_secret=None, user_agent=None, **kwargs):
    global API_KEY
    global ENTITY_SECRET
    if api_key is None:
        api_key = load_access_token()
    if entity_secret is None:
        entity_secret = load_entity_secret()
    API_KEY = api_key
    ENTITY_SECRET = entity_secret
    init_configurations_client(user_agent)
    conf = developer_controlled_wallets.Configuration(
        access_token=api_key,
        entity_secret=entity_secret,
        public_key=get_public_key(),
        **kwargs
    )
    return developer_controlled_wallets.ApiClient(configuration=conf, user_agent=user_agent)


def init_user_controlled_wallets_client(api_key=None, user_agent=None, **kwargs):
    global API_KEY
    if api_key is None:
        api_key = load_access_token()
    API_KEY = api_key
    init_configurations_client(user_agent)
    conf = user_controlled_wallets.Configuration(
        access_token=api_key,
        **kwargs
    )
    return user_controlled_wallets.ApiClient(configuration=conf, user_agent=user_agent)


def init_smart_contract_platform_client(api_key=None, entity_secret=None, user_agent=None, **kwargs):
    global API_KEY
    global ENTITY_SECRET
    if api_key is None:
        api_key = load_access_token()
    if entity_secret is None:
        entity_secret = load_entity_secret()
    API_KEY = api_key
    ENTITY_SECRET = entity_secret
    init_configurations_client(user_agent)
    conf = smart_contract_platform.Configuration(
        access_token=api_key,
        entity_secret=entity_secret,
        public_key=get_public_key(),
        **kwargs
    )
    return smart_contract_platform.ApiClient(configuration=conf, user_agent=user_agent)


def load_public_key():
    global CIRCLE_PUBLIC_KEY
    global CONF_CLIENT
    init_configurations_client()
    if not CIRCLE_PUBLIC_KEY:
        api_instance = configurations.DeveloperAccountApi(CONF_CLIENT)
        try:
            api_response = api_instance.get_public_key()
            CIRCLE_PUBLIC_KEY = api_response.data.public_key
        except configurations.ApiException as e:
            print("Exception when calling DeveloperAccountApi->get_public_key: %s\n" % e)


def get_public_key():
    global CIRCLE_PUBLIC_KEY
    if CIRCLE_PUBLIC_KEY is None:
        init_configurations_client()
    return CIRCLE_PUBLIC_KEY


def load_access_token():
    try:
        return os.environ["CIRCLE_WEB3_API_KEY"]
    except:
        raise Exception("No API Key found")


def load_entity_secret():
    try:
        return os.environ["CIRCLE_ENTITY_SECRET"]
    except:
        raise Exception("No Entity Secret found")
