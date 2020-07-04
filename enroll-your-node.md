# Enroll Your Node
## Pull request to the VALIDATORS.md file

You can go to https://github.com/nearprotocol/stakewars/blob/master/VALIDATORS.md click the pencil icon to edit directly or fork the stakewars repo, then clone it to your local, add with your favourite editor, then push to your repo, then do a pull request to the stakewars.


We will show the first one:

1.Click the right pencil icon:

![](./images/do-pr-01.png?raw=true)

2.Then add one line with following format:

```
| Logo | Validator | Blurb | Account ID | Fees | Country | Pool ID | Locked |
```

such as:

```
| :) | xiaoshen | Near the future. | @xiaoshen.betanet | 10% | CN | [@stakepool2.xiaoshen.betanet](https://explorer.betanet.near.org/accounts/stakepool2.xiaoshen.betanet) | YES |
```

3.click the propose change button

![](./images/do-pr-02.png?raw=true)

After this, click "Create pull request" button. Then you just need wait it to be merged.

## Lock your contract

Suppose our pool id is `stakepool.xiaoshen.betanet`.

first check the public key:

```
near keys stakepool.xiaoshen.betanet | grep public_key
```

then lock your contract by:

```
near delete-key --accessKey 2dUvtR2okEYHK9vXCt8bVJ7Kvr5c66gammqJtLHEDBFf --accountId zpool
```

if you succeed, you can see the transaction in the explorer: https://explorer.betanet.near.org/, and the pool account:

![](./images/lock-contract.png?raw=true)

## Delegate some tokens

Let's deposit 10 Near.

```
near call stakepool.xiaoshen.betanet deposit '{}' --accountId xiaoshen.betanet --amount 10
```

The outputs like below:

![](./images/12.png?raw=true)

Then Stake 10 Near,

Note, we use yocto here `(1 NEAR= 10^24 yocto)`:

```
near call stakepool.xiaoshen.betanet stake '{"amount": "1000000000000000000000000"}' --accountId xiaoshen.betanet
```

The outputs like below:

![](./images/13.png?raw=true)


## Become a validator

If you get enough tokens,you will enter valdiators set.

You can check validators set as:

```
# This epoch
near validators current

# Next epoch
near validators next

# Proposal epoch
near validators proposal

```


## Check that your pool

First you can check as upper steps, is the pool in the validators set.


Next, check the seat price:

```
near state stakingPool_ID
```

Your pool's stake should be larger than the seat price.


Also, you can open the logs and see if we are a validator:
```
nearup logs -f

# or

docker logs -f nearcore

```

If you see "V" in the logs, it means you are a validator.


![](./images/validator-logs.png?raw=true)

The `98` after V means there are 98 validators total.
