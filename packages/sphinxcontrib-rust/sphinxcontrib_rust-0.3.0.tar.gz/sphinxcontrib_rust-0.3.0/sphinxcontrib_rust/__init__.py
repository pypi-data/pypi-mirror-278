"""Init module for the extension with the ``setup`` function used by Sphinx"""

import json
import os
from dataclasses import asdict, dataclass
from importlib.metadata import version
import subprocess
from shutil import which
from typing import Any, Mapping

import sphinx.config
from sphinx.application import Sphinx
from sphinx.util import logging

from sphinxcontrib_rust.domain import RustDomain

__PKG_NAME = "sphinxcontrib_rust"
__VERSION__ = version(__PKG_NAME)
__LOGGER = logging.getLogger(__PKG_NAME)


@dataclass
class CrateConfiguration:
    """Dataclass for the crate configuration.

    This is the Python equivalent of :rust:struct:`sphinx-rustdocgen::Configuration`.
    It is serialized as JSON and shared with the Rust executable.
    """

    crate_name: str
    src_dir: str
    doc_dir: str
    format: str = "rst"
    visibility: str = "pub"
    force: bool = False

    @classmethod
    def from_sphinx_config(
        cls, sphinx_config: sphinx.config.Config
    ) -> tuple[str, dict[str, "CrateConfiguration"]]:
        """Extract the configuration for the crates from the Sphinx configuration.

        The function mainly checks whether a given configuration option is global
        or per crate and creates the appropriate configuration for each crate. If
        all options are global, all crates will have the same configuration other
        than their ``src_dir`` field.

        Args:
            :config: The Sphinx configuration.

        Returns:
            A tuple of the path of the executable for generating the docs and a dict
            of crate name to crate configuration mapping.
        """

        executable = sphinx_config.rust_rustdocgen or which("sphinx-rustdocgen")
        if executable is None:
            raise ValueError(
                "Could not find the sphinx-rustdocgen executable. "
                "Make sure it is configured or on the system path."
            )
        if not os.access(executable, os.X_OK):
            raise ValueError(f"{executable} is not an executable file.")

        # Possible values of the generate mode.
        generate_modes = ["always", "changed", "skip"]
        if sphinx_config.rust_generate_mode not in generate_modes:
            raise ValueError(
                f"Invalid value {sphinx_config.rust_generate_mode} for rust_generate_mode. "
                f"Must be one of {generate_modes}"
            )

        if sphinx_config.rust_generate_mode == "skip":
            # Skip parsing if the docs will never be generated.
            return executable, {}

        crate_configs = {}
        for crate, src_dir in sphinx_config.rust_crates.items():
            crate_configs[crate] = CrateConfiguration(
                crate_name=crate,
                src_dir=str(src_dir),
                doc_dir=str(
                    sphinx_config.rust_doc_dir
                    if isinstance(sphinx_config.rust_doc_dir, str)
                    else sphinx_config.rust_doc_dir[crate]
                ),
                format=(
                    sphinx_config.rust_rustdoc_fmt
                    if isinstance(sphinx_config.rust_rustdoc_fmt, str)
                    else sphinx_config.rust_rustdoc_fmt[crate]
                ),
                visibility=(
                    sphinx_config.rust_visibility
                    if isinstance(sphinx_config.rust_visibility, str)
                    else sphinx_config.rust_visibility[crate]
                ),
                force=sphinx_config.rust_generate_mode == "always",
            )

        return executable, crate_configs


# noinspection PyUnusedLocal
def generate_docs(app: Sphinx, config: sphinx.config.Config):
    """Generate the Rust docs once the configuration has been read

    Args:
        :app: The Sphinx application.
        :config: The parsed configuration.
    """
    # pylint: disable=unused-argument
    executable, crate_configs = CrateConfiguration.from_sphinx_config(config)

    for crate, crate_config in crate_configs.items():
        __LOGGER.info(
            "[sphinxcontrib_rust] Processing contents of crate %s from directory %s",
            crate,
            crate_config.src_dir,
        )
        __LOGGER.info(
            "[sphinxcontrib_rust] Generated files will be saved in %s/%s",
            crate_config.doc_dir,
            crate,
        )

        args = [
            executable,
            json.dumps(asdict(crate_config)),
        ]

        try:
            subprocess.run(
                args,
                check=True,
                text=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as ex:
            __LOGGER.exception(
                "sphinx-rustdocgen executable returned non-zero status code."
            )
            __LOGGER.error("\n=== Captured stderr ===\n")
            __LOGGER.error(ex.stderr)
            __LOGGER.error("\n=== Captured stdout ===\n")
            __LOGGER.error(ex.stdout)


__REQUIRED_EXTENSIONS = []
"""Extensions required by this module. Currently none, but kept here for future"""

__CONFIG_OPTIONS = (
    ("rust_crates", None, "env", [dict]),
    ("rust_doc_dir", None, "env", [str, dict]),
    ("rust_rustdocgen", None, "env", [str]),
    ("rust_generate_mode", "changed", "env", [str, dict]),
    ("rust_rustdoc_fmt", "rst", "env", [str, dict]),
    ("rust_visibility", "pub", "env", [str, dict]),
)
"""The configuration options added by the extension.

Each entry is tuple consisting of

* The option name.
* The default value.
* The rebuild condition, which can be one of

  * "html": Change needs a full rebuild of HTML.
  * "env": Change needs a full rebuild of the build environment.
  * "": No rebuild required.

* A list of types for the value.
"""


def setup(app: Sphinx) -> Mapping[str, Any]:
    """Set up the extension"""

    app.require_sphinx("7.0")

    for extension in __REQUIRED_EXTENSIONS:
        app.setup_extension(extension)

    for option in __CONFIG_OPTIONS:
        app.add_config_value(*option)

    app.add_domain(RustDomain)
    app.connect("config-inited", generate_docs)

    # See https://www.sphinx-doc.org/en/master/extdev/index.html#extension-metadata
    return {
        "version": __VERSION__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
