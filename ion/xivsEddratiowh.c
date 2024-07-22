/****************************************************************
Program to compute the run of ionization parameter versus Eddington ratio
at a specific radius along the disk (measured in rg) due to illumination
from a lamppost X-ray source with height h (also in rg).
 
We use eqs. 4-8 in Vincent et al. (2016) to set up the calculation of
the flux. The fitting formulas from Fukumura & Kazanas (2007) are used
to compute the radiation pattern on the disk.  

Initially, h will be constant, but eventually h will be made a function
of Eddington ratio.

We'll output 2 models in the output file. One for f=0.45, and one for
f \propto L/Ledd^{-0.77}.

Command line parameters:
        - radius of reflection (in rg; must be > rms)
  	- height of lamppost (in rg; must be > 3)
        - spin (needed for g_lp)

****************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "complex.h"
#include "nrutil.h"

#define EPS 2.0e-6
#define MAXM 100
#define NRANSI
#define EPSS 1.0e-7
#define MR 8
#define MT 10
#define MAXIT (MT*MR)

#define PI 3.141592654
#define RMAX 200.0
#define NSTEP 500
#define ALPHA 0.1
#define ETA 0.1

double FKFitFormula(double radius, double height);
double glp(double radius, double spin, double height);
double dS(double radius, double spin);
double RMS(double spin);
double F(double loglambda);
void zroots(fcomplex a[], int m, fcomplex roots[], int polish);

int main(int argc, char *argv[]) {
  FILE *outputfp;
  char radnam[80], hnam[80], spinnam[80], outfnam[80]="xiLedd_r";
  double height, spin, radius, rad;
  double logrmin, logrmax, lograd, dlogr;
  double integral, rfac, rmin;
  double y,x,Rr, Rt, Rz;
  double A,B,C,E,L,temp1,temp2,temp3,temp4;
  double lambda, loglambda, loglambdamin, loglambdamax, dlambda;
  double xi,y1,y2,y3,yms;
  fcomplex b1[4],roots2[3];
  

  int k;
  
  if(argc < 4) {
    fprintf(stderr, "Usage: radius [rg], lamppost height [rg], spin\n");
    exit (1);
  }
  
  rad = atof(argv[1]);
  height = atof(argv[2]);
  spin = atof(argv[3]);

  sscanf(argv[1],"%s",radnam);
  sscanf(argv[2],"%s",hnam);
  sscanf(argv[3],"%s",spinnam);

  strcat(outfnam,radnam);
  strcat(outfnam,"_h");
  strcat(outfnam,hnam);
  strcat(outfnam,"_a");
  strcat(outfnam,spinnam);
  strcat(outfnam,".dat");

  /* set rmin to the radius of marginal stability */
  rmin=RMS(spin);

  /* if input radius < rmin then print error and exit */
  if (rad < rmin) {
    printf("Input radius (%lg) < radius of marginal stability (%lg). Quitting...\n",rad,rmin);
    exit(1);
  }

  /* Compute the integral needed for calculating the ionization parameter */
  logrmin=log10(rmin);
  logrmax=log10(RMAX);
  dlogr=(logrmax-logrmin)/NSTEP;
  integral=0.0;

  for (k=0; k <= NSTEP; k++) {
    lograd=logrmin+k*dlogr;
    if ( (k % 2) == 0) 
      rfac=2.0;
    else 
      rfac=4.0;
    if( (k == 0) || (k == NSTEP))
      rfac=1.0;

    radius=pow(10.0,lograd);
    integral+=FKFitFormula(radius,height)*glp(radius,spin,height)*glp(radius,spin,height)*dS(radius,spin)*rfac*radius*log(10.0)*dlogr/3.0;
  }
    
  
  if (x < 4.0) {
    x=4.0;
  }

  printf("%lg\t %lg\n", rmin, rad);

  y=sqrt(x);
  yms=sqrt(rmin);
  b1[0]=Complex((2.0*spin),0.0);
  b1[1]=Complex(-3.0,0.0);
  b1[2]=Complex(0.0,0.0);
  b1[3]=Complex(1.0,0.0);
  zroots(b1,3,roots2,1);
  y1=roots2[3].r;
  y2=roots2[2].r;
  y3=roots2[1].r;
  A=1.0 - (2.0/x) + ((spin*spin)/(x*x));
  B=1.0 - (3.0/x) + ((2.0*(spin*spin))/(pow(x,1.5)));
  E=(1.0-(2.0/x)+(spin*(pow(x,-1.5))))/sqrt(B);
  temp1=(1.0-2.0*spin*(pow(x,-1.5))+(spin/x)*(spin/x));
  L=sqrt(x)*temp1/sqrt(B);
  Rz=(L*L - ((E-1.0)*spin*spin))/x;
  if (y3 == 0.0) { 
    temp3=0.0;
  } else {
    temp4=(3.0*(y3-spin)*(y3-spin))/(y*y3*(y3-y1)*(y3-y2));
    temp3=temp4*log((y-y3)/(yms-y3));
  }
  if (y2 == 0.0) {
    temp2=0.0;
  } else {
    temp4=(3.0*(y2-spin)*(y2-spin))/(y*y2*(y2-y1)*(y2-y3));
    temp2=temp4*log((y-y2)/(yms-y2));
  }
  if (y1 == 0.0) {
    temp1=0.0;
  } else {
    temp4=(3.0*(y1-spin)*(y1-spin))/(y*y1*(y1-y2)*(y1-y3));
    temp1=temp4*log((y-y1)/(yms-y1));
  }
  C=1.0-(yms/y)-((3*spin*log(y/yms))/(2*y))-temp1-temp2-temp3;
  Rr=C/B;
  Rt=C/A;

  /* printf("%lg\t %lg\t %lg\t %lg\t %lg\t %lg\n",y1,y2,y3,Rr,Rt,Rz); */

  /* open output file */
  if( (outputfp = fopen(outfnam,"w")) == NULL) {
    fprintf(stderr, "Error opening file %s\n",outfnam);
    exit(1);
  } 

  /* Rr=1.0;Rz=1.0;Rt=1.0; */
  /* start loop of Eddington Ratios */
  loglambdamin=-2.0;
  loglambdamax=0.5;
  dlambda=(loglambdamax-loglambdamin)/NSTEP;

  for (k=0; k <= NSTEP; k++) {
    loglambda=loglambdamin+k*dlambda;
    lambda=pow(10.0,loglambda);

    xi=(5.44e10)*pow((ETA/0.1),-2)*(ALPHA/0.1)*pow(lambda,3.0)*pow(rad,-1.5)*pow(Rz,-2)*pow(Rr,3)*F(loglambda)*pow((1-F(loglambda)),3)*FKFitFormula(rad,height)*glp(rad,spin,height)*glp(rad,spin,height)/(Rt*integral);

    fprintf(outputfp,"%lg\t %lg\n",loglambda,xi);
  }
  fclose(outputfp);

  return 0;
}

