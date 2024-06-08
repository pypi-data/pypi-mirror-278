import pytest

from eventum_content_manager.validators import (validate_csv_filename,
                                                validate_jinja_filename,
                                                validate_yaml_filename)


@pytest.mark.parametrize(
    ('filename',),
    [
        ('template.jinja', ),
        ('template.json.jinja', ),
        ('test_template.json.jinja', ),
        ('test_template_2.json.jinja', ),
    ]
)
def test_validate_jinja_filename_valid(filename):
    validate_jinja_filename(filename)


@pytest.mark.parametrize(
    ('filename',),
    [
        ('template.json', ),
        ('test template.jinja', ),
        ('template', ),
        ('', ),
    ]
)
def test_validate_jinja_filename_invalid(filename):
    with pytest.raises(ValueError):
        validate_jinja_filename(filename)


@pytest.mark.parametrize(
    ('filename',),
    [
        ('config.yaml', ),
        ('config.yml', ),
        ('test_config.yml', ),
        ('test_config2.yaml', ),
    ]
)
def test_validate_yaml_filename_valid(filename):
    validate_yaml_filename(filename)


@pytest.mark.parametrize(
    ('filename',),
    [
        ('config.toml', ),
        ('test config.yml', ),
        ('config', ),
        ('', ),
    ]
)
def test_validate_yaml_filename_invalid(filename):
    with pytest.raises(ValueError):
        validate_yaml_filename(filename)


@pytest.mark.parametrize(
    ('filename',),
    [
        ('sample.csv', ),
        ('test_sample.csv', ),
        ('test_sample2.csv', ),
    ]
)
def test_validate_csv_filename_valid(filename):
    validate_csv_filename(filename)


@pytest.mark.parametrize(
    ('filename',),
    [
        ('sample.xls', ),
        ('test sample.csv', ),
        ('sample', ),
        ('', ),
    ]
)
def test_validate_csv_filename_invalid(filename):
    with pytest.raises(ValueError):
        validate_csv_filename(filename)
