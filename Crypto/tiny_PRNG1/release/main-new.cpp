#include <cstdio>
#include <cassert>
#include <cstdlib>
#include <cstdint>
#include <random>
#include <fstream>
#include <iostream>
#include <cstring>

uint64_t s[2];

static inline uint64_t rotl(const uint64_t x, int k) {
  return (x << k) | (x >> (64 - k));
}

uint64_t next(void) {
  const uint64_t s0 = s[0];
  uint64_t s1 = s[1];
  const uint64_t result = s0 + s1;

  s1 ^= s0;
  s[0] = rotl(s0, 55) ^ s1 ^ (s1 << 14);
  s[1] = rotl(s1, 36);
  return result;
}

char flag[50]="ACTF{xoroshiro128plus}";
char banner[] =
"██╗    ██╗███████╗██╗     ██╗      ██████╗"
" ██████╗ ███╗   ███╗███████╗            ████████╗ ██████╗ \n"
"██║    ██║██╔════╝██║     ██║     ██╔════╝"
"██╔═══██╗████╗ ████║██╔════╝            ╚══██╔══╝██╔═══██╗\n"
"██║ █╗ ██║█████╗  ██║     ██║     ██║     "
"██║   ██║██╔████╔██║█████╗                 ██║   ██║   ██║\n"
"██║███╗██║██╔══╝  ██║     ██║     ██║     "
"██║   ██║██║╚██╔╝██║██╔══╝                 ██║   ██║   ██║\n"
"╚███╔███╔╝███████╗███████╗███████╗╚██████╗"
"╚██████╔╝██║ ╚═╝ ██║███████╗               ██║   ╚██████╔╝\n"
" ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝"
" ╚═════╝ ╚═╝     ╚═╝╚══════╝               ╚═╝    ╚═════╝ \n"
"                                          "
"                                                          \n"
"        ██████╗  █████╗ ██████╗           "
"      ██████╗ ██████╗ ███╗   ██╗ ██████╗  ██╗             \n"
"        ██╔══██╗██╔══██╗██╔══██╗          "
"      ██╔══██╗██╔══██╗████╗  ██║██╔════╝ ███║             \n"
"        ██████╔╝███████║██║  ██║          "
"      ██████╔╝██████╔╝██╔██╗ ██║██║  ███╗╚██║             \n"
"        ██╔══██╗██╔══██║██║  ██║          "
"      ██╔═══╝ ██╔══██╗██║╚██╗██║██║   ██║ ██║             \n"
"        ██████╔╝██║  ██║██████╔╝          "
"      ██║     ██║  ██║██║ ╚████║╚██████╔╝ ██║             \n"
"        ╚═════╝ ╚═╝  ╚═╝╚═════╝           "
"      ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═╝             ";
int main() {
  s[0] = *reinterpret_cast<uint64_t *>(flag + 5);
  s[1] = *reinterpret_cast<uint64_t *>(flag + 13);
  assert(("Flag length correct", strlen(flag) == 22));
  puts(banner);
  while (1) {
    int option;
    uint32_t tmp1, tmp2;
    std::cout << "What you want to do?\n"
         "1) Check next 10 random number\n"
         "2) Read the source code\n"
         "3) Exit\n"
         "> " << std::flush;
    std::cin >> option;
    switch (option) {
    case 1:
      for (int i = 0; i < 10; ++i) {
        std::cout<< next() << " ";
      }
      std::cout << std::endl;
      break;
    case 2:
      system("cat /pwn/main.cpp");
      break;
    case 3:
      exit(0);
    default:
      std::cout << "What's your mean by "<< option << "?\n" << std::flush;
      break;
    }
  }
  return 0;
}
