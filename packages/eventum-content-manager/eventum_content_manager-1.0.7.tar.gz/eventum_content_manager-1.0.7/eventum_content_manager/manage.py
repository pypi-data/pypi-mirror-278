import os
import pathlib
from glob import glob
from typing import Any, Callable, Iterable, TypeVar

import yaml

from eventum_content_manager.validators import (validate_csv_filename,
                                                validate_jinja_filename,
                                                validate_yaml_filename)

USER_HOME_DIR = pathlib.Path.home().absolute()
CONTENT_BASE_DIR = os.path.join(USER_HOME_DIR, '.eventum', 'content')

TIME_PATTERNS_DIR = os.path.join(CONTENT_BASE_DIR, 'time_patterns')
CSV_SAMPLES_DIR = os.path.join(CONTENT_BASE_DIR, 'samples')
EVENT_TEMPLATES_DIR = os.path.join(CONTENT_BASE_DIR, 'templates')
APPLICATION_CONFIGS_DIR = os.path.join(CONTENT_BASE_DIR, 'configs')
COMPOSE_CONFIGS_DIR = os.path.join(CONTENT_BASE_DIR, 'compose')


# For read functions we should initialize structure.
# Creation of subdirectories in save functions is handled on their own.
for dir in [
    TIME_PATTERNS_DIR, CSV_SAMPLES_DIR,
    EVENT_TEMPLATES_DIR, APPLICATION_CONFIGS_DIR
]:
    os.makedirs(dir, exist_ok=True)


class ContentManagementError(Exception):
    """Base exception for all content manipulation errors."""


def _get_filenames(root_dir: str, patterns: list[str]) -> list[str]:
    """Get all relative paths of currently existing files that
    match the provided patterns. Paths are relative to `root_dir`.
    The filenames search is recursive.
    """
    return [
        file for pattern in patterns
        for file in glob(
            pathname=pattern,
            root_dir=root_dir,
            recursive=True,
            include_hidden=True
        )
    ]


def get_time_pattern_filenames() -> list[str]:
    """Get all relative paths of currently existing time patterns in
    content directory. Paths are relative to time patterns directory.
    """
    return _get_filenames(
        root_dir=TIME_PATTERNS_DIR,
        patterns=['**/*.yml', '**/*.yaml']
    )


def get_template_filenames() -> list[str]:
    """Get all relative paths of currently existing templates in
    content directory. Paths are relative to templates directory.
    """
    return _get_filenames(
        root_dir=EVENT_TEMPLATES_DIR,
        patterns=['**/*.jinja']
    )


def get_csv_sample_filenames() -> list[str]:
    """Get all relative paths of currently existing samples in
    content directory. Paths are relative to samples directory.
    """
    return _get_filenames(
        root_dir=CSV_SAMPLES_DIR,
        patterns=['**/*.csv']
    )


def get_app_config_filenames() -> list[str]:
    """Get all relative paths of currently existing app configuration
    files in content directory. Paths are relative to app configs
    directory.
    """
    return _get_filenames(
        root_dir=APPLICATION_CONFIGS_DIR,
        patterns=['**/*.yml', '**/*.yaml']
    )


def get_compose_config_filenames() -> list[str]:
    """Get all relative paths of currently existing compose
    configuration files in content directory. Paths are relative to
    compose configs directory.
    """
    return _get_filenames(
        root_dir=COMPOSE_CONFIGS_DIR,
        patterns=['**/*.yml', '**/*.yaml']
    )


def _save_object(
    content: Any,
    path: str,
    root_dir: str | None = None,
    filename_validator: Callable[[str], None] | None = None,
    formatter: Callable[[Any], str] | None = None,
    overwrite: bool = False
) -> None:
    """Save `content` to specified `path`. If path is  relative then
    `root_dir` must be provided and it is used as base directory for
    `path`. If `filename_validator` is provided then it's called with
    filename part of `path`. If file is already exists under specified
    location and `overwrite` is `False`, then exception is raised. If
    `formatter` is provided it is called with `content` parameter and
    returned value is used as new content that will be written to file.
    Parameter `formatter` must be provided if `content` parameter is
    not of class `str`.
    """
    if not os.path.isabs(path):
        if root_dir is None:
            raise ContentManagementError(
                'Parameter `root_dir` must be provided when relative '
                '`path` is used'
            )
        path = os.path.join(root_dir, path)

    base_path, filename = os.path.split(path)

    if filename_validator is not None:
        try:
            filename_validator(filename)
        except ValueError as e:
            raise ContentManagementError(str(e)) from e

    if overwrite is False and os.path.exists(path):
        raise ContentManagementError(
            'File already exists in specified location'
        )

    os.makedirs(base_path, exist_ok=True)

    if formatter is not None:
        try:
            content = formatter(content)
        except Exception as e:
            raise ContentManagementError(f'Failed to format content: {e}')
    elif not isinstance(content, str):
        raise ContentManagementError(
            'Parameter `formatter` must be provided when `content` '
            'in not of class string'
        )

    try:
        with open(path, 'w') as f:
            f.write(content)
    except OSError as e:
        raise ContentManagementError(str(e)) from e


def save_time_pattern(
    config: dict,
    path: str,
    overwrite: bool = False
) -> None:
    """Save time pattern in specified path. If path is relative then it
    is saved in content directory.
    """
    _save_object(
        content=config,
        path=path,
        root_dir=TIME_PATTERNS_DIR,
        filename_validator=validate_yaml_filename,
        formatter=yaml.dump,
        overwrite=overwrite
    )


def save_template(
    content: str,
    path: str,
    overwrite: bool = False
) -> None:
    """Save template in specified path. If path is relative then it
    is saved in content directory.
    """
    _save_object(
        content=content,
        path=path,
        root_dir=EVENT_TEMPLATES_DIR,
        filename_validator=validate_jinja_filename,
        overwrite=overwrite
    )


