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
WuttaPOS - timestamp control
"""

import threading
import time

import flet as ft

from .base import WuttaControl


class WuttaTimestamp(WuttaControl):

    def __init__(self, *args, **kwargs):
        self.weight = kwargs.pop('weight', None)
        self.size = kwargs.pop('size', None)
        super().__init__(*args, **kwargs)

    def build(self):
        text = self.render_time(self.app.localtime())
        self.display = ft.Text(text, weight=self.weight, size=self.size)

        thread = threading.Thread(target=self.update_display)
        thread.start()

        return self.display

    def render_time(self, value):
        return value.strftime('%a %d %b %Y %I:%M:%S %p')

    def update_display(self):
        while True:
            if self.page:
                self.display.value = self.render_time(self.app.localtime())
                self.update()
            time.sleep(0.5)
