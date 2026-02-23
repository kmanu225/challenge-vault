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

double get_time()
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
    FILE *in_file  = fopen(fname, "r"); // read the grid
    if (in_file == NULL)
    {
        printf("No file found\n");
        exit(0);
    }
    for(int i=0; i<9; i++)
    {
        fscanf(in_file, "%d %d %d %d %d %d %d %d %d",
                &grid[i][0],&grid[i][1],&grid[i][2],
                &grid[i][3],&grid[i][4],&grid[i][5],
                &grid[i][6],&grid[i][7],&grid[i][8]);
    }
}

int getBlockFromRowColumn(int row, int column)
{
    return 3*(row/3)+column/3;
}

int checkColumn(char grid[][9], int nb)
{
    int found[10] = {0};
    for(int i=0; i<9; i++)
    {
        int c = grid[i][nb];
        found[c]++;
        if(c>0 && found[c]>1)
            return FALSE;
    }

    return TRUE;
}

int checkRow(char grid[][9], int nb)
{
    int found[10] = {0};
    for(int i=0; i<9; i++)
    {
        int c = grid[nb][i];
        found[c]++;
        if(c>0 && found[c]>1)
            return FALSE;
    }

    return TRUE;
}

int checkBlock(char grid[][9], int nb)
{
    int found[10] = {0};
    int nb_x = nb%3;
    int nb_y = nb/3;
    for(int i=0; i<3; i++)
        for(int j=0; j<3; j++)
        {
            int c = grid[3*nb_x+i][3*nb_y+j];
            found[c]++;
            if(c>0 && found[c]>1)
                return FALSE;
        }

    return TRUE;
}


DWORD WINAPI checkAllColumns(LPVOID grid)
{
    for(int i=0; i<9; i++)
        if(!checkColumn(grid, i))
            return FALSE;

    return TRUE;
}

DWORD WINAPI checkAllRows(LPVOID grid)
{
    for(int i=0; i<9; i++)
        if(!checkRow(grid, i))
            return FALSE;

    return TRUE;
}

DWORD WINAPI checkAllBlocks(LPVOID grid)
{
    for(int i=0; i<9; i++)
        if(!checkBlock(grid, i))
            return FALSE;

    return TRUE;
}


int checkGrid(char grid[][9])
{
    return checkAllRows(grid) && checkAllColumns(grid) && checkAllBlocks(grid);
}

int checkGridParallel(char grid[][9])
{
    HANDLE hArray[3];
    hArray[0] = CreateThread(NULL,0,checkAllRows,grid,0,NULL);
    hArray[1] = CreateThread(NULL,0,checkAllColumns,grid,0,NULL);
    hArray[2] = CreateThread(NULL,0,checkAllBlocks,grid,0,NULL);

    int exitr, exitc, exitb;
    WaitForMultipleObjects(3, hArray, TRUE, INFINITE); // wait all

    DWORD exitcode[3];
    for(int i=0; i<3; i++)
    {
        GetExitCodeThread(hArray[i], &exitcode[i]);
        CloseHandle(hArray[i]);
    }

    return exitcode[0] && exitcode[1] && exitcode[2];
}

int checkCell(char grid[][9], int row, int column)
{
    return checkRow(grid, row) && checkColumn(grid, column) && checkBlock(grid, getBlockFromRowColumn(row, column));
}

double benchmark_check(int checkFn(char[][9]), char grid[][9])
{
    double before = get_time();
    double nb_iter = 0;

    while(get_time() - before < 5)
    {
        nb_iter += 1;
        (*checkFn)(grid);
    }
    return 1000*(get_time() - before)/nb_iter;
}

char (*solution)[9][9] = NULL;
volatile int nb_iter = 0;

DWORD WINAPI backtrackParallel(LPVOID ptr)
{
    char (*grid)[][9] = (char (*)[9][9]) ptr;
    nb_iter++;
    int row=-1,column=-1;
    for(int i=0; i<9; i++)
    {
        for(int j=0; j<9; j++)
        {
            if((*grid)[i][j]==0)
            {
                row=i;
                column=j;
                break;
            }
        }
        if(row != -1)
            break;
    }

    if(row == -1) // solved !
    {
        solution = grid;
        return TRUE;
    }

    HANDLE hArray[9];
    int nb_thread = 0;
    for(int n=1; n<=9; n++)
    {
        (*grid)[row][column] = n;
        if(checkCell(*grid, row, column))
        {
            char (*new_grid)[9][9];
            new_grid=(char (*)[9][9]) malloc(sizeof(char)*9*9);
            // copy of the grid
            memcpy(new_grid, grid, 9*9*sizeof(char));
            hArray[nb_thread] = CreateThread(NULL,0,backtrackParallel,(LPVOID) new_grid,0,NULL);
            if(hArray[nb_thread] == NULL)
            {
                printf("Too many threads!\n");
                GetLastError();
                exit(1);
            }

            nb_thread++;
        }
    }

    for(int n=0; n<nb_thread; n++)
    {
        WaitForSingleObject(hArray[n], INFINITE);
        int output;
        GetExitCodeThread(hArray[n], &output);
        CloseHandle(hArray[n]);

        if(output == TRUE)
            return TRUE;
    }

    free(grid);
    return FALSE;
}

int backtrack(char grid[][9])
{
    nb_iter++;
    int row=-1,column=-1;
    for(int i=0; i<9; i++)
    {
        for(int j=0; j<9; j++)
            if(grid[i][j]==0)
            {
                row=i;
                column=j;
                break;
            }
        if(row != -1)
            break;
    }

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


void* fastBacktrack(char grid[][9])
{
    nb_iter++;
    int row=-1,column=-1;
    for(int i=0; i<9; i++)
    {
        for(int j=0; j<9; j++)
            if(grid[i][j]==0)
            {
                row=i;
                column=j;
                break;
            }
        if(row != -1)
            break;
    }

    if(row == -1) // solved !
        return (char*) grid;

    for(int n=1; n<=9; n++)
    {
        grid[row][column] = n;
        if(checkCell(grid, row, column))
        {
            char* output = fastBacktrack(grid);
            if(output != NULL)
                return output;
        }
    }
    grid[row][column] = 0;
    return NULL;
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
            /* printf("Benchmark checkGrid: %fms\n",benchmark_check(checkGrid, grid)); */
            /* printf("Benchmark checkGridParallel: %fms\n",benchmark_check(checkGridParallel, grid)); */

            char (*new_grid)[9][9];
            new_grid=(char (*)[9][9]) malloc(sizeof(char)*9*9);
            // copy of the grid
            memcpy(new_grid, grid, 9*9*sizeof(char));

            double before = get_time();
            nb_iter = 0;
            int solved = backtrack(new_grid);
            if(solved)
            {
                printf("Solve time: %fs\n",(get_time()-before));
                printf("Iterations: %d\n", nb_iter);
                printf("Solution :\n");
                printGrid(solution);
            }

            before = get_time();
            nb_iter = 0;
            solved = backtrackParallel(new_grid);
            if(solved)
            {
                printf("Solve time: %fs\n",(get_time()-before));
                printf("Iterations: %d\n", nb_iter);
                printf("Solution :\n");
                printGrid(solution);
            }
            else
            {
                printf("No solution !\n");
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
