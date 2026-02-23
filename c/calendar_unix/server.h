#include <sys/socket.h>
#include <netinet/in.h> 

struct sockaddr_in {
    short            sin_family;   // e.g: AF_INET
    unsigned short   sin_port;     // e.g: htons(3490)
    struct in_addr   sin_addr;     // détaillé ci-dessous
    char             sin_zero[8];  // '0' habituellement
};

typedef sockaddr_in sockaddr_in;

struct in_addr {
    unsigned long s_addr;  // initialiser avec inet_aton()
};
typedef in_addr in_addr;