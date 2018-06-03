#define _GNU_SOURCE
#include "stdio.h"
#include "wiringPi.h"
#include "sched.h"
#define rec_num 10000

void get_hight_Pri(){
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(3,&mask);
    if (sched_setaffinity(0,sizeof(mask),&mask)==-1)
            printf("affinity set fail!");
    piHiPri(99);

}