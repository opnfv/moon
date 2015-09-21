Installation
============

# This part describes the installation of cpabe and peks.
# You will need to install some official packages that can be
# retrieved online on official repositories.
# You will need to install manually 3 libraries
# Root privileges are required

# Install official packages:
# build-essebtial and autotools-dev for compilation and installation
# libglib2.0-dev for the glib library
# libgmp3-dev for the GMP library
# flex and bison are necessary for the libbswabe library
# libssl-dev is necessary for the crypto operations

`sudo apt-get install build-essential autotools-dev libglib2.0-dev libgmp3-dev flex bison libssl-dev`

# Three libraries have to be installed manually:
# PBC: Pairing Based Cryptography (for pairing operations over elliptic curves)
#      More info: http://crypto.stanford.edu/pbc/
#
# libbswabe: Core operations for cpabe and peks
#            More info: http://acsc.cs.utexas.edu/cpabe/
#
# cpabe: Cyphertext-Policy Attribute Based Encryption library
#        Implements the 4 algorithms for CPABE: setup, keygen, enc and dec
#        Implements the 4 algorithms for PEKS: setup, enc, trap and test
#        More info: http://acsc.cs.utexas.edu/cpabe/


# Replace <PATH-TO-REP> with the path to the POC repository


Install pbc
-----------

* `cd <PATH-TO-REP>/pbc-0.5.14`

* `./configure`

* `make`

* `sudo make install`

Install libbswabe
-----------------

* `cd <PATH-TO-REP>/libbswabe-0.9/`

* `./configure`

* `make`

* `sudo make install`


Install cpabe
-------------

* `cd <PATH-TO-REP>/cpabe-0.11/`

* `./configure`

* `make`

* sudo make install


Manual
======

# Below we describe each functionality of the cpabe and peks:
# For using with the python wrapper, just call ./[PROG-NAME].py [OPTIONS...] ...
# The pythons scripts are in the folder <PATH-TO-REP>/python
# Ex: ./cpabe-setup.py -h
# Some examples are given at the end of this document.

cpabe-setup:

	Usage: cpabe-setup [OPTION ...]

	Generate system parameters, a public key, and a master secret key
	for use with cpabe-keygen, cpabe-enc, and cpabe-dec.

	Output will be written to the files "pub_key" and "master_key"
	unless the --output-public-key or --output-master-key options are
	used.

	Mandatory arguments to long options are mandatory for short options too.

	 -h, --help                    print this message

	 -v, --version                 print version information

	 -p, --output-public-key FILE  write public key to FILE

	 -m, --output-master-key FILE  write master secret key to FILE

	 -d, --deterministic           use deterministic "random" numbers
	                               (only for debugging)


