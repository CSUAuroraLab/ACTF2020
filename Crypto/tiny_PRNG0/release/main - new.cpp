#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <random>
#include <fstream>
#include <iostream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

template<class T>
T read_urandom() {
  union {
    T value;
    char cs[sizeof(T)];
  } u;

  std::ifstream rfin("/dev/urandom");
  rfin.read(u.cs, sizeof(u.cs));
  rfin.close();

  return u.value;
}

char flag[50];
char banner[] =
" __        _______ _     _     ____ ___  __  __ _____     _____ ___  \n"
" \\ \\      / / ____| |   | |   / ___/ _ \\|  \\/  | ____|   |_   _/ _ \\ \n"
"  \\ \\ /\\ / /|  _| | |   | |  | |  | | | | |\\/| |  _|       | || | | |\n"
"   \\ V  V / | |___| |___| |__| |__| |_| | |  | | |___      | || |_| |\n"
"    \\_/\\_/  |_____|_____|_____\\____\\___/|_|_ |_|_____|___  |_| \\___/ \n"
"     | __ )  / \\  |  _ \\         |  _ \\|  _ \\| \\ | |/ ___|/ _ \\      \n"
"     |  _ \\ / _ \\ | | | |        | |_) | |_) |  \\| | |  _| | | |     \n"
"     | |_) / ___ \\| |_| |        |  __/|  _ <| |\\  | |_| | |_| |     \n"
"     |____/_/   \\_\\____/         |_|   |_| \\_\\_| \\_|\\____|\\___/      ";
int main() {
  std::mt19937 mt(read_urandom<uint32_t>());
  std::ifstream rfin("/pwn/flag");
  rfin.read(flag, 50);
  rfin.close();

  puts(banner);
  while (1) {
    int option;
    uint32_t tmp1, tmp2;
    std::cout << "What you want to do?\n"
         "1) Check next 10 random number\n"
         "2) Guess next random number\n"
         "3) Read the source code\n"
         "4) Exit\n"
         "> " << std::flush;
    std::cin >> option;
    switch (option) {
    case 1:
      for (int i = 0; i < 10; ++i) {
        std::cout<< mt() << " ";
      }
      std::cout << std::endl;
      break;
    case 2:
      std::cout << "So next random number is: " << std::flush;
      std::cin >> tmp1;
      tmp2 = mt();
      if (tmp1 == tmp2) {
        std::cout << "WELL DONE!" << std::endl << flag << std::flush;
      } else {
        std::cout <<"Ops, right answer is " << tmp2 << std::endl << std::flush;
      }
      break;
    case 3:
      system("cat /pwn/main.cpp");
      break;
    case 4:
      exit(0);
    default:
      std::cout << "What's your mean by "<< option << "?\n" << std::flush;
      break;
    }
  }
  return 0;
}
