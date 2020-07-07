# mc_tools
Tools for MC-related activities.


## Installation
Install all Python dependencies with:
```
pip -r ./requirements.txt
```

The scripts in the `bin` folder then can be invoked.


## Usage:
### `dec_print.py`
This script prints out all explicitly defined decays in a `.dec` file:
```
dec_print.py <path_to_dec_file>
```

**Note**: Sometimes one may encounter the following warning:
```
UserWarning:
Corresponding 'Decay' statement for 'CDecay' statement(s) of following particle(s) not found:
anti-B0sig.
Skipping creation of these charge-conjugate decay trees.
```

That warning is generated when parsing:
```
./dec_files/lhcb-semileptonic/11873010.dec
```

This just means that in the `.dec` file, the `anti-B0sig` is not explicitly
defined as the anti particle of `B0sig`, but in the end, the parsing is still
successful, and `anti-B0sig` decay chains can be successfully inferred.

To fix this, just add the following line to that file:
```
ChargeConj anti-B0sig      B0sig
```
