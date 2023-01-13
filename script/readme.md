
# script

## config.sh

## EXT script

<https://github.com/bashup/dotenv>

### dotenv cli

    $ dotenv --help
        Usage:
        dotenv [-f|--file FILE] COMMAND [ARGS...]
        dotenv -h|--help

        Options:
        -f, --file FILE          Use a file other than .env

        Read Commands:
        get KEY                  Get raw value of KEY (or fail)
        parse [KEY...]           Get trimmed KEY=VALUE lines for named keys (or all)
        export [KEY...]          Export the named keys (or all) in shell format

        Write Commands:
        set [+]KEY[=VALUE]...    Set or unset values (in-place w/.bak); + sets default
        puts STRING              Append STRING to the end of the file
        generate KEY [CMD...]    Set KEY to the output of CMD unless it already exists;
                                return the new or existing value.

        $ echo '  # This is my .env file' >prod.env
        $ echo '  FOO=bar  ' >>prod.env

        $ cat prod.env
        # This is my .env file
        FOO=bar

        $ dotenv -f prod.env get FOO
        bar
