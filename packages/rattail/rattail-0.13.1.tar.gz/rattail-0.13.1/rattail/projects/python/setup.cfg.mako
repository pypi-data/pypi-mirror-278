## -*- coding: utf-8; mode: conf; -*-
# -*- coding: utf-8; -*-

[metadata]
name = ${pypi_name}
version = attr: ${pkg_name}.__version__
author = Your Name
author_email = you@example.com
# url = https://example.com/
description = ${description}
long_description = file: README.md

classifiers =
        % for classifier in sorted(classifiers):
        ${classifier}
        % endfor
        # TODO: remove this if you intend to publish your project
        # (it's here by default, to prevent accidental publishing)
        'Private :: Do Not Upload',

[options]
install_requires =
        % for pkg, spec in requires.items():
        % if spec:
        ${pkg if spec is True else spec}
        % endif
        % endfor
        # TODO: these may be needed to build/release package
        #'build',
        #'invoke',
        #'twine',

packages = find:
include_package_data = True


[options.entry_points]

% for key, values in entry_points.items():
${key} =
        % for value in values:
        ${value}
        % endfor
% endfor
