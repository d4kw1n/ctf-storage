# Challenge: Accumulator

## Type: Interger Overflow

## Info

I'll give you a flag if you can get a negative number by adding only positive numbers.

```sh
nc rivit.dev 10009
```

## Solution

- This challenge is an integer overflow type. The program asks us to exit the while loop and we can get the flag. The program allows us to enter a number, then it will sum it with the old value.
- The range of integers is from `2147483648` to `2147483647`. So we just need to enter `2147483647` first, then we enter `1` and the program will exit the while loop and we can get the flag.
