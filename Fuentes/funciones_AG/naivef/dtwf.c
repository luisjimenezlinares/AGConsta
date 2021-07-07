#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INF 9999999;


struct Result{
  double D;
  int* w1;
  int* w2;
  int size;
};


struct Vector{
  double *s;
  int size;
};


double min(double a, double b, double c){
  double minimo;
  if(a<=b && a<=c){
    minimo = a;
  }
  else if(b<=a && b<=c){
    minimo = b;
  }
  else{
    minimo = c;
  }

  return minimo;
}


int min2(int a, int b){
  if(a <= b)
    return a;
  return b;
}

int max2(int a, int b){
  if(a>=b)
    return a;
  return b;
}


double min_arg(double a, double b, double c){
  double minimo;
  if(a<=b && a<=c){
    minimo = 0;
  }
  else if(b<=a && b<=c){
    minimo = 1;
  }
  else{
    minimo = 2;
  }

  return minimo;
}


double absolut(double x){
  if(x<0){
   x *= (-1);
  }
  return x;
}


int* reverse(int *w, int size){
  int *w_r = malloc(sizeof(int)*size);
  for(int i=0;i<size;i++){
    w_r[i] = w[size-i-1];
  }
  free(w);
  return w_r;
}


double dist(double x1, double x2){
  return absolut(x2 - x1);
}


struct Result dtw_(double *s1, double *s2, int size1, int size2, int (*window)[2], int wind){ 
  int i, j, *w1, *w2, min_pos, iw=1, iw1=size1-1, iw2=size2-1;
  struct Result result; 
  
  double **dtwmatrix = (double**)malloc(sizeof(double*)*size1);
  for(int i=0;i<size1;i++){
  	dtwmatrix[i] = (double*)malloc(sizeof(double)*size2);
  	memset(dtwmatrix[i], 9999999, sizeof(double)*size2);
  }
  
  
  //memset(dtwmatrix, 9999999, sizeof(double)*size1*size2);
  
  w1 = malloc(sizeof(double)*(size1+size2));
  w2 = malloc(sizeof(double)*(size1+size2));
  
  dtwmatrix[0][0] = dist(s1[0], s2[0]);
  
  if(wind == 0){
    for(i=1;i<size1;i++){
      dtwmatrix[i][0] = dist(s1[i], s2[0]) + dtwmatrix[i-1][0];
    }
    for(i=1;i<size2;i++){
      dtwmatrix[0][i] = dist(s1[0], s2[i]) + dtwmatrix[0][i-1];
    }
    for(i=1;i<size1;i++){
      for(j=1;j<size2;j++){
				dtwmatrix[i][j] = dist(s1[i], s2[j]) + min(dtwmatrix[i-1][j],
				dtwmatrix[i][j-1],
				dtwmatrix[i-1][j-1]);
      }
    }
  }
  else{
    for(i=1;window[i][0]==0;i++){
      dtwmatrix[i][0] = dist(s1[i], s2[0]) + dtwmatrix[i-1][0];
    }

    for(i=1;i<=window[0][1];i++){
      dtwmatrix[0][i] = dist(s1[0], s2[i]) + dtwmatrix[0][i-1];
    }
    
    for(i=1;i<size1;i++){
      for(j=max2(1,window[i][0]);j<=window[i][1];j++){
				dtwmatrix[i][j] = dist(s1[i], s2[j]) + min(dtwmatrix[i-1][j],
				dtwmatrix[i][j-1],
				dtwmatrix[i-1][j-1]);
      }
    }
  }
  w1[0] = size1-1;
  w2[0] = size2-1;
    
  while(iw1>0 && iw2>0){
  	min_pos = min_arg(dtwmatrix[iw1-1][iw2],
			  dtwmatrix[iw1][iw2-1],
			  dtwmatrix[iw1-1][iw2-1]);
	if(min_pos == 0){
	  w1[iw] = iw1-1;
	  w2[iw] = iw2;
	  iw1--;
        }
	else if(min_pos == 1){
	  w1[iw] = iw1;
	  w2[iw] = iw2-1;
	  iw2--;
	}
	else{
	  w1[iw] = iw1-1;
	  w2[iw] = iw2-1;
	  iw1--;
	  iw2--;
	}
	iw++;
  }
  if(iw1==0 && iw2>0){
    iw2--;
    for(;iw2>=0;iw2--){
      w1[iw] = 0;
      w2[iw] = iw2;
      iw++;
    }
  }
  else if(iw1>0 && iw2==0){
    iw1--;
    for(;iw1>=0;iw1--){
      w1[iw] = iw1;
      w2[iw] = 0;
      iw++;
    }
  }
  w1 = reverse(w1, iw);
  w2 = reverse(w2, iw);

