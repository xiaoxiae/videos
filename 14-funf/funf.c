#include<stdio.h>

int f(int x, int y)
{
  if (y != 0)
    return f(
       x ^ y,
      (x & y) << 1
    );
  return x;
}

int main()
{
  printf(
    "%d", f(61, 25)
  );
}