def save_csv_sample(
    sample: Iterable[Iterable[str]],
    path: str,
    overwrite: bool = False
) -> None:
    """Save csv sample in specified path. If path is relative then it
    is saved in content directory.
    """
    _save_object(
        content=sample,
        path=path,
        root_dir=CSV_SAMPLES_DIR,
        filename_validator=validate_csv_filename,
        formatter=lambda sample: os.linesep.join(
            [','.join(row) for row in sample]
        ),
        overwrite=overwrite
    )


def save_app_config(
    config: dict,
    path: str,
    overwrite: bool = False
) -> None:
    """Save app configuration in specified path. If path is relative
    then it is saved in content directory.
    """
    _save_object(
        content=config,
        path=path,
        root_dir=APPLICATION_CONFIGS_DIR,
        filename_validator=validate_yaml_filename,
        formatter=yaml.dump,
        overwrite=overwrite
    )


def save_compose_config(
    config: dict,
    path: str,
    overwrite: bool = False
) -> None:
    """Save compose configuration in specified path. If path is
    relative then it is saved in content directory.
    """
    _save_object(
        content=config,
        path=path,
        root_dir=COMPOSE_CONFIGS_DIR,
        filename_validator=validate_yaml_filename,
        formatter=yaml.dump,
        overwrite=overwrite
    )


LoaderT = TypeVar('LoaderT')


def _load_object(
    path: str,
    root_dir: str | None = None,
    loader: Callable[[str], LoaderT] | None = None
) -> LoaderT | str:
    """Load object from specified `path`. If path is relative then
    `root_dir` must be provided and it is used as base directory for
    `path`. If `loader` is provided then it is called on content read
    from the file and result of call used as returned value. Otherwise
    content of a file as string is returned.
    """
    if not os.path.isabs(path):
        if root_dir is None:
            raise ContentManagementError(
                'Parameter `root_dir` must be provided when relative '
                '`path` is used'
            )
        path = os.path.join(root_dir, path)

    try:
        with open(path) as f:
            content = f.read()
    except OSError as e:
        raise ContentManagementError(str(e)) from e

    if loader is None:
        return content

    try:
        return loader(content)
    except Exception as e:
        raise ContentManagementError(f'Failed to load content: {e}')


def load_time_pattern(path: str) -> Any:
    """Load specified time pattern. If path is relative then it is
    loaded from content directory.
    """
    return _load_object(
        path=path,
        root_dir=TIME_PATTERNS_DIR,
        loader=lambda content: yaml.load(content, yaml.SafeLoader)
    )


def load_template(path: str) -> str:
    """Load specified template. If path is relative then it is
    loaded from content directory.
    """
    return _load_object(
        path=path,
        root_dir=EVENT_TEMPLATES_DIR
    )


def load_csv_sample(
    path: str,
    delimiter: str = ','
) -> tuple[tuple[str, ...], ...]:
    """Load specified csv sample and return it as list of tuples. If
    path is relative then it is loaded from content directory.
    """
    def csv_loader(content: str) -> tuple[tuple[str, ...], ...]:
        return tuple(
            [
                tuple(line.split(delimiter))
                for line in content.strip().split(os.linesep)
            ]
        )

    return _load_object(    # type: ignore[return-value]
        path=path,
        root_dir=CSV_SAMPLES_DIR,
        loader=csv_loader
    )


def load_app_config(path: str) -> Any:
    """Load specified application config. If path is relative then it
    is loaded from content directory.
    """
    return _load_object(
        path=path,
        root_dir=APPLICATION_CONFIGS_DIR,
        loader=lambda content: yaml.load(content, yaml.SafeLoader)
    )


def load_compose_config(path: str) -> Any:
    """Load specified compose config. If path is relative then it
    is loaded from content directory.
    """
    return _load_object(
        path=path,
        root_dir=COMPOSE_CONFIGS_DIR,
        loader=lambda content: yaml.load(content, yaml.SafeLoader)
    )


def _delete_object(path: str, root_dir: str | None = None) -> None:
    """Delete file under specified path. If path is relative then
    `root_dir` must be provided and it is used as base directory for
    `path`.
    """
    if not os.path.isabs(path):
        if root_dir is None:
            raise ContentManagementError(
                'Parameter `root_dir` must be provided when relative '
                '`path` is used'
            )
        path = os.path.join(root_dir, path)

    if not os.path.exists(path):
        raise ContentManagementError(
            f'Failed to delete: no such file "{path}"'
        )

    os.remove(path)


def delete_time_pattern(path: str) -> None:
    """Delete specified time pattern. If path is relative then it will
    be deleted from content directory.
    """
    _delete_object(
        path=path,
        root_dir=TIME_PATTERNS_DIR
    )


def delete_template(path: str) -> None:
    """Delete specified template. If path is relative then it will be
    deleted from content directory.
    """
    _delete_object(
        path=path,
        root_dir=EVENT_TEMPLATES_DIR
    )


def delete_csv_sample(path: str) -> None:
    """Delete specified csv sample. If path is relative then it will be
    deleted from content directory.
    """
    _delete_object(
        path=path,
        root_dir=CSV_SAMPLES_DIR
    )


def delete_app_config(path: str) -> None:
    """Delete specified app config. If path is relative then it will be
    deleted from content directory.
    """
    _delete_object(
        path=path,
        root_dir=APPLICATION_CONFIGS_DIR
    )


def delete_compose_config(path: str) -> None:
    """Delete specified compose config. If path is relative then it
    will be deleted from content directory.
    """
    _delete_object(
        path=path,
        root_dir=COMPOSE_CONFIGS_DIR
    )
