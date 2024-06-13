from typing import List


def test_remove():
    l: List[str] = [1, 2, 3]

    l.remove(1)
    l.insert(0, 4)
    assert len(l) == 3
    assert l == [4, 2, 3]
