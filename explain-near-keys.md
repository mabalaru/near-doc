# keys types
There are 3 types of key pairs on NEAR platform:

- signer keys (aka. account keys, access keys, etc)
- validator keys
- node keys

I won't repeat it here, but you can read it more at [near documentation](https://docs.near.org/docs/validator/keys).


# near login

## what is near-shell?

Near-Shell is a Node.js application that uses the nearlib library to connect to the Near-Shell platform, generate secure keys and send transactions on your behalf (the account under which we are logged in).


## how does it work?

near-shell will use the env to decide which network in use, so we need to `export NODE_ENV = betanet` first to tell near-shell that we work on betanet.

then use `near login`, it will output a url which we can follow and confirm the action in our betanet wallet account. Then we need to write the username in the shell.

After a successful login, the keys are generated in json format along the path:

```
~/.near-credentials/betanet
```

The content of the key as follows:

```
{"account_id":"xiaoshen.betanet","public_key":"ed25519:EBHLC47HTu9xScxxxxxxxxxxxxxxxxxxxjxC3u","private_key":"ed25519:xxxxxxxxxxxxxxxxxx"}
```

you can check that it contains "account_id" and key pairs.




# manage backup

## near login backup

Just backup the folder `~/.near-credentials/betanet`.

In order to recover from it, we need to transfer this folder to our user's home directory without having to log in.


Say we want to call contract with account we doesn't login, it fails:

![](./images/near-shell-fail.png?raw=true)


After copy the account file in `~/.near-credentials/betanet`, it works:

![](./images/near-shell-success.png?raw=true)

## signer keys backup
Just backup the Mnemonic code when you create the wallet

## validator keys backup
They are created at `~/.near/betanet/validator_key.json`.

You can reset and replace them after shutting down the node.

Just backup the file is ok.

## node keys backup


They are created at `~/.near/betanet/node_key.json` when you create new node. 

No need to backup.