  result.D = dtwmatrix[size1-1][size2-1];
  result.w1 = w1;
  result.w2 = w2;
  result.size = iw;
  
  
  for(int i=0;i<size1;i++)
  	free(dtwmatrix[i]);
  free(dtwmatrix);
  
  
  return result;
}


struct Vector reduce_by_half(double *s, int size){
  int limit = size - size%2;
  double* s_reduced = malloc(sizeof(double)*limit/2);
  struct Vector vector;
			     
  for(int i=0,j=0;i<limit;i+=2,j++){
    s_reduced[j] = (s[i]+s[i+1])/2;
  }

  vector.s = s_reduced;
  vector.size = limit/2;
  return vector;
}


void expand_window(int *w1, int *w2, int size1, int size2, int sw1, int radius, int (*w)[2]){
  int pos1, pos2, i, r1, r2; 
  
  for(i=0;i<sw1;i++){
    for(r1=-radius;r1<=radius;r1++){
      for(r2=-radius;r2<=radius;r2++){
				pos1 = (w1[i] + r1)*2;
				pos2 = (w2[i] + r2)*2;
				
				if(pos1>=0 && pos1<size1 && pos2>=0 && pos2<size2){
					w[pos1][0] = min2(pos2, w[pos1][0]);
					w[pos1][1] = max2(pos2, w[pos1][1]);
				}
				if(pos1+1>=0 && pos1+1<size1 && pos2>=0 && pos2<size2){
					w[pos1+1][0] = min2(pos2, w[pos1+1][0]);
					w[pos1+1][1] = max2(pos2, w[pos1+1][1]);
				}
				if(pos1>=0 && pos1<size1 && pos2+1>=0 && pos2+1<size2){
					w[pos1][0] = min2(pos2+1, w[pos1][0]);
					w[pos1][1] = max2(pos2+1, w[pos1][1]);
				}
				if(pos1+1>=0 && pos1+1<size1 && pos2+1>=0 && pos2+1<size2){
					w[pos1+1][0] = min2(pos2+1, w[pos1+1][0]);
					w[pos1+1][1] = max2(pos2+1, w[pos1+1][1]);
				}
      }
    }
  }
}

struct Result fastdtw_(double *s1, double *s2, int size1, int size2, int radius){
  int min_time_size = radius + 2;
  struct Vector s1_shrinked, s2_shrinked;
  struct Result result;
  int w[1][2];
  
  if(size1 < min_time_size || size2 < min_time_size){
    return dtw_(s1, s2, size1, size2, w, 0);
  }
  
  s1_shrinked = reduce_by_half(s1, size1);
  s2_shrinked = reduce_by_half(s2, size2);

  result = fastdtw_(s1_shrinked.s, s2_shrinked.s, s1_shrinked.size, s2_shrinked.size, radius);

  int window[size1][2];
  
  for(int i=0;i<size1;i++){
    for(int j=0;j<2;j++){
      if(j==0){
		window[i][j] = INF;
      }
      else{
		window[i][j] = -INF;
      }
    }
  }
  
  expand_window(result.w1, result.w2, size1, size2, result.size, radius, window);
  
  free(s1_shrinked.s);
  free(s2_shrinked.s);
  free(result.w1);
  free(result.w2);

  return dtw_(s1, s2, size1, size2, window, 1); 
}


struct Result fastdtw(double *s1, double *s2, int size1, int size2, int radius){
  struct Result result;
  result = fastdtw_(s1, s2, size1, size2, radius);
  return result;
}


struct Result dtw(double *s1, double *s2, int size1, int size2){
  struct Result result;
  int w[1][2];
  result = dtw_(s1, s2, size1, size2, w, 0); 
  
  return result;
}


void freeptr(int *ptr){
	free(ptr);
}


void main(){
  double s1[18] = {1,1,1,2,3,4,5,8,9,10,11,12,12,12,12,13,14,15};
  double s2[18] = {1,2,3,4,5,5,5,5,6, 7, 8, 9,10,12,13,14,11,22};
  struct Result result = dtw(s1, s2, 18, 18);
  printf("%f\n", result.D);

  for(int i=0;i<result.size;i++){
    printf("%d ", result.w1[i]);
  }
  printf("\n");
  for(int i=0;i<result.size;i++)
    printf("%d ", result.w2[i]);
    printf("\n");
}
