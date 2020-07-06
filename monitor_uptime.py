import requests
import json

remote_url = "https://rpc.betanet.near.org"
local_url = "http://127.0.0.1:3030"
pool_id = "stakepool2.xiaoshen.betanet"


def rpc_status(url):
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "status",
        "params": '[]',
        "id": "dontcare",
    })
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data=data, headers=headers)
    return json.loads(r.content)


def rpc_valdiators(url):
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "validators",
        "params": [None],
        "id": "dontcare",
    })
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data=data, headers=headers)
    return json.loads(r.content)


def send_alert():
    pass


if __name__ == "__main__":
    print("------")
    remote_status = rpc_status(remote_url)

    # remote node version
    remote_node_version_build = remote_status.get('result').get('version').get('build')
    remote_node_version_version = remote_status.get('result').get('version').get('version')
    print("remote node version is: {}, {}".format(remote_node_version_build, remote_node_version_version))

    local_status = rpc_status(local_url)

    # local node version
    local_node_version_build = local_status.get('result').get('version').get('build')
    local_node_version_version = local_status.get('result').get('version').get('version')
    print("local node version is: {}, {}".format(local_node_version_build, local_node_version_version))

    # compare remote and local
    if remote_node_version_version != local_node_version_version:
        print("remote({})and local({}) version is not same, consider upgrade.".format(remote_node_version_version,
                                                                                      local_node_version_version))
        send_alert()

    # check if we are validator in the remote
    is_validator = False
    for validator in remote_status.get('result').get('validators'):
        if validator.get('account_id') == pool_id:
            is_validator = True

    if is_validator:
        print("we are validators")
    else:
        print("we are not validators")
        send_alert()

    # check produced blocks
    r = rpc_valdiators(remote_url)
    for cv in r.get('result').get('current_validators'):
        if cv.get('account_id') == pool_id:
            print("produced blocks:", cv.get('num_produced_blocks'))
            print("expected blocks:", cv.get('num_expected_blocks'))
            if cv.get('num_produced_blocks') / cv.get('num_expected_blocks') < 0.9:
                print("pay attention to produced blocks!")
                send_alert()

    # check kicked out validators
    for cv in r.get('result').get('prev_epoch_kickout'):
        if cv.get('account_id') == pool_id:
            print("Oh, kicked out prev epoch, resaon:{}".format(cv.get('reason')))
            send_alert()

    print("End.")
