"""This module gets all assets from all Rari Fuse pools and outputs SQL for use in Dune Analytics
"""
import json
#import sys
#import requests
from brownie import Contract


def main():
    """main"""
    all_assets = get_all_assets()
    query = generate_sql_query(all_assets)

    with open('rari.sql', 'w') as f:
        f.write(query)
        f.close()


def get_all_assets():
    """Gets the pools from the FusePoolDirectory and gets the assets from each pool.
        The assets are returned as a list of tuples, which is appended to the existing list.
        Contract objects are stored as an alias to persist between sessions for speed up on subsequent runs.
    """
    #Contract('FusePoolDirectory').set_alias(alias=None) #uncomment to clear contract aliases for troubleshooting
    try: 
        Contract('FusePoolDirectory').alias
    except ValueError:
        Contract.from_explorer('0x835482FE0532f169024d5E9410199369aAD5C77E').set_alias('FusePoolDirectory', persist=True)

    fuse_pool_directory = Contract('0x835482FE0532f169024d5E9410199369aAD5C77E')
    all_pools = fuse_pool_directory.getAllPools()

    index = 0
    pool_start = 0 #skip pools & start here
    pool_count = 10000 #stop before index for this many pools
    all_assets = []
    for pool in all_pools:
        if index < pool_count and index >= pool_start:
            assets_return_val = get_assets_from_pool(index, pool[0], pool[2])
            all_assets += assets_return_val
        index += 1

    return all_assets



def get_assets_from_pool(pool_index, pool_name, comptroller):
    """Gets the assets from the pool specified by comptroller.
        Returns a list of tuples, with each element containing the details of an asset in a pool.
        Contract objects are stored as an alias to persist between sessions for speed up on subsequent runs.
    """
    #using a local copy of abi for speed & convenience.  Retrieved from etherscan '0xE16DB319d9dA7Ce40b666DD2E365a4b8B3C18217'
    comptroller_abi = json.loads(open('interfaces/comptroller.json').read())
    #Contract('comptroller_' + comptroller).set_alias(alias=None)  #uncomment to clear contract aliases for troubleshooting
    try: 
        Contract('comptroller_' + comptroller).alias
    except ValueError:
        Contract.from_abi('Comptroller', comptroller, comptroller_abi).set_alias('comptroller_' + comptroller, persist=True)
    

    # nitialise the comptroller contract & grab the list of pool assets
    pool_contract = Contract('comptroller_' + comptroller)

    fuse_pool_assets = pool_contract.getAllMarkets()

    #using a local copy for speed & convenience.  Retrieved from etherscan '0x67Db14E73C2Dce786B5bbBfa4D010dEab4BBFCF9'
    cerc20_abi = json.loads(open('interfaces/CErc20Delegate.json').read())
    #print(cerc20_abi)

    #loop through the data & store in list of tuples
    return_list = []
    for asset in fuse_pool_assets:
        #Contract('token_' + asset[0]).set_alias(alias=None)  #uncomment to clear contract aliases for troubleshooting
        
        #get the ftoken object
        try: 
            Contract('token_' + asset).alias
        except ValueError:
            #using local abi as etherscan isn't reliably detecting asset tokens as proxy contracts
            Contract.from_abi('CErc20Delegate', asset, cerc20_abi).set_alias('token_' + asset, persist=True)

        ftoken_contract = Contract('token_' + asset)
        
        #get the underlying token
        underlying = ftoken_contract.underlying()

        #change out wETH for ETH so that ERC20 methods work
        if underlying == '0x0000000000000000000000000000000000000000':
            underlying = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

        try: 
            Contract('token_' + underlying).alias
        except ValueError:
            #lazily using CErc20Delegate for underlying because it implements .name, .decimals, .symbol 
            Contract.from_abi('CErc20Delegate', underlying, cerc20_abi).set_alias('token_' + underlying, persist=True)

        underlying_contract = Contract('token_' + underlying)
        # element schema (pool_index, pool_name, comptroller, asset_address, asset_name, asset_symbol \
        #                   asset_decimals, underlying_address, underlying_name, underlying_symbol, underlying_decimals)
        
        #special case for MKR, non-ERC20 compliant causes int overflow as expected strings are stored as byte32
        if underlying == '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2':  
            element = (pool_index, pool_name, comptroller, asset, ftoken_contract.name(), \
                ftoken_contract.symbol(), ftoken_contract.decimals(), underlying, \
                'Maker', 'MKR', underlying_contract.decimals())
        else:
            element = (pool_index, pool_name, comptroller, asset, ftoken_contract.name(), \
                ftoken_contract.symbol(), ftoken_contract.decimals(), underlying, \
                underlying_contract.name(), underlying_contract.symbol(), underlying_contract.decimals())

        print(element)
        return_list.append(element)
    
    return return_list

    #for element in return_list:
    #    print(element)


