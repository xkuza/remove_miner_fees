# mining_fees_remover

Removes miner fees using nfqueue.
-Tested on ubuntu 16.04 mining on nanopool with claymore dual ethereum miner for linux version 9.4.
-Tested also with Claymore 10.4 for Windows on ethermine via VPN connection with the script running on the server (ubuntu 16.04). In this case it works for all the mining rigs connected to the VPN server.

# How does this work?

It modifies outgoing packets using nfqueue, substituting the dev fee wallet address with your own wallet address.

# Setup

Disable ufw

```
sudo ufw disable
```

Install python-nfqueue and python-scapy. Has been tested with python-nfqueue 0.5-1build2 and python-scapy 2.2.0-1 from the ubuntu 16.04 repositories, if using different versions you may need to modify the code as described [here](https://github.com/gkovacs/remove_miner_fees/issues/1)

```
sudo apt-get install python-nfqueue python-scapy
```

Download the program and run it as root (nfqueue needs to be run as root). Keep it running in the background

```
wget https://raw.githubusercontent.com/xkuza/remove_miner_fees/master/nodevfee.py
sudo python nodevfee.py
```

Now you can start the miner

```
./ethdcrminer64 -epool eth-eu.nanopool.org:9999 -ewal 0xf5ec8c6afc3dd2712b43b95128813bd09787a782/xkuza -epsw x
```

# Specifying where mining fees should be redirected

Note that this program redirects mining fees to `0xf5ec8c6afc3dd2712b43b95128813bd09787a782` by default. You will want to substitute that with your own wallet address in the source code by editing the variable `my_eth_address`

# Using pools other than nanopool

Note that this program assumes port `9999` by default (used by nanopool). Substitute the port by editing the number after `--dport 9999` in the `iptables` command.


# Original Author

[Geza Kovacs](https://github.com/gkovacs/)

# Licence

[GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)

# Original Donations

ETH `0xb70fc6f9865ce18c20d90ebf067d9951918f8933`

BTC `1PYmDbxXDS9FjAdH8jxE2stdf1Yrsvqdos`

ZEC `t1Yi9izeKkWbVtXRrQNdUbs7BdZVbwVVRcw`

SIA `74ab711929bfc28359c8485a4e488d2f89b623771788fbeca7e7f5fe993ec691fec713e9f35b`
