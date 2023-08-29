#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    //This loop checks the name given against every candidate recorded and save the votes in order, on the ranks array
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    bool candidates_voted[candidate_count];
    //I need to know which candidates were voted on already, to know which are preferred over one another
    for (int i = 0; i < candidate_count; i++)
    {
        candidates_voted[i] = false;
    }

    //This loop goes through the votes in the rank array - Variable I
    for (int i = 0; i < candidate_count; i++)
    {
        //This loop goes through the preferences[x][] value of the preferences array
        for (int x = 0; x < candidate_count; x++)
        {
            //This loop goes through the preferences[][y] value of the preferences array
            for (int y = 0; y < candidate_count; y++)
            {
                if (x == y)
                {
                    preferences[x][y] = 0;
                    //do nothing
                }
                else if (ranks[i] == x && candidates_voted[y] == false)
                {
                    //the candidate that is voting right now is preffered over the next ones, so I save that knowledge
                    candidates_voted[x] = true;

                    preferences[x][y]++;
                }
            }
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    pair_count = 0;

    //go through the preferences array sequentially and determine if [x][y] is bigger then [y][x], if so save it to pairs
    for (int x = 0; x < candidate_count; x++)
    {
        for (int y = 0; y < candidate_count; y++)
        {
            if (x == y)
            {
                //do nothing
            }
            else if (preferences[x][y] > preferences [y][x])
            {
                pairs[pair_count].winner = x;
                pairs[pair_count].loser = y;

                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int swap_counter = 0, current, next, tradew, tradel;

    //Checking the pairs array, by having pairs[n] against pairs[n + 1], to see if they need to be sorted
    //using tradew and tradel to save the current pairs[n], to allocate to the n + 1, after copied over
    //current and next are used to simplify the comparison of strength of victory
    ///swap counter, is so we dont waste loops when it's done sorting

    for (int i = 0; i < pair_count; i++)
    {
        for (int n = 0; n < (pair_count - 1); n++)
        {
            current = preferences[pairs[n].winner][pairs[n].loser] - preferences[pairs[n].loser][pairs[n].winner];
            next = preferences[pairs[n + 1].winner][pairs[n + 1].loser] - preferences[pairs[n + 1].loser][pairs[n + 1].winner];

            if (current < next)
            {
                tradew = pairs[n].winner;
                tradel = pairs[n].loser;

                pairs[n].winner = pairs[n + 1].winner;
                pairs[n].loser = pairs[n + 1].loser;

                pairs[n + 1].winner = tradew;
                pairs[n + 1].loser = tradel;
            }
            swap_counter++;
        }
        if (swap_counter == 0)
        {
            return;
        }
        swap_counter = 0;
    }
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    int x, y;
    bool loop = false, loopers[candidate_count];

    for (int i = 0; i < candidate_count; i++)
    {
        loopers[i] = false;
    }

    for (int i = 0; i < pair_count; i++)
    {
        x = pairs[i].winner;
        y = pairs[i].loser;
        loop = false;

        for (int j = 0; j < candidate_count; j++)
        {
            //if the loser im pointing to is pointing to someone who pointed at me, call it a loop and dont create a connection
            if (locked[y][j] == true && locked[j][x] == true)
            {
                loop = true;
            }
        }
        //if it wasnt a loop, and who im pointing to, hasnt been pointed by anyone else, lock this pair
        if (loop == false && loopers[y] == false)
        {
            locked[x][y] = true;
            loopers[y] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    bool winner = false;

    //the loops checks if the candidate was pointed by anyone else, if not, it's the winner
    for (int x = 0; x < candidate_count; x++)
    {
        winner = true;

        for (int y = 0; y < candidate_count; y++)
        {
            if (locked[y][x] == true)
            {
                winner = false;
            }
        }

        if (winner == true)
        {
            printf("%s\n", candidates[x]);
            return;
        }

    }

    return;
}