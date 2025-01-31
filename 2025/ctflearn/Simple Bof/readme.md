# Challenge: Simple bof

## Type: Buffer Overflow

## Info

Want to learn the hacker's secret? Try to smash this buffer!

You need guidance? Look no further than to Mr. Liveoverflow. He puts out nice videos you should look if you haven't already

```sh
nc thekidofarcrania.com 35235
```

[bof.c](./bof.c)

## Solution

- When I tried to connect to the server, the server responded to me with the result of the visualization of the stack. Looking at it, we can know the value of the padding to overwrite the `secret` variable. => The padding is 32 (`buff`) and 16 (8 of padding and 8 of `notsecret`) => 48.
- Payload to exploit: [Solution](./solution.py)
