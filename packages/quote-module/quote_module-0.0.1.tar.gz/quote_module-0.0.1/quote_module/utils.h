

#ifndef __UTILS_C__
#define __UTILS_C__

int convert_BCD(const unsigned char bcd);
int convert_BCDs(const unsigned char *ptr, int len);

struct quote_s {
    char code_str[8];
    char timestamp_str[32];
    double close_price;
    int bool_close;
    int close_volume;
    int volume_acc;
    double ask_price[5];
    int ask_volume[5];
    double bid_price[5];
    int bid_volume[5];
    int bool_continue;
    int bool_bid_price;
    int bool_ask_price;
    int bool_odd;
    int number_best_ask;
    int number_best_bid;
    int tick_type;
    int bool_simtrade;
};

typedef void (*callback_str_t)(const char*);
typedef void (*callback_quote_t)(struct quote_s *);

void stock_quote_unpacker(const unsigned char *data,
                          unsigned int len,
                          void *arg,
                          const struct timeval *tv);

void future_quote_unpacker(const unsigned char *data,
                          unsigned int len,
                          void *arg,
                          const struct timeval *tv);

#endif // __UTILS_C__

