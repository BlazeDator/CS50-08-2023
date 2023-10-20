#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    //printf("%i letters\n", letters);
    //printf("%i words\n", words);
    //printf("%i sentences\n", sentences);

    //where L is the average number of letters per 100 words in the text, and S is the average number of sentences per 100 words in the text.
    float index;
    float L = (letters * 100) / words;
    float S = (sentences * 100) / words;

    //Coleman-Liau index Formula
    index = 0.0588 * L - 0.296 * S - 15.8;

    int grade = round(index);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 1 && grade < 16)
    {
        printf("Grade %i\n", grade);
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
}

int count_letters(string text)
{
    int i = 0, letters = 0;

    //This loop and conditional capitalize the current string character, if possible, then match them against the abcedary ascii range

    while (text[i] != '\0')
    {
        char c = toupper(text[i]);

        if (c >= 65 && c <= 90)
        {
            letters++;
        }

        i++;
    }

    return letters;
}

int count_words(string text)
{
    int i = 0, words = 0, lastletter = -1;


    while (text[i] != '\0')
    {
        //While the loop runs through the string, this conditionals save the position if letters were written in lastletter
        //then if theres an empty space adds one to the word count, and resets the last letter so we dont count empty spaces
        //the last conditional, checks for the end of the string to add the last word, if there isn't an empty space

        char c = toupper(text[i]);

        if (c == 32 && lastletter != -1)
        {
            words++;
            lastletter = -1;
        }
        else if (lastletter != -1 && c == 39 && text[i - 1] == 73) // checking for ' composited words like i've
        {
            words++;
            lastletter = i;
        }
        else if (c != 32 && ((c >= 65 && c <= 90) || ((c == 45) && lastletter != -1)))
        {
            lastletter = i;
        }
        else if (text[i + 1] == '\0' && lastletter != -1)
        {
            words++;
        }

        i++;
    }


    return words;
}

int count_sentences(string text)
{
    int i = 0, sentences = 0, lastletter = -1;

    //Here we check if there's been anything written before a punctuation mark if so, count it as a sentence

    while (text[i] != '\0')
    {
        if ((text[i] == 46 || text[i] == 63 || text[i] == 33) && lastletter != -1)
        {
            sentences++;
        }
        else if (text[i] != 32)
        {
            lastletter = i;
        }
        i++;
    }

    return sentences;
}