double F(double loglambda) {
  double temp;

  /* temp=(-0.44)*loglambda-1.227; */
  /* temp=(-0.77)*loglambda-1.887; */
  
  /* return pow(10.0,temp); */
  return 0.45;
}

double glp (double radius, double spin, double height) {
  double numer, denom;

  numer=(radius*sqrt(radius)+spin)*sqrt(height*height-2*height+spin*spin);
  denom=sqrt(radius)*sqrt(radius*radius-3*radius+2*spin*sqrt(radius))*sqrt(height*height+spin*spin);
  return (numer/denom);
}

double FKFitFormula (double radius, double height) {
  double temp1, temp2, F;

  if ((height > 6) && (height <= 100)) {
    temp1=(-1.026e-5)*(height-152.9)*(height*height-158.7*height+6569)/(radius*radius*radius);
    temp2=(-3.364e-2)*(height-348.7)*(height+11.98)*(height+139.4)/pow((height*height+pow((1+1/height),6)*radius*radius),1.5);
    F=temp1+temp2;
  } else if ((height <= 6) && (height >=3)) {
    temp1=79.56*(height-6.250)*(height*height-9.763*height+25.19)/(radius*radius*radius);
    temp2=(-3921)*(height-7.364)*(height*height-8.556*height+21.92)/pow((height*height+pow((1+1/height),6)*radius*radius),1.5);
    F=temp1+temp2;
  } else {
    printf("Invalid value of height, %lg\n",height);
    exit(1);
  }
  return F;
}

