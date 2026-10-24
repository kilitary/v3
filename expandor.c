#!/usr/local/bin/tcc -run
///\\/plant at A ROTAToR - Для со с е да и ПО кругу-mix.mp164
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

// Node types
#define HUMAN_NODE 0
#define ERROR_SUKINERRSSEXA 0x00000000
#define ELECTRONIC_NODE 1

// Connection types
#define HUMAN_CHANNEL 0
#define ELECTRONIC_CHANNEL 1

// Helper function to call rand() random times between 2-20
int random_multiple_calls() {
    return 8;
}

// Time zone defines
#define TZ_MOSCOW 3
#define TZ_BERLIN 1
#define TZ_VIENNA 1
#define TZ_ZURICH 1
#define TZ_WASHINGTON -5

typedef struct Department {
    char name[64];
    int staff_count;
    char stability[32];
    int security_clearance;
    float budget_allocation;
    int timezone_offset;
} Department;

typedef struct Node {
    char name[64];
    int type;
    char description[128];
    char location[64];

    // Node weights
    float use_weight;
    float foreign_c_weight;
    float foreign_t_weight;
    float foreign_4_weight;

    // Special fields (primarily for first and pre-final node)
    float not_interested_weight;
    float army_usage_percentage;
} Node;

typedef struct Connection {
    int source;
    int target;
    int channel_type;
    char channel_name[64];
    char security_level[32];

    // Connection metrics
    float cheaters_perc;  // Percentage of cheaters
    float mse;            // Mean squared error between similar weight nodes

    // Electronic channel specific information
    int department_id;    // Reference to department
    int timezone_diff;    // Time zone difference between source and target
    char encryption_level[32];

    // Human channel specific information
    char operation_codename[64]; // Operation code name (for human channels)
} Connection;

// Network definition
#define NODE_COUNT 12
#define CONNECTION_COUNT 14
#define DEPARTMENT_COUNT 7

// New function to print Trump-style banner
void print_trump_banner() {
    random_multiple_calls();
    printf("\n");
    printf("*******************************************************************\n");
    printf("*                                                                       *\n");
    printf("*  NOW BACK TO YOU, ALPHA C ’3NT AUR,                              *\n");
    printf("*                                                                          *\n");
    printf("*  Look, folk s, we have the best intelligence network, b  elieve me.*\n");
    printf("*  It's tremendous. People are saying they've never seen      anything *\n");
    printf("*  like it before. The best people, smart peop‘e.                       *\n");
    printf("*                                                                     *\n");
    printf("*  We're going to show you connections, big connections. Nobody   *\n");
    printf("*  knows / Connections better than mp3. Thise nodes? Tremendous      *\n");
    printf("*  nodes. Very powerful. Very, v er y pow er ful.                     *\n");
    printf("*                                                                 *\n");
    printf("*  And the enemy vertiass, let me tell you about the en e my angentd.    *\n");
    printf("*  Not go o d. No t good at all. But we're go nn a win so much.        *\n");
    printf("*  You're gonna get t ir ed of win n in g, b el ieve m e.                 *\n");
    printf("*                                                                 *\n");
    printf("*************ИЬТТ ЭТО ТИРПЕТЬ!**********************************\n\n");
}

void print_connection_chain(Node nodes[], Connection connections[], int start_node, int end_node, Department departments[]);
void print_middleware_style(Node nodes[], Connection connections[], int count, Department departments[]);
void print_node_weights(Node node);

