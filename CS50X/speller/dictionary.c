// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 676;

// Hash table
node *table[N];

// Dictionary Size
int dict_size = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int bucket = 0;
    node *scanner = NULL;// start a pointer node, that will be used just to check already allocated memory
    // Don't free it, since any memory it touches will be freed on unload function
    bucket = hash(word);// find out where to check the word;
    if (table[bucket] == NULL)// if there is no linked list on this hash table, the word is misspelled
    {
        return false;
    }
    else// if there is a linked list
    {
        scanner = table[bucket];// make my scanner node, point to the start of it
        while (scanner != NULL)// while there is nodes to scan, keep looping
        {
            if (strcasecmp(scanner->word, word) == 0)// if the current node->word is the same as the word provided, return true
            {
                return true;
            }
            else// go to next node
            {
                scanner = scanner->next;
            }
            // if there is no next node, loop will break
        }
    }
    // since there were no words in the linked list hashed equal to the word given, return false
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int bucket = 0, x = 0, y = 0;

    if (toupper(word[0]) > 64 && toupper(word[0]) < 91 && toupper(word[1]) > 64 && toupper(word[1]) < 91)
    {
        x = toupper(word[0]) - 65;
        y = toupper(word[1]) - 65;
        x = x * 26;
        //printf("x - %i, y - %i -> ", x, y); //TEST PURPOSES
        bucket = x + y;
    }
    else
    {
        bucket = 0;
    }

    return bucket;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");// Open dictionary
    if (dict == NULL) // If it didnt open, return unsuccessful
    {
        return false;
    }
    char *word = malloc(LENGTH + 1);// Create a string with size of largest word
    if (word == NULL)// if string didnt have enough memory stop
    {
        fclose(dict);
        return false;
    }
    node *n = malloc(sizeof(node));// create a new node
    if (n == NULL)// if n didnt have enough memory close
    {
        free(word);
        fclose(dict);
        return false;
    }

    int bucket = 0;// initialise bucket variable
    fscanf(dict, "%s", word);// Read first word
    while (feof(dict) == 0 && ferror(dict) == 0)//while there are words to read from file
    {
        bucket = hash(word);// find out where to store the word
        if (table[bucket] == NULL)// check if there is already nodes, if not, start a linked list
        {
            n->next = NULL;// create first node
            strcpy(n->word, word);//copy word into first node
            table[bucket] = n;// make hash table point to node
        }
        else// if there were nodes present
        {
            n->next = table[bucket];// make new node point to current linked list
            strcpy(n->word, word);// copy new word into node
            table[bucket] = n;// make hash table point to the new node
        }
        n = malloc(sizeof(node));// give the next node new memory, as to not overwrite the node created previously
        //printf("hash was - %i -> word was - %s\n", bucket, word); //TEST PURPOSES
        dict_size++;//increase dictionary count size
        fscanf(dict, "%s", word);//read next word
    }

    free(word);//free memory allocated to string
    free(n);//free memory allocated to new node
    fclose(dict);// Close Dictionary
    if (dict_size > 0)// if there were words read, dictionary was read
    {
        return true;
    }
    else//if not, something went wrong
    {
        return false;
    }
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (dict_size > 0)//check if dictionary was read, if so return size
    {
        return dict_size;
    }
    else// else it was empty
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    node *cleaner = NULL;// create the cleaner node which will travel the linked lists
    node *garbage = NULL;// create the garbage node which will clean any used nodes found by cleaner
    int count = 0;// initialise counter to know if there were as many nodes cleaned, as words read from dictionary

    for (int i = 0; i < N; i++)// travel trough the whole hash table
    {
        if (table[i] == NULL)// if no linked list present, go on your merry way
        {
            //do nothing, its already clean
        }
        else// if there was a linked list
        {
            cleaner = table[i];// make cleaner point to it
        }

        while (cleaner != NULL)// while cleaner is pointing at a node on the current linked list
        {
            garbage = cleaner;// make garbage point to current node
            cleaner = cleaner->next;// make cleaner point to next node
            free(garbage);// cleanup memory on garbage node
            count++;// add 1 to the nodes cleared
            // if the next node exists, repeat the process
        }
    }
    //printf("Nodes Cleared: %i\n", count); //TEST PURPOSES

    if (count == dict_size)// if there were as many nodes cleared as words in dictionary, it was successful
    {
        return true;
    }
    else// if not, return false
    {
        return false;
    }
}