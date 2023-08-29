#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

bool alphabetical(string text);
bool repeated(string text);

int main(int argc, string argv[])
{
    string key = argv[1];
    //check for human error

    if (argc <= 1 || argc > 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    else if (alphabetical(key) == false)
    {
        return 1;
    }
    else if (repeated(key) == true)
    {
        return 1;
    }
    else
    {
        //if everything goes ok do this

        string text = get_string("plaintext: ");
        string cipher = text;

        int length = strlen(text);
        int x = 0;

        for (int i = 0, n = length; i < n; i++)
        {
            if (isupper(text[i]))
            {
                x = text[i];
                cipher[i] = toupper(key[x - 65]);
            }
            else if (islower(text[i]))
            {
                x = text[i];
                cipher[i] = tolower(key[x - 97]);
            }
            else
            {
                cipher[i] = text[i];
            }
        }

        printf("ciphertext: %s\n", cipher);
        return 0;
    }
}

bool alphabetical(string text)
{
    int i = 0;

    while (text[i] != '\0')
    {
        if (isalpha(text[i]))
        {
            i++;
        }
        else
        {
            return false;
        }
    }

    return true;
}

bool repeated(string text)
{
    int i = 0, n = 0, times = 0;
    string used = text;
    while (text[i] != '\0')
    {
        while (used[n] != '\0')
        {
            if (toupper(text[i]) == toupper(used[n]))
            {
                times++;
            }
            n++;
        }
        if (times > 1)
        {
            return true;
        }
        n = 0;
        times = 0;
        i++;
    }
    return false;
}