# linkedit


[![PyPI version](https://badge.fury.io/py/linkedit.svg)](https://badge.fury.io/py/linkedit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This library was created to facilitate the use of linked lists with the same ease as regular lists in Python, while presenting them in a clearer and more aesthetic way, especially for beginners in data structures.


## Installation


You can install `linkedit` via pip:


```bash
pip install linkedit
```


## Usage 


### For Non Circular Singly Linked List


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7])
print(x)
```


### Output


```bash
[6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -> None (NULL)
```


#### You Can See All Nodes Details


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7], detail=True)
print(x)
```


### Output


```bash
╒═════════════════╤═════════════════════════╤══════════════╤══════════════════════╕
│ Current Value   │ Current Value @ddress   │ Next Value   │ Next Value @ddress   │
╞═════════════════╪═════════════════════════╪══════════════╪══════════════════════╡
│ 6               │ 0x7febe8213950          │ 3            │ 0x7febe8213990       │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 3               │ 0x7febe8213990          │ 8            │ 0x7febe82139d0       │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 8               │ 0x7febe82139d0          │ 1            │ 0x7febe823c110       │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 1               │ 0x7febe823c110          │ 9            │ 0x7febe805bd10       │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 9               │ 0x7febe805bd10          │ 5            │ 0x7febe805bb50       │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 5               │ 0x7febe805bb50          │ 7            │ 0x7febe805be50       │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 7               │ 0x7febe805be50          │ None (NULL)  │ 0x959cc0 (nil/0x0)   │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ None (NULL)     │ 0x959cc0 (nil/0x0)      │              │                      │
╘═════════════════╧═════════════════════════╧══════════════╧══════════════════════╛
```


#### You Can Change The Addresses Base From Hex(16) To Dec(10), Oct(8) Or Bin(2)


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7], detail=True, base=10)
print(x)
```


### Output


```bash
╒═════════════════╤═════════════════════════╤══════════════╤══════════════════════╕
│ Current Value   │ Current Value @ddress   │ Next Value   │ Next Value @ddress   │
╞═════════════════╪═════════════════════════╪══════════════╪══════════════════════╡
│ 6               │ 140217964133136         │ 3            │ 140217964133264      │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 3               │ 140217964133264         │ 8            │ 140217964133200      │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 8               │ 140217964133200         │ 1            │ 140217964298704      │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 1               │ 140217964298704         │ 9            │ 140217962282256      │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 9               │ 140217962282256         │ 5            │ 140217962281808      │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 5               │ 140217962281808         │ 7            │ 140217962282576      │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 7               │ 140217962282576         │ None (NULL)  │ 9804992 (nil/0)      │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ None (NULL)     │ 9804992 (nil/0)         │              │                      │
╘═════════════════╧═════════════════════════╧══════════════╧══════════════════════╛
```


#### You Can Add The Items In An Orderly Ascending Or Descending Manner


##### ASC


```python
from linkedit import singlyLinkedList


x = singlyLinkedList()
x.add(6)
x.add(3)
x.add(8)
x.add(1)
x.add(9)
x.add(5)
x.add(7)
print(x)
```


### Output


```bash
[1] -> [3] -> [5] -> [6] -> [7] -> [8] -> [9] -> None (NULL)
```


##### DESC


```python
from linkedit import singlyLinkedList


x = singlyLinkedList(reverse=True)
x.add(6)
x.add(3)
x.add(8)
x.add(1)
x.add(9)
x.add(5)
x.add(7)
print(x)
```

### Output


```bash
[9] -> [8] -> [7] -> [6] -> [5] -> [3] -> [1] -> None (NULL)
```


#### You Can Check If The Linked List Is Empty Or Not


```python
from linkedit import singlyLinkedList


