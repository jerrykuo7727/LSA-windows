#include "LSI_main.h"
char Directory[500];
using namespace std;

QRY_STRUCT QUERY[MAX_QRY_NO];
DOC_STRUCT VOICEFILE[MAX_DOC_NO];
short vf_order[MAX_DOC_NO],vf_TOP[MAX_DOC_NO];
float SVD_Sigma[LSI_DIM];
float SVD_U[MAX_WORD_LEXICON][LSI_DIM];
float SVD_V[MAX_DOC_NO][LSI_DIM];
float WD_IDF[MAX_WORD_LEXICON];
int USED_LSI_WORD_NO;
int USED_LSI_DIM;
int USED_LSI_DOC_NO;
int USED_QRY_NO;
void main()
{
    char File_Dir[300];

	getcwd(Directory,300);//找到目前程式執行路徑
    Load_SVD_Parameters("TDT2-DOC-TXT-SVD");
	Load_IDF("TDT2-TXT-WD-IDF");
	sprintf(File_Dir,"%s\\XinTestQryTDT2\\QUERY_WDID_NEW",DOC_Directory);
	Load_Query("listtdt2qry16","listS0Doc",File_Dir);
    Match_Query(); 

}//void main

void Match_Query()
{
  FILE *RESULTS;
  int qry_pos,vf_pos,i,j,k,temp;
  float sum;
  char fname[300];
  sprintf(fname,"%s\\assessment\\results_TDT2.txt",Directory); 

  if ((RESULTS = fopen(fname,"wt"))==NULL) 
       {
             printf("Open %s error!\n",fname);
             getch();
             exit(1);
     }
  fprintf(RESULTS,"total_doc_num=500 doc_type=2 qry_type=2\n");
  fprintf(RESULTS,"TotalDocSyl=106860 TotalDocSylCan=201356 Avg=1.88\n\n");

  for(qry_pos=0;qry_pos<USED_QRY_NO/*1*/;qry_pos++)
  {
    for(vf_pos=0;vf_pos<USED_LSI_DOC_NO;vf_pos++)
	{
		sum=(float) 0.0;
        for(k=1;k<LSI_DIM;k++)
            sum+=QUERY[qry_pos].LSI_Vector[k]*SVD_V[vf_pos][k];//fabs(SVD_V[vf_pos][k]);
        if((QUERY[qry_pos].norm>(float)0.0)&&(VOICEFILE[vf_pos].norm)>(float) 0.0)
           VOICEFILE[vf_pos].match_score=sum/(QUERY[qry_pos].norm*VOICEFILE[vf_pos].norm);
		else 
			VOICEFILE[vf_pos].match_score=(float) 0.0;
	}//for vf_pos
    //----------------Bubble Sort-------------------------//
	 for(i=0;i<USED_LSI_DOC_NO;i++)   vf_order[i]=i; 
			 		
     for(k=0;k<USED_LSI_DOC_NO;k++)
	 {
       for(i=0;i<USED_LSI_DOC_NO-1-k;i++)
	   {
         if(VOICEFILE[vf_order[i]].match_score>VOICEFILE[vf_order[i+1]].match_score)
		 {
             temp=vf_order[i];
             vf_order[i]=vf_order[i+1];
             vf_order[i+1]=temp;
         }
	   }
       vf_TOP[k]=vf_order[USED_LSI_DOC_NO-1-k];
     }//for k
	//----------------Bubble Sort-------------------------//
    printf("Query %d %10s\n",qry_pos+1,QUERY[qry_pos].name);
	for(k=0;k<20;k++)
		printf("%10s %10e %10s\n",VOICEFILE[vf_TOP[k]].name,
		VOICEFILE[vf_TOP[k]].match_score,VOICEFILE[vf_TOP[k]].name); 

	fprintf(RESULTS,"Query %d %10s XXXXXX %10s\n",qry_pos+1,QUERY[qry_pos].name,QUERY[qry_pos].title);
    fprintf(RESULTS,"SyllableNo=5 SyllableCanNo=10 Avg=2.00\n");
	for(k=0;k<USED_LSI_DOC_NO;k++)
		fprintf(RESULTS,"%-10s %e %10s\n",VOICEFILE[vf_TOP[k]].name,
		VOICEFILE[vf_TOP[k]].match_score,VOICEFILE[vf_TOP[k]].name);
    fprintf(RESULTS,"\n");
  }//for qry_pos
  fclose(RESULTS);
}
void Load_IDF(char *filename)
{
   FILE *INF;
   int count;
   float tmp_value;
   if ((INF = fopen(filename,"rt"))==NULL)
  {
             printf("Open %s error!\n",filename);
             getchar();
             exit(1);
  }
  count=0;
  while(!feof(INF))
  {
    fscanf(INF,"%d %f\n",&count,&tmp_value);
	WD_IDF[count]=tmp_value;
  }//while
  fclose(INF);
  printf("IDF Loading OK....\n");
}
void Load_Query(char *qrylistname,char *doclistname,char *Direct)
{
  FILE *LIST,*INF;
  int i,j,k,qry_pos,vf_pos,Temp_ID,temp_doc_no;
  char fname[300],buf1[400];
  float norm,Max_Val;
  USED_QRY_NO=0;
  
  if ((LIST = fopen(qrylistname,"rt"))==NULL)
  {
             printf("Open %s error!\n",qrylistname);
             getchar();
             exit(1);
  }
  while(!feof(LIST))
  {
    fscanf(LIST,"%s\n",fname);
    sprintf(buf1,"%s\\%s.query",Direct,fname);
 
	sprintf(QUERY[USED_QRY_NO].name,"%s.query",fname);
	strcpy(QUERY[USED_QRY_NO].title,"\0");
	QUERY[USED_QRY_NO].length=0;
	for(i=0;i<MAX_WORD_LEXICON;i++)
		QUERY[USED_QRY_NO].Vector[i]=(float) 0.0;

    if ((INF = fopen(buf1,"rt"))==NULL)
	{
             printf("Open %s error!\n",buf1);
             getchar();
             exit(1);
	}
    while(!feof(INF))
	{
      fscanf(INF,"%d ",&Temp_ID);
	  if(Temp_ID!=-1)
	  {
        QUERY[USED_QRY_NO].length++;
        QUERY[USED_QRY_NO].Vector[Temp_ID]+= (float)1.0;
	  }
	}//while QUERY
	
    fclose(INF);
	USED_QRY_NO++;
  }//while LIST
  fclose(LIST);
  printf("TOTAL QUERY NO=%d\n",USED_QRY_NO);
  if ((LIST = fopen(doclistname,"rt"))==NULL)
  {
             printf("Open %s error!\n",doclistname);
             getchar();
             exit(1);
  }
  temp_doc_no=0;
  while(!feof(LIST))
  {
	fscanf(LIST,"%s\n",fname);
	sprintf(VOICEFILE[temp_doc_no].name,"%s",fname);  
	temp_doc_no++;
  }
  fclose(LIST);

  //----------------Make Query LSI Vector-----------------//
  for(qry_pos=0;qry_pos<USED_QRY_NO;qry_pos++)
  {
    for(k=0;k<LSI_DIM;k++) QUERY[qry_pos].LSI_Vector[k]=(float) 0.0;


   /*
    Max_Val=(float) 0.0;
    for(j=0;j<MAX_WORD_LEXICON;j++)
		if(QUERY[qry_pos].Vector[j] > Max_Val)
              Max_Val=QUERY[qry_pos].Vector[j];
    */
    for(j=0;j<MAX_WORD_LEXICON;j++)
	{
       if(QUERY[qry_pos].Vector[j] > (float) 0.0)
	   {
          for(k=0;k<LSI_DIM;k++)
           QUERY[qry_pos].LSI_Vector[k]
		       +=(1+log(QUERY[qry_pos].Vector[j]))*WD_IDF[j]*SVD_U[j][k]; //Berlin's TFIDF
		      // +=((float)0.5+(float)0.5*QUERY[qry_pos].Vector[j]/Max_Val)*WD_IDF[j]*SVD_U[j][k]; //Salton's TFIDF
		  
		       //+=QUERY[qry_pos].Vector[j]*fabs(SVD_U[j][k]);
		       //+=(1+log(QUERY[qry_pos].Vector[j]))*WD_IDF[j]*SVD_U[j][k];//fabs(SVD_U[j][k]);
	   }//if 
	}//for MAX_WORD_NO
    /*
    for(k=0;k<LSI_DIM;k++)
	{
        for(j=0;j<MAX_WORD_LEXICON;j++)
         if(QUERY[qry_pos].Vector[j] > (float) 0.0)
           QUERY[qry_pos].LSI_Vector[k]
		       +=log(QUERY[qry_pos].Vector[j])*WD_IDF[j]*fabs(SVD_U[j][k]);
	}//for k
   */
	norm=(float) 0.0;
    for(k=0;k<LSI_DIM;k++)
        norm+=QUERY[qry_pos].LSI_Vector[k]*QUERY[qry_pos].LSI_Vector[k];

	if(norm<=(float) 0.0)
	  QUERY[qry_pos].norm=(float) 0.0;
    else
      QUERY[qry_pos].norm=(float)sqrt((double)norm);

  }//for qry_pos
  //for(k=0;k<LSI_DIM;k++)
	  //printf("QUERY[0][%3d]=%5.10f\n",k,QUERY[0].LSI_Vector[k]);
  //getchar();
  //----------------Calculate VoiceFile Norm-----------------//
  
  //printf("Total VF=%10d\n",USED_LSI_DOC_NO);
  //getchar();

  for(vf_pos=0;vf_pos<USED_LSI_DOC_NO;vf_pos++)
  {
	for(k=0;k<LSI_DIM;k++)
	    //SVD_V[vf_pos][k]=sqrt(SVD_Sigma[k])*SVD_V[vf_pos][k];
	    SVD_V[vf_pos][k]=pow(SVD_Sigma[k],2.0/3.0)*SVD_V[vf_pos][k];
	norm=(float) 0.0;
    for(k=0;k<LSI_DIM;k++)
        norm+=SVD_V[vf_pos][k]*SVD_V[vf_pos][k];
    
	//printf("[VF %3d]  %5.10f\n",vf_pos,sqrt((double)norm));

    if(norm<=(float) 0.0)
	  VOICEFILE[vf_pos].norm=(float) 0.0;
    else
      VOICEFILE[vf_pos].norm=(float)sqrt((double)norm);
  }//for vf_pos

}

