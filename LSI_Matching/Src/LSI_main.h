#include <conio.h>
#include <stdio.h>
#include <stdlib.h>
#include <io.h>
#include <string.h>
#include <dos.h>
#include <malloc.h>
#include <math.h>
#include <time.h>
#include <direct.h>
#include <cstring>
#include <iostream>

#define LSI_DIM 500
#define MAX_WORD_LEXICON 51253
#define MAX_DOC_NO  3500
#define MAX_QRY_NO  100
#define MAX_DOC_LENGTH  1000
#define DOC_Directory "D:\\IR\\TDT2" //Doc Directory
#define PATH_LSI_PARAMETERS "D:\\IR\\LSI_Parameters\\TDT2-TXT\\"

struct QRY_STRUCT
{
  short  length;
  char   name[300]; 
  char   title[300];
  float  norm;
  float  match_score; 
  float  Vector[MAX_WORD_LEXICON];
  float  LSI_Vector[LSI_DIM];
};

struct DOC_STRUCT
{
  short  length;
  char   name[300]; 
  float  norm;
  float  match_score; 
};


void Load_SVD_Parameters(char *filename);
void Load_Query(char *qrylistname,char *doclistname,char *Direct);
void Match_Query();
void Load_IDF(char *filename);