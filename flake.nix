{
  description = "Tools for MC-related activities.";

  inputs = rec {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    mach-nix = {
      url = "github:DavHau/mach-nix";
      inputs = { inherit nixpkgs flake-utils; };
    };
  };

  outputs = { self, nixpkgs, flake-utils, mach-nix }:
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
