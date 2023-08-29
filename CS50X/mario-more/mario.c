#include <cs50.h>
#include <stdio.h>

void bricks(int row);
void spaces(int row, int height);

int main(void)
{
    //iniatilise height integer
    int height = 0;

    //ask for user input until he cooperates
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    //create the mario pyramid according to the height received
    //spaces function compares the current row to the height to know how many empty spaces to make
    //bricks function adds the numbers of bricks depending on the row its on

    for (int i = 1; i <= height; i++)
    {
        spaces(i, height);
        bricks(i);
        printf("  ");
        bricks(i);
        printf("\n");
    }
}

void bricks(int row)
{
    for (int i = 0; i < row; i++)
    {
        printf("#");
    }
}

void spaces(int row, int height)
{
    for (int i = height; i > row; i--)
    {
        printf(" ");
    }
}