import os
import tempfile
from uuid import uuid4

import pytest

from eventum_content_manager.manage import (ContentManagementError,
                                            delete_app_config,
                                            delete_compose_config,
                                            delete_csv_sample, delete_template,
                                            delete_time_pattern,
                                            get_app_config_filenames,
                                            get_compose_config_filenames,
                                            get_csv_sample_filenames,
                                            get_template_filenames,
                                            get_time_pattern_filenames,
                                            load_app_config,
                                            load_compose_config,
                                            load_csv_sample, load_template,
                                            load_time_pattern, save_app_config,
                                            save_compose_config,
                                            save_csv_sample, save_template,
                                            save_time_pattern)

TESTS_DIR = '.tests'
TEMP_DIR = tempfile.gettempdir()


@pytest.fixture
def time_pattern_config() -> dict:
    return {'config_data': 'test'}


@pytest.fixture
def time_pattern_config_rel_path() -> str:
    filename = f'{uuid4()}.yml'.replace('-', '_')
    return os.path.join(TESTS_DIR, filename)


@pytest.fixture
def time_pattern_config_abs_path() -> str:
    filename = f'{uuid4()}.yml'.replace('-', '_')
    return os.path.join(TEMP_DIR, filename)


def test_operate_time_pattern(
    time_pattern_config,
    time_pattern_config_rel_path,
    time_pattern_config_abs_path
):
    # relative path
    save_time_pattern(
        config=time_pattern_config,
        path=time_pattern_config_rel_path,
        overwrite=True
    )
    assert time_pattern_config_rel_path in get_time_pattern_filenames()

    # raise on forbidden overwrite
    with pytest.raises(ContentManagementError):
        save_time_pattern(
            config=time_pattern_config,
            path=time_pattern_config_rel_path,
            overwrite=False
        )

    loaded_config = load_time_pattern(time_pattern_config_rel_path)
    assert loaded_config == time_pattern_config

    delete_time_pattern(time_pattern_config_rel_path)
    assert time_pattern_config_rel_path not in get_time_pattern_filenames()

    # absolute path
    save_time_pattern(
        config=time_pattern_config,
        path=time_pattern_config_abs_path,
        overwrite=True
    )
    assert os.path.exists(time_pattern_config_abs_path)

    loaded_config = load_time_pattern(time_pattern_config_abs_path)
    assert loaded_config == time_pattern_config

    delete_time_pattern(time_pattern_config_abs_path)
    assert not os.path.exists(time_pattern_config_abs_path)


@pytest.fixture
def template_content() -> str:
    return 'render me'


@pytest.fixture
def template_rel_path() -> str:
    filename = f'{uuid4()}.jinja'.replace('-', '_')
    return os.path.join(TESTS_DIR, filename)


@pytest.fixture
def template_abs_path() -> str:
    filename = f'{uuid4()}.jinja'.replace('-', '_')
    return os.path.join(TEMP_DIR, filename)


def test_operate_template(
    template_content,
    template_rel_path,
    template_abs_path
):
    # relative path
    save_template(
        content=template_content,
        path=template_rel_path,
        overwrite=True
    )
    assert template_rel_path in get_template_filenames()

    # raise on forbidden overwrite
    with pytest.raises(ContentManagementError):
        save_template(
            content=template_content,
            path=template_rel_path,
            overwrite=False
        )

    loaded_template = load_template(template_rel_path)
    assert loaded_template == template_content

    delete_template(template_rel_path)
    assert template_rel_path not in get_template_filenames()

    # absolute path
    save_template(
        content=template_content,
        path=template_abs_path,
        overwrite=True
    )
    assert os.path.exists(template_abs_path)

    loaded_template = load_template(template_abs_path)
    assert loaded_template == template_content

    delete_template(template_abs_path)
    assert not os.path.exists(template_abs_path)


@pytest.fixture
def app_config() -> dict:
    return {'config_data': 'test'}


@pytest.fixture
def app_config_rel_path() -> str:
    filename = f'{uuid4()}.yml'.replace('-', '_')
    return os.path.join(TESTS_DIR, filename)


@pytest.fixture
def app_config_abs_path() -> str:
    filename = f'{uuid4()}.yml'.replace('-', '_')
    return os.path.join(TEMP_DIR, filename)


