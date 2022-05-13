#! /bin/bash

# Clear Log Files
rm ./session-*.log
rm ./package/widgets/widgets-test-session.log

# Clear Cache
rm -rf ./package/__pycache__
rm -rf ./package/widgets/__pycache__
rm -rf ./package/widgets/fps/__pycache__
rm -rf ./package/widgets/fps/r307/__pycache__

# Clear Databases
rm ./database.json
rm ./package/widgets/database.json
