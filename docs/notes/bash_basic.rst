=====================
Bash Basic cheatsheet
=====================

.. contents:: Table of Contents
    :backlinks: none

Special Parameters
------------------

.. code-block:: bash

    #!/bin/bash

    foo() {
      # expand to the position params, equal to "$1$2..."
      echo $*
      # expand to the position params, equal to "$1" "$2" ...
      echo $@
      # expand to the number of position params
      echo $#
      # expand to the pid
      echo $$
      # expand to the exit status
      echo $?
      # expand to the name of shell script
      echo $0
    }

    foo "a" "b" "c"

Brace Expansion
---------------

.. code-block:: bash

    $ echo foo.{pdf,txt,png,jpg}
    foo.pdf foo.txt foo.png foo.jpg

Variable Expansion
------------------

.. code-block:: bash

    $ foo1="foo1"
    $ foo2="foo2"

    # expand to "$foo1 foo2"
    $ echo "${!foo*}"

    # expand to "$foo1" "$foo2"
    $ echo "${!foo@}"

String length
-------------

.. code-block:: bash

    echo ${#foo}
    7

String Slice
------------

.. code-block:: bash

    $ foo="01234567890abcdefg"

    # ${param:offset}
    $ echo ${foo:7}
    7890abcdefg

    $ echo ${foo: -7}
    abcdefg
    $ echo ${foo: -7:2}
    ab

    # ${param:offset:length}
    $ echo ${foo:7:3}
    789

Delete Match String
-------------------

.. code-block:: bash

    $ foo="123,456,789"
    # ${p##substring} delete longest match of substring from front
    $ echo ${foo##*,}
    789

    # ${p#substring} delete shortest match of substring from front
    echo ${foo#*,}
    456,789

    # ${p%%substring} delete longest match of substring from back
    $ echo ${foo%%,*}
    123

    $ echo ${foo%,*}
    123,456

Other examples

.. code-block:: bash

    disk="/dev/sda"
    $ echo ${disk##*/}
    sda

    $ disk="/dev/sda3"
    echo ${disk%%[0-9]*}
    /dev/sda

Here Documents
--------------

.. code-block:: bash

    cat <<EOF
        Hello Document
    EOF

Here Strings
------------

.. code-block:: bash

    # CMD <<< $w, where $w is expanded to the stdin of CMD

    bc <<< "1 + 2 * 3"

Logger
------

.. code-block:: bash

    REST='\e[0m'
    RED='\e[1;31m'
    GREEN='\e[1;32m'
    YELLOW='\e[1;33m'
    CYAN='\e[1;36m'

    info() {
      echo -e "[$(date +'%Y-%m-%dT%H:%M:%S%z')][${GREEN}info${REST}] $*"
    }

    debug() {
      echo -e "[$(date +'%Y-%m-%dT%H:%M:%S%z')][${CYAN}debug${REST}] $*"
    }

    warn() {
      echo -e "[$(date +'%Y-%m-%dT%H:%M:%S%z')][${YELLOW}warn${REST}] $*" >&2
    }

    err() {
      echo -e "[$(date +'%Y-%m-%dT%H:%M:%S%z')][${RED}error${REST}] $*" >&2
    }

Check Command Exist
-------------------

.. code-block:: bash

    cmd="tput"
    if command -v "${tput}" > /dev/null; then
      echo "$cmd exist"
    else
      echo "$cmd does not exist"
    fi

Read a File Line by Line
------------------------

.. code-block:: bash

   #!/bin/bash

   file="file.txt"
   while IFS= read -r l; do echo $l; done < "$file"

Read a File field wise
----------------------

.. code-block:: bash

   #!/bin/bash

   file="/etc/passwd"
   while IFS=: read -r n _ _ _ _ _ _; do echo $n; done < "$file"


Parse Arguments
---------------

.. code-block:: bash

	#!/bin/bash

	program="$1"

	usage() {
	  cat <<EOF

	Usage:	$program [OPTIONS] params

	Options:

	  -h,--help                show this help
	  -a,--argument string     set an argument

	EOF
	}

	arg=""
	params=""
	while (( "$#" )); do
	  case "$1" in
		-h|-\?|--help)
		  usage
		  exit 0
		  ;;

		-a|--argument)
		  arg="$2"
		  shift 2
		  ;;

		# stop parsing
		--)
		  shift
		  break
		  ;;

		# unsupport options
		-*|--*=)
		  echo "Error: unsupported option $1" >&2
		  exit 1
		  ;;

		# positional arguments
		*)
		  params="$params $1"
		  shift
		  ;;
	  esac
	done
