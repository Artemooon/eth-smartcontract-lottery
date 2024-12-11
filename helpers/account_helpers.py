from brownie import network, accounts, config

LOCAL_BLOCKCHAINS = ["development",  "ganache-local"]
FORKED_LOCAL_BLOCKCHAINS = ["mainnet-fork-dev"]


def get_account(index=None, _id=None):
    if index:
        return accounts[index]
    if _id:
        accounts.load(_id)
    if network.show_active() in LOCAL_BLOCKCHAINS or network.show_active() in FORKED_LOCAL_BLOCKCHAINS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])
