# Challenge: Lazy Game Challenge

## Type: Interger Overflow

## Info

I found an interesting game made by some guy named "John_123". It is some betting game. I made some small fixes to the game; see if you can still pwn this and steal $1000000 from me!

To get flag, pwn the server at:

```sh
nc thekidofarcrania.com 10001
```

## Solution

- This challenge is an integer overflow type, so we just try to bet a negative number. After that we try to guess the correct result. When we fail, our amount will be `new amount = old amount + total amount we bet` (total amount we bet < 0 => new amount will increase).