cpabe-keygen:

	Usage: cpabe-keygen [OPTION ...] PUB_KEY MASTER_KEY ATTR [ATTR ...]

	Generate a key with the listed attributes using public key PUB_KEY and
	master secret key MASTER_KEY. Output will be written to the file
	"priv_key" unless the -o option is specified.

	Attributes come in two forms: non-numerical and numerical. Non-numerical
	attributes are simply any string of letters, digits, and underscores
	beginning with a letter.

	Numerical attributes are specified as `attr = N', where N is a non-negative
	integer less than 2^64 and `attr' is another string. The whitespace around
	the `=' is optional. One may specify an explicit length of k bits for the
	integer by giving `attr = N#k'. Note that any comparisons in a policy given
	to cpabe-enc(1) must then specify the same number of bits, e.g.,
	`attr > 5#12'.

	The keywords `and', `or', and `of', are reserved for the policy language
	of cpabe-enc (1) and may not be used for either type of attribute.

	Mandatory arguments to long options are mandatory for short options too.

	 -h, --help               print this message

	 -v, --version            print version information

	 -o, --output FILE        write resulting key to FILE

	 -d, --deterministic      use deterministic "random" numbers
	                          (only for debugging)


cpabe-enc:

	Usage: cpabe-enc [OPTION ...] PUB_KEY FILE [POLICY]

	Encrypt FILE under the decryption policy POLICY using public key
	PUB_KEY. The encrypted file will be written to FILE.cpabe unless
	the -o option is used. The original file will be removed. If POLICY
	is not specified, the policy will be read from stdin.

	Mandatory arguments to long options are mandatory for short options too.

	 -h, --help               print this message

	 -v, --version            print version information

	 -k, --keep-input-file    don't delete original file

	 -o, --output FILE        write resulting key to FILE

	 -d, --deterministic      use deterministic "random" numbers
	                          (only for debugging)



cpabe-dec:

	Usage: cpabe-dec [OPTION ...] PUB_KEY PRIV_KEY FILE

	Decrypt FILE using private key PRIV_KEY and assuming public key
	PUB_KEY. If the name of FILE is X.cpabe, the decrypted file will
	be written as X and FILE will be removed. Otherwise the file will be
	decrypted in place. Use of the -o option overrides this
	behavior.

	Mandatory arguments to long options are mandatory for short options too.

	 -h, --help               print this message

	 -v, --version            print version information

	 -k, --keep-input-file    don't delete original file

	 -o, --output FILE        write output to FILE

	 -d, --deterministic      use deterministic "random" numbers
	                         (only for debugging)



cpabe-policyList:

	Usage: cpabe-policyList [OPTION ...] PUB_KEY CIPHERTEXT

	Print the access policy of a ciphertext CIPHERTEXT
	Mandatory arguments to long options are mandatory for short options too.

	 -h, --help                    print this message

	 -v, --version                 print version information

	 -d, --deterministic           use deterministic "random" numbers
	                               (only for debugging)


cpabe-attrList:

	Usage: cpabe-attrList [OPTION ...] PUB_KEY PRV_KEY

	Print the attributes of a private key PRV_KEY
	Mandatory arguments to long options are mandatory for short options too.

	 -h, --help                    print this message

	 -v, --version                 print version information

	 -d, --deterministic           use deterministic "random" numbers
	                               (only for debugging)


peks-ind:

	Usage: peks-index [OPTION ...] PUB_KEY IND

	Generate an encrypted index given a clear index IND.
	The clear index should be of the form:
	keyword_1
	keyword_2
	...
	It uses the public key PUB_KEY and a clear index IND.
	The encrypted index will be written to the file "enc_ind"
	unless the --output is used.

	Mandatory arguments to long options are mandatory for short options too.

	 -h, --help                    print this message

	 -v, --version                 print version information

	 -o, --output FILE  		write index to FILE

	 -d, --deterministic      	use deterministic "random" numbers



peks-trap:

	Usage: peks-trap [OPTION ...] PUB_KEY MSK_KEY KEYWORD

	Generate an encrypted trapdoor given a clear keyword KEYWORD.
	It uses the public key PUB_KEY and the master key MSK_KEY.
	The encrypted trapdoor will be written to the file "enc_trap"
	unless the --output is used.

	Mandatory arguments to long options are mandatory for short options too.

	 -h, --help                    print this message

	 -v, --version                 print version information

	 -o, --output FILE  		write index to FILE

	 -d, --deterministic      	use deterministic "random" numbers



peks-test:

	Usage: peks-index [OPTION ...] PUB_KEY IND TRAP

	Test a trapdoor over an encrypted index IND.
	It uses the public key PUB_KEY,
	an encrypted index IND and an encrypted trapdoor TRAP.
	returns 1 if there is a match, 0 if not

	Mandatory arguments to long options are mandatory for short options too.

	 -h, --help                    print this message

	 -v, --version                 print version information

	 -d, --deterministic      	use deterministic "random" numbers



# Examples (See also http://acsc.cs.utexas.edu/cpabe/tutorial.html)
# For using with the python wrapper, just call ./[PROG-NAME].py [OPTIONS...] ...
# The pythons scripts are in the folder <PATH-TO-REP>/python
# Ex: ./cpabe-setup.py

# Generate master key and public key
	$ cpabe-setup

	$ ls
	master_key  pub_key

# Generate private key for Sara and Kevin with attributes
# sysadmin, it_department for Sara
# business_staff, strategy_team for Kevin

	$ cpabe-keygen -o sara_priv_key pub_key master_key sysadmin it_department

	$ cpabe-keygen -o kevin_priv_key pub_key master_key business_staff strategy_team

	$ ls
	master_key  pub_key  sara_priv_key  kevin_priv_key

# Encrypt a file security_report.pdf with a policy (business_staff and strategy_team) or (sysadmin and business_staff)

	$ ls
	pub_key  security_report.pdf

	$ cpabe-enc pub_key security_report.pdf "(sysadmin and business_staff) or (business_staff and strategy_team)"

	$ ls
	pub_key  security_report.pdf.cpabe

# Print the policy of the ciphertext
        $ ls
        pub_key  security_report.pdf.cpabe

        $ cpabe-policyList pub_key security_report.pdf.cpabe
	business_staff sysadmin 2of2 business_staff strategy_team 2of2 1of2

# Print the attributes of Kevin's private key
	$ ls
        pub_key  kevin_priv_key

	$ cpabe-attrList pub_key kevin_priv_key

# Decryption with Kevin's private key

	$ ls
	pub_key kevin_priv_key security_report.pdf.cpabe

	$ cpabe-dec pub_key kevin_priv_key security_report.pdf.cpabe

	$ ls
	pub_key  kevin_priv_key  security_report.pdf

# Create an encrypted index

	$ ls
	pub_key testindex

	$ peks-ind pub_key testindex

	$ ls
	enc_ind pub_key testindex

# Create a trapdoor for the word my_keyword

	$ ls
	pub_key master_key

	$ peks-trap pub_key master_key my_keyword

	$ ls
	enc_trap pub_key master_key

# Test if an encrypted index matches with a trapdoor

	$ ls
	pub_key enc_ind enc_trap

	$ peks-test pub_key enc_ind enc_trap

	$ echo $?
	0