x = singlyLinkedList()
print(x.isEmpty())
```


### Output


```bash
True
```


#### You Can Do Right / Left Shifting


##### Right Shifting

```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7])
print(x)
x >> 3
print(x)
```


### Output


```bash
[6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -> None (NULL)
[9] -> [5] -> [7] -> [6] -> [3] -> [8] -> [1] -> None (NULL)
```


##### Left Shifting


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7])
print(x)
x << 3
print(x)
```


### Output


```bash
[6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -> None (NULL)
[1] -> [9] -> [5] -> [7] -> [6] -> [3] -> [8] -> None (NULL)
```


#### You Can Insert A New Value In The First Of Linked List Directely With prepend


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7])
print(x)
x.prepend(0)
print(x)
```


### Output


```bash
[6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -> None (NULL)
[0] -> [6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -> None (NULL)
```


#### You Can Change From Non Circular To Circular


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7])
print(x)
x.set_circular()
print(x)
```


### Output

```bash
[6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -> None (NULL)
> [6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -
```


#### You Can Change From Singly To Doubly 


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7])
print(x)
x = x.to_doubly()
print(x)
```


### Output


```bash
[6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -> None (NULL)
None (NULL) <- [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] -> None (NULL)
```


#### You Can Create A Dictionary From The Linked List 


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7])
y = x.to_dict()
print(x)
print(y)
```


### Output


```bash
[6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -> None (NULL)
{6: {'current value @ddress': '0x7f64a3e13910', 'next value': 3, 'next value @ddress': '0x7f64a3e13a10'}, 3: {'current value @ddress': '0x7f64a3e13a10', 'next value': 8, 'next value @ddress': '0x7f64a3e13a50'}, 8: {'current value @ddress': '0x7f64a3e13a50', 'next value': 1, 'next value @ddress': '0x7f64a3e3c190'}, 1: {'current value @ddress': '0x7f64a3e3c190', 'next value': 9, 'next value @ddress': '0x7f64a3c1bc50'}, 9: {'current value @ddress': '0x7f64a3c1bc50', 'next value': 5, 'next value @ddress': '0x7f64a3c1ba90'}, 5: {'current value @ddress': '0x7f64a3c1ba90', 'next value': 7, 'next value @ddress': '0x7f64a3c1bd90'}, 7: {'current value @ddress': '0x7f64a3c1bd90', 'next value': None, 'next value @ddress': '0x959cc0'}}
```


### For Circular Singly Linked List


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
print(x)
```


### Output


```bash
> [6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -
```


#### With All Nodes Details


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True, detail=True)
print(x)
```


### Output


```bash
╒═════════════════╤═════════════════════════╤══════════════╤══════════════════════╕
│   Current Value │ Current Value @ddress   │   Next Value │ Next Value @ddress   │
╞═════════════════╪═════════════════════════╪══════════════╪══════════════════════╡
│               6 │ 0x7fbe38bf3ad0          │            3 │ 0x7fbe38bf3b50       │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│               3 │ 0x7fbe38bf3b50          │            8 │ 0x7fbe38bf3b10       │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│               8 │ 0x7fbe38bf3b10          │            1 │ 0x7fbe38c07fd0       │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│               1 │ 0x7fbe38c07fd0          │            9 │ 0x7fbe38a07c50       │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│               9 │ 0x7fbe38a07c50          │            5 │ 0x7fbe38a07a90       │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│               5 │ 0x7fbe38a07a90          │            7 │ 0x7fbe38a07d90       │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│               7 │ 0x7fbe38a07d90          │            6 │ 0x7fbe38bf3ad0       │
╘═════════════════╧═════════════════════════╧══════════════╧══════════════════════╛
```


#### With Dec(10) Base


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True, detail=True, base=10)
print(x)
```


### Output


```bash
╒═════════════════╤═════════════════════════╤══════════════╤══════════════════════╕
│   Current Value │   Current Value @ddress │   Next Value │   Next Value @ddress │
╞═════════════════╪═════════════════════════╪══════════════╪══════════════════════╡
│               6 │         140374800546256 │            3 │      140374800546448 │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│               3 │         140374800546448 │            8 │      140374800546192 │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│               8 │         140374800546192 │            1 │      140374800629712 │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│               1 │         140374800629712 │            9 │      140374798531664 │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│               9 │         140374798531664 │            5 │      140374798531216 │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│               5 │         140374798531216 │            7 │      140374798531984 │
├─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│               7 │         140374798531984 │            6 │      140374800546256 │
╘═════════════════╧═════════════════════════╧══════════════╧══════════════════════╛
```


#### Adding Items In An Orderly Ascending And Descending Manner


##### ASC


```python
from linkedit import singlyLinkedList


x = singlyLinkedList(circular=True)
x.add(6)
x.add(3)
x.add(8)
x.add(1)
x.add(9)
x.add(5)
x.add(7)
print(x)
```


### Output


```bash
> [1] -> [3] -> [5] -> [6] -> [7] -> [8] -> [9] -
```


##### DESC


```python
from linkedit import singlyLinkedList


x = singlyLinkedList(circular=True, reverse=True)
x.add(6)
x.add(3)
x.add(8)
x.add(1)
x.add(9)
x.add(5)
x.add(7)
print(x)
```

### Output


```bash
> [9] -> [8] -> [7] -> [6] -> [5] -> [3] -> [1] -
```


#### Checking If The Linked List Is Empty Or Not


```python
from linkedit import singlyLinkedList


x = singlyLinkedList(circular=True)
print(x.isEmpty())
```


### Output


```bash
True
```


#### Do A Right / Left Shifting


##### Right Shifting


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
print(x)
x >> 3
print(x)
```


### Output


```bash
> [6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -
> [9] -> [5] -> [7] -> [6] -> [3] -> [8] -> [1] -
```


##### Left Shifting


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
print(x)
x << 3
print(x)
```


### Output


```bash
> [6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -
> [1] -> [9] -> [5] -> [7] -> [6] -> [3] -> [8] -
```


#### Inserting A New Value In The First Of The Linked List Directely Using prepend


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
print(x)
x.prepend(0)
print(x)
```


### Output


```bash
> [6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -
> [0] -> [6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -
```


#### You Can Change From Circular To Non Circular


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
print(x)
x.set_non_circular()
print(x)
```


### Output

```bash
> [6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -
[6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -> None (NULL)
```


#### Changing From Singly To Doubly 


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
print(x)
x = x.to_doubly()
print(x)
```


### Output


```bash
> [6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -
=> [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] <=
```


#### Creating A Dictionary From The Linked List 


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
y = x.to_dict()
print(x)
print(y)
```


### Output


```bash
> [6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -
{6: {'current value @ddress': '0x7f2ffda139d0', 'next value': 3, 'next value @ddress': '0x7f2ffda13a90'}, 3: {'current value @ddress': '0x7f2ffda13a90', 'next value': 8, 'next value @ddress': '0x7f2ffda13990'}, 8: {'current value @ddress': '0x7f2ffda13990', 'next value': 1, 'next value @ddress': '0x7f2ffda3c1d0'}, 1: {'current value @ddress': '0x7f2ffda3c1d0', 'next value': 9, 'next value @ddress': '0x7f2ffd81bb90'}, 9: {'current value @ddress': '0x7f2ffd81bb90', 'next value': 5, 'next value @ddress': '0x7f2ffd81b9d0'}, 5: {'current value @ddress': '0x7f2ffd81b9d0', 'next value': 7, 'next value @ddress': '0x7f2ffd81bcd0'}, 7: {'current value @ddress': '0x7f2ffd81bcd0', 'next value': 6, 'next value @ddress': '0x7f2ffda139d0'}}
```


#### Advanced Usage


##### You Can Loop Over All Linked List Values With A Time Complexity Of O(n)


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7])


# Forward
node = x.node(0)  # Or x.head
for _ in range(len(x)):
    print(f"[{node.get_data()}]", end=" -> None\n" if node == x.tail else " -> ")
    node = node.next_node()
```


### Output


```bash
[6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -> None
```


##### You Can Create A Dict Of Nodes Objects From The Linked List


```python
from linkedit import singlyLinkedList


x = singlyLinkedList([6, 3, 8, 1, 9, 5, 7])


nodes_object_list = x.to_dict(node=True)
print(nodes_object_list)
```


### Output


```bash
{6: {'current node': <linkedit.singlyLinkedListNode object at 0x7f0b6d613c10>, 'next node value': 3, 'next node': <linkedit.singlyLinkedListNode object at 0x7f0b6d613c90>}, 3: {'current node': <linkedit.singlyLinkedListNode object at 0x7f0b6d613c90>, 'next node value': 8, 'next node': <linkedit.singlyLinkedListNode object at 0x7f0b6d613c50>}, 8: {'current node': <linkedit.singlyLinkedListNode object at 0x7f0b6d613c50>, 'next node value': 1, 'next node': <linkedit.singlyLinkedListNode object at 0x7f0b6d63c450>}, 1: {'current node': <linkedit.singlyLinkedListNode object at 0x7f0b6d63c450>, 'next node value': 9, 'next node': <linkedit.singlyLinkedListNode object at 0x7f0b6d41bd10>}, 9: {'current node': <linkedit.singlyLinkedListNode object at 0x7f0b6d41bd10>, 'next node value': 5, 'next node': <linkedit.singlyLinkedListNode object at 0x7f0b6d41bb50>}, 5: {'current node': <linkedit.singlyLinkedListNode object at 0x7f0b6d41bb50>, 'next node value': 7, 'next node': <linkedit.singlyLinkedListNode object at 0x7f0b6d41be50>}, 7: {'current node': <linkedit.singlyLinkedListNode object at 0x7f0b6d41be50>, 'next node value': None, 'next node': None}}
```


### For Non Circular Doubly Linked List


```python
from linkedit import doublyLinkedList

x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7])
print(x)
```


### Output


```bash
None (NULL) <- [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] -> None (NULL)
```


#### With All Nodes Details


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7], detail=True)
print(x)
```


### Output


```bash
╒══════════════════╤══════════════════════════╤═════════════════╤═════════════════════════╤══════════════╤══════════════════════╕
│ Previous Value   │ Previous Value @ddress   │ Current Value   │ Current Value @ddress   │ Next Value   │ Next Value @ddress   │
╞══════════════════╪══════════════════════════╪═════════════════╪═════════════════════════╪══════════════╪══════════════════════╡
│                  │                          │ None (NULL)     │ 0x959cc0 (nil/0x0)      │              │                      │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ None (NULL)      │ 0x959cc0 (nil/0x0)       │ 6               │ 0x7effd8613950          │ 3            │ 0x7effd8613990       │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 6                │ 0x7effd8613950           │ 3               │ 0x7effd8613990          │ 8            │ 0x7effd86139d0       │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 3                │ 0x7effd8613990           │ 8               │ 0x7effd86139d0          │ 1            │ 0x7effd863c110       │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 8                │ 0x7effd86139d0           │ 1               │ 0x7effd863c110          │ 9            │ 0x7effd845bd10       │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 1                │ 0x7effd863c110           │ 9               │ 0x7effd845bd10          │ 5            │ 0x7effd845bb50       │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 9                │ 0x7effd845bd10           │ 5               │ 0x7effd845bb50          │ 7            │ 0x7effd845be50       │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 5                │ 0x7effd845bb50           │ 7               │ 0x7effd845be50          │ None (NULL)  │ 0x959cc0 (nil/0x0)   │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                  │                          │ None (NULL)     │ 0x959cc0 (nil/0x0)      │              │                      │
╘══════════════════╧══════════════════════════╧═════════════════╧═════════════════════════╧══════════════╧══════════════════════╛
```


#### With Dec(10) Base


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7], detail=True, base=10)
print(x)
```


### Output


```bash
╒══════════════════╤══════════════════════════╤═════════════════╤═════════════════════════╤══════════════╤══════════════════════╕
│ Previous Value   │ Previous Value @ddress   │ Current Value   │ Current Value @ddress   │ Next Value   │ Next Value @ddress   │
╞══════════════════╪══════════════════════════╪═════════════════╪═════════════════════════╪══════════════╪══════════════════════╡
│                  │                          │ None (NULL)     │ 9804992 (nil/0)         │              │                      │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ None (NULL)      │ 9804992 (nil/0)          │ 6               │ 140107643451856         │ 3            │ 140107643451984      │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 6                │ 140107643451856          │ 3               │ 140107643451984         │ 8            │ 140107643451920      │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 3                │ 140107643451984          │ 8               │ 140107643451920         │ 1            │ 140107643617424      │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 8                │ 140107643451920          │ 1               │ 140107643617424         │ 9            │ 140107641601424      │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 1                │ 140107643617424          │ 9               │ 140107641601424         │ 5            │ 140107641600976      │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 9                │ 140107641601424          │ 5               │ 140107641600976         │ 7            │ 140107641601744      │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│ 5                │ 140107641600976          │ 7               │ 140107641601744         │ None (NULL)  │ 9804992 (nil/0)      │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                  │                          │ None (NULL)     │ 9804992 (nil/0)         │              │                      │
╘══════════════════╧══════════════════════════╧═════════════════╧═════════════════════════╧══════════════╧══════════════════════╛
```


#### Adding The Items In An Orderly Ascending And Descending Manner


##### ASC


```python
from linkedit import doublyLinkedList


x = doublyLinkedList()
x.add(6)
x.add(3)
x.add(8)
x.add(1)
x.add(9)
x.add(5)
x.add(7)
print(x)
```


### Output


```bash
None (NULL) <- [1] <=> [3] <=> [5] <=> [6] <=> [7] <=> [8] <=> [9] -> None (NULL)
```


##### DESC


```python
from linkedit import doublyLinkedList


x = doublyLinkedList(reverse=True)
x.add(6)
x.add(3)
x.add(8)
x.add(1)
x.add(9)
x.add(5)
x.add(7)
print(x)
```

### Output


```bash
None (NULL) <- [9] <=> [8] <=> [7] <=> [6] <=> [5] <=> [3] <=> [1] -> None (NULL)
```


#### Checking If The Linked List Is Empty Or Not


```python
from linkedit import doublyLinkedList


x = doublyLinkedList()
print(x.isEmpty())
```


### Output


```bash
True
```


#### Do Right / Left Shifting


##### Right Shifting


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7])
print(x)
x >> 3
print(x)
```


### Output


```bash
None (NULL) <- [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] -> None (NULL)
None (NULL) <- [9] <=> [5] <=> [7] <=> [6] <=> [3] <=> [8] <=> [1] -> None (NULL)
```


##### Left Shifting


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7])
print(x)
x << 3
print(x)
```


### Output


```bash
None (NULL) <- [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] -> None (NULL)
None (NULL) <- [1] <=> [9] <=> [5] <=> [7] <=> [6] <=> [3] <=> [8] -> None (NULL)
```


#### Inserting A New Value In The First Of Linked List Directely Using prepend


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7])
print(x)
x.prepend(0)
print(x)
```


### Output


```bash
None (NULL) <- [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] -> None (NULL)
None (NULL) <- [0] <=> [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] -> None (NULL)
```


#### Changing From Non Circular To Circular


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7])
print(x)
x.set_circular()
print(x)
```


