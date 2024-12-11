from helpers.account_helpers import get_account
from helpers.contract_helpers import get_contract


def fund_with_link(contract_address, account=None, link_token=None, amount=25000000000000000000):
    account = account if account else get_account()
    link_token = link_token or get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # Creating a link token contract from the interface
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund the contract")
    return tx
