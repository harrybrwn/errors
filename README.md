# errors

Error handling for agile development.

lol, just kidding, import the `handle` decorator and it will redirect your errors to stackoverflow 😂

```python
from errors import handle

@handle
def raises_overflow():
	return raises_overflow()
```
