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
"Usage: peks-trap [OPTION ...] PUB_KEY MSK_KEY KEYWORD\n"
"\n"
"Generate an encrypted trapdoor given a clear keyword KEYWORD.\n"
"It uses the public key PUB_KEY and the master key MSK_KEY.\n"
"The encrypted trapdoor will be written to the file \"enc_trap\"\n"
"unless the --output is used.\n"
"\n"
"Mandatory arguments to long options are mandatory for short options too.\n\n"
" -h, --help                    print this message\n\n"
" -v, --version                 print version information\n\n"
" -o, --output FILE  		write index to FILE\n\n"
" -d, --deterministic      	use deterministic \"random\" numbers\n"
"";


char*  pub_file = 0;
char*  msk_file = 0;
char*  keyword = 0;
char*  out_file = "enc_trap";

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
		else if( !msk_file )
		{
			msk_file = argv[i];
		}
		else if( !keyword )
		{
			keyword = argv[i];
		}


	if( !pub_file || !msk_file || !keyword)
//	if( !pub_file || !ind_file)
		die(usage);

}

int
main( int argc, char** argv )
{

	bswabe_msk_t* msk;
	bswabe_pub_t* pub;
	peks_trap_t* trap;
	char bufKeyword[256];
	

	parse_args(argc, argv);

	/* Retrieve public key */	
	pub = bswabe_pub_unserialize(suck_file(pub_file), 1); 
	msk = bswabe_msk_unserialize(pub, suck_file(msk_file), 1);

	/* It is necessary to add \n at the end of the keyword */
	strcpy(bufKeyword, keyword);
	strcat(bufKeyword, "\n");

	trap = peks_trap( pub, msk, bufKeyword );

	spit_file(out_file, peks_trap_serialize(trap), 1);

	return 0;
}
