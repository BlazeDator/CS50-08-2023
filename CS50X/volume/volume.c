// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

typedef uint8_t byte;
typedef int16_t sample;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    byte *header = malloc(1);

    for (int i = 0; i < HEADER_SIZE; i++)
    {
        fread(header, 1, 1, input);
        fwrite(header, 1, 1, output);
    }

    free(header);
    // TODO: Read samples from input file and write updated data to output file
    sample *buffer = malloc(2);

    while (feof(input) == 0 && ferror(input) == 0)
    {
        fread(buffer, 2, 1, input);
        *buffer *= factor;
        if (feof(input) == 0 && ferror(input) == 0)
        {
            fwrite(buffer, 2, 1, output);
        }
    }

    free(buffer);
    // Close files

    fclose(input);
    fclose(output);
    return 0;
}