double dS (double radius, double spin) {
  double temp1, temp2;

  temp1=radius*radius+spin*spin+(2.0*spin*spin/radius);
  temp2=radius*radius-2.0*radius+spin*spin;

  return 2.0*PI*radius*sqrt(temp1/temp2);
}

double RMS (double spin) {
  /*     Calculate radius of marginal stability for a BH with spin a
	 Equations from Krolik (1999), page 108 */

  double temp1, temp2, Z1, Z2;

  temp1=pow((1.0+spin),(1.0/3.0))+pow((1.0-spin),(1.0/3.0));
  temp2=pow((1.0-spin*spin),(1.0/3.0));
  Z1=1.0+temp2*temp1;
  Z2=sqrt(3.0*spin*spin+Z1*Z1);

  temp1=sqrt((3.0-Z1)*(3.0+Z1+2.0*Z2));
  return (3.0+Z2-temp1);
}

void zroots(fcomplex a[], int m, fcomplex roots[], int polish)
{
	void laguer(fcomplex a[], int m, fcomplex *x, int *its);
	int i,its,j,jj;
	fcomplex x,b,c,ad[MAXM];

	for (j=0;j<=m;j++) ad[j]=a[j];
	for (j=m;j>=1;j--) {
		x=Complex(0.0,0.0);
		laguer(ad,j,&x,&its);
		if (fabs(x.i) <= 2.0*EPS*fabs(x.r)) x.i=0.0;
		roots[j]=x;
		b=ad[j];
		for (jj=j-1;jj>=0;jj--) {
			c=ad[jj];
			ad[jj]=b;
			b=Cadd(Cmul(x,b),c);
		}
	}
	if (polish)
		for (j=1;j<=m;j++)
			laguer(a,m,&roots[j],&its);
	for (j=2;j<=m;j++) {
		x=roots[j];
		for (i=j-1;i>=1;i--) {
			if (roots[i].r <= x.r) break;
			roots[i+1]=roots[i];
		}
		roots[i+1]=x;
	}
}

void laguer(fcomplex a[], int m, fcomplex *x, int *its)
{
	int iter,j;
	float abx,abp,abm,err;
	fcomplex dx,x1,b,d,f,g,h,sq,gp,gm,g2;
	static float frac[MR+1] = {0.0,0.5,0.25,0.75,0.13,0.38,0.62,0.88,1.0};

	for (iter=1;iter<=MAXIT;iter++) {
		*its=iter;
		b=a[m];
		err=Cabs(b);
		d=f=Complex(0.0,0.0);
		abx=Cabs(*x);
		for (j=m-1;j>=0;j--) {
			f=Cadd(Cmul(*x,f),d);
			d=Cadd(Cmul(*x,d),b);
			b=Cadd(Cmul(*x,b),a[j]);
			err=Cabs(b)+abx*err;
		}
		err *= EPSS;
		if (Cabs(b) <= err) return;
		g=Cdiv(d,b);
		g2=Cmul(g,g);
		h=Csub(g2,RCmul(2.0,Cdiv(f,b)));
		sq=Csqrt(RCmul((float) (m-1),Csub(RCmul((float) m,h),g2)));
		gp=Cadd(g,sq);
		gm=Csub(g,sq);
		abp=Cabs(gp);
		abm=Cabs(gm);
		if (abp < abm) gp=gm;
		dx=((FMAX(abp,abm) > 0.0 ? Cdiv(Complex((float) m,0.0),gp)
			: RCmul(exp(log(1+abx)),Complex(cos((float)iter),sin((float)iter)))));
		x1=Csub(*x,dx);
		if (x->r == x1.r && x->i == x1.i) return;
		if (iter % MT) *x=x1;
		else *x=Csub(*x,RCmul(frac[iter/MT],dx));
	}
	printf("too many iterations in laguer\n");
	return;
}
