FusePoolDirectory = Contract.from_explorer('0x835482FE0532f169024d5E9410199369aAD5C77E')
FusePoolDirectory.getAllPools()

for p in pools:
    print(p)


FusePoolLens = Contract.from_explorer('0x6Dc585Ad66A10214Ef0502492B0CC02F0e836eec')

import json
lens_abi = json.loads(lens_abi = json.loads(requests.get("https://raw.githubusercontent.com/Rari-Capital/rari-dApp/master/src/fuse-sdk/src/abi/FusePoolLens.json").json()
lens_abi = requests.get("https://raw.githubusercontent.com/Rari-Capital/rari-dApp/master/src/fuse-sdk/src/abi/FusePoolLens.json").json()
lens_abi = json.loads(open('scripts/FusePoolLens.json').read())


FusePoolLens = Contract.from_abi('FusePoolLens', '0x6Dc585Ad66A10214Ef0502492B0CC02F0e836eec', lens_abi)

FusePoolLens_proxy = Contract.from_explorer('0x6Dc585Ad66A10214Ef0502492B0CC02F0e836eec')

FusePoolLens_w3 = w3.eth.contract('0x6Dc585Ad66A10214Ef0502492B0CC02F0e836eec', abi = lens_abi)

from_address = {
    'from' : '0x4dD657E0AC3d6Eac84B1b3Be6dA0018d2AA1dbC8'
}





lens_abi = json.loads(open('scripts/FusePoolLens.json').read())
FusePoolLens = Contract.from_abi('FusePoolLens', '0x6Dc585Ad66A10214Ef0502492B0CC02F0e836eec', lens_abi)
FusePoolLens.getPoolAssetsWithData('0x4dD657E0AC3d6Eac84B1b3Be6dA0018d2AA1dbC8')

FusePoolLens.getPublicPoolsWithData()

#working
FusePoolLens.getPoolAssetsWithData('0x4dD657E0AC3d6Eac84B1b3Be6dA0018d2AA1dbC8')
FusePoolLens.getPoolSummary('0x4dD657E0AC3d6Eac84B1b3Be6dA0018d2AA1dbC8')

assets = FusePoolLens.getPoolAssetsWithData('0x4dD657E0AC3d6Eac84B1b3Be6dA0018d2AA1dbC8')
for a in assets:
    print(a)

FusePoolLens.getPoolAssetsWithData('0x4702D39c499236A43654c54783c3f24830E247dC')
