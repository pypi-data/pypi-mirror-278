#ifndef CCODATA_CONSTANTS_TYPE_H
#define CCODATA_CONSTANTS_TYPE_H

struct ccodata_constant_type{
    char name[65];
    double value;
    double uncertainty;
    char unit[33];
};

#endif
