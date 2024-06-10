import logging
import os
from argparse import Namespace
from typing import Dict, Optional, Pattern

from uploader.exceptions import NotInCI
from uploader.utils import is_local_dev

logger = logging.getLogger(__name__)


class TestRun:
    def __init__(self, args: Namespace) -> None:
        self.args = args

    # Testpulse custom variables. Can be passed via args or via env variables.
    # REQUIRED: should throw if not found in args or env variables
    @property
    def token(self) -> str:
        if self.args.token:
            return self.args.token
        if 'TESTPULSE_TOKEN' in os.environ:
            return os.environ['TESTPULSE_TOKEN']
        raise NotInCI("TESTPULSE_TOKEN")

    @property
    def test_results_regex(self) -> Optional[Pattern[str]]:
        return self.args.test_results_regex

    @property
    def coverage_results_regex(self) -> Optional[Pattern[str]]:
        return self.args.coverage_results_regex

    # NOT REQUIRED: in this case it's fine to return None
    @property
    def language_version(self) -> Optional[str]:
        if self.args.language_version:
            return self.args.language_version
        if 'TP_LANG_VERSION' in os.environ:
            return os.environ['TP_LANG_VERSION']
        return None

    @property
    def test_framework_version(self) -> Optional[str]:
        if self.args.test_framework_version:
            return self.args.test_framework_version
        if 'TP_TEST_FRAME_VERSION' in os.environ:
            return os.environ['TP_TEST_FRAME_VERSION']
        return None

    @property
    def config_file(self) -> Optional[str]:
        if self.args.config_file:
            return self.args.config_file
        if 'TP_CONFIG_FILE' in os.environ:
            return os.environ['TP_CONFIG_FILE']
        return None

    @property
    def test_type(self) -> Optional[str]:
        if self.args and self.args.test_type:
            return self.args.test_type
        if 'TP_TEST_TYPE' in os.environ:
            return os.environ['TP_TEST_TYPE']
        return None

    # The next ones are taken from GH default env variables.
    # They should always be != None. Otherwise it means we are not in CI.
    # https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables
    @property
    def repository(self) -> str:
        if 'GITHUB_REPOSITORY' in os.environ:
            # The ENV variable contains both owner and repo (like "octocat/Hello-World").
            # We need to strip the owner and only keep the repo ("Hello-World").
            owner_and_repo = os.environ['GITHUB_REPOSITORY']
            owner = f"{self.organization}/"
            if owner not in owner_and_repo:
                # VERY STRANGE scenario! Maybe the ENV variable changed?
                raise Exception(f"The ENV variable 'GITHUB_REPOSITORY' ({owner_and_repo}) "
                                f"does not contain the owner ({self.organization}).")
            return owner_and_repo.split(owner)[1]
        raise NotInCI("GITHUB_REPOSITORY")

    @property
    def operating_system(self) -> Optional[str]:
        if self.args.operating_system:
            return self.args.operating_system
        if 'RUNNER_OS' in os.environ:
            return os.environ['RUNNER_OS']
        raise NotInCI("RUNNER_OS")

    @property
    def commit(self) -> str:
        if 'GITHUB_SHA' in os.environ:
            return os.environ['GITHUB_SHA']
        raise NotInCI("GITHUB_SHA")

    @property
    def ref(self) -> str:
        if 'GITHUB_REF' in os.environ:
            return os.environ['GITHUB_REF']
        raise NotInCI("GITHUB_REF")

    @property
    def github_run_id(self) -> str:
        if 'GITHUB_RUN_ID' in os.environ:
            return os.environ['GITHUB_RUN_ID']
        raise NotInCI("GITHUB_RUN_ID")

    @property
    def organization(self) -> str:
        if 'GITHUB_REPOSITORY_OWNER' in os.environ:
            return os.environ['GITHUB_REPOSITORY_OWNER']
        raise NotInCI("GITHUB_REPOSITORY_OWNER")

    @property
    def test_configuration(self) -> Dict[str, str]:
        tc = {}
        if self.language_version:
            tc['languageVersion'] = self.language_version
        if self.operating_system:
            tc['operatingSystem'] = self.operating_system
        if self.test_framework_version:
            tc['testFrameworkVersion'] = self.test_framework_version

        return tc

    @property
    def branch(self) -> Optional[str]:
        if 'GITHUB_REF' in os.environ:
            if 'refs/heads/' in os.environ['GITHUB_REF']:
                return os.environ['GITHUB_REF'].replace('refs/heads/', '')
            return None
        raise NotInCI("GITHUB_REF")

    @property
    def pull_request_number(self) -> Optional[int]:
        if 'GITHUB_REF' in os.environ:
            if 'refs/pull/' in os.environ['GITHUB_REF']:
                github_ref = os.environ['GITHUB_REF']

                try:
                    pr_number = github_ref.replace('refs/pull/', '').replace('/merge', '')
                    return int(pr_number)
                except ValueError:
                    logger.error("Testpulse identified this as a PR, but could not get the PR number.")
                    return None
            return None
        if is_local_dev():
            return None
        raise NotInCI("GITHUB_REF")


class TokenVerification:
    @property
    def token(self) -> str:
        if 'TESTPULSE_TOKEN' in os.environ:
            return os.environ['TESTPULSE_TOKEN']
        raise NotInCI("TESTPULSE_TOKEN")
