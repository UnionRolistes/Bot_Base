cd ..
cd env

# for each file in the env directory
for file in *; do
  # if file is a default.*.env file
    if [[ $file == default.*.env ]]; then
        echo $file
        # check if the file wihout the default exists
        env_name=${file#default.}
        env_name=${env_name%.env}
        echo $env_name

        #print value of env_name
        # if it does not exist, create it
        if [ ! -f $env_name.env ]; then
            touch $env_name.env
        fi
        # for each line in the default file
        while IFS=: read -r -u 9 line || [ -n "$line" ]; do # || [ -n "$line" ] est tres important sinon le dernier element ne sera pas lu
            # if the line is not in the file, add it
            if ! grep -q "$line" $env_name.env; then
                #get env variable name
                env_var=${line%=*}
                #get env variable value without comment
                env_value=${line#*=}
                #remove comment
                env_value=${env_value%%#*}
                #if line has a comment
                if [[ $line == *#* ]]; then
                    #get comment with comment symbol
                    env_comment=\#${line#*#}
                else
                    env_comment=""
                fi
                echo $line
                echo "name: $env_var  || value: $env_value || comment: $env_comment"
                echo "---------------------------------"
                #ask user to change value of env variable
                echo "Enter value for $env_var (default: $env_value):"
                printf ""
                read varname
                if [ -z "$varname" ]; then
                    varname=$env_value
                fi

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
