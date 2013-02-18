# coding=utf-8
'''
 This program is free software. It comes without any warranty, to
 the extent permitted by applicable law. You can redistribute it
 and/or modify it under the terms of the Do What The Fuck You Want
 To Public License, Version 2, as published by Sam Hocevar. See
 http://sam.zoy.org/wtfpl/COPYING for more details.
'''

from pythonbuilder.core import use_plugin, init, Author

use_plugin('python.core')
use_plugin('python.install_dependencies')
use_plugin('python.unittest')
use_plugin('python.distutils')
use_plugin('python.coverage')

default_task = ['analyze', 'publish']

authors = [Author('Marcel Wolf', 'marcel.wolf@immobilienscout24.de')]
description = 'lint for YADT'

name = 'yadtlint'
license = ''
summary = 'lint yadt'
url = 'https://github.com/'
version = '0.0.1'


@init
def set_properties(project):

    project.set_property('coverage_break_build', True)
    project.get_property('distutils_commands').append('bdist_egg')