def debug_tokens():
    """Used to debug a troublesome token"""
    asset = '0x85b294139E77E7dE519A9bA9553D274d79E4812e'
    try: 
        Contract('token_' + asset).alias
    except ValueError:
        #using abi as etherscan isn't reliably detecting asset tokens as proxy contracts
        Contract.from_abi('CErc20Delegate', asset, cerc20_abi).set_alias('token_' + asset, persist=True)

    ftoken_contract = Contract('token_' + asset)
    print('ftoken - ' + asset)

    #get the underlying token
    underlying = ftoken_contract.underlying()

    #change out wETH for ETH so that ERC20 methods work
    if underlying == '0x0000000000000000000000000000000000000000':
        underlying = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
    print('underlying - ' + underlying)
    try: 
        Contract('token_' + underlying).alias
    except ValueError:
        #lazily using cERC20 for underlying because it implements .name, .decimals, .symbol correctly
        Contract.from_abi('CErc20Delegate', underlying, cerc20_abi).set_alias('token_' + underlying, persist=True)

    underlying_contract = Contract('token_' + underlying)   

    
    val = "some string"
    print(ftoken_contract.name())
    print(ftoken_contract.symbol())
    print(ftoken_contract.decimals())
    print(underlying_contract.name())
    print(underlying_contract.symbol())
    print(underlying_contract.decimals())


def generate_sql_query(assets):
    """Takes a list of tuples & formats to SQL text for use in Dune Analytics query"""

    sql_query_string = 'CREATE OR REPLACE VIEW dune_user_generated.rari_capital_fuse_ftokens (pool_index, pool_name, comptroller, ftoken_address, ftoken_name, ftoken_symbol, '
    sql_query_string += 'ftoken_decimals, underlying_address, underlying_name, underlying_symbol, underlying_decimals) AS VALUES \n'

    index = 0
    for asset in assets:
        if index > 0:
            sql_query_string += '  , (' + str(asset[0]) + '::numeric, '
        else:
            sql_query_string += '    (' + str(asset[0]) + '::numeric, '
        sql_query_string += "'" + asset[1].replace("'", "''") + "'::text, "
        sql_query_string += "'" + asset[2].replace("0x", "\\x") + "'::bytea, "
        sql_query_string += "'" + asset[3].replace("0x", "\\x") + "'::bytea, "
        sql_query_string += "'" + asset[4].replace("'", "''") + "'::text, "
        sql_query_string += "'" + asset[5].replace("'", "''") + "'::text, "
        sql_query_string += str(asset[6]) + "::numeric, "
        sql_query_string += "'" + asset[7].replace("0x", "\\x") + "'::bytea, "
        sql_query_string += "'" + asset[8].replace("'", "''") + "'::text, "
        sql_query_string += "'" + asset[9].replace("'", "''") + "'::text, "
        sql_query_string += str(asset[10]) + "::numeric"
        sql_query_string += ")\n"
        index +=1
    sql_query_string += ';'


    return sql_query_string
