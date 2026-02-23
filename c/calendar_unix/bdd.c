#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "bdd.h"
#include "utils.h"

// Retourne une string à partir d'un Day
char *day_to_string(enum Day d)
{
  switch (d)
  {
  case MON:
    return "Lundi";
  case TUE:
    return "Mardi";
  case WED:
    return "Mercredi";
  case THU:
    return "Jeudi";
  case FRI:
    return "Vendredi";
  case SAT:
    return "Samedi";
  case SUN:
    return "Dimanche";
  case NONE:
    return "Not a day";
  }
}

// Retourne un Day à partir d'un string
// dans le cas où la string ne correspond pas à un jour, on renvoie NONE
enum Day string_to_day(char *dd)
{
  char d[LINE_SIZE];
  strcpy(d, dd);
  // Conversion en minuscule
  for (int i = 0; i < strlen(d); i++)
    d[i] = tolower(d[i]);

  if (strcmp("lundi", d) == 0)
    return MON;
  else if (strcmp("mardi", d) == 0)
    return TUE;
  else if (strcmp("mercredi", d) == 0)
    return WED;
  else if (strcmp("jeudi", d) == 0)
    return THU;
  else if (strcmp("vendredi", d) == 0)
    return FRI;
  else if (strcmp("samedi", d) == 0)
    return SAT;
  else if (strcmp("dimanche", d) == 0)
    return SUN;
  else
    return NONE;
}

// Libère la mémoire d'un pointeur vers Data
void data_free(Data *d)
{
  free(d->name);
  free(d->activity);
  free(d);
}

// Modifie une chaîne de caratère correspondant à data
void data_format(char *l, Data *data)
{
  sprintf(l, "%s,%s,%s,%d\n",
          data->name, data->activity,
          day_to_string(data->day), data->hour);
}

// Retourne une structure Data à partir d'une ligne de donnée
//  get_data("toto,arc,lundi,4") ->  Data { "toto", "arc", MON, 4 };
//  Attention il faudra libérer la mémoire vous-même après avoir utilisé
//  le pointeur généré par cette fonction
Data *get_data(char *line)
{
  char *parse;
  Data *data = malloc(sizeof(Data));
  char error_msg[LINE_SIZE];
  sprintf(error_msg, "Erreur de parsing pour: %s\n", line);

  // On s'assure que la ligne qu'on parse soit dans le mémoire autorisée en
  //  écriture
  char *l = malloc(strlen(line) + 1);
  l = strncpy(l, line, strlen(line) + 1);

  parse = strtok(l, ",");
  if (parse == NULL)
    exit_msg(error_msg, 0);
  data->name = malloc(strlen(parse) + 1);
  strcpy(data->name, parse);

  parse = strtok(NULL, ",");
  if (parse == NULL)
    exit_msg(error_msg, 0);
  data->activity = malloc(strlen(parse) + 1);
  strcpy(data->activity, parse);

  parse = strtok(NULL, ",");
  if (parse == NULL)
    exit_msg(error_msg, 0);
  data->day = string_to_day(parse);

  parse = strtok(NULL, "\n");
  if (parse == NULL)
    exit_msg(error_msg, 0);
  data->hour = atoi(parse);
  free(l);

  return data;
}

// La fonction _add_data_  retourne 0 si l'opération s'est bien déroulé
// sinon -1
void add_data(Data *data)
{

  FILE *fp;
  char *l = malloc(sizeof(char) * LINE_SIZE);

  /* opening file for reading */
  fp = fopen(DATA, "a");
  if (fp == NULL)
  {
    perror("Error opening file");
    exit(-1);
  }

  // get the line corresponding to data
  data_format(l, data);
  fprintf(fp, "%s", l);

  fclose(fp);
  data_free(data);
  exit(0);
}

// Enlève la donnée _data_ de la base de donnée
void delete_data(Data *data)
{

  FILE *fp;     // Déclaration d'un flux
  FILE *new_fp; // Déclaration d'un flux pour le nouveau fichier

  char line[LINE_SIZE]; // Déclaration d'une ligne de taille LINE_SIZE
  char *items[4];

  // Ouverture du fichier foo en mode lecture et cration d'un nouveau fichier
  fp = fopen(DATA, "r");
  new_fp = fopen("new_data.txt", "w");

  // On vérifie si l'ouverture s'est bien passé
  if (fp == NULL || new_fp == NULL)
  {
    exit(-1); // Gestion de l'erreur
  }

  char *l = malloc(sizeof(char) * LINE_SIZE);
  data_format(l, data);
  // Tant qu'il reste des lignes à lire on les affiche
  while (fgets(line, sizeof(line), fp))
  {
    if (strcmp(l, line) == 0)
    {
      continue;
    }
    // write line to new file
    fprintf(new_fp, "%s", line);
  }

  free(l);
  // close files
  fclose(fp);
  fclose(new_fp);

  // delete original file
  if (remove(DATA) != 0)
  {
    perror("Error deleting file");
    exit(1);
  }

  // rename new file to original filename
  if (rename("new_data.txt", DATA) != 0)
  {
    perror("Error renaming file");
    exit(1);
  }

  printf("Data deleted successfully from file '%s'\n", DATA);
  data_free(data);
}

// Affiche le planning
void *see_all()
{
  FILE *fp;
  char line[LINE_SIZE]; // Déclaration d'une ligne de taille LINE_SIZE
  Data *data;

  fp = fopen(DATA, "r");

  // On vérifie si l'ouverture s'est bien passé
  if (fp == NULL)
  {
    exit(-1); // Gestion de l'erreur
  }

  while (fgets(line, sizeof(line), fp))
  {
    data = get_data(line);
    printf("%s %d : %s a %s\n", day_to_string(data->day), data->hour, data->name, data->activity);
    data_free(data);
  }

  
  fclose(fp);
  exit(0);
}

void create_data(Data *data, char *name, char *activity, char *day, int hour)
{
  data->name = malloc(LINE_SIZE * sizeof(char));
  data->activity = malloc(LINE_SIZE * sizeof(char));

  strcpy(data->name, name);
  strcpy(data->activity, activity);
  data->day = string_to_day(day);
  data->hour = hour;
}
int main(int argc, char **argv)
{

  char *command = argv[1];

  if (strcmp(command, "SEE") == 0)
  {
    see_all();
  }

  else if (argc > 2)
  {
    Data *data = malloc(sizeof(Data));
    data->name = malloc(LINE_SIZE * sizeof(char));
    data->activity = malloc(LINE_SIZE * sizeof(char));
    strcpy(data->name, argv[2]);
    strcpy(data->activity, argv[3]);
    data->day = string_to_day(argv[4]);
    data->hour = atoi(argv[5]);

    if (strcmp(command, "ADD") == 0)
    {
      add_data(data);
    }

    else if (strcmp(command, "DEL") == 0)
    {
      delete_data(data);
    }
  }

  return 0;
}
