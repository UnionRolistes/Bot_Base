# Set the current directory to the parent directory
cd ..

# Set the $tmp variable to an empty string
$tmp=""

# Find all docker-compose.yml files in subdirectories with a depth of 3 or less
Get-ChildItem -Recurse -Include docker-compose.yml -Depth 3 | ForEach-Object {
    # Concatenate the path to the docker-compose file to the $tmp variable
    $tmp = "${tmp} -f ${($_.FullName -replace '\\', '/')}"
}

# Set the current directory to the Bot_Base directory
cd Bot_Base

# Use docker-compose to generate a new docker-compose file based on the files found
& docker-compose $tmp config > conf-build-docker-compose.yml

# Use docker-compose to restart all containers in the stack defined in the new docker-compose file
& docker-compose -f conf-build-docker-compose.yml restart