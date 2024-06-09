# BestAPI

This is how Starlette would look like if I could add breaking changes freely.

BestAPI doesn't support:

- Python 3.8 or older.
- Trio.
- ASGI 2.0 interface.

## Checklist

[ ] Drop AnyIO and Starlette dependency.
[ ] Add `BaseResponse` as base class for response classes.
[ ] Background tasks: I need to work on a better API.
[ ] Use ClientDisconnect mechanism instead of `receive()` -> `http.disconnect` on `StreamingResponse`.
