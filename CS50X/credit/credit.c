#include <cs50.h>
#include <stdio.h>

long getdigit(long number, int digit);
bool checksum(long number);
void ccbrand(long number);

int main(void)
{
    long ccnumber = get_long("Number: ");
    if (checksum(ccnumber) == true)
    {
        ccbrand(ccnumber);
    }
    else
    {
        printf("INVALID\n");
    }
}

long getdigit(long number, int digit)
{
    long remainder;
    long num;
    //for loop that reads each digit until it reaches de desired one, in the int = digit, then returns it
    //everytime i divide it by ten, i reduce it by 1 digit making the last number the remainder when i do modulo operator by 10

    for (int i = 1; i <= 16; i++)
    {
        remainder = number % 10;
        number = number / 10;

        if (i == digit)
        {
            num = remainder;
        }
    }
    return num;
}

bool checksum(long number)
{
    long even = 0;
    long odd = 0;
    //if the multiplied number is higher than 1 digit, i need to take each number instead of adding the total, mistake made in last atttempt
    for (int i = 1; i <= 16; i++)
    {
        long current = getdigit(number, i);
        if (i % 2 == 0)
        {
            current *= 2;
            if (current >= 10)
            {
                even += getdigit(current, 1);
                even += getdigit(current, 2);
            }
            else
            {
                even += current;
            }
        }
        else
        {
            odd += current;
        }
    }
    //printf("even: %li\n", even);
    //printf("odd: %li\n", odd);
    //printf("total: %li\n", odd+even);
    if (getdigit(even + odd, 1) == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

void ccbrand(long number)
{
    if (getdigit(number, 16) == 5 && (getdigit(number, 15) >= 1 && getdigit(number, 15) <= 5))
    {
        printf("MASTERCARD\n");
    }
    else if (getdigit(number, 16) == 4)
    {
        printf("VISA\n");
    }
    else if (getdigit(number, 15) == 3 && (getdigit(number, 14) == 4 || getdigit(number, 14) == 7))
    {
        printf("AMEX\n");
    }
    else if (getdigit(number, 13) == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}