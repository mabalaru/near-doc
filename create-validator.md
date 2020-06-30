# Install near-shell

## Check node version

The version should be 10+.

```
node --version
v14.0.0

```



## Install

```
npm install -g near-shell
```

# Set environment variables

```
export NODE_ENV=betanet
```

Then check it

```
echo $NODE_ENV
betanet
```

# Create working directory
We set it to `~/stakewars`, but you can set your own.

```
mkdir stakewars && cd stakewars
```

# Create Account
## Wallet Account
Go to https://wallet.betanet.near.org/create/ ,the near wallet to create account.

### Choose name

![](./images/1.png?raw=true)


we choose the name `xiaoshen.betanet` as account name below.

### How to recovery 

![](./images/2.png?raw=true)

### Backup recovery phrase

![](./images/3.png?raw=true)

### Verify phrase

![](./images/4.png?raw=true)

After clicking verify, we create account successfully!


## Login account in near-shell

At `~/stakewars`, run the `near login`, it will outputs a url, jump to the url. 

It will ask you to do a auth.

![](./images/5.png?raw=true)


confirm again

![](./images/6.png?raw=true)


Then go back to the terminal and enter the account name, like below:

![](./images/7.png?raw=true)

Now we can check the credential files in `~/.near-credentials/betanet/`



## Stake Pool Account

Create our stake pool account, we choose the name `stakepool.xiaoshen.betanet` as the pool id below.

```
near create_account stakepool.xiaoshen.betanet --masterAccount=xiaoshen.betanet
```

Also, you can set the initial balance as:

```
near create_account stakepool.xiaoshen.betanet --masterAccount=xiaoshen.betanet --initialBalance 10
```

We can check the related credential files at `~/.near-credentials/betanet/`.


# Deploy node

## Open port

First Open 24567 for 0.0.0.0/0.

## Install nearup 
nearup is a tool to manage near nodes.

```
# install the dependency
sudo apt update
sudo apt install python3 git curl

# install nearup
curl --proto '=https' --tlsv1.2 -sSfL https://up.near.dev | python3
```

## Compile nearcore (Optional)
We can use docker to start nearcore directly, but we can also choose to complie and start one.

```
# install dependencies,like rustup,clang, ...


#  build nearcore
cd ~ && git clone -b beta https://github.com/nearprotocol/nearcore.git && cd nearcore
git branch
make release

# source ENV
source $HOME/.nearup/env
```

Then we can use `nearup betanet --nodocker --binary-path ~/nearcore/target/release` to start the node.

However,  we will show the docker way below.



## Start node
Use `nearup betanet` to start node.

![](./images/8.png?raw=true)

Then enter the stake pool id: `stakepool.xiaoshen.betanet`.

![](./images/9.png?raw=true)

## Check logs

```
docker logs -f nearcore
```

# Deploy and run a contract stake pool

## Download contract

At directory `~/stakewars/`,

```
git clone https://github.com/near/initial-contracts && cd initial-contracts/staking-pool
```

## Install rustup

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Compile contact

```
rustup target add wasm32-unknown-unknown
./build.sh

```

## Check the public key

```
cat ~/.near/betanet/validator_key.json |grep "public_key"
  "public_key": "ed25519:AnzkYpiQhcy7BbpxHwHpmg5podmzapmgN6GZ2yUjoLUf",

```

## Deploy contract

Specify the wasmFile as the one compiled before.

```
near deploy --accountId=stakepool.xiaoshen.betanet --wasmFile=initial-contracts/staking-pool/res/staking_pool.wasm
```

The outputs like below:

![](./images/10.png?raw=true)

## Initialize pool account

Here we set the fee 10%.

```
near call stakepool.xiaoshen.betanet new '{"owner_id": "xiaoshen.betanet", "stake_public_key": "AnzkYpiQhcy7BbpxHwHpmg5podmzapmgN6GZ2yUjoLUf", "reward_fee_fraction": {"numerator": 10, "denominator": 100}}' --account_id xiaoshen.betanet
```

The outputs like below:

![](./images/11.png?raw=true)


## Lock the pool

```
near keys stakepool.xiaoshen.betanet | grep public_key


near delete-key --accessKey !{The Output upper cmd} --accountId stakepool.xiaoshen.betanet
```

# Delegation

## Deposit

Let's deposit 10 Near.

```
near call stakepool.xiaoshen.betanet deposit '{}' --accountId xiaoshen.betanet --amount 10
```

The outputs like below:

![](./images/12.png?raw=true)

## Stake

Note, we use yocto here:

```
near call stakepool.xiaoshen.betanet stake '{"amount": "1000000000000000000000000"}' --accountId xiaoshen.betanet
```

The outputs like below:

![](./images/13.png?raw=true)


