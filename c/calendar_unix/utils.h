#include <stdlib.h>
#include <stdio.h>


static const char *DATA = "data.txt"; // Nom du fichier contenant les données
const char* SERVER_IP = "127.0.0.1";  // Adresse localhost (interface interne)*
#define SERVER_PORT 4000
#define LINE_SIZE 100
#define REPLY_SIZE 2000
#define DEBUG 0

//Renvoie un message d'erreur en cas de problème
void exit_msg(char* msg, int err) {
  fprintf(stderr, "Error - %s: ", msg);
  if (err) perror(NULL);
  exit(1);
}

