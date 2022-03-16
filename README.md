# Rari Fuse Assets for Dune Analytics

There isn't enough information in on-chain calls & events to easily get a full picture of Rari Fuse pools on Dune Analytics.  This eth-brownie script queries the Rari Fuse contracts on Ethereum mainnet and creates a [Dune User-Generated Table](https://docs.dune.xyz/data-tables/data-tables/user-generated) SQL file containing the Fuse Pool, Fuse fToken and underlying token details.


## Prerequisites

Please install or have installed the following:

- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)
## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already. Here is a simple way to install brownie.

```bash
pip install eth-brownie
```
Or, if that doesn't work, via pipx
```bash
pip install --user pipx
pipx ensurepath
# restart your terminal
pipx install eth-brownie
```

2. [Install ganache-cli](https://www.npmjs.com/package/ganache-cli)

```bash
npm install -g ganache-cli
```

3. Set up Brownie Environment

Configure .env file in the rari_fuse_sql folder with an Infura or Alchemy API ID, and an etherscan API id:

```
export ETHERSCAN_TOKEN=<your etherscan api id>
export WEB3_ALCHEMY_PROJECT_ID=<your api id>
#or
export WEB3_INFURA_PROJECT_ID=<your api id>
```

If using Alchemy, switch to Alchemy providers using:

```bash
brownie networks set_provider alchemy
```

## Quickstart


1. Clone this repo

```bash
git clone https://github.com/scottincrypto/dune-rari-fuse-assets
```

2. Run the script

```
cd rari_fuse_sql
brownie run fusepools
```

3. Execute the SQL

The contents of the resulting output file rari.sql can be copy/pasted into Dune Analytics to refresh the token list
