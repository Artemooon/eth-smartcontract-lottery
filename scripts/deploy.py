from helpers.contract_helpers import get_contract
from helpers.account_helpers import get_account
from helpers.fund_helpers import fund_with_link
from brownie import Lottery, config, network
import time


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(get_contract("eth_usd_price_feed").address,
                   get_contract("vrf_coordinator").address,
                   get_contract("link_token").address,
                   config["networks"][network.show_active()]["fee"],
                   config["networks"][network.show_active()]["keyhash"],
                   {"from": account},
                   publish_source=config["networks"][network.show_active()].get("verify", False),
                   )
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    start_lottery_tx = lottery.startLottery({"from": account})
    start_lottery_tx.wait(1)
    print("Lottery has started")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    entrance_fee = lottery.getEntranceFee() + 100000000
    enter_lottery_tx = lottery.enter({"from": account, "value": entrance_fee})
    enter_lottery_tx.wait(1)
    print("You entered the lottery")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)

    end_lottery_tx = lottery.endLottery({"from": account})
    end_lottery_tx.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
