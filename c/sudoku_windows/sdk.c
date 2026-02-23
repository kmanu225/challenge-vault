#include <windows.h>
#include <stdio.h>

#define TRUE 1
#define FALSE 0

/*
 * Row, column and block identification

   0 1 2 3 4 5 6 7 8
  +-----+-----+-----+
0 |     |     |     |
1 |blk 0|blk 1|blk 2|
2 |     |     |     |
  +-----+-----+-----+
3 |     |     |     |
4 |blk 3|blk 4|blk 5|
5 |     |     |     |
  +-----+-----+-----+
6 |     |     |     |
7 |blk 6|blk 7|blk 8|
8 |     |     |     |
  +-----+-----+-----+

*/


HANDLE mutex;

double getTime()
{
    LARGE_INTEGER t, f;
    QueryPerformanceCounter(&t);
    QueryPerformanceFrequency(&f);
    return (double)t.QuadPart/(double)f.QuadPart;
}

char char_from_int(int nb)
{
    if(nb==0) return ' ';
    return nb+'0';
}

// print the grid
void printGrid(char grid[][9])
{
    if(mutex == NULL)
    {
        mutex = CreateMutex( NULL, FALSE, NULL);
    }

    WaitForSingleObject(mutex, INFINITE);

    for(int i=0; i<3; i++)
    {
        printf("+-----+-----+-----+\n");
        for(int j=0; j<3; j++)
        {
            for(int k=0; k<3; k++)
            {
                printf("|%c %c %c",
                    char_from_int(grid[i*3+j][3*k]),
                    char_from_int(grid[i*3+j][3*k+1]),
                    char_from_int(grid[i*3+j][3*k+2]));
            }
            printf("|\n");
        }
    }
    printf("+-----+-----+-----+\n");

    ReleaseMutex(mutex);
}

// read the grid from the file
void readGrid(char grid[][9], char* fname)
{
    // TODO à compléter (Q1)
}

int getBlockFromRowColumn(int row, int column)
{
    return 3*(row/3)+column/3;
}

int checkColumn(char grid[][9], int nb)
{
    // TODO à compléter (Q2)
    return TRUE;
}

int checkRow(char grid[][9], int nb)
{
    // TODO à compléter (Q2)
    return TRUE;
}

int checkBlock(char grid[][9], int nb)
{
    // TODO à compléter (Q2)
    return TRUE;
}

int checkGrid(char grid[][9])
{
    // TODO à compléter (Q2)
    return TRUE;
}

DWORD WINAPI checkAllColumns(LPVOID grid)
{
    // TODO à compléter (Q3)
    return TRUE;
}

DWORD WINAPI checkAllRows(LPVOID grid)
{
    // TODO à compléter (Q3)
    return TRUE;
}

DWORD WINAPI checkAllBlocks(LPVOID grid)
{
    // TODO à compléter (Q3)
    return TRUE;
}

int checkGridParallel(char grid[][9])
{
    // TODO à compléter (Q3)
    return TRUE;
}

int checkCell(char grid[][9], int row, int column)
{
    // check if the grid is still valid after modifying the digit in grid[row][column]
    return checkRow(grid, row) && checkColumn(grid, column) && checkBlock(grid, getBlockFromRowColumn(row, column));
}

char (*solution)[9][9] = NULL;
volatile int nb_iter = 0;

DWORD WINAPI backtrackParallel(LPVOID ptr)
{
    char (*grid)[][9] = (char (*)[9][9]) ptr;
    // TODO: compléter (Q5)
    return FALSE;
}

int backtrack(char grid[][9])
{
    nb_iter++;
    int row=-1,column=-1;
    // TODO: à compléter (Q4)
    // compléter la recherche de "row" et "column". S'il n'y en a aucun, laisser "row" et "column" à -1.

    if(row == -1) // solved !
    {
        if(checkGrid(grid))
        {
            solution = grid;
            return TRUE;
        }
        else
        {
            free(grid);
            return FALSE;
        }
    }

    for(int n=1; n<=9; n++)
    {
        grid[row][column] = n;
        if(checkCell(grid, row, column))
        {
            char (*new_grid)[9][9];
            new_grid=(char (*)[9][9]) malloc(sizeof(char)*9*9);
            // copy of the grid
            memcpy(new_grid, grid, 9*9*sizeof(char));

            int output = backtrack(new_grid);
            if(output == TRUE)
                return TRUE;
        }
    }
    free(grid);
    return FALSE;
}


int main(int argc, char **argv)
{
    char grid[9][9]; // create a grid with 9 columns and 9 rows

    if(argc > 1)
    {
        readGrid(grid, argv[1]);

        printGrid(grid);
        if(!checkGrid(grid))
            printf("The grid is invalid!\n");
        else
        {
            char (*new_grid)[9][9];
            new_grid=(char (*)[9][9]) malloc(sizeof(char)*9*9);
            // copy of the grid
            memcpy(new_grid, grid, 9*9*sizeof(char));

            double before = getTime();
            nb_iter = 0;
            backtrack(grid);
            if(checkGrid(grid))
            {
                printf("Solve time: %fs\n",(getTime()-before));
                printf("Iterations: %d\n", nb_iter);
                printf("Solution :\n");
                printGrid(grid);
            }
        }
    }
    else
    {
        printf("Usage: %s filename.sdk\n", argv[0]);
        return 0;
    }

  return 0;
}
