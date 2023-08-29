#include <math.h>

#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    double avg = 0;//cant use integer for possible decimal numbers from division
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //add every rgb value, round it, and apply the "grey" value, to the original array
            avg = image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue;
            avg /= 3;
            avg = round(avg);
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
            avg = 0;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE mirror[height][width];
    int r_width = width - 1; //reverse width
    //save image array backwards on width to mirror
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            mirror[i][r_width] = image[i][j];
            r_width--;
        }
        r_width = width - 1;
    }
    //now save it to the original array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = mirror[i][j];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE blur [height][width];
    double red = 0, green = 0, blue = 0;//used for averages
    int top = -1, left = -1, bottom = 1, right = 1; //if not on edges initialise Top, Left at -1 and bottom, right at 1

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //for all pixels inside
            top = -1;
            left = -1;

            bottom = 1;
            right = 1;
            if (i == 0 && j == 0)//Top Left pixel
            {
                top = 0;
                left = 0;
            }
            else if (i == 0 && j == (width - 1))//top right pixel
            {
                top = 0;
                right = 0;
            }
            else if (i == (height -  1) && j == 0)//bottom left pixel
            {
                left = 0;
                bottom = 0;
            }
            else if (i == (height - 1) && j == (width - 1))//bottom right pixel
            {
                bottom = 0;
                right = 0;
            }
            else if (i == 0)//top edge
            {
                top = 0;
            }
            else if (i == (height - 1))//bottom edge
            {
                bottom = 0;
            }
            else if (j == 0)//left edge
            {
                left = 0;
            }
            else if (j == (height - 1))//right edge
            {
                right = 0;
            }

            //Variable x - will go trough the rows, and Variable y - will go trough the columns
            int pixels = 0;

            for (int x = top; x <= bottom; x++)
            {
                for (int y = left; y <= right; y++)
                {
                    pixels++;
                    red += image[i + x][j + y].rgbtRed;
                    green += image[i + x][j + y].rgbtGreen;
                    blue += image[i + x][j + y].rgbtBlue;
                }
            }

            red = round(red / pixels);
            green = round(green / pixels);
            blue = round(blue / pixels);

            blur[i][j].rgbtRed = red;
            blur[i][j].rgbtGreen = green;
            blur[i][j].rgbtBlue = blue;

            red = 0;
            green = 0;
            blue = 0;
        }
    }
    //now save it to the original array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = blur[i][j];
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE sobel[height][width];
    double xred = 0, xgreen = 0, xblue = 0, yred = 0, ygreen = 0, yblue = 0;//for sums
    int top = -1, left = -1, bottom = 1, right = 1; //if not on edges initialise Top, Left at -1 and bottom, right at 1
    
    //sobel matrixes
    int gx[3][3] =
    {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };

    int gy[3][3] =
    {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}
    };


    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //for all pixels inside
            top = -1;
            left = -1;

            bottom = 1;
            right = 1;
            if (i == 0 && j == 0)//Top Left pixel
            {
                top = 0;
                left = 0;
            }
            else if (i == 0 && j == (width - 1))//top right pixel
            {
                top = 0;
                right = 0;
            }
            else if (i == (height -  1) && j == 0)//bottom left pixel
            {
                left = 0;
                bottom = 0;
            }
            else if (i == (height - 1) && j == (width - 1))//bottom right pixel
            {
                bottom = 0;
                right = 0;
            }
            else if (i == 0)//top edge
            {
                top = 0;
            }
            else if (i == (height - 1))//bottom edge
            {
                bottom = 0;
            }
            else if (j == 0)//left edge
            {
                left = 0;
            }
            else if (j == (height - 1))//right edge
            {
                right = 0;
            }

            for (int x = top; x <= bottom; x++)
            {
                for (int y = left; y <= right; y++)
                {
                    int mx = x + 1, my = y + 1;
                    //values used to calculate pixels against gx matrix and gy matrix, adding 1 to reset to 0
                    //and using already existent image border detection to only use the needed matrix values

                    //calculate Gx kernel
                    xred += (image[i + x][j + y].rgbtRed * gx[mx][my]);
                    xgreen += (image[i + x][j + y].rgbtGreen * gx[mx][my]);
                    xblue += (image[i + x][j + y].rgbtBlue * gx[mx][my]);
                    //calculate Gy kernel
                    yred += (image[i + x][j + y].rgbtRed * gy[mx][my]);
                    ygreen += (image[i + x][j + y].rgbtGreen * gy[mx][my]);
                    yblue += (image[i + x][j + y].rgbtBlue * gy[mx][my]);

                }
            }

            //combine Gx kernel with Gy kernel
            //using xRGB for merging sobel
            xred = round(sqrt(pow(xred, 2) + pow(yred, 2)));
            xgreen = round(sqrt(pow(xgreen, 2) + pow(ygreen, 2)));
            xblue = round(sqrt(pow(xblue, 2) + pow(yblue, 2)));

            //check for erratic values, only 0 to 255
            if (xred < 0)
            {
                xred = 0;
            }
            else if (xred > 255)
            {
                xred = 255;
            }
            if (xgreen < 0)
            {
                xgreen = 0;
            }
            else if (xgreen > 255)
            {
                xgreen = 255;
            }
            if (xblue < 0)
            {
                xblue = 0;
            }
            else if (xblue > 255)
            {
                xblue = 255;
            }
            //save it on sobel array
            sobel[i][j].rgbtRed = xred;
            sobel[i][j].rgbtGreen = xgreen;
            sobel[i][j].rgbtBlue = xblue;

            //reinitialise sums
            xred = 0;
            xgreen = 0;
            xblue = 0;

            yred = 0;
            ygreen = 0;
            yblue = 0;
        }
    }

    //now save it to the original array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = sobel[i][j];
        }
    }

    return;
}