void Load_SVD_Parameters(char *filename)
{
  FILE *INF;
  char fname[300];
  int i,j,k;
  //-----Load SVD Sigma Matrix -------------------------------//
  sprintf(fname,"%s\\DIM%d\\TFIDF\\%s-S",PATH_LSI_PARAMETERS,LSI_DIM,filename);
  if ((INF = fopen(fname,"rt"))==NULL)
  {
             printf("Open %s error!\n",fname);
             getchar();
             exit(1);
  }
  fscanf(INF,"%d ",&USED_LSI_DIM);
  for(i=0;i<USED_LSI_DIM;i++)
       fscanf(INF,"%f ",&SVD_Sigma[i]);
  fclose(INF);

  //for(i=0;i<USED_LSI_DIM;i++)
    //  printf("SVD_Sigma[%3d]=%5.10f\n",i,SVD_Sigma[i]);
  //getchar();
  //-----Load SVD UT Matrix -------------------------------//
  sprintf(fname,"%s\\DIM%d\\TFIDF\\%s-Ut",PATH_LSI_PARAMETERS,LSI_DIM,filename);
  if ((INF = fopen(fname,"rt"))==NULL)
  {
             printf("Open %s error!\n",fname);
             getchar();
             exit(1);
  }
  fscanf(INF,"%d %d",&USED_LSI_DIM,&USED_LSI_WORD_NO);
  printf("USED_LSI_DIM=%3d  USED_LSI_WORD_NO=%d...\n",USED_LSI_DIM,USED_LSI_WORD_NO);

  for(i=0;i<USED_LSI_DIM;i++)
    for(j=0;j<USED_LSI_WORD_NO;j++)    
          fscanf(INF,"%f ",&SVD_U[j][i]);
  fclose(INF);
  //-----Load SVD VT Matrix -------------------------------//
  sprintf(fname,"%s\\DIM%d\\TFIDF\\%s-Vt",PATH_LSI_PARAMETERS,LSI_DIM,filename);
  if ((INF = fopen(fname,"rt"))==NULL)
  {
             printf("Open %s error!\n",fname);
             getchar();
             exit(1);
  }
  fscanf(INF,"%d %d",&USED_LSI_DIM,&USED_LSI_DOC_NO);
  printf("USED_LSI_DIM=%3d  USED_LSI_DOC_NO=%d...\n",USED_LSI_DIM,USED_LSI_DOC_NO);
  for(i=0;i<USED_LSI_DIM;i++)
     for(j=0;j<USED_LSI_DOC_NO;j++)  
          fscanf(INF,"%f ",&SVD_V[j][i]);
  fclose(INF);
  //------------------------------------------------------------
  printf("LSI Parameter Loading OK!.... \n");
}//void main