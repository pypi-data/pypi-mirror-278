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
WuttaPOS - txn item control
"""

import flet as ft

from .base import WuttaControl


class WuttaTxnItem(WuttaControl):
    """
    Control for displaying a transaction line item within main POS
    items list.
    """
    font_size = 24

    def __init__(self, config, row, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.row = row

    def build(self):

        self.major_style = ft.TextStyle(size=self.font_size,
                                        weight=ft.FontWeight.BOLD)

        self.minor_style = ft.TextStyle(size=int(self.font_size * 0.8),
                                        italic=True)

        if self.row.row_type in (self.enum.POS_ROW_TYPE_SELL,
                                 self.enum.POS_ROW_TYPE_OPEN_RING):
            return self.build_item_sell()

        elif self.row.row_type in (self.enum.POS_ROW_TYPE_TENDER,
                                   self.enum.POS_ROW_TYPE_CHANGE_BACK):
            return self.build_item_tender()

    def build_item_sell(self):

        self.quantity = ft.TextSpan(style=self.minor_style)
        self.txn_price = ft.TextSpan(style=self.minor_style)

        self.sales_total_style = ft.TextStyle(size=self.font_size,
                                              weight=ft.FontWeight.BOLD)

        self.sales_total = ft.TextSpan(style=self.sales_total_style)

        self.fs_flag = ft.TextSpan(style=self.minor_style)
        self.tax_flag = ft.TextSpan(style=self.minor_style)

        # set initial text display values
        self.refresh(update=False)

        return ft.Row(
            [
                ft.Text(
                    spans=[
                        ft.TextSpan(f"{self.row.description}",
                                    style=self.major_style),
                        ft.TextSpan("× ", style=self.minor_style),
                        self.quantity,
                        ft.TextSpan(" @ ", style=self.minor_style),
                        self.txn_price,
                    ],
                ),
                ft.Text(
                    spans=[
                        self.fs_flag,
                        self.tax_flag,
                        self.sales_total,
                    ],
                ),

            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def build_item_tender(self):
        return ft.Row(
            [
                ft.Text(
                    spans=[
                        ft.TextSpan(f"{self.row.description}",
                                    style=self.major_style),
                    ],
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(self.app.render_currency(self.row.tender_total),
                                    style=self.major_style),
                    ],
                ),

            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def refresh(self, update=True):

        if self.row.void:
            self.major_style.color = None
            self.major_style.decoration = ft.TextDecoration.LINE_THROUGH
            self.major_style.weight = None
            self.minor_style.color = None
            self.minor_style.decoration = ft.TextDecoration.LINE_THROUGH
        else:
            self.major_style.color = None
            self.major_style.decoration = None
            self.major_style.weight = ft.FontWeight.BOLD
            self.minor_style.color = None
            self.minor_style.decoration = None

        if self.row.row_type in (self.enum.POS_ROW_TYPE_SELL,
                                 self.enum.POS_ROW_TYPE_OPEN_RING):
            self.quantity.text = self.app.render_quantity(self.row.quantity)
            self.txn_price.text = self.app.render_currency(self.row.txn_price)
            self.sales_total.text = self.app.render_currency(self.row.sales_total)
            self.fs_flag.text = "FS   " if self.row.foodstamp_eligible else ""
            self.tax_flag.text = f"T{self.row.tax_code}   " if self.row.tax_code else ""

            if self.row.void:
                self.sales_total_style.color = None
                self.sales_total_style.decoration = ft.TextDecoration.LINE_THROUGH
                self.sales_total_style.weight = None
            else:
                if (self.row.row_type == self.enum.POS_ROW_TYPE_SELL
                    and self.row.txn_price_adjusted):
                    self.sales_total_style.color = 'orange'
                elif (self.row.row_type == self.enum.POS_ROW_TYPE_SELL
                      and self.row.cur_price and self.row.cur_price < self.row.reg_price):
                    self.sales_total_style.color = 'green'
                else:
                    self.sales_total_style.color = None
                self.sales_total_style.decoration = None
                self.sales_total_style.weight = ft.FontWeight.BOLD

        if update:
            self.update()
