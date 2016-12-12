#include "common.h"
#include "mpi.h"


int main(int argc, char *argv[])
{
	int proc_total;
	int proc_id;
	MPI_Comm_size(MPI_COMM_WORLD, &proc_total);
	printf("total proc %d\n", proc_total);
	
	return 0;
}
