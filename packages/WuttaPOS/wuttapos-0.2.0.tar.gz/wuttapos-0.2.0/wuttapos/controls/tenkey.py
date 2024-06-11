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
WuttaPOS - ten-key control
"""

import flet as ft

from .base import WuttaControl


class WuttaTenkeyMenu(WuttaControl):

    default_font_size = 40
    default_button_size = 100

    def __init__(self, *args, **kwargs):
        self.simple = kwargs.pop('simple', False)
        self.on_char = kwargs.pop('on_char', None)
        self.on_enter = kwargs.pop('on_enter', None)
        self.on_up_click = kwargs.pop('on_up_click', None)
        self.on_up_longpress = kwargs.pop('on_up_longpress', None)
        self.on_down_click = kwargs.pop('on_down_click', None)
        self.on_down_longpress = kwargs.pop('on_down_longpress', None)
        super().__init__(*args, **kwargs)

    def build(self):

        row1 = [
            self.make_tenkey_button("1"),
            self.make_tenkey_button("2"),
            self.make_tenkey_button("3"),
        ]
        if not self.simple:
            row1.extend([
                self.make_tenkey_button("-"),
            ])

        row2 = [
            self.make_tenkey_button("4"),
            self.make_tenkey_button("5"),
            self.make_tenkey_button("6"),
        ]
        if not self.simple:
            row2.extend([
                self.make_tenkey_button("↑", on_long_press=self.up_long_press),
            ])

        row3 = [
            self.make_tenkey_button("7"),
            self.make_tenkey_button("8"),
            self.make_tenkey_button("9"),
        ]
        if not self.simple:
            row3.extend([
                self.make_tenkey_button("↓", on_long_press=self.down_long_press),
            ])

        row4 = [
            self.make_tenkey_button("0"),
            # self.make_tenkey_button("00"),
            self.make_tenkey_button("."),
        ]
        if self.simple:
            row4.extend([
                self.make_tenkey_button("⏎"),
            ])
        else:
            row4.extend([
                self.make_tenkey_button("ENTER", width=self.default_button_size * 2),
            ])

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        controls=row1,
                        spacing=0,
                    ),
                    ft.Row(
                        controls=row2,
                        spacing=0,
                    ),
                    ft.Row(
                        controls=row3,
                        spacing=0,
                    ),
                    ft.Row(
                        controls=row4,
                        spacing=0,
                    ),
                ],
                spacing=0,
            ),
        )

    def make_tenkey_button(
            self,
            text,
            font_size=None,
            height=None,
            width=None,
            on_click=None,
            on_long_press=None,
    ):
        if not font_size:
            font_size = self.default_font_size
        if not height:
            height = self.default_button_size
        if not width:
            width = self.default_button_size
        if not on_click:
            on_click = self.tenkey_click

        return self.make_button(text, font_size=font_size,  bgcolor='green',
                                height=height, width=width,
                                on_click=on_click,
                                on_long_press=on_long_press)

    def tenkey_click(self, e):
        value = e.control.content.value

        if value in ('ENTER', '⏎'):
            if self.on_enter:
                self.on_enter(e)

        elif value == '↑': # UP
            if self.on_up_click:
                self.on_up_click(e)

        elif value == '↓': # DOWN
            if self.on_down_click:
                self.on_down_click(e)

        else: # normal char key
            if self.on_char:
                self.on_char(value)

    def up_long_press(self, e):
        if self.on_up_longpress:
            self.on_up_longpress(e)

    def down_long_press(self, e):
        if self.on_down_longpress:
            self.on_down_longpress(e)
