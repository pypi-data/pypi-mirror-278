==================
Sphinxcontrib-rust
==================

.. warning::

   This project is still under development. While basic features are
   available, there are still improvements to make. See :doc:`docs/limitations`
   for limitations and :doc:`TODO` for features that are not yet complete.

This is a `Sphinx`_ extension for integrating Rust programming language
projects in Sphinx builds.

You can read this documentation on `Gitlab Pages`_ or `readthedocs`_.

.. _`Gitlab Pages`: https://munir0b0t.gitlab.io/sphinxcontrib-rust

.. _`readthedocs`: https://sphinxcontrib-rust.readthedocs.io/en/latest/

Motivation
----------

This is primarily meant for teams and projects that are already
using Sphinx as a documentation build tool, and would like to
include documentation for Rust projects in it along with Python,
C and other languages.

Using the extension adds the following functionality:

1. Rust specific directives and roles that can be used to link and
   cross-reference rustdoc comments.

2. rustdoc comments may be written in reStructuredText. (This
   might break IDE and other integrations that expect Markdown).

This is not a replacement for `rustdoc`_, and since rustdoc is a part of
the Rust language itself, it will not have all the same features as `rustdoc`_

The goal is to provide a way for teams and projects using multiple languages
to publish a single, consolidated documentation and use this, along with
rustdoc, as part of the documentation workflow.

See :doc:`docs/limitations` for some cases where the tool will not work
the same as rustdoc.

.. _`usage`:

How to use
----------

Installation
++++++++++++

There are two components that are required for this to work

1. The ``sphinx-rustdocgen`` Rust crate for extracting the docs.
2. The ``sphinxcontrib_rust`` Python package, which is a Sphinx
   extension.

Both components are installed when installing the Python package with

.. code-block::

   pip install sphinxcontrib-rust

The installation will check for ``cargo`` in the ``$PATH`` environment
variable and will use that to build and install the Rust executable.

The executable is built with the Rust code shipped with the Python package.
This ensures that the Rust executable and Python package are always compatible
with each other.

Make sure that the path where ``cargo`` installs the executable is in
``$PATH`` as well. If the default installation directory is not part of the
``$PATH`` environment, the installed executable should be specified in the Sphinx
configuration with ``rust_rustdocgen`` option.

The Rust executable may also be installed independently from crates.io or built
with the shipped source code.

With reStructuredText
+++++++++++++++++++++

To use the extension with rst rustdoc comments, simply add the extension to the
``conf.py`` file. The various configuration options supported by the extension,
along with their defaults, are documented below.

.. code-block:: python

   extensions = ["sphinxcontrib_rust"]
   rust_crates = {
       "my_crate": "src/",
       "my_crate_derive": "my-crate-derive/src",
   }
   rust_doc_dir = "docs/crates/"

This will generate the documentation from your Rust crates and put them in the
``docs/crates/<crate_name>`` directories. You can link against the documentation
in your ``toctree`` by specifying the path to the ``main`` or ``lib`` file. See
:doc:`docs/including` for more details.

.. code-block::

   .. toctree::

      docs/crates/my_crate/main
      docs/crates/my_crate/lib

The extension also adds various roles for Rust items. The roles can be used
within the Sphinx documentation and also within the docstrings themselves.
The roles can even be used in docstrings of a different language that is part of
the same Sphinx project. The roles are documented in :doc:`docs/roles`.

The extension also provides various :doc:`docs/directives` and
:doc:`docs/indices` that can be used in the documentation.

With Markdown
+++++++++++++

This feature is still a work in progress, and needs more tests, but the aim
is to allow for a simpler transition to Sphinx without rewriting the comments
in reStructuredText.

To use the extension with the standard markdown rustdoc comments, add the
extension to the ``conf.py`` file and also add the `myst-parser`_ extension.
Sphinx also needs to be `configured for Markdown builds`_.

The various configuration options for the Rust extension, along with
their defaults, are documented below. Also see the `configuration options
for MyST`_ to customize the markdown.

.. code-block:: python

   extensions = ["sphinxcontrib_rust", "myst_parser"]
   source_suffix = {
       ".rst": "restructuredtext",
       ".md": "markdown",
       ".txt": "markdown", # Optional
   }
   myst_enable_extensions = {
       "colon_fence",
   }
   myst_ref_domains = [
       "rust",
   ]
   rust_crates = {
       "my_crate": "src/",
       "my_crate_derive": "my-crate-derive/src",
   }
   rust_doc_dir = "docs/crates/"


Note that ``myst-parser`` has to be installed as dependency to the Sphinx
build from PyPI with ``pip install myst-parser`` or by specifying it as a
dependency in ``setup.py`` or ``pyproject.toml`` of the project.

This enables all the same roles and indexes as with rst. Use the `myst-parser
syntax`_ for the roles.

Options
+++++++

Options are simply Python variables set in the ``conf.py`` file. Most options can
be provided as a global value or a dict of values per crate, with the crate name
as the key. The options that are global are listed separately below.

:rust_crates: (Required) A dict of crate names and their source code directories.
              This must be a dict even for a single crate. It determines which
              crates are documented.
:rust_doc_dir: (Required) A directory under which to write the docs for all crates,
               or a dict of directory for each crate name. The directories will be
               read by Sphinx during the build, so they must be part of the source
               tree and not under the build directory. The build process will create
               a directory with the crate name under this, even when specified per
               crate.
:rust_rustdoc_fmt: Either ``rst`` or ``md``. (Default: ``rst``)
:rust_visibility: Only includes documentation and indexes for items
                  with visibility greater than or equal to the setting.
                  The value can be ``pub``, ``crate`` or ``pvt``.
                  Visibility restrictions like ``super`` and ``in <path>`` are
                  not supported currently and are treated as private. (Default:
                  ``pub``).

The below options are global options, and cannot be specified per crate.

:rust_generate_mode: One of ``always``, ``skip`` or ``changed``. If set to
                     ``always``, all documents are regenerated. If set to ``skip``,
                     the docs are not regenerated at all. If set to ``changed``,
                     only docs whose source files have been modified since they
                     were last modified are regenerated. (Default: ``changed``)
:rust_rustdocgen: The path to the ``sphinx-rustdocgen`` executable to use.
                  The path must be an absolute path or relative to Sphinx's
                  working directory. (Default: Obtained from the ``$PATH``
                  environment variable.)

.. _`Sphinx`: https://www.sphinx-doc.org/en/master/index.html
.. _`myst-parser`: https://myst-parser.readthedocs.io/en/latest/index.html
.. _`configured for Markdown builds`: https://www.sphinx-doc.org/en/master/usage/markdown.html
.. _`configuration options for MyST`: https://myst-parser.readthedocs.io/en/latest/configuration.html
.. _`myst-parser syntax`:
   https://myst-parser.readthedocs.io/en/latest/syntax/roles-and-directives.html#roles-an-in-line-extension-point
.. _rustdoc: https://doc.rust-lang.org/rustdoc/index.html

.. _details:

.. toctree::
   :caption: Detailed docs
   :maxdepth: 2
   :glob:

   docs/including
   docs/roles
   docs/directives
   docs/indices
   docs/developing
   docs/limitations
   docs/sphinx-rustdocgen
   docs/sphinx-extension
   TODO
   CONTRIBUTING
