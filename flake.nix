{
  description = "Tools for MC-related activities.";

  inputs = rec {
    flake-utils.url = "github:numtide/flake-utils";
    mach-nix = {
      url = "github:DavHau/mach-nix";
    };
  };

  outputs = { self, flake-utils, mach-nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        mkPythonShell = mach-nix.lib.${system}.mkPythonShell;
      in
      {
        devShell = mkPythonShell {
          requirements = builtins.readFile ./requirements.txt + ''
            setuptools
            jedi
            flake8
            pylint
          '';
          # NOTE: "setuptools" is the most common missing dependency
        };
      });
}
