from uploader.domain import TestRun
from uploader.main import create_parser
from uploader.zipper import find_files


def test_find_files():
    parser = create_parser()
    args = parser.parse_args(['-tr', r'.*\.xml'])

    test_run = TestRun(args=args)
    result = find_files(test_run, 'tests/fixtures/test_results/')
    elements = [
        'tests/fixtures/test_results/pydriller_testresults.xml',
        'tests/fixtures/test_results/examples/pydriller_testresults.xml',
        'tests/fixtures/test_results/examples1/pydriller_testresults1.xml',
        'tests/fixtures/test_results/examples1/examples2/' +
        'pydriller_testresults2.xml',
    ]
    for el in elements:
        assert el in result
    assert len(elements) == len(result)


def test_find_files_exclude_dir():
    parser = create_parser()
    args = parser.parse_args(['-tr', r'.*\.xml'])

    test_run = TestRun(args=args)
    result = find_files(test_run, 'tests/fixtures/test_results_exclude_dirs/')
    elements = [
        'tests/fixtures/test_results_exclude_dirs/pydriller_testresults.xml',
    ]
    for el in elements:
        assert el in result
    assert len(elements) == len(result)


def test_find_files_with_config():
    parser = create_parser()
    args = parser.parse_args(['-tr', r'.*\.xml', '-cf', '.testpulse.yaml'])

    test_run = TestRun(args=args)
    result = find_files(test_run, 'tests/fixtures/test_results/')
    elements = [
        'tests/fixtures/test_results/.testpulse.yaml',
        'tests/fixtures/test_results/pydriller_testresults.xml',
        'tests/fixtures/test_results/examples/pydriller_testresults.xml',
        'tests/fixtures/test_results/examples1/pydriller_testresults1.xml',
        'tests/fixtures/test_results/examples1/examples2/' +
        'pydriller_testresults2.xml',
    ]
    for el in elements:
        assert el in result
    assert len(elements) == len(result)
