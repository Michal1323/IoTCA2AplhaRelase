from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

server_UUID = "ec0f9ad2-37e5-11eb-adc1-0242ac120002"   # this is our own.
cipherKey = "mycypher"
myChannel = "IOTCA"


############################


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-019b1a54-34ce-11eb-99ef-fa1b309c1f97'  # AMARAS SUSCRUBE KEY
pnconfig.publish_key = 'pub-c-4b294d7e-8be1-4dff-9ba7-d18d80953efd'  # AMARAS PUBLISH KEY
pnconfig.secret_key = "sec-c-NTM0ZjZmYjItYjJhYy00NGNlLWIwYzctYzI4MzNjYjZmOWIz"  # VISIBLE ON AMARAS PUBNUB
pnconfig.uuid = server_UUID  # need to generate
pnconfig.cipher_key = cipherKey
pubnub = PubNub(pnconfig)


def grant_access(auth_key, read, write):
    if read is True and write is True:
        grant_read_and_write_access(auth_key)
    elif read is True:
        grant_read_access(auth_key)
    elif write is True:
        grant_write_access(auth_key)
    else:
        revoke_access(auth_key)


def grant_read_and_write_access(auth_key):
    v = pubnub.grant() \
        .read(True) \
        .write(True) \
        .channels(myChannel) \
        .auth_keys(auth_key) \
        .ttl(6000) \
        .sync()
    print("------------------------------------")
    print("--- Granting Read & Write Access ---")
    for key, value in v.status.original_response.items():
        print(key, ":", value)
    print("------------------------------------")


def grant_read_access(auth_key):
    v = pubnub.grant() \
        .read(True) \
        .channels(myChannel) \
        .auth_keys(auth_key) \
        .ttl(6000) \
        .sync()
    print("------------------------------------")
    print("--- Granting Read Access ---")
    for key, value in v.status.original_response.items():
        print(key, ":", value)
    print("------------------------------------")


def grant_write_access(auth_key):
    v = pubnub.grant() \
        .write(True) \
        .channels(myChannel) \
        .auth_keys(auth_key) \
        .ttl(6000) \
        .sync()
    print("------------------------------------")
    print("--- Granting Write Access ---")
    for key, value in v.status.original_response.items():
        print(key, ":", value)
    print("------------------------------------")


def revoke_access(auth_key):
    v = pubnub.revoke() \
        .channels(myChannel) \
        .auth_keys(auth_key) \
        .sync()
    print("------------------------------------")
    print("--- Revoking Access ---")
    for key, value in v.status.original_response.items():
        print(key, ":", value)
    print("------------------------------------")
