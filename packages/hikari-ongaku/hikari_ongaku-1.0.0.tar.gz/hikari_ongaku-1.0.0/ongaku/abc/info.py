"""
Info ABC's.

The info abstract classes.
"""

from __future__ import annotations

import abc
import typing

if typing.TYPE_CHECKING:
    import datetime

__all__ = (
    "Version",
    "Git",
    "Plugin",
    "Info",
)


class Info(abc.ABC):
    """
    Information.

    All of the Info Version information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#info-response)
    """

    @property
    @abc.abstractmethod
    def version(self) -> Version:
        """The version of this Lavalink server."""
        ...

    @property
    @abc.abstractmethod
    def build_time(self) -> datetime.datetime:
        """The datetime object of when this Lavalink jar was built."""
        ...

    @property
    @abc.abstractmethod
    def git(self) -> Git:
        """The git information of this Lavalink server."""
        ...

    @property
    @abc.abstractmethod
    def jvm(self) -> str:
        """The JVM version this Lavalink server runs on."""
        ...

    @property
    @abc.abstractmethod
    def lavaplayer(self) -> str:
        """The Lavaplayer version being used by this server."""
        ...

    @property
    @abc.abstractmethod
    def source_managers(self) -> typing.Sequence[str]:
        """The enabled source managers for this server."""
        ...

    @property
    @abc.abstractmethod
    def filters(self) -> typing.Sequence[str]:
        """The enabled filters for this server."""
        ...

    @property
    @abc.abstractmethod
    def plugins(self) -> typing.Sequence[Plugin]:
        """The enabled plugins for this server."""
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Info):
            return False

        if self.version != other.version:
            return False

        if self.build_time != other.build_time:
            return False

        if self.git != other.git:
            return False

        if self.jvm != other.jvm:
            return False

        if self.lavaplayer != other.lavaplayer:
            return False

        if self.source_managers != other.source_managers:
            return False

        if self.filters != other.filters:
            return False

        if self.plugins != other.plugins:
            return False

        return True


class Version(abc.ABC):
    """
    Version information.

    All information, about the version of lavalink that is running.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#version-object)
    """

    @property
    @abc.abstractmethod
    def semver(self) -> str:
        """The full version string of this Lavalink server."""
        ...

    @property
    @abc.abstractmethod
    def major(self) -> int:
        """The major version of this Lavalink server."""
        ...

    @property
    @abc.abstractmethod
    def minor(self) -> int:
        """The minor version of this Lavalink server."""
        ...

    @property
    @abc.abstractmethod
    def patch(self) -> int:
        """The patch version of this Lavalink server."""
        ...

    @property
    @abc.abstractmethod
    def pre_release(self) -> str:
        """The pre-release version according to semver as a `.` separated list of identifiers."""
        ...

    @property
    @abc.abstractmethod
    def build(self) -> str | None:
        """The build metadata according to semver as a `.` separated list of identifiers."""
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return False

        if self.semver != other.semver:
            return False

        if self.major != other.major:
            return False

        if self.minor != other.minor:
            return False

        if self.patch != other.patch:
            return False

        if self.pre_release != other.pre_release:
            return False

        if self.build != other.build:
            return False

        return True


class Git(abc.ABC):
    """
    Git information.

    All of the information about the lavalink git information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#git-object)
    """

    @property
    @abc.abstractmethod
    def branch(self) -> str:
        """The branch this Lavalink server was built on."""
        ...

    @property
    @abc.abstractmethod
    def commit(self) -> str:
        """The commit this Lavalink server was built on."""
        ...

    @property
    @abc.abstractmethod
    def commit_time(self) -> datetime.datetime:
        """The datetime object of when the commit was created."""
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Git):
            return False

        if self.branch != other.branch:
            return False

        if self.commit != other.commit:
            return False

        if self.commit_time != other.commit_time:
            return False

        return True


class Plugin(abc.ABC):
    """
    Plugin information.

    All of the Information about the currently loaded plugins.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#plugin-object)
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The name of the plugin."""
        ...

    @property
    @abc.abstractmethod
    def version(self) -> str:
        """The version of the plugin."""
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Plugin):
            return False

        if self.name != other.name:
            return False

        if self.version != other.version:
            return False

        return True


# MIT License

# Copyright (c) 2023-present MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
