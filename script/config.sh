#!/bin/bash
# run to env directory and execute this script to create env files and set values

# for each file in the env directory
for file in *; do
  # if file is a default.*.env file
    if [[ $file == default.*.env ]]; then
        # check if the file wihout the default exists
        env_name=${file#default.}
        env_name=${env_name%.env}
        echo "---- $env_name.env ----"
        # if it does not exist, create it
        if [ ! -f $env_name.env ]; then
            touch $env_name.env
        fi
        # for each line in the default file
        while IFS=: read -r -u 9 line || [ -n "$line" ]; do # || [ -n "$line" ] est tres important sinon le dernier element ne sera pas lu
            # trim start of line
            line="${line#"${line%%[![:space:]]*}"}"
            # if line is not empty and does not start with #
            if [[ ! -z $line ]] && [[ $line != \#* ]]; then

                #get env variable name
                env_var=${line%=*}
                #get env variable value
                env_value=${line#*=}
                #remove comment if exist
                env_value=${env_value%%#*}
                # #if line has a comment get it
                # if [[ $line == *#* ]]; then
                #     #get comment with comment symbol
                #     env_comment=\#${line#*#}
                # else
                #     env_comment=""
                # fi

                # if env_var exist in $env_name.env rewrite env_value with value in $env_name.env
                # ps use actual value user as default valur
                if grep -q "$env_var" $env_name.env; then
                    env_value=$(grep "$env_var" $env_name.env | cut -d '=' -f2)
                    env_value=${env_value%%#*}
                fi
                #ask user to change value of env variable
                echo "Enter value for $env_var (default: $env_value):"
                printf ""
                read input
                # if varname as character
                if test ! -z "$input"; then
                        env_value=$input
                fi

                #if env_var exist in $env_name.env rewrite it
                if grep -q "$env_var" $env_name.env; then
                    sed -i "s/$env_var=.*/$env_var=$env_value/g" $env_name.env
                else
                    #add line to file
                    echo "$env_var=$env_value" >> $env_name.env
                fi


                ##add line to file
                #echo "$env_var=$env_value $env_comment" >> $env_name.env
                #------------------------------------------------------------------------------------------------
            fi
        done 9< $file
    fi
done


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
