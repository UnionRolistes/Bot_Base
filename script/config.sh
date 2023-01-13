#!/usr/bin/env bash
cd ..
cd env

# for each file in the env directory
for file in ./; do
  # if file is a default.*.env file
    if [[ $file == default.*.env ]]; then
        # check if the file wihout the default exists
        env_name=${file#default.}
        env_name=${env_name%.env}
        #print value of env_name
        echo $env_name
        # if it does not exist, create it
        if [ ! -f $env_name.env ]; then
            touch $env_name.env
        fi
        # append the contents of the default file to the env file
        cat $file >> $env_name.env
    fi


    # #example if,  if else, else
    # if [[ $file == default.*.env ]]; then
    #     env_name=${file#default.}
    #     env_name=${env_name%.env}
    #     touch $env_name.env
    #     cat $file >> $env_name.env
    # elif [[ $file == *.env ]]; then
    #     env_name=${file%.env}
    #     touch $env_name.env
    #     cat $file >> $env_name.env
    # else
    #     echo "File $file is not a valid env file"
    # fi
