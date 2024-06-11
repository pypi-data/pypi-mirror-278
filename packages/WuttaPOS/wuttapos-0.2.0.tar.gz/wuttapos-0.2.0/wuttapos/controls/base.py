# -*- coding: utf-8; -*-
################################################################################
#
#  WuttaPOS -- Pythonic Point of Sale System
#  Copyright © 2023 Lance Edgar
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
WuttaPOS - custom controls (base class)
"""

import flet as ft

from wuttapos.util import make_button, show_snackbar


class WuttaControl(ft.UserControl):

    def __init__(self, config, page=None, *args, **kwargs):
        self.on_reset = kwargs.pop('on_reset', None)

        super().__init__(*args, **kwargs)

        self.config = config
        self.app = config.get_app()
        self.enum = self.app.enum

        # TODO: why must we save this aside from self.page ?
        # but sometimes self.page gets set to None, so we must..
        self.mypage = page

    def informed_refresh(self, **kwargs):
        pass

    def make_button(self, *args, **kwargs):
        return make_button(*args, **kwargs)

    def reset(self, e=None):
        if self.on_reset:
            self.on_reset(e=e)

    def show_snackbar(self, text, bgcolor='yellow'):
        show_snackbar(self.mypage, text, bgcolor=bgcolor)
