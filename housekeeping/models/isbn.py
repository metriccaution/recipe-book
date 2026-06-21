def validate_isbn(raw: str) -> str:
    """Validate and normalise an ISBN string.

    Accepts ISBN-10 or ISBN-13 (with or without hyphens/spaces).
    Always returns a normalised ISBN-13 string (digits only, no separators).
    Raises ValueError if the input is not a valid ISBN.
    """
    cleaned = _clean(raw)

    if len(cleaned) == 10:
        _check_isbn10(cleaned)
        cleaned = _isbn10_to_isbn13(cleaned)
    elif len(cleaned) == 13:
        _check_isbn13(cleaned)
    else:
        raise ValueError(
            f"Invalid ISBN {raw!r}: expected 10 or 13 digits, got {len(cleaned)}."
        )

    return cleaned


def _clean(raw: str) -> str:
    """Strip whitespace and hyphens; upper-case so 'x' == 'X' for ISBN-10."""
    return raw.replace("-", "").replace(" ", "").upper()


def _check_isbn10(s: str) -> None:
    """Raise ValueError if s is not a valid ISBN-10 checksum."""
    if not all(c.isdigit() for c in s[:9]):
        raise ValueError(f"Invalid ISBN-10 {s!r}: first 9 characters must be digits.")
    if s[9] not in "0123456789X":
        raise ValueError(
            f"Invalid ISBN-10 {s!r}: check character must be a digit or 'X'."
        )

    total = sum((10 - i) * (10 if c == "X" else int(c)) for i, c in enumerate(s))
    if total % 11 != 0:
        raise ValueError(f"Invalid ISBN-10 {s!r}: checksum failed.")


def _check_isbn13(s: str) -> None:
    """Raise ValueError if s is not a valid ISBN-13 checksum."""
    if not s.isdigit():
        raise ValueError(f"Invalid ISBN-13 {s!r}: all 13 characters must be digits.")

    weights = [1 if i % 2 == 0 else 3 for i in range(13)]
    total = sum(w * int(c) for w, c in zip(weights, s))
    if total % 10 != 0:
        raise ValueError(f"Invalid ISBN-13 {s!r}: checksum failed.")


def _isbn10_to_isbn13(s: str) -> str:
    """Convert a validated ISBN-10 string to ISBN-13."""
    body = "978" + s[:9]
    weights = [1 if i % 2 == 0 else 3 for i in range(12)]
    total = sum(w * int(c) for w, c in zip(weights, body))
    check = (10 - (total % 10)) % 10
    return body + str(check)
