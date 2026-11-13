# tools

Build, checks and the pull tool (owner S10). `verify.sh` runs every check. Each check ships a self-test with a known-bad and a known-clean sample, and follows the exit contract: 0 clean, 1 finding, 2 usage error, 3 could not check.
