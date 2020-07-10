# mc_tools
Tools for MC-related activities.

**Note**: This project includes CERN's `DecFiles` as a submodule. However,
normally the submodule doesn't need to be initialized by normal user, as it is
only useful when updating the `.dec` YAML database.


## Installation
Install all Python dependencies with:
```
pip -r ./requirements.txt
```


## Usage
### `bin/dec_print.py`
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
./bin/dec_files/lhcb-semileptonic/11873010.dec
```

This just means that in the `.dec` file, the `anti-B0sig` is not explicitly
defined as the anti particle of `B0sig`, but in the end, the parsing is still
successful, and `anti-B0sig` decay chains can be successfully inferred.

To fix this, just add the following line to that file:
```
ChargeConj anti-B0sig      B0sig
```

### `bin/get_dec_file.py`
Multiple `.dec` files can be downloaded with:
```
./bin/get_dec_file.py -d 11873010 60002018 -o dec_files
```

The script accepts the following parameters:

- `-d`: event types. Multiple event types should be separated with space
- `-o`: Output directory for downloaded `.dec` files. Default to `.`
- `-t`: The tag of the `DecFiles` repository. Default to `v30r46`
