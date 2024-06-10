# PYLISTING
Functions to work with list in python


# install
- `pip install pylistin`



# API

## list_reduce `<E, T>(list: list[E], callback: (ac: T, item: E, index: int, list: list[E]) -> T,  ac_init: T) -> T `

Move in for each all elements with a `lamda` function or `def` as callback for return  a one result.

this function is used to loop through a list and accumulate a value.

```python
from pylisting import list_reduce

list_reduce([2,5,9], lambda ac, item: ac + item, 0) # 

```