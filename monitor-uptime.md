# How to monitor uptime


We can use rpc methods mentioned at https://docs.near.org/docs/interaction/rpc to query info about our validators.

I create a simple python script to show this.

You can check the code here: [](./monitor_uptime.py).

## monitor node version

we can query remote rpc("https://rpc.betanet.near.org") and local node rpc("http://127.0.0.1:3030") to know if we need to upgrade.

Using "status" rpc to query status:

```
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

```

query remote and local, then compare. if not same, send_alert.
```
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
```



## monitor if we are validators

Also extract data from status rpc, if not validator , send alert!
```
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
``` 

## monitor produced blocks


Using "validators" rpc to query how many blocks we need and have produced.

If the percentage is below 90%, send alert.

```
    # check produced blocks
    r = rpc_valdiators(remote_url)
    for cv in r.get('result').get('current_validators'):
        if cv.get('account_id') == pool_id:
            print("produced blocks:", cv.get('num_produced_blocks'))
            print("expected blocks:", cv.get('num_expected_blocks'))
            if cv.get('num_produced_blocks') / cv.get('num_expected_blocks') < 0.9:
                print("pay attention to produced blocks!")
                send_alert()

```

## monitor kicked validators 

Using "validators" rpc to query if we are kicked out. If it is, send alert. 
```
    # check kicked out validators
    for cv in r.get('result').get('prev_epoch_kickout'):
        if cv.get('account_id') == pool_id:
            print("Oh, kicked out prev epoch, resaon:{}".format(cv.get('reason')))
            send_alert()
```

## Demo Result
```
python3 monitor_uptime.py

remote node version is: 68f22b1d, 1.1.0
local node version is: 68f22b1d, 1.1.0
we are validators
produced blocks: 65
expected blocks: 66
End.
```

## Notice
1. You should change the pool_id in the script to yours.
2. The script should be add to cron jobs to run once for a while. 
3. Currently `send_alert()` methods is not implemented. We just use `print` here, 
but you can implemente `send_alert` to send email or message or to grafana etc.

