# -*- coding: utf-8; -*-
######################################################################
#
#  Messkit -- Generic-ish Data Utility App
#  Copyright © 2022-2024 Lance Edgar
#
#  This file is part of Messkit.
#
#  Messkit is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Messkit is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Messkit.  If not, see <http://www.gnu.org/licenses/>.
#
######################################################################
"""
Messkit install handler
"""

from rattail import install as base
from rattail.commands.util import rprint, basic_prompt


class MesskitInstallHandler(base.InstallHandler):
    """
    Custom install handler for Messkit
    """

    def do_install_steps(self):
        super().do_install_steps()
        self.install_poser()

    def install_poser(self):
        if not basic_prompt("make poser dir?", True, is_bool=True):
            return False

        rprint()

        # make poser dir
        poser_handler = self.app.get_poser_handler()
        poserdir = poser_handler.make_poser_dir()

        rprint("\n\tposer dir created:  [bold green]{}[/bold green]".format(
            poserdir))
        return True
