#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef uint8_t BYTE;
int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)//check for right number of arguments
    {
        printf("Invalid number of arguments, should be ./recover file");
        return 1;
    }
    FILE *file = fopen(argv[1], "r");

    BYTE *buffer = malloc(512);
    BYTE *signature = malloc(5);
    int jpgs_c = 0; //jpgs counter, for naming purposes
    bool readingjpg = false;

    signature[0] = 0xff;//checking for jpg signature
    signature[1] = 0xd8;
    signature[2] = 0xff;
    signature[3] = 0xe0;//4th byte value minimum
    signature[4] = 0xef;//4th byte value maximum

    char *naming = malloc(8);
    sprintf(naming, "%03d.jpg", jpgs_c);//used for naming files, %03d adds 2 leading zeroes if 1-9, 1 leading zero if 10 - 99

    FILE *newjpg = fopen(naming, "w");//initialise first jpg file

    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)//as long as there is new 512 blocks, keep checking for and writing jpgs
    {
        if (buffer[0] == signature[0] && buffer[1] == signature[1] && buffer[2] == signature[2] && buffer[3] >= signature[3]
            && buffer[3] <= signature[4])
        {
            //only enters here if jpg signature found
            if (readingjpg == false)//if not writing yet, start writing a new jpg
            {
                readingjpg = true;
                fwrite(buffer, 1, BLOCK_SIZE, newjpg);
            }
            else if (readingjpg == true)//if writing a jpg before, this means there is a new one on this block
            {
                //close the last one
                fclose(newjpg);
                jpgs_c++;
                //name the new one
                sprintf(naming, "%03d.jpg", jpgs_c);
                //start writing it
                newjpg = fopen(naming, "w");
                fwrite(buffer, 1, BLOCK_SIZE, newjpg);
            }
        }
        else if (readingjpg == true)//if no new signature and was writing jpg keep writing
        {
            fwrite(buffer, 1, BLOCK_SIZE, newjpg);
        }
    }
    //clean up memory
    free(buffer);
    free(signature);
    free(naming);
    fclose(file);
    fclose(newjpg);//close last opened jpg
    return 0;
}