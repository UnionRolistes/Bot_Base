# Set the current directory to the parent directory
Set-Location ..

# Find all docker-compose.yml files in subdirectories with a depth of 3 or less
$files = Get-ChildItem -Path . -Filter docker-compose.yml -Recurse -Depth 3

# for each file found, add "-f $file.x" to the tmp variable
$tmp = $files | ForEach-Object { " -f $($_.FullName)" }

# Set the current directory to the Bot_Base directory
Set-Location Bot_Base

# Use docker-compose to generate a new docker-compose file based on the files found
& docker-compose $tmp config > "conf-build-docker-compose.yml"


# Use docker-compose to restart all containers in the stack defined in the new docker-compose file
& docker-compose -f conf-build-docker-compose.yml up -d --remove-orphans --force-recreate --build