### Output

```bash
None (NULL) <- [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] -> None (NULL)
=> [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] <=
```


#### You Can Change From Doubly To Singly 


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7])
print(x)
x = x.to_singly()
print(x)
```


### Output


```bash
None (NULL) <- [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] -> None (NULL)
[6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -> None (NULL)
```


#### Creating A Dictionary From The Linked List 


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7])
y = x.to_dict()
print(x)
print(y)
```


### Output


```bash
None (NULL) <- [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] -> None (NULL)
{6: {'current value @ddress': '0x7fb9c6117990', 'next value': 3, 'next value @ddress': '0x7fb9c6117a90'}, 3: {'current value @ddress': '0x7fb9c6117a90', 'next value': 8, 'next value @ddress': '0x7fb9c6117ad0'}, 8: {'current value @ddress': '0x7fb9c6117ad0', 'next value': 1, 'next value @ddress': '0x7fb9c6140250'}, 1: {'current value @ddress': '0x7fb9c6140250', 'next value': 9, 'next value @ddress': '0x7fb9c5f23b10'}, 9: {'current value @ddress': '0x7fb9c5f23b10', 'next value': 5, 'next value @ddress': '0x7fb9c5f23950'}, 5: {'current value @ddress': '0x7fb9c5f23950', 'next value': 7, 'next value @ddress': '0x7fb9c5f23c50'}, 7: {'current value @ddress': '0x7fb9c5f23c50', 'next value': None, 'next value @ddress': '0x959cc0'}}
```


### For Circular Doubly Linked List


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
print(x)
```


### Output


```bash
=> [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] <=
```


#### With All Nodes Details


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True, detail=True)
print(x)
```


### Output


```bash
╒══════════════════╤══════════════════════════╤═════════════════╤═════════════════════════╤══════════════╤══════════════════════╕
│   Previous Value │ Previous Value @ddress   │   Current Value │ Current Value @ddress   │   Next Value │ Next Value @ddress   │
╞══════════════════╪══════════════════════════╪═════════════════╪═════════════════════════╪══════════════╪══════════════════════╡
│                7 │ 0x7ff7a725be10           │               6 │ 0x7ff7a7413ad0          │            3 │ 0x7ff7a7413b50       │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                6 │ 0x7ff7a7413ad0           │               3 │ 0x7ff7a7413b50          │            8 │ 0x7ff7a7413b10       │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                3 │ 0x7ff7a7413b50           │               8 │ 0x7ff7a7413b10          │            1 │ 0x7ff7a7427fd0       │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                8 │ 0x7ff7a7413b10           │               1 │ 0x7ff7a7427fd0          │            9 │ 0x7ff7a725bcd0       │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                1 │ 0x7ff7a7427fd0           │               9 │ 0x7ff7a725bcd0          │            5 │ 0x7ff7a725bb10       │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                9 │ 0x7ff7a725bcd0           │               5 │ 0x7ff7a725bb10          │            7 │ 0x7ff7a725be10       │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                5 │ 0x7ff7a725bb10           │               7 │ 0x7ff7a725be10          │            6 │ 0x7ff7a7413ad0       │
╘══════════════════╧══════════════════════════╧═════════════════╧═════════════════════════╧══════════════╧══════════════════════╛
```


#### With Dec(10) Base


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True, detail=True, base=10)
print(x)
```


### Output


```bash
╒══════════════════╤══════════════════════════╤═════════════════╤═════════════════════════╤══════════════╤══════════════════════╕
│   Previous Value │   Previous Value @ddress │   Current Value │   Current Value @ddress │   Next Value │   Next Value @ddress │
╞══════════════════╪══════════════════════════╪═════════════════╪═════════════════════════╪══════════════╪══════════════════════╡
│                7 │          140070320684368 │               6 │         140070322534992 │            3 │      140070322535184 │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                6 │          140070322534992 │               3 │         140070322535184 │            8 │      140070322534928 │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                3 │          140070322535184 │               8 │         140070322534928 │            1 │      140070322700432 │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                8 │          140070322534928 │               1 │         140070322700432 │            9 │      140070320684048 │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                1 │          140070322700432 │               9 │         140070320684048 │            5 │      140070320683600 │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                9 │          140070320684048 │               5 │         140070320683600 │            7 │      140070320684368 │
├──────────────────┼──────────────────────────┼─────────────────┼─────────────────────────┼──────────────┼──────────────────────┤
│                5 │          140070320683600 │               7 │         140070320684368 │            6 │      140070322534992 │
╘══════════════════╧══════════════════════════╧═════════════════╧═════════════════════════╧══════════════╧══════════════════════╛
```


#### Adding The Items In An Orderly Ascending And Descending Manner


##### ASC


```python
from linkedit import doublyLinkedList


x = doublyLinkedList(circular=True)
x.add(6)
x.add(3)
x.add(8)
x.add(1)
x.add(9)
x.add(5)
x.add(7)
print(x)
```


### Output


```bash
=> [1] <=> [3] <=> [5] <=> [6] <=> [7] <=> [8] <=> [9] <=
```


##### DESC


```python
from linkedit import doublyLinkedList


x = doublyLinkedList(circular=True, reverse=True)
x.add(6)
x.add(3)
x.add(8)
x.add(1)
x.add(9)
x.add(5)
x.add(7)
print(x)
```

### Output


```bash
=> [9] <=> [8] <=> [7] <=> [6] <=> [5] <=> [3] <=> [1] <=
```


#### Checking If The Linked List Is Empty Or Not


```python
from linkedit import doublyLinkedList


x = doublyLinkedList(circular=True)
print(x.isEmpty())
```


### Output


```bash
True
```


#### Do Right / Left Shifting


##### Right Shifting


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
print(x)
x >> 3
print(x)
```


### Output


```bash
=> [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] <=
=> [9] <=> [5] <=> [7] <=> [6] <=> [3] <=> [8] <=> [1] <=
```


##### Left Shifting


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
print(x)
x << 3
print(x)
```


### Output


```bash
=> [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] <=
=> [1] <=> [9] <=> [5] <=> [7] <=> [6] <=> [3] <=> [8] <=
```


#### Inserting A New Value In The First Of Linked List Directely Using prepend


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
print(x)
x.prepend(0)
print(x)
```


### Output


```bash
=> [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] <=
=> [0] <=> [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] <=
```


#### Changing From Circular To Non Circular


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
print(x)
x.set_non_circular()
print(x)
```


### Output

```bash
=> [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] <=
None (NULL) <- [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] -> None (NULL)
```


#### You Can Change From Doubly To Singly 


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
print(x)
x = x.to_singly()
print(x)
```


### Output


```bash
=> [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] <=
> [6] -> [3] -> [8] -> [1] -> [9] -> [5] -> [7] -
```


#### Creating A Dictionary From The Linked List 


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7], circular=True)
y = x.to_dict()
print(x)
print(y)
```


### Output


```bash
=> [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] <=
{6: {'current value @ddress': '0x7f5366a139d0', 'next value': 3, 'next value @ddress': '0x7f5366a13a90'}, 3: {'current value @ddress': '0x7f5366a13a90', 'next value': 8, 'next value @ddress': '0x7f5366a13990'}, 8: {'current value @ddress': '0x7f5366a13990', 'next value': 1, 'next value @ddress': '0x7f5366a3c1d0'}, 1: {'current value @ddress': '0x7f5366a3c1d0', 'next value': 9, 'next value @ddress': '0x7f536681bb90'}, 9: {'current value @ddress': '0x7f536681bb90', 'next value': 5, 'next value @ddress': '0x7f536681b9d0'}, 5: {'current value @ddress': '0x7f536681b9d0', 'next value': 7, 'next value @ddress': '0x7f536681bcd0'}, 7: {'current value @ddress': '0x7f536681bcd0', 'next value': 6, 'next value @ddress': '0x7f5366a139d0'}}
```


#### Advanced Usage


##### Looping Over All Linked List Values With A Time Complexity Of O(n)


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7])


print("Forward : ")
node = x.node(0)  # Or x.head
print("None <- ", end="")
for _ in range(len(x)):
    print(f"[{node.get_data()}]", end=" -> None\n" if node == x.tail else " <=> ")
    node = node.next_node()


print("Backward : ")
node = x.node(-1)  # Or x.tail
print("None <- ", end="")
for _ in range(len(x)):
    print(f"[{node.get_data()}]", end=" -> None\n" if node == x.head else " <=> ")
    node = node.prev_node()
```


### Output


```bash
Forward : 
None <- [6] <=> [3] <=> [8] <=> [1] <=> [9] <=> [5] <=> [7] -> None
Backward : 
None <- [7] <=> [5] <=> [9] <=> [1] <=> [8] <=> [3] <=> [6] -> None
```


##### You Can Create A Dict Of Nodes Objects From The Linked List


```python
from linkedit import doublyLinkedList


x = doublyLinkedList([6, 3, 8, 1, 9, 5, 7])


nodes_object_list = x.to_dict(node=True)
print(nodes_object_list)
```


### Output


```bash
{6: {'prev node value': None, 'prev node @ddress': None, 'current node': <linkedit.doublyLinkedListNode object at 0x7ff5514d79d0>, 'next node value': 3, 'next node': <linkedit.doublyLinkedListNode object at 0x7ff5514d7a50>}, 3: {'prev node value': 6, 'prev node @ddress': <linkedit.doublyLinkedListNode object at 0x7ff5514d79d0>, 'current node': <linkedit.doublyLinkedListNode object at 0x7ff5514d7a50>, 'next node value': 8, 'next node': <linkedit.doublyLinkedListNode object at 0x7ff5514d7a10>}, 8: {'prev node value': 3, 'prev node @ddress': <linkedit.doublyLinkedListNode object at 0x7ff5514d7a50>, 'current node': <linkedit.doublyLinkedListNode object at 0x7ff5514d7a10>, 'next node value': 1, 'next node': <linkedit.doublyLinkedListNode object at 0x7ff55128fe50>}, 1: {'prev node value': 8, 'prev node @ddress': <linkedit.doublyLinkedListNode object at 0x7ff5514d7a10>, 'current node': <linkedit.doublyLinkedListNode object at 0x7ff55128fe50>, 'next node value': 9, 'next node': <linkedit.doublyLinkedListNode object at 0x7ff55128fc90>}, 9: {'prev node value': 1, 'prev node @ddress': <linkedit.doublyLinkedListNode object at 0x7ff55128fe50>, 'current node': <linkedit.doublyLinkedListNode object at 0x7ff55128fc90>, 'next node value': 5, 'next node': <linkedit.doublyLinkedListNode object at 0x7ff55128ff90>}, 5: {'prev node value': 9, 'prev node @ddress': <linkedit.doublyLinkedListNode object at 0x7ff55128fc90>, 'current node': <linkedit.doublyLinkedListNode object at 0x7ff55128ff90>, 'next node value': 7, 'next node': <linkedit.doublyLinkedListNode object at 0x7ff55128fed0>}, 7: {'prev node value': 5, 'prev node @ddress': <linkedit.doublyLinkedListNode object at 0x7ff55128ff90>, 'current node': <linkedit.doublyLinkedListNode object at 0x7ff55128fed0>, 'next node value': None, 'next node': None}}
```


### Important Note


You can use all list methods with singly / doubly linked list sush as [append, clear, copy, count, extand, insert, index, pop, remove, reverse, sort], and all operations you can do with a list can do with this linked list.


### For Non Circular Orthogonal Linked List


```python
from linkedit import orthogonalLinkedList


x = orthogonalLinkedList([[6, 3, 8], [1, 9, 5], [7, 2, 4]])
print(x)
```

### Output


```bash
╒══════╤══════╤══════╤══════╤══════╕
│      │ None │ None │ None │      │
├──────┼──────┼──────┼──────┼──────┤
│ None │ 6    │ 3    │ 8    │ None │
├──────┼──────┼──────┼──────┼──────┤
│ None │ 1    │ 9    │ 5    │ None │
├──────┼──────┼──────┼──────┼──────┤
│ None │ 7    │ 2    │ 4    │ None │
├──────┼──────┼──────┼──────┼──────┤
│      │ None │ None │ None │      │
╘══════╧══════╧══════╧══════╧══════╛
```


#### With All Nodes Details


```python
from linkedit import orthogonalLinkedList


x = orthogonalLinkedList([[6, 3, 8], [1, 9, 5], [7, 2, 4]], detail=True)
print(x)
```


### Output


```bash
╒══════╤════════════════╤════════════╤════════════════╤═══════════╤════════════════╤════════╤════════════════╤════════╤════════════════╕
│ Up   │ Up @           │ Previous   │ Previous @     │   Current │ Current @      │ Down   │ Down @         │ Next   │ Next @         │
╞══════╪════════════════╪════════════╪════════════════╪═══════════╪════════════════╪════════╪════════════════╪════════╪════════════════╡
│ None │ 0x959cc0       │ None       │ 0x959cc0       │         6 │ 0x7f20d0213250 │ 1      │ 0x7f20d0213cd0 │ 3      │ 0x7f20d0213c50 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│ None │ 0x959cc0       │ 6          │ 0x7f20d0213250 │         3 │ 0x7f20d0213c50 │ 9      │ 0x7f20d023c090 │ 8      │ 0x7f20d0213c90 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│ None │ 0x959cc0       │ 3          │ 0x7f20d0213c50 │         8 │ 0x7f20d0213c90 │ 5      │ 0x7f20d005bcd0 │ None   │ 0x959cc0       │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│ 6    │ 0x7f20d0213250 │ None       │ 0x959cc0       │         1 │ 0x7f20d0213cd0 │ 7      │ 0x7f20d005bb10 │ 9      │ 0x7f20d023c090 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│ 3    │ 0x7f20d0213c50 │ 1          │ 0x7f20d0213cd0 │         9 │ 0x7f20d023c090 │ 2      │ 0x7f20d005be10 │ 5      │ 0x7f20d005bcd0 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│ 8    │ 0x7f20d0213c90 │ 9          │ 0x7f20d023c090 │         5 │ 0x7f20d005bcd0 │ 4      │ 0x7f20d005bd50 │ None   │ 0x959cc0       │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│ 1    │ 0x7f20d0213cd0 │ None       │ 0x959cc0       │         7 │ 0x7f20d005bb10 │ None   │ 0x959cc0       │ 2      │ 0x7f20d005be10 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│ 9    │ 0x7f20d023c090 │ 7          │ 0x7f20d005bb10 │         2 │ 0x7f20d005be10 │ None   │ 0x959cc0       │ 4      │ 0x7f20d005bd50 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│ 5    │ 0x7f20d005bcd0 │ 2          │ 0x7f20d005be10 │         4 │ 0x7f20d005bd50 │ None   │ 0x959cc0       │ None   │ 0x959cc0       │
╘══════╧════════════════╧════════════╧════════════════╧═══════════╧════════════════╧════════╧════════════════╧════════╧════════════════╛
```


### For Circular Orthogonal Linked List


```python
from linkedit import orthogonalLinkedList


x = orthogonalLinkedList([[6, 3, 8], [1, 9, 5], [7, 2, 4]], circular=True)
print(x)
```


### Output


```bash
╒═══╤═══╤═══╕
│ 6 │ 3 │ 8 │
├───┼───┼───┤
│ 1 │ 9 │ 5 │
├───┼───┼───┤
│ 7 │ 2 │ 4 │
╘═══╧═══╧═══╛
```


#### with All Nodes Details


```python
from linkedit import orthogonalLinkedList


x = orthogonalLinkedList([[6, 3, 8], [1, 9, 5], [7, 2, 4]], circular=True, detail=True)
print(x)
```


### Output


```bash
╒══════╤════════════════╤════════════╤════════════════╤═══════════╤════════════════╤════════╤════════════════╤════════╤════════════════╕
│   Up │ Up @           │   Previous │ Previous @     │   Current │ Current @      │   Down │ Down @         │   Next │ Next @         │
╞══════╪════════════════╪════════════╪════════════════╪═══════════╪════════════════╪════════╪════════════════╪════════╪════════════════╡
│    7 │ 0x7f01e6153ad0 │          8 │ 0x7f01e6317cd0 │         6 │ 0x7f01e6316250 │      1 │ 0x7f01e6317d10 │      3 │ 0x7f01e6317c90 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│    2 │ 0x7f01e6153dd0 │          6 │ 0x7f01e6316250 │         3 │ 0x7f01e6317c90 │      9 │ 0x7f01e632bfd0 │      8 │ 0x7f01e6317cd0 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│    4 │ 0x7f01e6153d10 │          3 │ 0x7f01e6317c90 │         8 │ 0x7f01e6317cd0 │      5 │ 0x7f01e6153c90 │      6 │ 0x7f01e6316250 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│    6 │ 0x7f01e6316250 │          5 │ 0x7f01e6153c90 │         1 │ 0x7f01e6317d10 │      7 │ 0x7f01e6153ad0 │      9 │ 0x7f01e632bfd0 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│    3 │ 0x7f01e6317c90 │          1 │ 0x7f01e6317d10 │         9 │ 0x7f01e632bfd0 │      2 │ 0x7f01e6153dd0 │      5 │ 0x7f01e6153c90 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│    8 │ 0x7f01e6317cd0 │          9 │ 0x7f01e632bfd0 │         5 │ 0x7f01e6153c90 │      4 │ 0x7f01e6153d10 │      1 │ 0x7f01e6317d10 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│    1 │ 0x7f01e6317d10 │          4 │ 0x7f01e6153d10 │         7 │ 0x7f01e6153ad0 │      6 │ 0x7f01e6316250 │      2 │ 0x7f01e6153dd0 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│    9 │ 0x7f01e632bfd0 │          7 │ 0x7f01e6153ad0 │         2 │ 0x7f01e6153dd0 │      3 │ 0x7f01e6317c90 │      4 │ 0x7f01e6153d10 │
├──────┼────────────────┼────────────┼────────────────┼───────────┼────────────────┼────────┼────────────────┼────────┼────────────────┤
│    5 │ 0x7f01e6153c90 │          2 │ 0x7f01e6153dd0 │         4 │ 0x7f01e6153d10 │      8 │ 0x7f01e6317cd0 │      7 │ 0x7f01e6153ad0 │
╘══════╧════════════════╧════════════╧════════════════╧═══════════╧════════════════╧════════╧════════════════╧════════╧════════════════╛
```


#### Advanced Usage


```python
from linkedit import orthogonalLinkedList


x = orthogonalLinkedList([[6, 3, 8], [1, 9, 5], [7, 2, 4]])


print("Printing All Data Using x.node : ")
for i in range(len(x.node)):
    for j in range(len(x.node[i])):
        print(x.node[i][j].get_data())


print("Printing All Data Using x.node And x.shape : ")
for i in range(x.shape[0]):
    for j in range(x.shape[1]):
        print(x.node[i][j].get_data())


center = x.node[1][1]
print(f"All Neighbors Of The Center Node {center.get_data()} : ")
print(f"up : {center.up_node().get_data()}")
print(f"prev : {center.prev_node().get_data()}")
print(f"down : {center.down_node().get_data()}")
print(f"next : {center.next_node().get_data()}")
```


### Output


```bash
Printing All Data Using x.node : 
6
3
8
1
9
5
7
2
4
Printing All Data Using x.node And x.shape : 
6
3
8
1
9
5
7
2
4
All Neighbors Of The Center Node 9 : 
up : 3
prev : 1
down : 2
next : 5
```


### Note


You can import sll in place of singlyLinkedList and dll in place of doublyLinkedList and oll in place of orthogonalLinkedList.


## License


This project is licensed under the MIT LICENSE - see the [LICENSE](https://opensource.org/licenses/MIT) for more details.
