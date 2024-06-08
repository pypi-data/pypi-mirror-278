# Copyright 2021 Pex project contributors.
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import absolute_import

import glob
import json
import os
import subprocess
from contextlib import contextmanager
from textwrap import dedent

import pytest

from pex.atomic_directory import atomic_directory
from pex.common import temporary_dir
from pex.interpreter import PythonInterpreter
from pex.typing import TYPE_CHECKING
from pex.venv.virtualenv import Virtualenv
from testing import PY310, data, ensure_python_interpreter, make_env, run_pex_command

if TYPE_CHECKING:
    from typing import Any, Callable, ContextManager, Iterator, Optional, Tuple


@pytest.fixture(scope="session")
def pexpect_timeout():
    # type: () -> int

    # The default here of 5 provides enough margin for PyPy which has slow startup.
    return int(os.environ.get("_PEX_PEXPECT_TIMEOUT", "5"))


@pytest.fixture(scope="session")
def is_pytest_xdist(worker_id):
    # type: (str) -> bool
    return worker_id != "master"


@pytest.fixture(scope="session")
def shared_integration_test_tmpdir(
    tmpdir_factory,  # type: Any
    is_pytest_xdist,  # type: bool
):
    # type: (...) -> str
    tmpdir = str(tmpdir_factory.getbasetemp())

    # We know pytest-xdist creates a subdir under the pytest session tmp dir for each worker; so we
    # go up a level to lock a directory all workers can use.
    if is_pytest_xdist:
        tmpdir = os.path.dirname(tmpdir)

    return os.path.join(tmpdir, "shared_integration_test_tmpdir")


@pytest.fixture(scope="session")
def pex_bdist(
    pex_project_dir,  # type: str
    shared_integration_test_tmpdir,  # type: str
):
    # type: (...) -> str
    pex_bdist_chroot = os.path.join(shared_integration_test_tmpdir, "pex_bdist_chroot")
    wheels_dir = os.path.join(pex_bdist_chroot, "wheels_dir")
    with atomic_directory(pex_bdist_chroot) as chroot:
        if not chroot.is_finalized():
            pex_pex = os.path.join(chroot.work_dir, "pex.pex")
            run_pex_command(
                args=[pex_project_dir, "-o", pex_pex, "--include-tools"]
            ).assert_success()
            extract_dir = os.path.join(chroot.work_dir, "wheels_dir")
            subprocess.check_call(
                args=[pex_pex, "repository", "extract", "-f", extract_dir],
                env=make_env(PEX_TOOLS=True),
            )
    wheels = glob.glob(os.path.join(wheels_dir, "pex-*.whl"))
    assert 1 == len(wheels)
    return wheels[0]


@pytest.fixture
def tmp_workdir():
    # type: () -> Iterator[str]
    cwd = os.getcwd()
    with temporary_dir() as tmpdir:
        os.chdir(tmpdir)
        try:
            yield os.path.realpath(tmpdir)
        finally:
            os.chdir(cwd)


@pytest.fixture(scope="session")
def mitmdump_venv(shared_integration_test_tmpdir):
    # type: (str) -> Virtualenv
    mitmproxy_venv_dir = os.path.join(shared_integration_test_tmpdir, "mitmproxy")
    with atomic_directory(mitmproxy_venv_dir) as atomic_venvdir:
        if not atomic_venvdir.is_finalized():
            python = ensure_python_interpreter(PY310)
            Virtualenv.create_atomic(
                venv_dir=atomic_venvdir,
                interpreter=PythonInterpreter.from_binary(python),
                force=True,
            )
            mitmproxy_lock = data.path("locks", "mitmproxy.lock.json")
            subprocess.check_call(
                args=[
                    python,
                    "-m",
                    "pex.cli",
                    "venv",
                    "create",
                    "-d",
                    atomic_venvdir.work_dir,
                    "--lock",
                    mitmproxy_lock,
                ]
            )
    return Virtualenv(mitmproxy_venv_dir)


@pytest.fixture
def run_proxy(
    mitmdump_venv,  # type: Virtualenv
    tmpdir,  # type: Any
):
    # type: (...) -> Callable[[Optional[str]], ContextManager[Tuple[int, str]]]
    confdir = os.path.join(str(tmpdir), "confdir")
    messages = os.path.join(str(tmpdir), "messages")
    addon = os.path.join(str(tmpdir), "addon.py")
    with open(addon, "w") as fp:
        fp.write(
            dedent(
                """\
                import json

                from mitmproxy import ctx


                def running() -> None:
                    port = ctx.master.addons.get("proxyserver").listen_addrs()[0][1]
                    with open({msg_channel!r}, "w") as fp:
                        json.dump({{"port": port}}, fp)
                """.format(
                    msg_channel=messages
                )
            )
        )

    @contextmanager
    def _run_proxy(
        proxy_auth=None,  # type: Optional[str]
    ):
        # type: (...) -> Iterator[Tuple[int, str]]
        os.mkfifo(messages)
        args = [
            mitmdump_venv.interpreter.binary,
            mitmdump_venv.bin_path("mitmdump"),
            "--set",
            "confdir={confdir}".format(confdir=confdir),
            "-p",
            "0",
            "-s",
            addon,
        ]
        if proxy_auth:
            args.extend(["--proxyauth", proxy_auth])
        proxy_process = subprocess.Popen(args)
        try:
            with open(messages, "r") as fp:
                data = json.load(fp)
            yield data["port"], os.path.join(confdir, "mitmproxy-ca.pem")
        finally:
            proxy_process.kill()
            os.unlink(messages)

    return _run_proxy


@pytest.fixture
def clone(tmpdir):
    # type: (Any) -> Callable[[str, str], str]

    def _clone(
        git_project_url,  # type: str
        commit,  # type: str
    ):
        project_dir = os.path.join(str(tmpdir), "project")

        subprocess.check_call(args=["git", "clone", git_project_url, project_dir])
        subprocess.check_call(
            args=["git", "config", "advice.detachedHead", "false"], cwd=project_dir
        )
        subprocess.check_call(args=["git", "checkout", commit], cwd=project_dir)
        return project_dir

    return _clone
