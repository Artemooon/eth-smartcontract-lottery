from brownie import Lottery, accounts, config, network, exceptions

from helpers.account_helpers import LOCAL_BLOCKCHAINS, get_account
from helpers.contract_helpers import get_contract
from helpers.fund_helpers import fund_with_link
from scripts.deploy import deploy_lottery
from web3 import Web3
from web3.exceptions import BadResponseFormat
import pytest


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip()
    lottery = deploy_lottery()
    # 3,600 eth / usd
    # usdEntryFee is 50
    # 3,600/1 == 50/x == 0.13
    expected_entrance_fee = Web3.to_wei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    print("entrance_fee", entrance_fee)
    # Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_start():
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    with pytest.raises(BadResponseFormat):
        lottery.enter({"from": account, "value": lottery.getEntranceFee()})


def test_cant_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    assert lottery.players(0) == account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery.address)
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2


def test_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAINS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})

    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 10000})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee() + 10000})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee() + + 10000})

    fund_with_link(lottery.address)
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomaness(request_id, STATIC_RNG, lottery.address, {"from": account})

    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()

    assert lottery.recentWinnser() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery
