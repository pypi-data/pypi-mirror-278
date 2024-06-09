# Copyright (c) 2024 Khiat Mohammed Abderrezzak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Author: Khiat Mohammed Abderrezzak <khiat.abderrezzak@gmail.com>


"""Sophisticate Linked List"""


__all__ = [
    "singlyLinkedList",
    "sll",
    "doublyLinkedList",
    "dll",
    "orthogonalLinkedList",
    "oll",
]


from tabulate import tabulate


def _red(text: str) -> str:
    """Red Coloring Function"""
    return "\033[91;1m{}\033[00m".format(text)


def _green(text: str) -> str:
    """Green Coloring Function"""
    return "\033[92;1m{}\033[00m".format(text)


def _yellow(text: str) -> str:
    """Yellow Coloring Function"""
    return "\033[93;1m{}\033[00m".format(text)


def _blue(text: str) -> str:
    """Blue Coloring Function"""
    return "\033[94;1m{}\033[00m".format(text)


def _cyan(text: str) -> str:
    """Cyan Coloring Function"""
    return "\033[36;1m{}\033[00m".format(text)


def _white(text: str) -> str:
    """White Coloring Function"""
    return "\033[37;1m{}\033[00m".format(text)


# for the background coloring
_BG_RED: str = "\033[41m"
_RESET: str = "\033[0m"


class _singlyLinkedListNode:
    def __init__(
        self: "_singlyLinkedListNode",
        data: object,
    ) -> None:
        self.data: object = data
        self.next: _singlyLinkedListNode | None = None

    def get_data(
        self: "_singlyLinkedListNode",
    ) -> object:
        return self.data

    def next_node(self: "_singlyLinkedListNode") -> "_singlyLinkedListNode":
        return self.next


class _doublyLinkedListNode:
    def __init__(
        self: "_doublyLinkedListNode",
        data: object,
    ) -> None:
        self.data: object = data
        self.prev: _doublyLinkedListNode | None = None
        self.next: _doublyLinkedListNode | None = None

    def get_data(
        self: "_doublyLinkedListNode",
    ) -> object:
        return self.data

    def prev_node(self: "_doublyLinkedListNode") -> "_doublyLinkedListNode":
        return self.prev

    def next_node(self: "_doublyLinkedListNode") -> "_doublyLinkedListNode":
        return self.next


class _linkedList:
    def __init__(
        self: object,
        data: object = None,
        *,
        circular: bool = False,
        detail: bool = False,
        base: int = 16,
        reverse: bool = False,
    ) -> None:
        """constructor special method"""
        self.circular: bool = circular
        self.detail: bool = detail
        if self.detail:
            self.base: int = base
        else:
            # if detail is not true we assign directely the default base 16 hexa
            self._base: int = 16
        # O(1) len (track the object)
        self.len: int = 0
        self._tail: _singlyLinkedListNode | _doublyLinkedListNode | None = None
        self.head: _singlyLinkedListNode | _doublyLinkedListNode | None = data
        self.rev: bool = reverse

    def __len__(self: object) -> int:
        """length special method"""
        return self.len

    def __contains__(
        self: object,
        item: object,
    ) -> bool:
        head: _singlyLinkedListNode | _doublyLinkedListNode = self._head
        for _ in range(self.len):
            if head.data == item:
                return True
            head: object | None = head.next
        return False

    def __mul__(self: object, other: int) -> object:
        if not isinstance(other, int):
            raise ValueError("Unsupported operand type for *")
        if self.isEmpty():
            for _ in range(other):
                self.append(None)
        else:
            length = self.len
            for _ in range(other - 1):
                head: _singlyLinkedListNode | _doublyLinkedListNode = self._head
                for _ in range(length):
                    self.append(head.data)
                    head = head.next
        return self

    def __setitem__(
        self: object,
        index: int,
        value: object,
    ) -> None:
        self.node(index).data = value

    def __eq__(
        self: object,
        other: object,
    ) -> bool:
        if isinstance(other, singlyLinkedList) or isinstance(other, doublyLinkedList):
            if id(self) == id(other):
                return True
            elif len(self) != len(other):
                return False
            elif len(self) == 0 and len(other) == 0:
                return True
            else:
                head1: _singlyLinkedListNode | _doublyLinkedListNode = self._head
                head2: _singlyLinkedListNode | _doublyLinkedListNode = other._head
                for _ in range(len(self)):
                    if head1.data == head2.data:
                        pass
                    else:
                        return False
                    head1: _singlyLinkedListNode | _doublyLinkedListNode | None = (
                        head1.next
                    )
                    head2: _singlyLinkedListNode | _doublyLinkedListNode | None = (
                        head2.next
                    )
                return True
        else:
            return False

    def __gt__(
        self: object,
        other: object,
    ) -> bool:
        if isinstance(other, singlyLinkedList) or isinstance(other, doublyLinkedList):
            return len(self) > len(other)
        else:
            raise TypeError(
                f"'>' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __ge__(
        self: object,
        other: object,
    ) -> bool:
        if isinstance(other, singlyLinkedList) or isinstance(other, doublyLinkedList):
            return len(self) >= len(other)
        else:
            raise TypeError(
                f"'>=' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
            )

    @property
    def base(self: object) -> int:
        """base getter"""
        return self._base

    @base.setter
    def base(self: object, base: int) -> None:
        """base setter"""
        valid_bases: list = [2, 8, 10, 16]
        if not isinstance(base, int):
            # if the base is not an integer we keep the default base 16 hexa
            self._base: int = 16
            print(
                _red("Warning")
                + _white(" : Base must be integer, ")
                + _red(f"{type(base)} ")
                + _white("object not valid")
            )
        else:
            if base not in valid_bases:
                # if the base is not a valid base integer we keep the default base 16 hexa
                self._base: int = 16
                print(
                    _red("Warning")
                    + _white(" : Base must be one of these ")
                    + _green("[")
                    + _blue("2")
                    + _white(", ")
                    + _blue("8")
                    + _white(", ")
                    + _blue("10")
                    + _white(", ")
                    + _blue("16")
                    + _green("]")
                    + _white(", ")
                    + _red(f"{base} ")
                    + _white("not a valid base")
                )
            else:
                self._base: int = base

    def node(self: object, index: int) -> _singlyLinkedListNode | _doublyLinkedListNode:
        """node(s) searching method"""
        if not isinstance(index, int):
            if not self.circular:
                raise TypeError(
                    "non circular singly linked list indices must be integers"
                )
            else:
                raise TypeError("circular singly linked list indices must be integers")
        elif not self._head or index >= self.len:
            if not self.circular:
                raise IndexError("non circular singly linked list index out of range")
            else:
                raise IndexError("circular singly linked list index out of range")
        else:
            if index == 0:
                return self._head
            else:
                if index < 0:
                    if -index <= self.len:
                        index = self.len + index
                    else:
                        if not self.circular:
                            raise IndexError(
                                "non circular singly linked list index out of range"
                            )
                        else:
                            raise IndexError(
                                "circular singly linked list index out of range"
                            )
                head: _singlyLinkedListNode | _doublyLinkedListNode = self._head
                if index == self.len - 1:
                    return self._tail
                for _ in range(index):
                    head: _singlyLinkedListNode | _doublyLinkedListNode | None = (
                        head.next
                    )
                return head

    @property
    def tail(
        self: object,
    ) -> _singlyLinkedListNode | _doublyLinkedListNode:
        return self._tail

    @tail.deleter
    def tail(self: object) -> None:
        self._tail = None

    def isEmpty(self: object) -> bool:
        return not self._head

    def index(
        self: object,
        value: object,
    ) -> int:
        """Return first index of value.

        Raises ValueError if the value is not present."""
        head: _singlyLinkedListNode | _doublyLinkedListNode | None = self._head
        for i in range(self.len):
            if head.data == value:
                return i
            head: _singlyLinkedListNode | _doublyLinkedListNode | None = head.next
        if not self.circular:
            error_msg: str = f"{value} is not in the non circular linked list"
            raise ValueError(error_msg)
        else:
            error_msg: str = f"{value} is not in the circular linked list"
            raise ValueError(error_msg)

    def clear(self: object) -> None:
        self._head: None = None
        self._tail: None = None
        self.len: int = 0

    def append(
        self: object,
        data: object,
    ) -> None:
        """Append object to the end of the linked list."""
        self.insert(self.len, data)

    def remove(
        self: object,
        value: object,
    ) -> None:
        """Remove first occurrence of value.

        Raises ValueError if the value is not present."""
        node_index: int = self.index(value)
        try:
            self.pop(node_index)
            return
        except IndexError as e0:
            pass
        if not self.circular:
            error_msg: str = f"{value} not in the non circular singly linked list"
            raise ValueError(error_msg)
        else:
            error_msg: str = f"{value} not in the circular singly linked list"
            raise ValueError(error_msg)

    # O(n log n) sort (Tim Sort => hybrid sorting algorithm = Merge Sort + Insertion Sort)
    def sort(self: object, *, reverse: bool = False) -> None:
        """Sort the linked list in ascending order and return None.

        The sort is in-place (i.e. the linked list itself is modified) and stable (i.e. the order of two equal elements is maintained).

        If a key function is given, apply it once to each linked list item and sort them, ascending or descending, according to their function values.

        The reverse flag can be set to sort in descending order."""
        non_sorted_list: list = []
        head: _singlyLinkedListNode | _doublyLinkedListNode | None = self._head
        if self.len >= 1:
            for _ in range(self.len - 1):
                if type(head.data) == type(head.next.data):
                    non_sorted_list.append(head.data)
                    head: _singlyLinkedListNode | _doublyLinkedListNode | None = (
                        head.next
                    )
                else:
                    raise TypeError(
                        f"'<' not supported between instances of '{type(head.data).__name__}' and '{type(head.next.data).__name__}'"
                    )
            non_sorted_list.append(head.data)
            non_sorted_list.sort(reverse=reverse)
            head: _singlyLinkedListNode | _doublyLinkedListNode = self._head
            for i in range(self.len):
                head.data = non_sorted_list[i]
                head: _singlyLinkedListNode | _doublyLinkedListNode | None = head.next

    def count(
        self: object,
        value: object,
    ) -> int:
        """Return number of occurrences of value."""
        head: _singlyLinkedListNode | _doublyLinkedListNode | None = self._head
        counter: int = 0
        if self.len >= 1:
            for _ in range(self.len):
                if head.data == value:
                    counter += 1
                head: _singlyLinkedListNode | _doublyLinkedListNode | None = head.next
            return counter

    def __rshift__(self: object, rotate: int) -> None:
        if not isinstance(rotate, int):
            raise TypeError("rotate must be an integer")
        helper1: list = []
        helper2: list = []
        head: _singlyLinkedListNode | _doublyLinkedListNode | None = self._head
        try:
            rotate: int = rotate % self.len
        except ZeroDivisionError as e1:
            return
        for _ in range(self.len - rotate):
            helper1.append(head.data)
            head: _singlyLinkedListNode | _doublyLinkedListNode | None = head.next
        for _ in range(self.len - rotate, self.len):
            helper2.append(head.data)
            head: _singlyLinkedListNode | _doublyLinkedListNode | None = head.next
        head: _singlyLinkedListNode | _doublyLinkedListNode | None = self._head
        helper2.extend(helper1)
        for i in range(self.len):
            head.data = helper2[i]
            head: _singlyLinkedListNode | _doublyLinkedListNode | None = head.next

    def __lshift__(self: object, rotate: int) -> None:
        if not isinstance(rotate, int):
            raise TypeError("rotate must be an integer")
        helper1: list = []
        helper2: list = []
        head: _singlyLinkedListNode | _doublyLinkedListNode | None = self._head
        try:
            rotate: int = rotate % self.len
        except ZeroDivisionError as e2:
            return
        for _ in range(rotate):
            helper1.append(head.data)
            head: _singlyLinkedListNode | _doublyLinkedListNode | None = head.next
        for _ in range(rotate, self.len):
            helper2.append(head.data)
            head: _singlyLinkedListNode | _doublyLinkedListNode | None = head.next
        head: object | None = self._head
        helper2.extend(helper1)
        for i in range(self.len):
            head.data = helper2[i]
            head: _singlyLinkedListNode | _doublyLinkedListNode | None = head.next

    def prepend(
        self: object,
        data: object,
    ) -> None:
        self.insert(0, data)


class singlyLinkedList(_linkedList):
    @property
    def head(
        self: "singlyLinkedList",
    ) -> _singlyLinkedListNode:
        return self._head

    @head.setter
    def head(
        self: "singlyLinkedList",
        data: object,
    ) -> None:
        self._head: None = None
        if isinstance(data, singlyLinkedList):
            self._head: _singlyLinkedListNode | None = data._head
        elif isinstance(data, _singlyLinkedListNode):
            old_head: _singlyLinkedListNode = data
            old_self_head: _singlyLinkedListNode = data
            new_head: _singlyLinkedListNode = _singlyLinkedListNode(data.data)
            self._head: _singlyLinkedListNode = new_head
            self.len += 1
            old_head: _singlyLinkedListNode | None = old_head.next
            while old_head and old_head != old_self_head:
                new_node: _singlyLinkedListNode = _singlyLinkedListNode(old_head.data)
                self.len += 1
                new_head.next = new_node
                new_head: _singlyLinkedListNode | None = new_head.next
                old_head: _singlyLinkedListNode | None = old_head.next
            if self.circular:
                new_node.next = self._head
            self._tail: _singlyLinkedListNode = new_node
        else:
            try:
                if len(data) > 0:
                    for i in data:
                        self.append(i)
            except TypeError as e3:
                if data is not None:
                    new_node: _singlyLinkedListNode = _singlyLinkedListNode(data)
                    self.len += 1
                    self._head: _singlyLinkedListNode = new_node
                    if self.circular:
                        new_node.next = new_node
                    self._tail: _singlyLinkedListNode = new_node

    @head.deleter
    def head(self: "singlyLinkedList") -> None:
        self._head: None = None

    def copy(self: "singlyLinkedList") -> "singlyLinkedList":
        """Return a shallow copy of the non circular/circular singly linked list."""
        return singlyLinkedList(
            self._head,
            detail=self.detail,
            circular=self.circular,
            base=self._base,
        )

    def set_circular(self: "singlyLinkedList") -> None:
        self._tail.next = self._head
        self.circular: bool = True

    def set_non_circular(self: "singlyLinkedList") -> None:
        self._tail.next = None
        self.circular: bool = False

    def __add__(
        self: "singlyLinkedList",
        other: object,
    ) -> None:
        helper: list = []
        head1: _singlyLinkedListNode | None = self._head
        if isinstance(other, singlyLinkedList) or isinstance(other, doublyLinkedList):
            head2: _singlyLinkedListNode | None = other._head
        else:
            other: singlyLinkedList = singlyLinkedList(other)
            head2: _singlyLinkedListNode = other._head
        for _ in range(self.len):
            helper.append(head1.data)
            head1: _singlyLinkedListNode | None = head1.next
        for _ in range(other.len):
            helper.append(head2.data)
            head2: _singlyLinkedListNode | None = head2.next
        return singlyLinkedList(helper, circular=other.circular)

    def __str__(self: "singlyLinkedList") -> str:
        """Return str(self)."""
        if not self._head:
            if not self.circular:
                raise TypeError("Empty non circular singly linked list")
            else:
                raise TypeError("Empty circular singly linked list")
        else:
            head: _singlyLinkedListNode = self._head
            linked_list: list = []
            counter: int = 0
            if not self.detail:
                while head and head.next != self._head:
                    if isinstance(head.data, str):
                        if len(head.data) == 0:
                            linked_list.append(f"[{head.data}] -> ")
                        elif len(head.data) == 1:
                            linked_list.append(f"['{head.data}'] -> ")
                        else:
                            linked_list.append(f'["{head.data}"] -> ')
                    else:
                        linked_list.append(f"[{head.data}] -> ")
                    head: _singlyLinkedListNode | None = head.next
                if not self.circular:
                    linked_list.append("None (NULL)")
                else:
                    linked_list.insert(0, "> ")
                    if isinstance(head.data, str):
                        if len(head.data) == 0:
                            linked_list.append(f"[{head.data}]")
                        elif len(head.data) == 1:
                            linked_list.append(f"['{head.data}']")
                        else:
                            linked_list.append(f'["{head.data}"]')
                    else:
                        linked_list.append(f"[{head.data}]")
                    linked_list.append(" -")
                return "".join(linked_list)
            else:
                linked_list.append(
                    [
                        _white("Current Value"),
                        _white("Current Value ") + _green("@") + _white("ddress"),
                        _white("Next Value"),
                        _white("Next Value ") + _green("@") + _white("ddress"),
                    ]
                )
                if head.next == self._head:
                    linked_list.append(
                        [
                            (
                                _blue(f"{head.data}")
                                if not isinstance(head.data, str)
                                else (
                                    _blue(f"'{head.data}'")
                                    if len(head.data) == 1
                                    else (
                                        _blue(f'"{head.data}"')
                                        if len(head.data) > 1
                                        else f"{head.data}"
                                    )
                                )
                            ),
                            _cyan(
                                f"{bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head))}"
                            ),
                            (
                                _blue(f"{head.next.data}")
                                if not isinstance(head.next.data, str)
                                else (
                                    _blue(f"'{head.next.data}'")
                                    if len(head.next.data) == 1
                                    else (
                                        _blue(f'"{head.next.data}"')
                                        if len(head.next.data) > 1
                                        else f"{head.next.data}"
                                    )
                                )
                            ),
                            _cyan(
                                f"{bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next))}"
                            ),
                        ]
                    )
                elif not head.next:
                    linked_list.append(
                        [
                            (
                                _blue(f"{head.data}")
                                if not isinstance(head.data, str)
                                else (
                                    _blue(f"'{head.data}'")
                                    if len(head.data) == 1
                                    else (
                                        _blue(f'"{head.data}"')
                                        if len(head.data) > 1
                                        else f"{head.data}"
                                    )
                                )
                            ),
                            _cyan(
                                f"{bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head))}"
                            ),
                            f"{_blue('None')} {_green('(')}{_red('NULL')}{_green(')')}",
                            _yellow(
                                f"{bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next))} "
                            )
                            + _white("(")
                            + _red("nil")
                            + _white("/")
                            + (
                                _red("0b0")
                                if self._base == 2
                                else (
                                    _red("0o0")
                                    if self._base == 8
                                    else (
                                        _red("0") if self._base == 10 else _red("0x0")
                                    )
                                )
                            )
                            + _white(")"),
                        ]
                    )
                    head: _singlyLinkedListNode | None = head.next
                else:
                    linked_list.append(
                        [
                            (
                                _blue(f"{head.data}")
                                if not isinstance(head.data, str)
                                else (
                                    _blue(f"'{head.data}'")
                                    if len(head.data) == 1
                                    else (
                                        _blue(f'"{head.data}"')
                                        if len(head.data) > 1
                                        else f"{head.data}"
                                    )
                                )
                            ),
                            f"{_cyan(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))}",
                            (
                                _blue(f"{head.next.data}")
                                if not isinstance(head.next.data, str)
                                else (
                                    _blue(f"'{head.next.data}'")
                                    if len(head.next.data) == 1
                                    else (
                                        _blue(f'"{head.next.data}"')
                                        if len(head.next.data) > 1
                                        else f"{head.next.data}"
                                    )
                                )
                            ),
                            f"{_yellow(bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next)))}",
                        ]
                    )
                    head: _singlyLinkedListNode | None = head.next
                    while head and head.next != self._head:
                        first: str = (
                            f"{(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))}"
                        )
                        second: str = (
                            f"{bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next))}"
                            + (" " if head.next is None else "")
                        )
                        try:
                            after: str = (
                                _blue(f"{head.next.data}")
                                if not isinstance(head.next.data, str)
                                else (
                                    _blue(f"'{head.next.data}'")
                                    if len(head.next.data) == 1
                                    else (
                                        _blue(f'"{head.next.data}"')
                                        if len(head.next.data) > 1
                                        else f"{head.next.data}"
                                    )
                                )
                            )
                        except AttributeError as e4:
                            after: str = (
                                f"{_blue('None')} {_green('(')}{_red('NULL')}{_green(')')}"
                            )
                        linked_list.append(
                            [
                                (
                                    _blue(f"{head.data}")
                                    if not isinstance(head.data, str)
                                    else (
                                        _blue(f"'{head.data}'")
                                        if len(head.data) == 1
                                        else (
                                            _blue(f'"{head.data}"')
                                            if len(head.data) > 1
                                            else f"{head.data}"
                                        )
                                    )
                                ),
                                _yellow(first) if counter % 2 == 0 else _red(first),
                                after,
                                (
                                    (
                                        _red(second)
                                        + _white("(")
                                        + _green("nil")
                                        + _white("/")
                                        + (
                                            _green("0b0")
                                            if self._base == 2
                                            else (
                                                _green("0o0")
                                                if self._base == 8
                                                else (
                                                    _green("0")
                                                    if self._base == 10
                                                    else _green("0x0")
                                                )
                                            )
                                        )
                                        + _white(")")
                                        if second.endswith(" ")
                                        else _red(second)
                                    )
                                    if counter % 2 == 0
                                    else (
                                        _yellow(second)
                                        + _white("(")
                                        + _red("nil")
                                        + _white("/")
                                        + (
                                            _red("0b0")
                                            if self._base == 2
                                            else (
                                                _red("0o0")
                                                if self._base == 8
                                                else (
                                                    _red("0")
                                                    if self._base == 10
                                                    else _red("0x0")
                                                )
                                            )
                                        )
                                        + _white(")")
                                        if second.endswith(" ")
                                        else _yellow(second)
                                    )
                                ),
                            ]
                        )
                        counter += 1
                        head: _singlyLinkedListNode | None = head.next
                    if self.circular:
                        first: str = (
                            f"{(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))}"
                        )
                        second: str = (
                            f"{bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next))}"
                        )
                        linked_list.append(
                            [
                                (
                                    _blue(f"{head.data}")
                                    if not isinstance(head.data, str)
                                    else (
                                        _blue(f"'{head.data}'")
                                        if len(head.data) == 1
                                        else (
                                            _blue(f'"{head.data}"')
                                            if len(head.data) > 1
                                            else f"{head.data}"
                                        )
                                    )
                                ),
                                _yellow(first) if counter % 2 == 0 else _red(first),
                                (
                                    _blue(f"{head.next.data}")
                                    if not isinstance(head.next.data, str)
                                    else (
                                        _blue(f"'{head.next.data}'")
                                        if len(head.next.data) == 1
                                        else (
                                            _blue(f'"{head.next.data}"')
                                            if len(head.next.data) > 1
                                            else f"{head.next.data}"
                                        )
                                    )
                                ),
                                _cyan(second),
                            ]
                        )
                if not self.circular:
                    linked_list.append(
                        [
                            f"{_blue('None')} {_green('(')}{_red('NULL')}{_green(')')}",
                            (
                                (
                                    f"{_yellow(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))} "
                                    + _white("(")
                                    + _red("nil")
                                    + _white("/")
                                    + (
                                        _red("0b0")
                                        if self._base == 2
                                        else (
                                            _red("0o0")
                                            if self._base == 8
                                            else (
                                                _red("0")
                                                if self._base == 10
                                                else _red("0x0")
                                            )
                                        )
                                    )
                                    + _white(")")
                                )
                                if counter % 2 == 0
                                else (
                                    f"{_red(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))} "
                                    + _white("(")
                                    + _green("nil")
                                    + _white("/")
                                    + (
                                        _green("0b0")
                                        if self._base == 2
                                        else (
                                            _green("0o0")
                                            if self._base == 8
                                            else (
                                                _green("0")
                                                if self._base == 10
                                                else _green("0x0")
                                            )
                                        )
                                    )
                                    + _white(")")
                                )
                            ),
                            _BG_RED + " " * len("next value") + _RESET,
                            _BG_RED + " " * len("next value @ddress") + _RESET,
                        ]
                    )
                return tabulate(linked_list, headers="firstrow", tablefmt="fancy_grid")

    def insert(
        self: "singlyLinkedList",
        index: int,
        data: object,
    ) -> None:
        """Insert object before index."""
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if not self._head:
            new_node: _singlyLinkedListNode = _singlyLinkedListNode(data)
            self._head: _singlyLinkedListNode = new_node
            self.len += 1
            self._tail: _singlyLinkedListNode = new_node
            if self.circular:
                self._head.next = self._head
        else:
            if index == 0:
                new_node: _singlyLinkedListNode = _singlyLinkedListNode(data)
                self.len += 1
                new_node.next = self._head
                if self.circular:
                    self._tail.next = new_node
                self._head: object = new_node
            elif index >= self.len:
                new_node: _singlyLinkedListNode = _singlyLinkedListNode(data)
                self._tail.next = new_node
                if self.circular:
                    new_node.next = self._head
                self.len += 1
                self._tail: _singlyLinkedListNode = new_node
            else:
                if index < 0:
                    if index > -self.len:
                        index = self.len + index
                    else:
                        self.insert(0, data)
                        return
                new_node: _singlyLinkedListNode = _singlyLinkedListNode(data)
                prev_head: _singlyLinkedListNode = self.node(index - 1)
                new_node.next = prev_head.next
                prev_head.next = new_node
                self.len += 1

    def pop(self: "singlyLinkedList", index: int = -1) -> object:
        """Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range."""
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if not self._head:
            if not self.circular:
                raise IndexError("pop from empty non circular singly linked list")
            else:
                raise IndexError("pop from empty circular singly linked list")
        else:
            head: _singlyLinkedListNode = self._head
            if index == 0 or index == -self.len:
                old_head_value: object = self._head.data
                old_head: _singlyLinkedListNode = self._head
                if not self.circular:
                    self._head: _singlyLinkedListNode = head.next
                    if self.len == 1:
                        self._tail: None = None
                    self.len -= 1
                else:
                    if self._head != head.next:
                        self._tail.next = head.next
                        self._head: _singlyLinkedListNode = head.next
                    else:
                        self._head: None = None
                        self._tail: None = None
                    self.len -= 1
                del old_head
                return old_head_value
            elif index == -1 or index == self.len - 1:
                prev_current: _singlyLinkedListNode = self.node(index - 1)
                removed_node_value: object = prev_current.next.data
                removed_node: _singlyLinkedListNode = prev_current.next
                if self.circular:
                    prev_current.next = self._head
                else:
                    prev_current.next = None
                self.len -= 1
                self._tail: _singlyLinkedListNode = prev_current
                del removed_node
                return removed_node_value
            elif index > self.len - 1 or index < -self.len:
                raise IndexError("pop index out of range")
            else:
                prev_node: _singlyLinkedListNode = self.node(index - 1)
                removed_node_value: object = prev_node.next.data
                removed_node: _singlyLinkedListNode = prev_node.next
                prev_node.next = prev_node.next.next
                self.len -= 1
                del removed_node
                return removed_node_value

    def extend(
        self: "singlyLinkedList",
        extended_object: object,
    ) -> None:
        """Extend non circular/circular singly linked list by appending elements from the iterable."""
        if isinstance(extended_object, singlyLinkedList):
            first_last_node: _singlyLinkedListNode | None = self._tail
            second_first_node: _singlyLinkedListNode | None = extended_object._head
            for _ in range(extended_object.len):
                new_node: _singlyLinkedListNode = _singlyLinkedListNode(
                    second_first_node.data
                )
                first_last_node.next = new_node
                first_last_node: _singlyLinkedListNode = first_last_node.next
                second_first_node: _singlyLinkedListNode | None = second_first_node.next
            self.len += extended_object.len
            if self.circular:
                first_last_node.next = self._head
        else:
            extended_linked_list: singlyLinkedList = singlyLinkedList(extended_object)
            self.extend(extended_linked_list)

    def __getitem__(self: "singlyLinkedList", index: int) -> object:
        if not isinstance(index, slice):
            return self.node(index).data
        else:
            head: _singlyLinkedListNode | None = self._head
            new_list: list = []
            for _ in range(self.len):
                new_list.append(head.data)
                head: _singlyLinkedListNode | None = head.next
            try:
                new_list: list = new_list[index.start : index.stop : index.step]
                return singlyLinkedList(
                    new_list,
                    detail=self.detail,
                    circular=self.circular,
                    base=self._base,
                )
            except TypeError as e5:
                pass
            raise TypeError(
                "slice indices must be integers or None or have an __index__ method"
            )

    def to_doubly(self: "singlyLinkedList") -> "doublyLinkedList":
        return doublyLinkedList() + self

    def add(
        self: "singlyLinkedList",
        data: object,
    ) -> None:
        """To add in an organized manner"""
        if not self._head:
            self._head: _singlyLinkedListNode = _singlyLinkedListNode(data)
            self.len += 1
            self._tail: _singlyLinkedListNode = self._head
            if self.circular:
                self._head.next = self._head
        else:
            head: _singlyLinkedListNode = self._head
            prev_head: _singlyLinkedListNode | None = None
            for i in range(self.len):
                if type(head.data) != type(data):
                    raise TypeError(
                        f"'<' not supported between instances of '{type(head.data).__name__}' and '{type(data).__name__}'"
                    )
                else:
                    if not self.rev:
                        if data < head.data:
                            if i == 0 or i == self.len - 1:
                                self.insert(i, data)
                                break
                            else:
                                new_node: _singlyLinkedListNode = _singlyLinkedListNode(
                                    data
                                )
                                new_node.next = head
                                prev_head.next = new_node
                                self.len += 1
                                break
                        else:
                            prev_head: _singlyLinkedListNode = head
                            head = head.next
                    else:
                        if data > head.data:
                            if i == 0 or i == self.len - 1:
                                self.insert(i, data)
                                break
                            else:
                                new_node: _singlyLinkedListNode = _singlyLinkedListNode(
                                    data
                                )
                                new_node.next = head
                                prev_head.next = new_node
                                self.len += 1
                                break
                        else:
                            prev_head: _singlyLinkedListNode = head
                            head: _singlyLinkedListNode = head.next
            else:
                self.insert(self.len, data)

    def to_dict(self: "singlyLinkedList", node: bool = False) -> dict:
        head: _singlyLinkedListNode | None = self._head
        new_dict: dict = {}
        for _ in range(self.len):
            try:
                next_value: object = head.next.data
            except AttributeError as e6:
                next_value: None = None
            new_dict[head.data] = {
                "current value @ddress" if not node else "current node": (
                    (
                        (
                            bin(id(head))
                            if self._base == 2
                            else (
                                oct(id(head))
                                if self._base == 8
                                else id(head) if self._base == 10 else hex(id(head))
                            )
                        )
                    )
                    if not node
                    else head
                ),
                "next value" if not node else "next node value": next_value,
                "next value @ddress" if not node else "next node": (
                    (
                        bin(id(head.next))
                        if self._base == 2
                        else (
                            oct(id(head.next))
                            if self._base == 8
                            else (
                                id(head.next)
                                if self._base == 10
                                else hex(id(head.next))
                            )
                        )
                    )
                    if not node
                    else head.next
                ),
            }
            head: _singlyLinkedListNode | None = head.next
        return new_dict

    def reverse(self: "singlyLinkedList") -> None:
        head: _singlyLinkedListNode | None = self._head
        elements: list = []
        for _ in range(self.len):
            elements.append(head.data)
            head: _singlyLinkedListNode | None = head.next
        head: _singlyLinkedListNode | None = self._head
        for i in range(1, self.len + 1):
            head.data = elements[-i]
            head: _singlyLinkedListNode | None = head.next


class sll(singlyLinkedList):
    pass


class doublyLinkedList(_linkedList):
    @property
    def head(
        self: "doublyLinkedList",
    ) -> _doublyLinkedListNode:
        return self._head

    @head.setter
    def head(
        self: "doublyLinkedList",
        data: object,
    ) -> None:
        self._head: None = None
        if isinstance(data, doublyLinkedList):
            self._head: _doublyLinkedListNode | None = data._head
        elif isinstance(data, _doublyLinkedListNode):
            old_head: _doublyLinkedListNode = data
            old_self_head: _doublyLinkedListNode = data
            new_head: _doublyLinkedListNode = _doublyLinkedListNode(data.data)
            if self.circular:
                new_head.prev = data.prev
            self._head: _doublyLinkedListNode = new_head
            self.len += 1
            old_head: _doublyLinkedListNode | None = old_head.next
            while old_head and old_head != old_self_head:
                new_node: _doublyLinkedListNode = _doublyLinkedListNode(old_head.data)
                self.len += 1
                new_head.next = new_node
                new_node.prev = new_head
                new_head: _doublyLinkedListNode | None = new_head.next
                old_head: _doublyLinkedListNode | None = old_head.next
            if self.circular:
                new_node.next = self._head
            self._tail: _doublyLinkedListNode = new_node
        else:
            try:
                if len(data) > 0:
                    for i in data:
                        self.append(i)
            except TypeError as e7:
                if data is not None:
                    new_node: _doublyLinkedListNode = _doublyLinkedListNode(data)
                    self.len += 1
                    self._head: _doublyLinkedListNode = new_node
                    if self.circular:
                        new_node.next = new_node
                        new_node.prev = new_node
                    self._tail: _doublyLinkedListNode = new_node

    @head.deleter
    def head(self: "doublyLinkedList") -> None:
        self._head: None = None

    def set_circular(self: "doublyLinkedList") -> None:
        self._tail.next = self._head
        self._head.prev = self._tail
        self.circular: bool = True

    def set_non_circular(self: "doublyLinkedList") -> None:
        self._tail.next = None
        self._head.prev = None
        self.circular: bool = False

    def __add__(
        self: "doublyLinkedList",
        other: object,
    ) -> None:
        helper: list = []
        head1: _doublyLinkedListNode | None = self._head
        if isinstance(other, doublyLinkedList) or isinstance(other, singlyLinkedList):
            head2: _doublyLinkedListNode | None = other._head
        else:
            other: _doublyLinkedListNode = doublyLinkedList(other)
            head2: _doublyLinkedListNode = other._head
        for _ in range(self.len):
            helper.append(head1.data)
            head1: _doublyLinkedListNode | None = head1.next
        for _ in range(other.len):
            helper.append(head2.data)
            head2: _doublyLinkedListNode | None = head2.next
        return doublyLinkedList(helper, circular=other.circular)

    def __str__(self: "doublyLinkedList") -> str:
        """Return str(self)."""
        if not self._head:
            if not self.circular:
                raise TypeError("Empty non circular doubly linked list")
            else:
                raise TypeError("Empty circular doubly linked list")
        else:
            head: _doublyLinkedListNode = self._head
            linked_list: list = []
            counter: int = 0
            if not self.detail:
                if not self.circular:
                    linked_list.append("None (NULL) <- ")
                else:
                    linked_list.append("=> ")
                while head and head.next != self._head:
                    if not isinstance(head.data, str):
                        linked_list.append(
                            f"[{head.data}] " + ("<=> " if head.next else "-> ")
                        )
                    else:
                        if len(head.data) == 0:
                            linked_list.append(
                                f"[{head.data}] " + ("<=> " if head.next else "-> ")
                            )
                        elif len(head.data) == 1:
                            linked_list.append(
                                f"['{head.data}'] " + ("<=> " if head.next else "-> ")
                            )
                        else:
                            linked_list.append(
                                f'["{head.data}"] ' + ("<=> " if head.next else "-> ")
                            )
                    head: _doublyLinkedListNode | None = head.next
                if not self.circular:
                    if self.len > 1:
                        linked_list.append("None (NULL)")
                    else:
                        try:
                            if not isinstance(head.data, str):
                                linked_list.append(f"[{head.data}] -> None (NULL)")
                            else:
                                if len(head.data) == 0:
                                    linked_list.append(f"[{head.data}] -> None (NULL)")
                                elif len(head.data) == 1:
                                    linked_list.append(
                                        f"['{head.data}'] -> None (NULL)"
                                    )
                                else:
                                    linked_list.append(
                                        f'["{head.data}"] -> None (NULL)'
                                    )
                        except AttributeError as e8:
                            linked_list.append("None (NULL)")
                else:
                    if not isinstance(head.data, str):
                        linked_list.append(f"[{head.data}] <=")
                    else:
                        if len(head.data) == 0:
                            linked_list.append(f"[{head.data}] <=")
                        elif len(head.data) == 1:
                            linked_list.append(f"['{head.data}'] <=")
                        else:
                            linked_list.append(f'["{head.data}"] <=')
                return "".join(linked_list)
            else:
                linked_list.append(
                    [
                        _white("Previous Value"),
                        _white("Previous Value ") + _green("@") + _white("ddress"),
                        _white("Current Value"),
                        _white("Current Value ") + _green("@") + _white("ddress"),
                        _white("Next Value"),
                        _white("Next Value ") + _green("@") + _white("ddress"),
                    ]
                )
                if not self.circular:
                    linked_list.append(
                        [
                            _BG_RED + " " * len("previous value") + _RESET,
                            _BG_RED + " " * len("previous value @ddress") + _RESET,
                            f"{_blue('None')} {_green('(')}{_red('NULL')}{_green(')')}",
                            f"{_yellow(bin(id(None)) if self._base == 2 else oct(id(None)) if self._base == 8 else id(None) if self._base == 10 else hex(id(None)))} "
                            + _white("(")
                            + _red("nil")
                            + _white("/")
                            + (
                                _red("0b0")
                                if self._base == 2
                                else (
                                    _red("0o0")
                                    if self._base == 8
                                    else (
                                        _red("0") if self._base == 10 else _red("0x0")
                                    )
                                )
                            )
                            + _white(")"),
                            _BG_RED + " " * len("next value") + _RESET,
                            _BG_RED + " " * len("next value @ddress") + _RESET,
                        ]
                    )
                try:
                    helper: object = head.next.data
                except AttributeError as e9:
                    helper: None = None
                linked_list.append(
                    [
                        (
                            f"{_blue('None')} {_green('(')}{_red('NULL')}{_green(')')}"
                            if not head.prev
                            else (
                                _blue(f"{head.prev.data}")
                                if not isinstance(head.prev.data, str)
                                else (
                                    _blue(f"'{head.prev.data}'")
                                    if len(head.prev.data) == 1
                                    else (
                                        _blue(f'"{head.prev.data}"')
                                        if len(head.prev.data) > 1
                                        else f"{head.prev.data}"
                                    )
                                )
                            )
                        ),
                        f"{_yellow(bin(id(head.prev)) if self._base == 2 else oct(id(head.prev)) if self._base == 8 else id(head.prev) if self._base == 10 else hex(id(head.prev)))} "
                        + (
                            _white("(")
                            + _red("nil")
                            + _white("/")
                            + (
                                _red("0b0")
                                if self._base == 2
                                else (
                                    _red("0o0")
                                    if self._base == 8
                                    else (
                                        _red("0") if self._base == 10 else _red("0x0")
                                    )
                                )
                            )
                            + _white(")")
                            if head.prev is None
                            else ""
                        ),
                        (
                            _blue(f"{head.data}")
                            if not isinstance(head.data, str)
                            else (
                                _blue(f"'{head.data}'")
                                if len(head.data) == 1
                                else (
                                    _blue(f'"{head.data}"')
                                    if len(head.data) > 1
                                    else f"{head.data}"
                                )
                            )
                        ),
                        f"{_red(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))}",
                        (
                            _blue(
                                f"{helper}"
                                + f"{(_green(' (') + _red('NULL') + _green(')')) if not helper else ''}"
                            )
                            if not isinstance(helper, str)
                            else (
                                _blue(f"'{helper}'")
                                if len(head.next.data) == 1
                                else (
                                    _blue(f'"{helper}"')
                                    if len(head.next.data) > 1
                                    else f"{helper}"
                                )
                            )
                        ),
                        (
                            f"{_yellow(bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next)))} "
                            + (
                                _white("(")
                                + _red("nil")
                                + _white("/")
                                + (
                                    _red("0b0")
                                    if self._base == 2
                                    else (
                                        _red("0o0")
                                        if self._base == 8
                                        else (
                                            _red("0")
                                            if self._base == 10
                                            else _red("0x0")
                                        )
                                    )
                                )
                                + _white(")")
                                if head.next is None
                                else ""
                            )
                        ),
                    ]
                )
                head: _doublyLinkedListNode | None = head.next
                while head and head.next != self._head:
                    first: str = (
                        f"{bin(id(head.prev)) if self._base == 2 else oct(id(head.prev)) if self._base == 8 else id(head.prev) if self._base == 10 else hex(id(head.prev))}"
                    )
                    second: str = (
                        f"{(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))}"
                    )
                    last: str = (
                        f"{bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next))}"
                        + (" " if head.next is None else "")
                    )
                    try:
                        after: str = (
                            _blue(f"{head.next.data}")
                            if not isinstance(head.next.data, str)
                            else (
                                _blue(f"'{head.next.data}'")
                                if len(head.next.data) == 1
                                else (
                                    _blue(f'"{head.next.data}"')
                                    if len(head.next.data) > 1
                                    else f"{head.next.data}"
                                )
                            )
                        )
                    except AttributeError as e10:
                        after: str = (
                            f"{_blue('None')} {_green('(')}{_red('NULL')}{_green(')')}"
                        )
                    linked_list.append(
                        [
                            (
                                _blue(f"{head.prev.data}")
                                if not isinstance(head.prev.data, str)
                                else (
                                    _blue(f"'{head.prev.data}'")
                                    if len(head.prev.data) == 1
                                    else (
                                        _blue(f'"{head.prev.data}"')
                                        if len(head.prev.data) > 1
                                        else f"{head.prev.data}"
                                    )
                                )
                            ),
                            _red(first) if counter % 2 == 0 else _yellow(first),
                            (
                                _blue(f"{head.data}")
                                if not isinstance(head.data, str)
                                else (
                                    _blue(f"'{head.data}'")
                                    if len(head.data) == 1
                                    else (
                                        _blue(f'"{head.data}"')
                                        if len(head.data) > 1
                                        else f"{head.data}"
                                    )
                                )
                            ),
                            _yellow(second) if counter % 2 == 0 else _red(second),
                            after,
                            (
                                (
                                    _red(last)
                                    + _white("(")
                                    + _yellow("nil")
                                    + _white("/")
                                    + (
                                        _yellow("0b0")
                                        if self._base == 2
                                        else (
                                            _yellow("0o0")
                                            if self._base == 8
                                            else (
                                                _yellow("0")
                                                if self._base == 10
                                                else _yellow("0x0")
                                            )
                                        )
                                    )
                                    + _white(")")
                                    if last.endswith(" ")
                                    else _red(last)
                                )
                                if counter % 2 == 0
                                else (
                                    _yellow(last)
                                    + _white("(")
                                    + _red("nil")
                                    + _white("/")
                                    + (
                                        _red("0b0")
                                        if self._base == 2
                                        else (
                                            _red("0o0")
                                            if self._base == 8
                                            else (
                                                _red("0")
                                                if self._base == 10
                                                else _red("0x0")
                                            )
                                        )
                                    )
                                    + _white(")")
                                    if last.endswith(" ")
                                    else _yellow(last)
                                )
                            ),
                        ]
                    )
                    counter += 1
                    head: _doublyLinkedListNode | None = head.next
                if not self.circular:
                    linked_list.append(
                        [
                            _BG_RED + " " * len("previous value") + _RESET,
                            _BG_RED + " " * len("previous value @ddress") + _RESET,
                            f"{_blue('None')} {_green('(')}{_red('NULL')}{_green(')')}",
                            (
                                f"{_yellow(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))} "
                                + _white("(")
                                + _red("nil")
                                + _white("/")
                                + (
                                    _red("0b0")
                                    if self._base == 2
                                    else (
                                        _red("0o0")
                                        if self._base == 8
                                        else (
                                            _red("0")
                                            if self._base == 10
                                            else _red("0x0")
                                        )
                                    )
                                )
                                + _white(")")
                                if counter % 2 == 0
                                else f"{_red(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))} "
                                + _white("(")
                                + _yellow("nil")
                                + _white("/")
                                + (
                                    _yellow("0b0")
                                    if self._base == 2
                                    else (
                                        _yellow("0o0")
                                        if self._base == 8
                                        else (
                                            _yellow("0")
                                            if self._base == 10
                                            else _yellow("0x0")
                                        )
                                    )
                                )
                                + _white(")")
                            ),
                            _BG_RED + " " * len("next value") + _RESET,
                            _BG_RED + " " * len("next value @ddress") + _RESET,
                        ]
                    )
                else:
                    if self.len != 1:
                        first: str = (
                            f"{bin(id(head.prev)) if self._base == 2 else oct(id(head.prev)) if self._base == 8 else id(head.prev) if self._base == 10 else hex(id(head.prev))}"
                        )
                        second: str = (
                            f"{(bin(id(head)) if self._base == 2 else oct(id(head)) if self._base == 8 else id(head) if self._base == 10 else hex(id(head)))}"
                        )
                        last: str = (
                            f"{bin(id(head.next)) if self._base == 2 else oct(id(head.next)) if self._base == 8 else id(head.next) if self._base == 10 else hex(id(head.next))}"
                        )
                        after: str = (
                            _blue(f"{head.next.data}")
                            if not isinstance(head.next.data, str)
                            else (
                                _blue(f"'{head.next.data}'")
                                if len(head.next.data) == 1
                                else (
                                    _blue(f'"{head.next.data}"')
                                    if len(head.next.data) > 1
                                    else f"{head.next.data}"
                                )
                            )
                        )
                        linked_list.append(
                            [
                                (
                                    _blue(f"{head.prev.data}")
                                    if not isinstance(head.prev.data, str)
                                    else (
                                        _blue(f"'{head.prev.data}'")
                                        if len(head.prev.data) == 1
                                        else (
                                            _blue(f'"{head.prev.data}"')
                                            if len(head.prev.data) > 1
                                            else f"{head.prev.data}"
                                        )
                                    )
                                ),
                                _red(first) if counter % 2 == 0 else _yellow(first),
                                (
                                    _blue(f"{head.data}")
                                    if not isinstance(head.data, str)
                                    else (
                                        _blue(f"'{head.data}'")
                                        if len(head.data) == 1
                                        else (
                                            _blue(f'"{head.data}"')
                                            if len(head.data) > 1
                                            else f"{head.data}"
                                        )
                                    )
                                ),
                                _yellow(second) if counter % 2 == 0 else _red(second),
                                after,
                                _red(last) if counter % 2 == 0 else _yellow(last),
                            ]
                        )
                return tabulate(linked_list, headers="firstrow", tablefmt="fancy_grid")

    def copy(self: "doublyLinkedList") -> "doublyLinkedList":
        """Return a shallow copy of a non circular/circular doubly linked list."""
        return doublyLinkedList(
            self._head,
            detail=self.detail,
            circular=self.circular,
            base=self._base,
        )

    def __getitem__(self: "doublyLinkedList", index: int) -> object:
        if not isinstance(index, slice):
            return self.node(index).data
        else:
            head: _doublyLinkedListNode | None = self._head
            new_list: list = []
            for _ in range(self.len):
                new_list.append(head.data)
                head: _doublyLinkedListNode | None = head.next
            try:
                new_list: list = new_list[index.start : index.stop : index.step]
                return doublyLinkedList(
                    new_list,
                    detail=self.detail,
                    circular=self.circular,
                    base=self._base,
                )
            except TypeError as e11:
                pass
            raise TypeError(
                "slice indices must be integers or None or have an __index__ method"
            )

    def insert(
        self: "doublyLinkedList",
        index: int,
        data: object,
    ) -> None:
        """Insert object before index."""
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if not self._head:
            new_node: _doublyLinkedListNode = _doublyLinkedListNode(data)
            self._head: _doublyLinkedListNode = new_node
            self._tail: _doublyLinkedListNode = new_node
            self.len: int = 1
            if self.circular:
                new_node.next = new_node
                new_node.prev = new_node
        else:
            if index >= self.len:
                new_node: _doublyLinkedListNode = _doublyLinkedListNode(data)
                self._tail.next = new_node
                new_node.prev = self._tail
                self._tail: _doublyLinkedListNode = new_node
                if self.circular:
                    self._tail.next = self._head
                    self._head.prev = self._tail
                self.len += 1
            elif index <= -self.len or index == 0:
                new_node: _doublyLinkedListNode = _doublyLinkedListNode(data)
                new_node.next = self._head
                self._head.prev = new_node
                self._head: _doublyLinkedListNode = new_node
                if self.circular:
                    self._head.prev = self._tail
                    self._tail.next = self._head
                self.len += 1
            else:
                current: _doublyLinkedListNode = self.node(index)
                new_node: _doublyLinkedListNode = _doublyLinkedListNode(data)
                new_node.prev = current.prev
                new_node.next = current
                current.prev.next = new_node
                current.prev = new_node
                self.len += 1

    def pop(self: "doublyLinkedList", index: int = -1) -> object:
        """Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range."""
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if not self._head:
            if not self.circular:
                raise IndexError("pop from empty non circular doubly linked list")
            else:
                raise IndexError("pop from empty circular doubly linked list")
        else:
            if self.len > 1:
                if index == -1 or index == self.len - 1:
                    returned_value: object = self._tail.data
                    removed_node: _doublyLinkedListNode = self._tail
                    self._tail: _doublyLinkedListNode = self._tail.prev
                    if self.circular:
                        self._tail.next = self._head
                        self._head.prev = self._tail
                    else:
                        self._tail.next = None
                    self.len -= 1
                    del removed_node
                    return returned_value
                elif index == 0 or index == -self.len:
                    returned_value: object = self._head.data
                    removed_node: _doublyLinkedListNode = self._head
                    self._head: _doublyLinkedListNode = self._head.next
                    if self.circular:
                        self._head.prev = self._tail
                        self._tail.next = self._head
                    else:
                        self._head.prev = None
                    self.len -= 1
                    del removed_node
                    return returned_value
                elif index >= self.len or index < -self.len:
                    raise IndexError("pop index out of range")
                else:
                    current: _doublyLinkedListNode = self.node(index)
                    returned_value: object = current.data
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    self.len -= 1
                    del current
                    return returned_value
            else:
                if index == 0 or index == -1:
                    returned_value: object = self._head.data
                    removed_node: _doublyLinkedListNode = self._head
                    self._head: None = None
                    self._tail: None = None
                    self.len: int = 0
                    del removed_node
                    return returned_value
                else:
                    raise IndexError("pop index out of range")

    def extend(
        self: "doublyLinkedList",
        extended_object: object,
    ) -> None:
        """Extend non circular/circular doubly linked list by appending elements from the iterable."""
        if isinstance(extended_object, doublyLinkedList):
            first_last_node: _doublyLinkedListNode | None = self._tail
            second_first_node: _doublyLinkedListNode | None = extended_object._head
            for _ in range(extended_object.len):
                new_node: _doublyLinkedListNode = _doublyLinkedListNode(
                    second_first_node.data
                )
                first_last_node.next = new_node
                new_node.prev = first_last_node
                first_last_node: _doublyLinkedListNode = first_last_node.next
                second_first_node: _doublyLinkedListNode | None = second_first_node.next
            self.len += extended_object.len
            if self.circular:
                first_last_node.next = self._head
                self._head.prev = first_last_node
        else:
            extended_linked_list: doublyLinkedList = doublyLinkedList(extended_object)
            self.extend(extended_linked_list)

    def to_singly(self: "doublyLinkedList") -> singlyLinkedList:
        return singlyLinkedList() + self

    def add(
        self: "doublyLinkedList",
        data: object,
    ) -> None:
        """To add in an organized manner"""
        if not self._head:
            self._head: _doublyLinkedListNode = _doublyLinkedListNode(data)
            self.len += 1
            self._tail: _doublyLinkedListNode = self._head
            if self.circular:
                self._head.next = self._head
                self._head.prev = self._head
        else:
            head: _doublyLinkedListNode = self._head
            for i in range(self.len):
                if type(head.data) != type(data):
                    raise TypeError(
                        f"'<' not supported between instances of '{type(head.data).__name__}' and '{type(data).__name__}'"
                    )
                else:
                    if not self.rev:
                        if data < head.data:
                            if i == 0 or i == self.len - 1:
                                self.insert(i, data)
                                break
                            else:
                                new_node: _doublyLinkedListNode = _doublyLinkedListNode(
                                    data
                                )
                                new_node.next = head
                                new_node.prev = head.prev
                                head.prev.next = new_node
                                head.prev = new_node
                                self.len += 1
                                break
                        else:
                            head: _doublyLinkedListNode | None = head.next
                    else:
                        if data > head.data:
                            if i == 0 or i == self.len - 1:
                                self.insert(i, data)
                                break
                            else:
                                new_node: _doublyLinkedListNode = _doublyLinkedListNode(
                                    data
                                )
                                new_node.next = head
                                new_node.prev = head.prev
                                head.prev.next = new_node
                                head.prev = new_node
                                self.len += 1
                                break
                        else:
                            head: _doublyLinkedListNode | None = head.next
            else:
                self.insert(self.len, data)

    def to_dict(self: "doublyLinkedList", node: bool = False) -> dict:
        head: _doublyLinkedListNode | None = self._head
        new_dict: dict = {}
        for _ in range(self.len):
            try:
                next_value: object = head.next.data
            except AttributeError as e12:
                next_value: None = None
            new_dict[head.data] = {
                "prev value" if not node else "prev node value": (
                    (head.prev.data if head.prev is not None else None)
                    if not node
                    else head.prev.data if head.prev is not None else None
                ),
                "prev value @ddress" if not node else "prev node @ddress": (
                    (
                        bin(id(head.prev))
                        if self._base == 2
                        else (
                            oct(id(head.prev))
                            if self._base == 8
                            else (
                                id(head.prev)
                                if self._base == 10
                                else hex(id(head.prev))
                            )
                        )
                    )
                    if not node
                    else head.prev
                ),
                "current value @ddress" if not node else "current node": (
                    (
                        (
                            bin(id(head))
                            if self._base == 2
                            else (
                                oct(id(head))
                                if self._base == 8
                                else id(head) if self._base == 10 else hex(id(head))
                            )
                        )
                    )
                    if not node
                    else head
                ),
                "next value" if not node else "next node value": next_value,
                "next value @ddress" if not node else "next node": (
                    (
                        bin(id(head.next))
                        if self._base == 2
                        else (
                            oct(id(head.next))
                            if self._base == 8
                            else (
                                id(head.next)
                                if self._base == 10
                                else hex(id(head.next))
                            )
                        )
                    )
                    if not node
                    else head.next
                ),
            }
            head: _doublyLinkedListNode | None = head.next
        return new_dict

    def reverse(self: "doublyLinkedList") -> None:
        head: _doublyLinkedListNode = self._head
        tail: _doublyLinkedListNode = self._tail
        for _ in range(self.len // 2):
            head.data, tail.data = tail.data, head.data
            head: _doublyLinkedListNode | None = head.next
            tail: _doublyLinkedListNode | None = tail.prev


class dll(doublyLinkedList):
    pass


class orthogonalLinkedListNode:
    def __init__(
        self: "orthogonalLinkedListNode",
        data: object,
    ) -> None:
        self.prev: None = None
        self.next: None = None
        self.up: None = None
        self.down: None = None
        self.data: object = data

    def prev_node(self: "orthogonalLinkedListNode") -> "orthogonalLinkedListNode":
        return self.prev

    def next_node(self: "orthogonalLinkedListNode") -> "orthogonalLinkedListNode":
        return self.next

    def up_node(self: "orthogonalLinkedListNode") -> "orthogonalLinkedListNode":
        return self.up

    def down_node(self: "orthogonalLinkedListNode") -> "orthogonalLinkedListNode":
        return self.down

    def get_data(
        self: "orthogonalLinkedListNode",
    ) -> object:
        return self.data


class orthogonalLinkedList:
    def __init__(
        self: "orthogonalLinkedList",
        data: list,
        *,
        circular: bool = False,
        detail: bool = False,
    ) -> None:
        self.circular: bool = circular
        self.detail: bool = detail
        self.head: list = data

    @property
    def tail(
        self: "orthogonalLinkedList",
    ) -> orthogonalLinkedListNode:
        return self._head[-1][-1]

    def __len__(self: "orthogonalLinkedList") -> int:
        return len(self._head) * len(self._head[0])

    @property
    def shape(self: "orthogonalLinkedList") -> tuple[int, int]:
        return (len(self._head), len(self._head[0]))

    def __getitem__(self: "orthogonalLinkedList", index: int):
        values: list = []
        for i in range(len(self._head[index])):
            values.append(self._head[index][i].data)
        return values

    def __setitem__(
        self: "orthogonalLinkedList",
        index: int,
        value: object,
    ) -> None:
        if len(value) == len(self._head[index]):
            for i in range(len(self._head[index])):
                self._head[index][i].data = value[i]
        else:
            raise TypeError("columns len not the same")

    @property
    def head(
        self: "orthogonalLinkedList",
    ) -> orthogonalLinkedListNode:
        return self._head[0][0]

    @head.setter
    def head(self: "orthogonalLinkedList", data: list) -> None:
        if isinstance(data, list):
            som: int = 0
            for i in range(len(data)):
                try:
                    som += len(data[i])
                except TypeError as e13:
                    raise TypeError("just 2D array(list) allowed") from None
            if som % len(data):
                raise TypeError("2D array(list) columns is not with the same length")
            else:
                data[0][0] = orthogonalLinkedListNode(data[0][0])
                for i in range(len(data)):
                    for j in range(len(data[i])):
                        if i == 0:
                            try:
                                data[i][j + 1] = orthogonalLinkedListNode(
                                    data[i][j + 1]
                                )
                            except IndexError as e14:
                                pass
                        try:
                            data[i + 1][j] = orthogonalLinkedListNode(data[i + 1][j])
                        except IndexError as e15:
                            pass
                        if i == 0:
                            if j == 0:
                                try:
                                    data[i][j].next = data[i][j + 1]
                                except IndexError as e16:
                                    pass
                            elif j == len(data[i]) - 1:
                                data[i][j].prev = data[i][j - 1]
                            else:
                                data[i][j].prev = data[i][j - 1]
                                data[i][j].next = data[i][j + 1]
                            try:
                                data[i][j].down = data[i + 1][j]
                            except IndexError as e17:
                                pass
                        elif i == len(data) - 1:
                            if j == 0:
                                try:
                                    data[i][j].next = data[i][j + 1]
                                except IndexError as e18:
                                    pass
                            elif j == len(data[i]) - 1:
                                data[i][j].prev = data[i][j - 1]
                            else:
                                data[i][j].prev = data[i][j - 1]
                                data[i][j].next = data[i][j + 1]
                            data[i][j].up = data[i - 1][j]
                        else:
                            if j == 0:
                                try:
                                    data[i][j].next = data[i][j + 1]
                                except IndexError as e19:
                                    pass
                            elif j == len(data[i]) - 1:
                                data[i][j].prev = data[i][j - 1]
                            else:
                                data[i][j].prev = data[i][j - 1]
                                data[i][j].next = data[i][j + 1]
                            data[i][j].up = data[i - 1][j]
                            data[i][j].down = data[i + 1][j]
                if self.circular:
                    for i in range(len(data)):
                        for j in range(len(data[i])):
                            if data[i][j].prev is None:
                                data[i][j].prev = data[i][-1]
                            if data[i][j].next is None:
                                data[i][j].next = data[i][0]
                            if data[i][j].up is None:
                                data[i][j].up = data[-1][j]
                            if data[i][j].down is None:
                                data[i][j].down = data[0][j]
                self._head: list = data
        else:
            raise TypeError("just array(list) data type allowed")

    def __str__(self: "orthogonalLinkedList") -> str:
        linked_list: list = []
        if not self.detail:
            if not self.circular:
                linked_list.append(["None"] * (len(self._head[0]) + 2))
                linked_list[0][0], linked_list[0][-1] = "", ""
            for i in range(len(self._head)):
                helper: list = []
                if not self.circular:
                    helper.append("None")
                for j in range(len(self._head[i])):
                    if not isinstance(self._head[i][j].data, str):
                        helper.append(self._head[i][j].data)
                    else:
                        if len(self._head[i][j].data) == 0:
                            helper.append(self._head[i][j].data)
                        elif len(self._head[i][j].data) == 1:
                            helper.append(f"'{self._head[i][j].data}'")
                        else:
                            helper.append(f'"{self._head[i][j].data}"')
                if not self.circular:
                    helper.append("None")
                linked_list.append(helper)
            if not self.circular:
                linked_list.append(["None"] * (len(self._head[0]) + 2))
                linked_list[-1][0], linked_list[-1][-1] = "", ""
            return tabulate(linked_list, tablefmt="fancy_grid")
        else:
            counter: int = 0
            linked_list.append(
                [
                    _white("Up"),
                    _white("Up ") + _green("@"),
                    _white("Previous"),
                    _white("Previous ") + _green("@"),
                    _white("Current"),
                    _white("Current ") + _green("@"),
                    _white("Down"),
                    _white("Down ") + _green("@"),
                    _white("Next"),
                    _white("Next ") + _green("@"),
                ]
            )
            for i in range(len(self._head)):
                for j in range(len(self._head[i])):
                    try:
                        if not isinstance(self._head[i][j].prev.data, str):
                            prev_data: str = _blue(f"{self._head[i][j].prev.data}")
                        else:
                            if len(self._head[i][j].prev.data) == 0:
                                prev_data: str = self._head[i][j].prev.data
                            elif len(self._head[i][j].prev.data) == 1:
                                prev_data: str = _blue(
                                    f"'{self._head[i][j].prev.data}'"
                                )
                            else:
                                prev_data: str = _blue(
                                    f'"{self._head[i][j].prev.data}"'
                                )
                    except AttributeError as e20:
                        prev_data: str = _blue("None")
                    try:
                        if not isinstance(self._head[i][j].next.data, str):
                            next_data: str = _blue(f"{self._head[i][j].next.data}")
                        else:
                            if len(self._head[i][j].next.data) == 0:
                                next_data: str = self._head[i][j].next.data
                            elif len(self._head[i][j].next.data) == 1:
                                next_data: str = _blue(
                                    f"'{self._head[i][j].next.data}'"
                                )
                            else:
                                next_data: str = _blue(
                                    f'"{self._head[i][j].next.data}"'
                                )
                    except AttributeError as e21:
                        next_data: str = _blue("None")
                    try:
                        if not isinstance(self._head[i][j].up.data, str):
                            up_data: str = _blue(f"{self._head[i][j].up.data}")
                        else:
                            if len(self._head[i][j].up.data) == 0:
                                up_data: str = self._head[i][j].up.data
                            elif len(self._head[i][j].up.data) == 1:
                                up_data: str = _blue(f"'{self._head[i][j].up.data}'")
                            else:
                                up_data: str = _blue(f'"{self._head[i][j].up.data}"')
                    except AttributeError as e22:
                        up_data: str = _blue("None")
                    try:
                        if not isinstance(self._head[i][j].down.data, str):
                            down_data: str = _blue(f"{self._head[i][j].down.data}")
                        else:
                            if len(self._head[i][j].down.data) == 0:
                                down_data: str = self._head[i][j].down.data
                            elif len(self._head[i][j].down.data) == 1:
                                down_data: str = _blue(
                                    f"'{self._head[i][j].down.data}'"
                                )
                            else:
                                down_data: str = _blue(
                                    f'"{self._head[i][j].down.data}"'
                                )
                    except AttributeError as e23:
                        down_data: str = _blue("None")
                    current_data: str = (
                        _blue(f"{self._head[i][j].data}")
                        if not isinstance(self._head[i][j].data, str)
                        else (
                            self._head[i][j].data
                            if len(self._head[i][j].data) == 0
                            else (
                                _blue(f"'{self._head[i][j].data}'")
                                if len(self._head[i][j].data) == 1
                                else _blue(f'"{self._head[i][j].data}"')
                            )
                        )
                    )
                    up_add: str = (
                        (
                            _yellow(f"{hex(id(self._head[i][j].up))}")
                            if counter % 2 == 0
                            else _red(f"{hex(id(self._head[i][j].up))}")
                        )
                        if self._head[i][j].up is not None
                        else _cyan(f"{hex(id(self._head[i][j].up))}")
                    )
                    counter += 1
                    prev_add: str = (
                        (
                            _yellow(f"{hex(id(self._head[i][j].prev))}")
                            if counter % 2 == 0
                            else _red(f"{hex(id(self._head[i][j].prev))}")
                        )
                        if self._head[i][j].prev is not None
                        else _cyan(f"{hex(id(self._head[i][j].prev))}")
                    )
                    counter += 1
                    current_add: str = (
                        (
                            _yellow(f"{hex(id(self._head[i][j]))}")
                            if counter % 2 == 0
                            else _red(f"{hex(id(self._head[i][j]))}")
                        )
                        if self._head[i][j] is not None
                        else _cyan(f"{hex(id(self._head[i][j]))}")
                    )
                    counter += 1
                    down_add: str = (
                        (
                            _yellow(f"{hex(id(self._head[i][j].down))}")
                            if counter % 2 == 0
                            else _red(f"{hex(id(self._head[i][j].down))}")
                        )
                        if self._head[i][j].down is not None
                        else _cyan(f"{hex(id(self._head[i][j].down))}")
                    )
                    counter += 1
                    next_add: str = (
                        (
                            _yellow(f"{hex(id(self._head[i][j].next))}")
                            if counter % 2 == 0
                            else _red(f"{hex(id(self._head[i][j].next))}")
                        )
                        if self._head[i][j].next is not None
                        else _cyan(f"{hex(id(self._head[i][j].next))}")
                    )
                    counter += 1
                    linked_list.append(
                        [
                            up_data,
                            up_add,
                            prev_data,
                            prev_add,
                            current_data,
                            current_add,
                            down_data,
                            down_add,
                            next_data,
                            next_add,
                        ]
                    )
            return tabulate(linked_list, headers="firstrow", tablefmt="fancy_grid")

    @property
    def node(self: "orthogonalLinkedList") -> list:
        return self._head


class oll(orthogonalLinkedList):
    pass


def _main() -> None:
    print("linkedit")


if __name__ == "__main__":
    _main()
