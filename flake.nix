{
  description = "Tools for MC-related activities.";

  inputs = {
    root-curated.url = "github:umd-lhcb/root-curated";
    nixpkgs.follows = "root-curated/nixpkgs";
    flake-utils.follows = "root-curated/flake-utils";
  };

  outputs = { self, root-curated, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
      in
      {
        devShell = pkgs.mkShell {
          name = "mc_tools";
          buildInputs = with pythonPackages; [
            # Linters
            pylint

            # Python requirements (enough to get a virtualenv going).
            virtualenvwrapper
            numpy
            pandas
            lark-parser
            attrs
            pyyaml
            chardet
          ];

          shellHook = ''
            # Allow the use of wheels.
            SOURCE_DATE_EPOCH=$(date +%s)
            VENV=./.virtualenv

            if test ! -d $VENV; then
              virtualenv $VENV
            fi
            source $VENV/bin/activate

            # allow for the environment to pick up packages installed with virtualenv
            export PYTHONPATH=$VENV/${python.sitePackages}/:$PYTHONPATH

            # Update PATH
            export PATH=$(pwd)/bin:$PATH
          '';
        };
      });
}
