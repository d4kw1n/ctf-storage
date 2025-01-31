# Challenge: RIP my bof

## Type: Ret2win

## Info

Okay so we have a bof, can we get it to redirect IP (instruction pointer) to something else?

If you get stuck liveoverflow covers you again!

```sh
nc thekidofarcrania.com 4902
```

## Solution

- This challenge is of the ret2win type. We just need to find the padding and overwrite the return address to redirect the program (the `win` function).
- Payload to exploit: [Solution](./solution.py)