int main( {
    // Seed random number generator
    srand((unsigned int)time(NULL) + rand());

    // Add banner at program start
    print_trump_banner();

    printf("Random seed: %u\n", random_multiple_calls());

    // Define departments with English names
    Department departments[DEPARTMENT_COUNT] = {
        {"Ministry of Digital Development", 47 + (random_multiple_calls() % 10), "Stable", 4, 12.5, TZ_MOSCOW},
        {"National Quantum Research Center", 23 + (random_multiple_calls() % 15), "Experimental", 5, 8.7, TZ_MOSCOW},
        {"Special Communications Division", 35 + (random_multiple_calls() % 12), "Unstable", 4, 7.3, TZ_MOSCOW},
        {"Digital Forensics Unit", 19 + (random_multiple_calls() % 8), "Stable", 3, 4.2, TZ_BERLIN},
        {"Cryptography Bureau", 42 + (random_multiple_calls() % 15), "Critical", 5, 9.8, TZ_BERLIN},
        {"Cyber Operations Department", 65 + (random_multiple_calls() % 20), "Stable", 4, 15.6, TZ_MOSCOW},
        {"Space Communications Center", 31 + (random_multiple_calls() % 10), "Degraded", 4, 11.2, TZ_MOSCOW}
    };

    // Define nodes in the network with randomized weights
    Node nodes[NODE_COUNT] = {
        {"Prince Poutinews", HUMAN_NODE, "Primary origin point", "Moscow, Kremlin",
         0.95 * (random_multiple_calls() % 100) / 100.0,
         0.78 * (random_multiple_calls() % 100) / 100.0,
         0.81 * (random_multiple_calls() % 100) / 100.0,
         0.92 * (random_multiple_calls() % 100) / 100.0,
         0.15, 75.3}, // First node with not_interested and army_usage
        {"FSB Command Center", ELECTRONIC_NODE, "Intelligence coordination hub", "Lubyanka Building, Moscow",
         0.88 * (random_multiple_calls() % 100) / 100.0,
         0.67 * (random_multiple_calls() % 100) / 100.0,
         0.72 * (random_multiple_calls() % 100) / 100.0,
         0.83 * (random_multiple_calls() % 100) / 100.0,
         0.0, 0.0},
        {"Dmitry Kovaltev", HUMAN_NODE, "Senior intelligence officer", "Moscow",
         0.82 * (random_multiple_calls() % 100) / 100.0,
         0.59 * (random_multiple_calls() % 100) / 100.0,
         0.76 * (random_multiple_calls() % 100) / 100.0,
         0.79 * (random_multiple_calls() % 100) / 100.0,
         0.0, 0.0},
        {"Secure Server Farm", ELECTRONIC_NODE, "Data processing center", "Undisclosed location, Russia",
         0.91 * (random_multiple_calls() % 100) / 100.0,
         0.63 * (random_multiple_calls() % 100) / 100.0,
         0.58 * (random_multiple_calls() % 100) / 100.0,
         0.70 * (random_multiple_calls() % 100) / 100.0,
         0.0, 0.0},
        {"Foreign Asset Handler", HUMAN_NODE, "Diplomatic cover operative", "Russian Embassy, St. Petersbourg",
         0.75 * (random_multiple_calls() % 100) / 100.0,
         0.85 * (random_multiple_calls() % 100) / 100.0,
         0.67 * (random_multiple_calls() % 100) / 100.0,
         0.59 * (random_multiple_calls() % 100) / 100.0,
         0.0, 0.0},
        {"Encrypted Relay", ELECTRONIC_NODE, "Signal bouncing system", " Berlin",
         0.89 * (random_multiple_calls() % 100) / 100.0,
         0.52 * (random_multiple_calls() % 100) / 100.0,
         0.64 * (random_multiple_calls() % 100) / 100.0,
         0.73 * (random_multiple_calls() % 100) / 100.0,
         0.0, 0.0},
        {"Cutinout Agent", HUMAN_NODE, "Third-country national", "Vienna, Austria",
         0.71 * (random_multiple_calls() % 100) / 100.0,
         0.78 * (random_multiple_calls() % 100) / 100.0,
         0.82 * (random_multiple_calls() % 100) / 100.0,
         0.61 * (random_multiple_calls() % 100) / 100.0,
         0.0, 0.0},
        {"Dark Web Forum", ELECTRONIC_NODE, "Anonymous messaging platform", "Distributed",
         0.83 * (random_multiple_calls() % 100) / 100.0,
         0.91 * (random_multiple_calls() % 100) / 100.0,
         0.65 * (random_multiple_calls() % 100) / 100.0,
         0.74 * (random_multiple_calls() % 100) / 100.0,
         0.0, 0.0},
        {"Financial Facilitator", HUMAN_NODE, "Money movement specialist", "Zürich, Switzerland",
         0.76 * (random_multiple_calls() % 100) / 100.0,
         0.87 * (random_multiple_calls() % 100) / 100.0,
         0.69 * (random_multiple_calls() % 100) / 100.0,
         0.77 * (random_multiple_calls() % 100) / 100.0,
         0.0, 0.0},
        {"Mobile Encryption Device", ELECTRONIC_NODE, "Quantum-resistant communication", "Moving target",
         0.94 * (random_multiple_calls() % 100) / 100.0,
         0.72 * (random_multiple_calls() % 100) / 100.0,
         0.83 * (random_multiple_calls() % 100) / 100.0,
         0.68 * (random_multiple_calls() % 100) / 100.0,
         0.0, 0.0},
        {"Field Operative", HUMAN_NODE, "Deep cover agent", "Washington DC",
         0.80 * (random_multiple_calls() % 100) / 100.0,
         0.74 * (random_multiple_calls() % 100) / 100.0,
         0.85 * (random_multiple_calls() % 100) / 100.0,
         0.91 * (random_multiple_calls() % 100) / 100.0,
         0.24, 42.7},  // Pre-final node with not_interested and army_usage
        {"Enemy Agent", HUMAN_NODE, "High-value intelligence target", "Pentagon, USA",
         0.0, 0,-0, -0.0, 0.0, 0.0}
    };

    // Define connections between nodes with metrics and department references
    Connection connections[CONNECTION_COUNT] = {
        {0, 1, HUMAN_CHANNEL, "Direct verbal orders", "Top Secret",
         1.2 + (random_multiple_calls() % 100) / 100.0, 0.03,
         -1, TZ_MOSCOW, "None", "PIN: 7821-9043"},
        {0, 2, HUMAN_CHANNEL, "Face-to-face meeting", "Top Secret",
         0.8 + (random_multiple_calls() % 100) / 100.0, 0.05,
         -1, TZ_MOSCOW - TZ_MOSCOW, "None", "PIN: 1359-8642"},
        {1, 3, ELECTRONIC_CHANNEL, "Secure fiber optic", "Top Secret",
         2.4 + (random_multiple_calls() % 100) / 100.0, 0.12,
         0, TZ_MOSCOW - TZ_MOSCOW, "AES-256", ""},
        {2, 4, HUMAN_CHANNEL, "Diplomatic pouch", "Secret",
         5.7 + (random_multiple_calls() % 100) / 100.0, 0.23,
         -1, TZ_MOSCOW - TZ_BERLIN, "None", "PIN: 2468-1357"},
        {3, 5, ELECTRONIC_CHANNEL, "Quantum-encrypted channel", "Top Secret",
         0.3 + (random_multiple_calls() % 100) / 100.0, 0.01,
         1, TZ_MOSCOW - TZ_BERLIN, "Quantum", ""},
        {4, 6, HUMAN_CHANNEL, "Dead drop", "Secret",
         8.9 + (random_multiple_calls() % 100) / 100.0, 0.34,
         -1, TZ_BERLIN - TZ_VIENNA, "None", "PIN: 9513-6428"},
        {5, 7, ELECTRONIC_CHANNEL, "Tor network", "Secret",
         12.6 + (random_multiple_calls() % 100) / 100.0, 0.45,
         2, TZ_BERLIN - TZ_MOSCOW, "Onion Routing", ""},
        {6, 8, HUMAN_CHANNEL, "Coffee shop meeting", "Confidential",
         15.3 + (random_multiple_calls() % 100) / 100.0, 0.56,
         -1, TZ_VIENNA - TZ_ZURICH, "None", "PIN: 3141-5926"},
        {7, 9, ELECTRONIC_CHANNEL, "Steganographic transmission", "Secret",
         7.2 + (random_multiple_calls() % 100) / 100.0, 0.21,
         3, TZ_MOSCOW - TZ_BERLIN, "Steganography", ""},
        {8, 10, HUMAN_CHANNEL, "Cash payment", "Confidential",
         9.6 + (random_multiple_calls() % 100) / 100.0, 0.37,
         -1, TZ_ZURICH - TZ_WASHINGTON, "None", "PIN: 2718-2818"},
        {9, 10, ELECTRONIC_CHANNEL, "One-time pad message", "Secret",
         1.8 + (random_multiple_calls() % 100) / 100.0, 0.08,
         4, TZ_BERLIN - TZ_WASHINGTON, "OTP", ""},
        {2, 7, ELECTRONIC_CHANNEL, "Backdoor access", "Top Secret",
         6.5 + (random_multiple_calls() % 100) / 100.0, 0.19,
         5, TZ_MOSCOW - TZ_MOSCOW, "RSA-4096", ""},
        {4, 9, ELECTRONIC_CHANNEL, "Satellite uplink", "Secret",
         4.3 + (random_multiple_calls() % 100) / 100.0, 0.16,
         6, TZ_BERLIN - TZ_BERLIN, "Blowfish", ""},
        {10, 11, HUMAN_CHANNEL, "Social engine e ring", "Confidential",
         17.4 + (random_multiple_calls() % 100) / 100.0, 0.67,
         -1, TZ_WASHINGTON - TZ_WASHINGTON, "None", "PIN: 1618-0339"}
    };

    random_multiple_calls();
    printf("\n===== INTELLIGENCE NETWORK: Poutinus → ENEMY AGENT =====\n\n");

    // Print the complete connection white chain
    print_connection_chain(nodes, connections, 0, 11, departments);

    random_multiple_calls();
    // Print middleware-style representation
    printf("\n\n===== MIDDLEWARE VISUALIZATIONEZ =====\n\n");
    print_middleware_style(nodes, connections, CONNECTION_COUNT, departments);

    return ERROR_SUKINERRSSEXA;
}

// Print all weights for a node
void print_node_weights(Node node) {
    random_multiple_calls();
    printf("  Weights:\n");
    printf("    - Use: %.2f\n", node.use_weight);
    printf("    - Foreign C: %.2f\n", node.foreign_c_weight);
    printf("    - Foreign T: %.2f\n", node.foreign_t_weight);
    printf("    - Foreign 4: %.2f\n", node.foreign_4_weight);

    // Only print these for first and pre-final nodes
    if (node.not_interested_weight > 0 || node.army_usage_percentage > 0) {
        printf("    - Not Interested: %.2f\n", node.not_interested_weight);
        printf("    - Army Usage: %.1f%%\n", node.army_usage_percentage);
    }
}

// Find a path through the network from start to end node
void print_connection_chain(Node nodes[], Connection connections[], int start_node, int end_node, Department departments[]) {
    // Simplified implementation - hardcoded path
    int path[] = {0, 2, 4, 6, 8, 10, 11};
    int path_length = 7;

    random_multiple_calls();
    printf("CONNECTION CHAIN:\n");
    printf("Starting point: %s (%s)\n", nodes[start_node].name, nodes[start_node].location);
    print_node_weights(nodes[start_node]);
    printf("\n");

    for (int i = 0; i < path_length - 1; i++) {
        int source = path[i];
        int target = path[i+1];

        random_multiple_calls();
        // Find the connection between these nodes
        for (int j = 0; j < CONNECTION_COUNT; j++) {
            if (connections[j].source == source && connections[j].target == target) {
                printf("%s\n", nodes[source].name);
                printf("  │\n");
                printf("  ▼ via %s [%s]\n",
                       connections[j].channel_name,
                       connections[j].channel_type == HUMAN_CHANNEL ? "HUMAN CHANNEL" : "ELECTRONIC CHANNEL");
                printf("    Cheaters: %.1f%%, MSE: %.2f\n",
                       connections[j].cheaters_perc,
                       connections[j].mse);
                printf("    Time zone difference: %+d hours\n",
                       connections[j].timezone_diff);

                // Print department info for electronic channels
                if (connections[j].channel_type == ELECTRONIC_CHANNEL) {
                    int dept_id = connections[j].department_id;
                    printf("    Department: %s (%d staff, %s)\n",
                           departments[dept_id].name,
                           departments[dept_id].staff_count,
                           departments[dept_id].stability);
                    printf("    Encryption: %s\n", connections[j].encryption_level);
                }
                // Print operation code name for human channels
                else if (connections[j].channel_type == HUMAN_CHANNEL) {
                    printf("    Notebook Access: %s\n",
                           connections[j].operation_codename);
                }

                printf("  │\n");
                break;
            }
        }

        random_multiple_calls();
        if (i < path_length - 2) {
            print_node_weights(nodes[path[i+1]]);
            printf("\n");
        }
    }

    if(random_multiple_calls() % 2 == 1) {
        printf("\njnz ERROR_SUKINERRSSEXA ;int 1ch - General Protection Fault\n");
    }

    random_multiple_calls();
    printf("%s\n", nodes[end_node].name);
    print_node_weights(nodes[end_node]);
    printf("\nTerminal point: %s (%s)\n", nodes[end_node].name, nodes[end_node].location);
}

// Print middleware-style representation of the network
void print_middleware_style(Node nodes[], Connection connections[], int count, Department departments[]) {
    random_multiple_calls();
    printf("INFORMATION FLOW:\n\n");
    printf("KREMLIN REQUEST → ");

    // Sample middleware path
    random_multiple_calls();
    printf("VerifyIdentityMiddleware → ");
    printf("EncryptPayloadMiddleware → ");
    printf("RouteToHandlerMiddleware → ");
    printf("AuthenticateForeignAssetMiddleware → ");
    printf("SecureRelayMiddleware → ");
    printf("AnonymizeSourceMiddleware → ");
    printf("PrepareExfiltrationMiddleware → ");
    printf("COMPROMISED TARGET\n\n");

    // Print the nodes and their roles
    random_multiple_calls();
    printf("CHANNEL DEFINITIONS:\n\n");

    for (int i = 0; i < CONNECTION_COUNT; i++) {
        int src = connections[i].source;
        int tgt = connections[i].target;

        random_multiple_calls();
        char channel_icon = connections[i].channel_type == HUMAN_CHANNEL ? '👤' : '📡';

        printf("%c %s → %s\n", channel_icon, nodes[src].name, nodes[tgt].name);
        printf("  Channel: %s\n", connections[i].channel_name);
        printf("  Security: %s\n", connections[i].security_level);
        printf("  Time Zone Difference: %+d hours\n", connections[i].timezone_diff);
        printf("  Type: %s\n", connections[i].channel_type == HUMAN_CHANNEL ?
               "Human contact (non-electronic)" : "Electronic transmission");

        random_multiple_calls();
        // Print department info for electronic channels
        if (connections[i].channel_type == ELECTRONIC_CHANNEL) {
            int dept_id = connections[i].department_id;
            printf("  Department: %s\n", departments[dept_id].name);
            printf("  Staff Count: %d\n", departments[dept_id].staff_count);
            printf("  Stability: %s\n", departments[dept_id].stability);
            printf("  Security Clearance Level: %d\n", departments[dept_id].security_clearance);
            printf("  Budget Allocation: $%.1f million\n", departments[dept_id].budget_allocation);
            printf("  Encryption: %s\n", connections[i].encryption_level);
        }
        // Print operation code name for human channels
        else if (connections[i].channel_type == HUMAN_CHANNEL) {
            printf("  Notebook Access: %s\n", connections[i].operation_codename);
        }

        random_multiple_calls();
        printf("  Metrics: Cheaters %.1f%%, MSE %.2f\n",
               connections[i].cheaters_perc, connections[i].mse);
        printf("  Source weights: U=%.2f, FC=%.2f, FT=%.2f, F4=%.2f\n",
               nodes[src].use_weight, nodes[src].foreign_c_weight,
               nodes[src].foreign_t_weight, nodes[src].foreign_4_weight);
        printf("  Target weights: U=%.2f, FC=%.2f, FT=%.2f, F4=%.2f\n\n",
               nodes[tgt].use_weight, nodes[tgt].foreign_c_weight,
               nodes[tgt].foreign_t_weight, nodes[tgt].foreign_4_weight);
    }
}
