# coding=utf-8
'''
 This program is free software. It comes without any warranty, to
 the extent permitted by applicable law. You can redistribute it
 and/or modify it under the terms of the Do What The Fuck You Want
 To Public License, Version 2, as published by Sam Hocevar. See
 http://sam.zoy.org/wtfpl/COPYING for more details.
'''
from pythonbuilder.core import use_plugin, init, Author

use_plugin('copy_resources')
use_plugin('filter_resources')

use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.install_dependencies')
use_plugin('python.distutils')

authors = [Author('Marcel Wolf', 'marcel.wolf@immobilienscout24.de')]
description = 'linter for YADT'

name = 'yadtlint'
license = 'GNU GPL v3'
summary = 'a linter yadt'
url = 'https://github.com/locolupo/yadtlint'
version = '0.0.1'


default_task = ['publish']


@init
def set_properties(project):
    project.build_depends_on('mockito')

    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('filter_resources_glob').append('**/yadtcontroller/__init__.py')

@init(environments="teamcity")
def set_properties_for_teamcity(project):
    import os
    project.version = '%s-%s' % (project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['install_build_dependencies', 'package']
    project.get_property('distutils_commands').append('bdist_rpm')
