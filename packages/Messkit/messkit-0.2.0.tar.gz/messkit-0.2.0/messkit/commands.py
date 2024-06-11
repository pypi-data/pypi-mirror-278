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
Messkit commands
"""

import typer

from rattail.commands.typer import typer_callback


messkit_typer = typer.Typer(
    callback=typer_callback,
    help="Messkit (Generic Data App)"
)


@messkit_typer.command()
def install(
        ctx: typer.Context,
):
    """
    Install the Messkit app
    """
    from messkit.install import MesskitInstallHandler

    config = ctx.parent.rattail_config
    handler = MesskitInstallHandler(
        config,
        app_title="Messkit",
        app_package='messkit',
        app_eggname='Messkit',
        app_pypiname='Messkit',
        main_image_url='/messkit/img/messkit.png',
        header_image_url='/messkit/img/messkit-small.png',
        favicon_url='/messkit/img/messkit-small.png')
    handler.run()
