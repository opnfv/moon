#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <glib.h>
#include <pbc.h>
#include <pbc_random.h>

#include "bswabe.h"
#include "common.h"
#include "policy_lang.h"

char* usage =
"Usage: peks-index [OPTION ...] PUB_KEY IND TRAP\n"
"\n"
"Test a trapdoor over an encrypted index IND.\n"
"It uses the public key PUB_KEY,\n"
"an encrypted index IND and an encrypted trapdoor TRAP.\n"
"returns 1 if there is a match, 0 if not\n"
"\n"
"Mandatory arguments to long options are mandatory for short options too.\n\n"
" -h, --help                    print this message\n\n"
" -v, --version                 print version information\n\n"
" -d, --deterministic      	use deterministic \"random\" numbers\n"
"";


char*  pub_file = 0;
char*  ind_file = 0;
char*  trap_file = 0;

void
parse_args( int argc, char** argv )
{
	int i;

	for( i = 1; i < argc; i++ )
		if(      !strcmp(argv[i], "-h") || !strcmp(argv[i], "--help") )
		{
			printf("%s", usage);
			exit(0);
		}
		else if( !strcmp(argv[i], "-v") || !strcmp(argv[i], "--version") )
		{
			printf(CPABE_VERSION, "-keygen");
			exit(0);
		}
		else if( !strcmp(argv[i], "-d") || !strcmp(argv[i], "--deterministic") )
		{
			pbc_random_set_deterministic(0);
		}
		else if( !pub_file )
		{
			pub_file = argv[i];
		}
		else if( !ind_file )
		{
			ind_file = argv[i];
		}
		else if( !trap_file )
		{
			trap_file = argv[i];
		}



	if( !pub_file || !ind_file || !trap_file)
		die(usage);

}

int
main( int argc, char** argv )
{

	bswabe_pub_t* pub;
	peks_ind_t* ind;
	peks_trap_t* trap;

	
	parse_args(argc, argv);

	/* Retrieve public key */	
	pub = bswabe_pub_unserialize(suck_file(pub_file), 1); 

	ind = peks_ind_unserialize(pub, suck_file(ind_file), 1);

	trap = peks_trap_unserialize( pub, suck_file(trap_file), 1 );

	if( !peks_test_ind( pub, ind, trap ))
		return 1;
	else	
		return 0;
}
