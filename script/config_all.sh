cd ..
# for each directory in the current directory
for dir in *; do
    # if env directory exist
    if [ -d "$dir/env" ]; then
        #run config.sh in env directory
        cd $dir/env
        ../../Bot_Base/script/config.sh
        cd ../..
    fi
done