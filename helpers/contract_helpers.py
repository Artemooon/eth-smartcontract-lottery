from brownie import network, accounts, config, MockV3Aggregator, Contract, VRFCoordinatorV2Mock, LinkToken

from constants.fee_constants import DECIMALS, INITIAL_VALUE
from helpers.account_helpers import LOCAL_BLOCKCHAINS, get_account

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorV2Mock,
    "link_token": LinkToken,
}


def get_contract(contract_name: str):
    """ This function will grab the contract addresses  from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and return that mock contract

    Args:
        contract_name: str
    Returns:
        brownie.network.contract.ProjectContract: The most recently deployed version of this contract
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAINS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    LinkToken.deploy({"from": account})
    VRFCoordinatorV2Mock.deploy(config["networks"][network.show_active()]["fee"], config["networks"][network.show_active()]["fee"], {"from": account})
    print("Deployed mock")