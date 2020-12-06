from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

server_UUID = "631ec964-3407-11eb-adc1-0242ac120002"
cipherKey = "myCipherKey"
myChannel = "JLRSPY"

############################
pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'your subscribe key'
pnconfig.publish_key = 'your public key'
pnconfig.secret_key = "your secret key"
pnconfig.uuid = server_UUID
pnconfig.cipher_key = cipherKey
pubnub = PubNub(pnconfig)



def grantAccess(auth_key, read, write):
    if read is True and write is True:
        grantReadAndWriteAccess(auth_key)
    elif read is True:
        grantReadAccess(auth_key)
    elif write is True:
        grantWriteAccess(auth_key)
    else:
        revokeAccess(auth_key)


def grantReadAndWriteAccess(auth_key):
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


def grantReadAccess(auth_key):
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


def grantWriteAccess(auth_key):
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


def revokeAccess(auth_key):
    v = pubnub.revoke() \
        .channels(myChannel) \
        .auth_keys(auth_key) \
        .sync()
    print("------------------------------------")
    print("--- Revoking Access ---")
    for key, value in v.status.original_response.items():
        print(key, ":", value)
    print("------------------------------------")
