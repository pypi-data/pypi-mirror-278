import os
from string import ascii_letters, digits
from typing import Iterable


def _validate_filename(
    filename: str,
    extensions: Iterable[str],
    allowed_symbols: str
) -> None:
    """Check if provided `filename` is in format <basename>.<extension>
    where basename consists only of `allowed_symbols`. Raise
    `ValueError` on validation failure.
    """
    if not filename:
        raise ValueError(
            'File name cannot be empty'
        )

    filename, ext = os.path.splitext(filename)

    restricted_symbols = set(filename) - set(allowed_symbols)
    if restricted_symbols:
        raise ValueError(
            'Some restricted symbols encountered in the filename: '
            f'{restricted_symbols}'
        )

    if ext not in extensions:
        raise ValueError(f'Only {extensions} extensions are allowed')


def validate_yaml_filename(filename: str) -> None:
    """Check if provided `filename` is a proper yaml filename. Raise
    `ValueError` on validation failure.
    """
    _validate_filename(
        filename=filename,
        extensions=['.yml', '.yaml'],
        allowed_symbols=ascii_letters + digits + '_'
    )


def validate_jinja_filename(filename: str) -> None:
    """Check if provided `filename` is a proper jinja filename. Raise
    `ValueError` on validation failure.
    """
    _validate_filename(
        filename=filename,
        extensions=['.jinja'],
        allowed_symbols=ascii_letters + digits + '_.'
    )


def validate_csv_filename(filename: str) -> None:
    """Check if provided `filename` is a proper csv filename. Raise
    `ValueError` on validation failure.
    """
    _validate_filename(
        filename=filename,
        extensions=['.csv'],
        allowed_symbols=ascii_letters + digits + '_'
    )