def test_operate_app_config(
    app_config,
    app_config_rel_path,
    app_config_abs_path
):
    # relative path
    save_app_config(
        config=app_config,
        path=app_config_rel_path,
        overwrite=True
    )
    assert app_config_rel_path in get_app_config_filenames()

    # raise on forbidden overwrite
    with pytest.raises(ContentManagementError):
        save_app_config(
            config=app_config,
            path=app_config_rel_path,
            overwrite=False
        )

    loaded_config = load_app_config(app_config_rel_path)
    assert loaded_config == app_config

    delete_app_config(app_config_rel_path)
    assert app_config_rel_path not in get_app_config_filenames()

    # absolute path
    save_app_config(
        config=app_config,
        path=app_config_abs_path,
        overwrite=True
    )
    assert os.path.exists(app_config_abs_path)

    loaded_config = load_app_config(app_config_abs_path)
    assert loaded_config == app_config

    delete_app_config(app_config_abs_path)
    assert not os.path.exists(app_config_abs_path)


@pytest.fixture
def csv_sample() -> tuple[tuple[str, ...], ...]:
    return tuple(
        (
            ('1', 'nick', 'nick@example.com'),
        )
    )


@pytest.fixture
def csv_sample_rel_path() -> str:
    filename = f'{uuid4()}.csv'.replace('-', '_')
    return os.path.join(TESTS_DIR, filename)


@pytest.fixture
def csv_sample_abs_path() -> str:
    filename = f'{uuid4()}.csv'.replace('-', '_')
    return os.path.join(TEMP_DIR, filename)


def test_operate_csv_sample(
    csv_sample,
    csv_sample_rel_path,
    csv_sample_abs_path
):
    # relative path
    save_csv_sample(
        sample=csv_sample,
        path=csv_sample_rel_path,
        overwrite=True
    )
    assert csv_sample_rel_path in get_csv_sample_filenames()

    # raise on forbidden overwrite
    with pytest.raises(ContentManagementError):
        save_csv_sample(
            sample=csv_sample,
            path=csv_sample_rel_path,
            overwrite=False
        )

    loaded_sample = load_csv_sample(csv_sample_rel_path)
    assert loaded_sample == csv_sample

    delete_csv_sample(csv_sample_rel_path)
    assert csv_sample_rel_path not in get_csv_sample_filenames()

    # absolute path
    save_csv_sample(
        sample=csv_sample,
        path=csv_sample_abs_path,
        overwrite=True
    )
    assert os.path.exists(csv_sample_abs_path)

    loaded_sample = load_csv_sample(csv_sample_abs_path)
    assert loaded_sample == csv_sample

    delete_csv_sample(csv_sample_abs_path)
    assert not os.path.exists(csv_sample_abs_path)


@pytest.fixture
def compose_config() -> dict:
    return {'config_data': 'test'}


@pytest.fixture
def compose_config_rel_path() -> str:
    filename = f'{uuid4()}.yml'.replace('-', '_')
    return os.path.join(TESTS_DIR, filename)


@pytest.fixture
def compose_config_abs_path() -> str:
    filename = f'{uuid4()}.yml'.replace('-', '_')
    return os.path.join(TEMP_DIR, filename)


def test_operate_compose_config(
    compose_config,
    compose_config_rel_path,
    compose_config_abs_path
):
    # relative path
    save_compose_config(
        config=compose_config,
        path=compose_config_rel_path,
        overwrite=True
    )
    assert compose_config_rel_path in get_compose_config_filenames()

    # raise on forbidden overwrite
    with pytest.raises(ContentManagementError):
        save_compose_config(
            config=compose_config,
            path=compose_config_rel_path,
            overwrite=False
        )

    loaded_config = load_compose_config(compose_config_rel_path)
    assert loaded_config == compose_config

    delete_compose_config(compose_config_rel_path)
    assert compose_config_rel_path not in get_compose_config_filenames()

    # absolute path
    save_compose_config(
        config=compose_config,
        path=compose_config_abs_path,
        overwrite=True
    )
    assert os.path.exists(compose_config_abs_path)

    loaded_config = load_compose_config(compose_config_abs_path)
    assert loaded_config == compose_config

    delete_compose_config(compose_config_abs_path)
    assert not os.path.exists(compose_config_abs_path)
