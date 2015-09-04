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
"Usage: peks-index [OPTION ...] PUB_KEY IND\n"
"\n"
"Generate an encrypted index given a clear index IND.\n"
"The clear index should be of the form:\n"
"keyword_1\n"
"keyword_2\n"
"...\n"
"It uses the public key PUB_KEY and a clear index IND.\n"
"The encrypted index will be written to the file \"enc_ind\"\n"
"unless the --output is used.\n"
"\n"
"Mandatory arguments to long options are mandatory for short options too.\n\n"
" -h, --help                    print this message\n\n"
" -v, --version                 print version information\n\n"
" -o, --output FILE  		write index to FILE\n\n"
" -d, --deterministic      	use deterministic \"random\" numbers\n"
"";


char*  pub_file = 0;
// char*  msk_file = 0;
char*  ind_file = 0;

char*  out_file = "enc_ind";

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
		else if( !strcmp(argv[i], "-o") || !strcmp(argv[i], "--output") )
		{
			if( ++i >= argc )
				die(usage);
			else
				out_file = argv[i];
		}
		else if( !strcmp(argv[i], "-d") || !strcmp(argv[i], "--deterministic") )
		{
			pbc_random_set_deterministic(0);
		}
		else if( !pub_file )
		{
			pub_file = argv[i];
		}
/*		else if( !msk_file )
		{
			msk_file = argv[i];
		}*/
		else if( !ind_file )
		{
			ind_file = argv[i];
		}


//	if( !pub_file || !msk_file || !ind_file)
	if( !pub_file || !ind_file)
		die(usage);

}

int
main( int argc, char** argv )
{

	bswabe_pub_t* pub;
	peks_ind_t* ind;

	
	parse_args(argc, argv);

	/* Retrieve public key */	
	pub = bswabe_pub_unserialize(suck_file(pub_file), 1); 

	ind = peks_enc_ind( pub, ind_file );

	spit_file(out_file, peks_ind_serialize(ind), 1);

// For testing (requires the master key)
/*	

	bswabe_msk_t* msk;
	peks_ind_t* ind2;
	
	peks_trap_t* trap;

	msk = bswabe_msk_unserialize(pub, suck_file(msk_file), 1);
	ind2 = peks_ind_unserialize(pub, suck_file(out_file), 1);

	trap = peks_trap( pub, msk, "test\n" );

	if( !peks_test_ind( pub, ind2, trap ))
		printf("The encrypted index contains the word test\n");
*/	
	return 0;
}
