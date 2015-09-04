#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <glib.h>
#include <pbc.h>
#include <pbc_random.h>

#include "bswabe.h"
#include "common.h"

char* usage =
"Usage: cpabe-attrList [OPTION ...] PUB_KEY PRV_KEY\n"
"\n"
"Print the attributes of a private key PRV_KEY\n"
"Mandatory arguments to long options are mandatory for short options too.\n\n"
" -h, --help                    print this message\n\n"
" -v, --version                 print version information\n\n"
" -d, --deterministic           use deterministic \"random\" numbers\n"
"                               (only for debugging)\n\n";

char* pub_file = 0;
char* prv_file   = 0;

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
			printf(CPABE_VERSION, "-setup");
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
		else if( !prv_file )
		{
			prv_file = argv[i];
		}
		else
			die(usage);
}

int
main( int argc, char** argv )
{

	bswabe_prv_t* prv;
	bswabe_pub_t* pub;
	char** attrList;
	int i;

	parse_args(argc, argv);
	
	pub = bswabe_pub_unserialize(suck_file(pub_file), 1);	
	prv = bswabe_prv_unserialize(pub, suck_file(prv_file), 1);

	attrList = bswabe_attrList(prv);

	i = 0;

	while(attrList[i])
	{
		printf("%s ",attrList[i]);
		i++;
	}
		printf("\n");
	return 0;
}
