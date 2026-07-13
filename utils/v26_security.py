import random
from typing import List

_s1 = [chr(c) for c in [118, 50, 54, 88, 75, 55, 112, 81, 110, 68]]
_s2 = [chr(c) for c in [77, 57, 118, 50, 67, 120, 76, 52, 114, 84, 97, 81, 56, 107, 80]]

SALT1 = "".join(_s1)
SALT2 = "".join(_s2)


if len(SALT1) != 10 or len(SALT2) != 15:
    raise RuntimeError("invalid V26 session salts")


def _positions(length: int, count: int, seed: str) -> List[int]:
    if length < 0 or count <= 0:
        raise ValueError("invalid V26 session layout")
    rng = random.Random(seed)
    return sorted(rng.sample(range(length + count), count))


def v26_protect(obf: str) -> str:
    if not isinstance(obf, str):
        raise TypeError("V26 session must be a string")
    minimum_length = len(SALT1) + len(SALT2) + 1
    if len(obf) < minimum_length:
        raise ValueError(
            "Invalid V26 session format. Please generate a new session using "
            "@v26_session_maker_bot and copy the complete session string."
        )

    pos2 = _positions(len(obf) - len(SALT2), len(SALT2), seed=SALT2)
    lst = list(obf)
    for idx in reversed(pos2):
        lst.pop(idx)
    s1 = "".join(lst)

    pos1 = _positions(len(s1) - len(SALT1), len(SALT1), seed=SALT1)
    lst = list(s1)
    for idx in reversed(pos1):
        lst.pop(idx)
    return "".join(lst)
