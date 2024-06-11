# -*- coding: utf-8; -*-
################################################################################
#
#  WuttaPOS -- Pythonic Point of Sale System
#  Copyright © 2023-2024 Lance Edgar
#
#  This file is part of WuttaPOS.
#
#  WuttaPOS is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  WuttaPOS is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  WuttaPOS.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
WuttaPOS commands
"""

import logging

import typer

from rattail.files import resource_path
from rattail.commands.typer import typer_callback


log = logging.getLogger(__name__)


wuttapos_typer = typer.Typer(
    callback=typer_callback,
    help="WuttaPOS (point of sale)"
)


@wuttapos_typer.command('open')
def typer_open(
        ctx: typer.Context,
):
    """
    Open the Point of Sale app
    """
    from wuttapos.app import run_app

    config = ctx.parent.rattail_config
    run_app(config)


@wuttapos_typer.command()
def serve(
        ctx: typer.Context,
):
    """
    Run the POS app as a web service
    """
    import flet as ft
    from wuttapos.app import main

    config = ctx.parent.rattail_config
    kw = {}

    host = config.get('wuttapos', 'serve.host',
                      default='0.0.0.0')
    kw['host'] = host

    port = config.getint('wuttapos', 'serve.port',
                         default=8332)
    kw['port'] = port

    # TODO: we technically "support" this, in that we do pass the
    # value on to Flet, but in practice it does not work right
    path = config.get('wuttapos', 'serve.path', default='')
    if path:
        path = path.strip('/') + '/'
        kw['name'] = path
        # kw['route_url_strategy'] = 'hash'

    log.info(f"will serve WuttaPOS on http://{host}:{port}/{path}")
    ft.app(target=main, view=None,
           assets_dir=resource_path('wuttapos:assets'),
           **kw)


@wuttapos_typer.command()
def status(
        ctx: typer.Context,
):
    """
    Show status of the POS lane
    """
    print("TODO: show status")
