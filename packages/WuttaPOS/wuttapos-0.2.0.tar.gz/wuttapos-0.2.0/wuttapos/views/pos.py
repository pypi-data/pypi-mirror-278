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
WuttaPOS - POS view
"""

import decimal
import logging
import time

import flet as ft

from .base import WuttaView
from wuttapos.controls.loginform import WuttaLoginForm
from wuttapos.controls.custlookup import WuttaCustomerLookup
from wuttapos.controls.itemlookup import WuttaProductLookup
from wuttapos.controls.deptlookup import WuttaDepartmentLookup
from wuttapos.controls.txnlookup import WuttaTransactionLookup
from wuttapos.controls.txnitem import WuttaTxnItem
from wuttapos.controls.tenkey import WuttaTenkeyMenu


log = logging.getLogger(__name__)


class POSView(WuttaView):
    """
    Main POS view for WuttaPOS
    """

    # TODO: should be configurable?
    default_button_size = 100
    default_font_size = 40

    disabled_bgcolor = '#aaaaaa'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # keep a list of "informed" controls - i.e. child controls
        # within this view, which need to stay abreast of global
        # changes to the transaction, customer etc.
        self.informed_controls = []
        if hasattr(self, 'header'):
            self.informed_controls.append(self.header)

    def informed_refresh(self):
        for control in self.informed_controls:
            control.informed_refresh()

    def reset(self, e=None, clear_quantity=True):
        """
        This is a convenience method, meant only to clear the main
        input and set focus to it.  Will also update() the page.

        The ``e`` arg is ignored and accepted only so this method may
        be registered as an event handler, e.g. ``on_cancel``.
        """
        # clear set (@) quantity
        if clear_quantity:
            if self.set_quantity.data:
                self.set_quantity.data = None
                self.set_quantity.value = None
                self.set_quantity_button.visible = True

        # clear/focus main input
        self.main_input.value = ''
        self.main_input.focus()

        self.page.update()

    def set_customer(self, customer, batch=None, user=None):
        session = self.app.get_session(customer)
        if not batch:
            batch = self.get_current_batch(session)
        if user:
            user = session.get(user.__class__, user.uuid)
        else:
            user = self.get_current_user(session)

        handler = self.get_batch_handler()
        handler.set_customer(batch, customer, user=user)

        self.page.session.set('txn_display', handler.get_screen_txn_display(batch))
        self.page.session.set('cust_uuid', customer.uuid)
        self.page.session.set('cust_display', handler.get_screen_cust_display(customer=customer))
        self.informed_refresh()
        self.refresh_totals( batch)

        self.show_snackbar(f"CUSTOMER SET: {customer}", bgcolor='green')

    def item_click(self, e):

        value = self.main_input.value
        if value:
            if not self.attempt_add_product():
                self.item_lookup(value)

        elif self.selected_item:
            row = self.selected_item.data['row']
            if row.product_uuid:
                if self.attempt_add_product(uuid=row.product_uuid):
                    self.clear_item_selection()
                    self.page.update()
            else:
                self.item_lookup()

        else:
            self.item_lookup()

    def refresh_totals(self, batch):
        reg = ft.TextStyle(size=22)
        bold = ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)

        self.subtotals.spans.clear()

        self.subtotals.spans.append(ft.TextSpan("Sales  ", style=reg))
        total = self.app.render_currency(batch.sales_total or 0)
        self.subtotals.spans.append(ft.TextSpan(total, style=bold))

        for btax in sorted(batch.taxes.values(),
                           key=lambda t: t.tax_code):
            if btax.tax_total:
                self.subtotals.spans.append(ft.TextSpan(f"    Tax {btax.tax_code}  ", style=reg))
                total = self.app.render_currency(btax.tax_total)
                self.subtotals.spans.append(ft.TextSpan(total, style=bold))

        if batch.tender_total:
            self.subtotals.spans.append(ft.TextSpan(f"    Tend  ", style=reg))
            total = self.app.render_currency(batch.tender_total)
            self.subtotals.spans.append(ft.TextSpan(total, style=bold))

        self.fs_balance.spans.clear()

        fs_balance = batch.get_fs_balance()
        if fs_balance:
            self.fs_balance.spans.append(ft.TextSpan("FS  ", style=reg))
            total = self.app.render_currency(fs_balance)
            self.fs_balance.spans.append(ft.TextSpan(total, style=bold))

        self.balances.spans.clear()

        self.balances.spans.append(ft.TextSpan("    ", style=reg))
        total = self.app.render_currency(batch.get_balance() or 0)
        self.balances.spans.append(
            ft.TextSpan(total, style=ft.TextStyle(size=40, weight=ft.FontWeight.BOLD)))

        self.totals_row.bgcolor = 'orange'

    def attempt_add_product(self, uuid=None, record_badscan=False):
        session = self.app.make_session()
        handler = self.get_batch_handler()
        user = self.get_current_user(session)
        batch = self.get_current_batch(session, user=user)
        entry = self.main_input.value

        quantity = 1
        if self.set_quantity.data is not None:
            quantity = self.set_quantity.data

        product = None
        item_entry = entry
        if uuid:
            product = session.get(self.model.Product, uuid)
            assert product
            key = self.app.get_product_key_field()
            item_entry = str(getattr(product, key) or '') or uuid

        try:
            row = handler.process_entry(batch, product or entry, quantity=quantity,
                                        item_entry=item_entry, user=user)
        except Exception as error:
            session.rollback()
            self.show_snackbar(f"ERROR: {error}", bgcolor='yellow')
            row = None

        else:

            if row:
                session.commit()

                if row.row_type == self.enum.POS_ROW_TYPE_BADPRICE:
                    self.show_snackbar(f"Product has invalid price: {row.item_entry}",
                                       bgcolor='yellow')

                else:
                    self.add_row_item(row, scroll=True)
                    self.refresh_totals(batch)
                    self.reset()

            else:

                if record_badscan:
                    handler.record_badscan(batch, entry, quantity=quantity, user=user)

                self.show_snackbar(f"PRODUCT NOT FOUND: {entry}", bgcolor='yellow')

            session.commit()
            self.refresh_totals(batch)

        session.close()
        self.page.update()
        return bool(row)

    def item_lookup(self, value=None):

        def select(uuid):
            self.attempt_add_product(uuid=uuid)
            dlg.open = False
            self.reset()

        def cancel(e):
            dlg.open = False
            self.reset(clear_quantity=False)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Product Lookup"),
            content=WuttaProductLookup(self.config, initial_search=value,
                                       on_select=select, on_cancel=cancel),
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def customer_lookup(self, value=None, user=None):

        def select(uuid):
            session = self.app.make_session()
            customer = session.get(self.model.Customer, uuid)
            self.set_customer(customer, user=user)
            session.commit()
            session.close()

            dlg.open = False
            self.reset()

        def cancel(e):
            dlg.open = False
            self.reset()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Customer Lookup"),
            content=WuttaCustomerLookup(self.config, initial_search=value,
                                        on_select=select, on_cancel=cancel),
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def customer_info(self):
        clientele = self.app.get_clientele_handler()
        session = self.app.make_session()

        entry = self.main_input.value
        if entry:
            different = True
            customer = clientele.locate_customer_for_entry(session, entry)
            if not customer:
                session.close()
                self.show_snackbar(f"CUSTOMER NOT FOUND: {entry}", bgcolor='yellow')
                self.page.update()
                return

        else:
            different = False
            customer = session.get(self.model.Customer, self.page.session.get('cust_uuid'))
            assert customer

        info = clientele.get_customer_info_markdown(customer)
        session.close()

        def close(e):
            dlg.open = False
            self.reset()

        font_size = self.default_font_size * 0.8
        dlg = ft.AlertDialog(
            # modal=True,
            title=ft.Text("Customer Info"),
            content=ft.Container(ft.Column(
                [
                    ft.Container(
                        content=ft.Text("NOTE: this is a DIFFERENT customer than the txn has!"),
                        bgcolor='yellow',
                        visible=different,
                    ),
                    ft.Divider(),
                    ft.Container(
                        theme_mode=ft.ThemeMode.SYSTEM,
                        theme=ft.Theme(text_theme=ft.TextTheme(
                            body_medium=ft.TextStyle(
                                size=24,
                                color='black',
                            ))),
                        content=ft.Markdown(info),
                    ),
                ],
                height=500,
                width=500,
            )),
            actions=[
                ft.Container(content=ft.Text("Close",
                                             size=font_size,
                                             weight=ft.FontWeight.BOLD),
                             height=self.default_button_size * 0.8,
                             width=self.default_button_size * 1.2,
                             alignment=ft.alignment.center,
                             bgcolor='blue',
                             border=ft.border.all(1, 'black'),
                             border_radius=ft.border_radius.all(5),
                             on_click=close),
            ],
            # actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def customer_prompt(self):

        def view_info(e):
            dlg.open = False
            self.page.update()

            # cf. https://github.com/flet-dev/flet/issues/1670
            time.sleep(0.1)

            self.customer_info()

        def remove(e):
            dlg.open = False
            self.page.update()

            # cf. https://github.com/flet-dev/flet/issues/1670
            time.sleep(0.1)

            self.remove_customer_prompt()

        def replace(e):
            dlg.open = False
            self.page.update()

            # nb. do this just in case we must show login dialog
            # cf. https://github.com/flet-dev/flet/issues/1670
            time.sleep(0.1)

            self.authorized_action('pos.swap_customer', self.replace_customer,
                                   message="Replace Customer")

        def cancel(e):
            dlg.open = False
            self.reset()

        font_size = self.default_font_size * 0.8
        dlg = ft.AlertDialog(
            # modal=True,
            title=ft.Text("Customer Already Selected"),
            content=ft.Text("What would you like to do?", size=20),
            actions=[
                ft.Container(content=ft.Text("Remove",
                                             size=font_size,
                                             weight=ft.FontWeight.BOLD),
                             height=self.default_button_size,
                             width=self.default_button_size * 2.5,
                             alignment=ft.alignment.center,
                             bgcolor='red',
                             border=ft.border.all(1, 'black'),
                             border_radius=ft.border_radius.all(5),
                             on_click=remove),
                ft.Container(content=ft.Text("Replace",
                                             size=font_size,
                                             color='black',
                                             weight=ft.FontWeight.BOLD),
                             height=self.default_button_size,
                             width=self.default_button_size * 2.5,
                             alignment=ft.alignment.center,
                             bgcolor='yellow',
                             border=ft.border.all(1, 'black'),
                             border_radius=ft.border_radius.all(5),
                             on_click=replace),
                ft.Container(content=ft.Text("View Info",
                                             size=font_size,
                                             weight=ft.FontWeight.BOLD),
                             height=self.default_button_size,
                             width=self.default_button_size * 2.5,
                             alignment=ft.alignment.center,
                             bgcolor='blue',
                             border=ft.border.all(1, 'black'),
                             border_radius=ft.border_radius.all(5),
                             on_click=view_info),
                ft.Container(content=ft.Text("Cancel",
                                             size=font_size,
                                             # color='black',
                                             weight=ft.FontWeight.BOLD),
                             height=self.default_button_size,
                             width=self.default_button_size * 2.5,
                             alignment=ft.alignment.center,
                             border=ft.border.all(1, 'black'),
                             border_radius=ft.border_radius.all(5),
                             on_click=cancel),
            ])

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def remove_customer_prompt(self):

        def remove(e):
            dlg.open = False
            self.page.update()

            # nb. do this just in case we must show login dialog
            # cf. https://github.com/flet-dev/flet/issues/1670
            time.sleep(0.1)

            self.authorized_action('pos.del_customer', self.remove_customer,
                                   message="Remove Customer")

        def cancel(e):
            dlg.open = False
            self.reset()

        font_size = self.default_font_size * 0.8
        dlg = ft.AlertDialog(
            title=ft.Text("Remove Customer"),
            content=ft.Text("Really remove the customer from this transaction?", size=20),
            actions=[
                ft.Container(content=ft.Text("Yes, Remove",
                                             size=font_size,
                                             weight=ft.FontWeight.BOLD),
                             height=self.default_button_size,
                             width=self.default_button_size * 2.5,
                             alignment=ft.alignment.center,
                             bgcolor='red',
                             border=ft.border.all(1, 'black'),
                             border_radius=ft.border_radius.all(5),
                             on_click=remove),
                ft.Container(content=ft.Text("Cancel",
                                             size=font_size,
                                             weight=ft.FontWeight.BOLD),
                             height=self.default_button_size,
                             width=self.default_button_size * 2.5,
                             alignment=ft.alignment.center,
                             border=ft.border.all(1, 'black'),
                             border_radius=ft.border_radius.all(5),
                             on_click=cancel),
            ])

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def remove_customer(self, user):
        session = self.app.make_session()
        handler = self.get_batch_handler()
        batch = self.get_current_batch(session)
        user = session.get(user.__class__, user.uuid)
        handler.set_customer(batch, None, user=user)
        session.commit()
        session.close()

        self.page.session.set('cust_uuid', None)
        self.page.session.set('cust_display', None)
        self.informed_refresh()
        self.show_snackbar("CUSTOMER REMOVED", bgcolor='yellow')
        self.reset()

    def replace_customer(self, user):
        entry = self.main_input.value
        if entry:
            if not self.attempt_set_customer(entry, user=user):
                self.customer_lookup(entry, user=user)
        else:
            self.customer_lookup(user=user)

    def attempt_set_customer(self, entry=None, user=None):
        session = self.app.make_session()

        customer = self.app.get_clientele_handler().locate_customer_for_entry(session, entry)
        if customer:

            self.set_customer(customer, user=user)
            self.reset()

        else: # customer not found
            self.show_snackbar(f"CUSTOMER NOT FOUND: {entry}", bgcolor='yellow')
            # TODO: should use reset() here?
            self.main_input.focus()
            self.page.update()

        session.commit()
        session.close()
        return bool(customer)

    def customer_click(self, e):

        # prompt user to replace customer if already set
        if self.page.session.get('cust_uuid'):
            self.customer_prompt()

        else:
            value = self.main_input.value
            if value:
                # okay try to set it with given value
                if not self.attempt_set_customer(value):
                    self.customer_lookup(value)

            else:
                # no value provided, so do lookup
                self.customer_lookup()

    def tenkey_char(self, key):
        self.main_input.value = f"{self.main_input.value or ''}{key}"
        self.main_input.focus()
        self.page.update()

    def tenkey_enter(self, e):
        self.main_submit()

    def tenkey_up_click(self, e):

        # select previous item, if selection in progress
        if self.selected_item:
            i = self.items.controls.index(self.selected_item)
            if i > 0:
                self.items.scroll_to(delta=-50, duration=100)
                self.select_txn_item(self.items.controls[i - 1])
                return

        self.items.scroll_to(delta=-50, duration=100)
        self.page.update()

    def tenkey_up_longpress(self, e):
        self.items.scroll_to(delta=-500, duration=100)
        self.page.update()

    def tenkey_down_click(self, e):

        # select next item, if selection in progress
        if self.selected_item:
            i = self.items.controls.index(self.selected_item)
            if (i + 1) < len(self.items.controls):
                self.items.scroll_to(delta=50, duration=100)
                self.select_txn_item(self.items.controls[i + 1])
                return

        self.items.scroll_to(delta=50, duration=100)
        self.page.update()

    def tenkey_down_longpress(self, e):
        self.items.scroll_to(delta=500, duration=100)
        self.page.update()

    def build_controls(self):

        session = self.app.make_session()
        handler = self.get_batch_handler()
        self.tender_cash = handler.get_tender(session, 'cash')
        self.tender_check = handler.get_tender(session, 'check')
        self.tender_foodstamp = handler.get_tender(session, 'foodstamp')
        session.expunge_all()
        session.close()

        self.main_input = ft.TextField(on_submit=self.main_submit,
                                       text_size=24,
                                       text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                       autofocus=True)

        self.selected_item = None
        self.items = ft.ListView(
            item_extent=50,
            height=800,
        )

        self.subtotals = ft.Text(spans=[])
        self.fs_balance = ft.Text(spans=[])
        self.balances = ft.Text(spans=[])

        self.totals_row = ft.Container(
            ft.Row(
                [
                    self.subtotals,
                    ft.Row(
                        [
                            self.fs_balance,
                            self.balances,
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.only(10, 0, 10, 0),
        )

        self.items_column = ft.Column(
            controls=[
                ft.Container(
                    content=self.items,
                    padding=ft.padding.only(10, 0, 10, 0)),
                self.totals_row,
            ],
            expand=1,
        )

        def backspace_click(e):
            if self.main_input.value:
                self.main_input.value = self.main_input.value[:-1]
            self.main_input.focus()
            self.page.update()

        def clear_entry_click(e):
            if self.main_input.value:
                self.main_input.value = ""
            elif self.set_quantity.data is not None:
                self.set_quantity.data = None
                self.set_quantity.value = None
                self.set_quantity_button.visible = True
            elif self.selected_item:
                self.clear_item_selection()
            self.main_input.focus()
            self.page.update()

        self.tenkey_menu = WuttaTenkeyMenu(self.config,
                                           on_char=self.tenkey_char,
                                           on_enter=self.tenkey_enter,
                                           on_up_click=self.tenkey_up_click,
                                           on_up_longpress=self.tenkey_up_longpress,
                                           on_down_click=self.tenkey_down_click,
                                           on_down_longpress=self.tenkey_down_longpress)

        meta_button_height = self.default_button_size
        meta_button_width = meta_button_height * 2
        meta_font_size = self.default_font_size

        def meta_button(text, font_size=None, bgcolor='blue', data=None, on_click=None):
            return self.make_button(text,
                                    font_size=font_size or meta_font_size,
                                    height=meta_button_height,
                                    width=meta_button_width,
                                    bgcolor=bgcolor,
                                    data=data,
                                    on_click=on_click)

        self.meta_menu = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            meta_button("CUST", bgcolor='blue', on_click=self.customer_click),
                            meta_button("VOID", bgcolor='red', on_click=self.void_click),
                        ],
                        spacing=0,
                    ),
                    ft.Row(
                        [
                            meta_button("ITEM", bgcolor='blue', on_click=self.item_click),
                            meta_button("MGR", bgcolor='yellow', on_click=self.manager_click),
                        ],
                        spacing=0,
                    ),
                    ft.Row(
                        [
                            meta_button("OPEN RING", font_size=32, bgcolor='blue',
                                        on_click=self.open_ring_click),
                            meta_button("NO SALE", bgcolor='yellow', on_click=self.nosale_click),
                        ],
                        spacing=0,
                    ),
                    ft.Row(
                        [
                            meta_button("Adjust\nPrice", font_size=30, bgcolor='yellow',
                                        on_click=self.adjust_price_click),
                            meta_button("REFUND", bgcolor='red', on_click=self.refund_click),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=0,
            ),
            expand=0)

        context_button_height = self.default_button_size
        context_button_width = context_button_height * 2
        context_font_size = self.default_font_size

        def context_button(text, on_click=None, data=None):
            return ft.Container(content=ft.Text(text, size=context_font_size,
                                                weight=ft.FontWeight.BOLD),
                                height=context_button_height,
                                width=context_button_width,
                                on_click=on_click,
                                data=data,
                                alignment=ft.alignment.center,
                                border=ft.border.all(1, 'black'),
                                border_radius=ft.border_radius.all(5),
                                bgcolor='orange')

        self.context_menu = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self.make_cash_button(),
                            self.make_check_button(),
                        ],
                        spacing=0,
                    ),
                    ft.Row(
                        [
                            self.make_foodstamp_button(),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=0,
            ),
            expand=0)

        self.suspend_menu = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self.make_suspend_button(),
                            self.make_resume_button(),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=0,
            ),
            expand=0)

        self.set_quantity = ft.Text(value=None, data=None, weight=ft.FontWeight.BOLD, size=40)

        self.set_quantity_button = self.make_button("@",
                                                    font_size=40,
                                                    height=70,
                                                    width=70,
                                                    bgcolor='green',
                                                    on_click=self.set_quantity_click)

        return [
            self.build_header(),

            ft.Row(
                [
                    self.make_logo_image(height=80),
                    ft.Row(
                        [
                            ft.Row(
                                [
                                    self.set_quantity,
                                    self.set_quantity_button,
                                ],
                            ),
                            self.main_input,
                            self.make_button("⌫", font_size=40, bgcolor='green',
                                             height=70, width=70,
                                             on_click=backspace_click),
                            self.make_button("CE", font_size=40, bgcolor='green',
                                             height=70, width=70,
                                             on_click=clear_entry_click),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                    ),
                ],
            ),

            ft.Row(),
            ft.Row(),
            ft.Row(),

            ft.Row(
                [
                    self.items_column,
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    self.tenkey_menu,
                                    self.meta_menu,
                                ],
                            ),
                            ft.Row(
                                [
                                    self.context_menu,
                                    self.suspend_menu,
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.START,
                            ),
                        ],
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        ]

    def make_text(self, *args, **kwargs):
        kwargs.setdefault('weight', ft.FontWeight.BOLD)
        kwargs.setdefault('size', 24)
        return ft.Text(*args, **kwargs)

    def set_quantity_click(self, e):
        quantity = self.main_input.value
        valid = False

        if self.set_quantity.data is not None:
            quantity = self.set_quantity.data
            self.show_snackbar(f"QUANTITY ALREADY SET: {quantity}", bgcolor='yellow')

        else:
            try:
                quantity = decimal.Decimal(quantity)
                valid = True
            except decimal.InvalidOperation:
                pass

            if valid and quantity:
                self.set_quantity.data = quantity
                self.set_quantity.value = self.app.render_quantity(quantity) + " @ "
                self.set_quantity_button.visible = False
                self.main_input.value = ""
                self.main_input.focus()

            else:
                self.show_snackbar(f"INVALID @ QUANTITY: {quantity}", bgcolor='yellow')

        self.page.update()

    def make_tender_button(self, tender, **kwargs):
        if isinstance(tender, self.model.Tender):
            info = {'tender_code': tender.code,
                    'tender_name': tender.name}
        else:
            info = tender

        kw = {
            'font_size': self.default_font_size,
            'height': self.default_button_size,
            'width': self.default_button_size * 2,
            'on_click': self.tender_click,
            'bgcolor': 'orange',
        }
        kw.update(kwargs)
        kw['data'] = info
        return self.make_button(info['tender_name'], **kw)

    def make_cash_button(self, **kwargs):
        cash = self.tender_cash or {'tender_code': 'CA',
                                    'tender_name': "Cash"}
        return self.make_tender_button(cash, **kwargs)

    def make_check_button(self, **kwargs):
        check = self.tender_check or {'tender_code': 'CK',
                                      'tender_name': "Check"}
        return self.make_tender_button(check, **kwargs)

    def make_foodstamp_button(self, **kwargs):
        foodstamp = self.tender_foodstamp or {'tender_code': 'FS',
                                              'tender_name': "Food Stamps"}
        kwargs.setdefault('font_size', 34)
        return self.make_tender_button(foodstamp, **kwargs)

    def make_suspend_button(self, **kwargs):
        return self.make_button("SUSPEND", bgcolor='purple',
                                font_size=self.default_font_size,
                                height=self.default_button_size,
                                width=self.default_button_size * 2,
                                on_click=self.suspend_click)

    def suspend_click(self, e):
        session = self.app.make_session()
        batch = self.get_current_batch(session, create=False)
        session.close()

        # nothing to suspend if no batch
        if not batch:
            self.show_snackbar("NO TRANSACTION", bgcolor='yellow')
            self.reset()
            return

        def confirm(e):
            dlg.open = False
            self.page.update()

            # nb. do this just in case we must show login dialog
            # cf. https://github.com/flet-dev/flet/issues/1670
            time.sleep(0.1)

            self.authorized_action('pos.suspend', self.suspend_transaction,
                                   message="Suspend Transaction")

        def cancel(e):
            dlg.open = False
            self.reset()

        # prompt to suspend
        dlg = ft.AlertDialog(
            title=ft.Text("Confirm SUSPEND"),
            content=ft.Text("Really SUSPEND transaction?"),
            actions=[
                self.make_button(f"Yes, SUSPEND", font_size=self.default_font_size,
                                 height=self.default_button_size,
                                 width=self.default_button_size * 3,
                                 bgcolor='yellow',
                                 on_click=confirm),
                self.make_button("Cancel", font_size=self.default_font_size,
                                 height=self.default_button_size,
                                 width=self.default_button_size * 2.5,
                                 on_click=cancel),
            ])

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def suspend_transaction(self, user):
        session = self.app.make_session()
        batch = self.get_current_batch(session)
        user = session.get(user.__class__, user.uuid)
        handler = self.get_batch_handler()

        handler.suspend_transaction(batch, user)

        session.commit()
        session.close()
        self.clear_all()
        self.reset()

    def make_resume_button(self, **kwargs):
        return self.make_button("RESUME", bgcolor='purple',
                                font_size=self.default_font_size,
                                height=self.default_button_size,
                                width=self.default_button_size * 2,
                                on_click=self.resume_click)

    def resume_click(self, e):
        session = self.app.make_session()
        batch = self.get_current_batch(session, create=False)
        session.close()

        # can't resume if txn in progress
        if batch:
            self.show_snackbar("TRANSACTION IN PROGRESS", bgcolor='yellow')
            self.reset()
            return

        def select(uuid):
            session = self.app.make_session()
            user = self.get_current_user(session)
            handler = self.get_batch_handler()

            # TODO: this would need to work differently if suspended
            # txns are kept in a central server DB
            batch = session.get(self.app.model.POSBatch, uuid)

            batch = handler.resume_transaction(batch, user)
            session.commit()

            session.refresh(batch)
            self.load_batch(batch)
            session.close()

            dlg.open = False
            self.reset()

        def cancel(e):
            dlg.open = False
            self.reset()

        # prompt to choose txn
        dlg = ft.AlertDialog(
            title=ft.Text("Resume Transaction"),
            content=WuttaTransactionLookup(self.config, page=self.page, mode='resume',
                                           on_select=select, on_cancel=cancel),
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def get_current_user(self, session):
        uuid = self.page.session.get('user_uuid')
        if uuid:
            return session.get(self.model.User, uuid)

    def get_current_batch(self, session, user=None, create=True):
        handler = self.get_batch_handler()

        if not user:
            user = self.get_current_user(session)

        training = bool(self.page.session.get('training'))
        batch, created = handler.get_current_batch(user, training_mode=training,
                                                   create=create, return_created=True)

        if created:
            self.page.session.set('txn_display', handler.get_screen_txn_display(batch))
            self.informed_refresh()

        return batch

    def refresh_training(self):
        if self.page.session.get('training'):
            self.bgcolor = '#E4D97C'
        else:
            self.bgcolor = None

    def did_mount(self):
        session = self.app.make_session()
        batch = self.get_current_batch(session, create=False)
        if batch:
            self.load_batch(batch)
        else:
            self.page.session.set('txn_display', None)
            self.page.session.set('cust_uuid', None)
            self.page.session.set('cust_display', None)
            self.informed_refresh()

        self.refresh_training()

        # TODO: i think commit() was for when it auto-created the
        # batch, so that can go away now..right?
        #session.commit()
        session.close()
        self.page.update()

    def load_batch(self, batch):
        """
        Load the given batch as the current transaction.
        """
        handler = self.get_batch_handler()
        self.page.session.set('txn_display', handler.get_screen_txn_display(batch))
        self.page.session.set('cust_uuid', batch.customer_uuid)
        self.page.session.set('cust_display', handler.get_screen_cust_display(batch=batch))

        self.items.controls.clear()
        for row in batch.active_rows():
            self.add_row_item(row)
        self.items.scroll_to(offset=-1, duration=100)

        self.refresh_totals(batch)
        self.informed_refresh()

    def not_supported(self, e=None, feature=None):

        # test error handler
        if e.control.data and e.control.data.get('error'):
            raise RuntimeError("NOT YET SUPPORTED")

        text = "NOT YET SUPPORTED"
        if not feature and e:
            feature = e.control.content.value.replace('\n', ' ')
        if feature:
            text += f": {feature}"
        self.show_snackbar(text, bgcolor='yellow')
        self.page.update()

    def require_decimal(self, value):
        try:
            amount = decimal.Decimal(value)
        except decimal.InvalidOperation:
            self.show_snackbar(f"Amount is not valid: {value}", bgcolor='yellow')
            return False

        if '.' not in value:
            self.show_snackbar(f"Decimal point required: {value}", bgcolor='yellow')
            return False

        return amount

    def open_ring_click(self, e):
        value = self.main_input.value or None
        if not value:
            self.show_snackbar("Must first enter an amount")
            self.reset()
            return

        amount = self.require_decimal(value)
        if amount is False:
            self.reset()
            return

        def select(uuid):
            session = self.app.make_session()
            user = self.get_current_user(session)
            batch = self.get_current_batch(session, user=user)
            handler = self.get_batch_handler()

            quantity = 1
            if self.set_quantity.data is not None:
                quantity = self.set_quantity.data

            row = handler.add_open_ring(batch, uuid, amount, quantity=quantity, user=user)
            session.commit()

            self.add_row_item(row, scroll=True)
            self.refresh_totals(batch)
            session.close()

            dlg.open = False
            self.reset()

        def cancel(e):
            dlg.open = False
            self.reset(clear_quantity=False)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Department Lookup - for {self.app.render_currency(amount)} OPEN RING"),
            content=WuttaDepartmentLookup(self.config, on_select=select, on_cancel=cancel),
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def adjust_price_click(self, e):

        if not len(self.items.controls):
            self.show_snackbar("There are no line items", bgcolor='yellow')
            self.reset()
            return

        if not self.selected_item:
            self.show_snackbar("Must first select a line item", bgcolor='yellow')
            self.main_input.focus()
            self.page.update()
            return

        row = self.selected_item.data['row']
        if row.void or row.row_type not in (self.enum.POS_ROW_TYPE_SELL,
                                            self.enum.POS_ROW_TYPE_OPEN_RING):
            self.show_snackbar("This item cannot be adjusted", bgcolor='yellow')
            self.main_input.focus()
            self.page.update()
            return

        self.authorized_action('pos.override_price', self.adjust_price,
                               message="Adjust Price")

    def adjust_price(self, user):

        def cancel(e):
            dlg.open = False
            self.main_input.focus()
            self.page.update()

        def clear(e):
            price_override.value = ''
            price_override.focus()
            self.page.update()

        def tenkey_char(key):
            price_override.value = f"{price_override.value or ''}{key}"
            self.page.update()

        def confirm(e):
            price = self.require_decimal(price_override.value)
            if price is False:
                self.main_input.focus()
                self.page.update()
                return

            dlg.open = False

            session = self.app.make_session()
            user = self.get_current_user(session)
            handler = self.get_batch_handler()

            row = self.selected_item.data['row']
            row = session.get(row.__class__, row.uuid)

            new_row = handler.override_price(row, user, price)
            session.commit()

            # update screen to reflect new balance
            batch = row.batch
            self.refresh_totals(batch)

            # update item display
            self.selected_item.data['row'] = row
            self.selected_item.content.row = row
            self.selected_item.content.refresh()
            self.items.update()

            session.expunge_all()
            session.close()
            self.clear_item_selection()
            self.reset()

        row = self.selected_item.data['row']

        price = f'{row.txn_price:0.2f}'
        if self.main_input.value:
            try:
                price = decimal.Decimal(self.main_input.value)
            except decimal.InvalidOperation:
                pass
            else:
                price = f'{price:0.2f}'

        price_override = ft.TextField(value=price,
                                      text_size=32,
                                      text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                      autofocus=True,
                                      on_submit=confirm)

        current_price = self.app.render_currency(row.cur_price)
        if current_price:
            current_price += ' [{}]'.format(self.enum.PRICE_TYPE.get(row.cur_price_type,
                                                                     row.cur_price_type))

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Adjust Price"),
            content=ft.Container(
                ft.Column(
                    [
                        ft.Divider(),
                        ft.Row(
                            [
                                ft.Text("Reg Price:",
                                        size=32, weight=ft.FontWeight.BOLD),
                                ft.Text(self.app.render_currency(row.reg_price),
                                        size=32, weight=ft.FontWeight.BOLD),
                            ],
                        ),
                        ft.Row(),
                        ft.Row(
                            [
                                ft.Text("Cur Price:",
                                        size=32, weight=ft.FontWeight.BOLD),
                                ft.Text(current_price,
                                        size=32, weight=ft.FontWeight.BOLD),
                            ],
                        ),
                        ft.Row(),
                        ft.Row(),
                        ft.Row(
                            [
                                ft.Text("Txn Price:",
                                        size=32, weight=ft.FontWeight.BOLD),
                                ft.VerticalDivider(),
                                ft.Text("$", size=32, weight=ft.FontWeight.BOLD),
                                price_override,
                            ],
                        ),
                        ft.Row(),
                        ft.Row(),
                        ft.Row(
                            [
                                WuttaTenkeyMenu(self.config, simple=True,
                                                on_char=tenkey_char,
                                                on_enter=confirm),
                                self.make_button("Clear",
                                                 height=self.default_button_size * 0.8,
                                                 width=self.default_button_size * 1.2,
                                                 on_click=clear),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                    ],
                ),
                height=700,
                width=550,
            ),
            actions=[
                self.make_button("Cancel",
                                 height=self.default_button_size * 0.8,
                                 width=self.default_button_size * 1.2,
                                 on_click=cancel),
                self.make_button("Confirm",
                                 bgcolor='blue',
                                 height=self.default_button_size * 0.8,
                                 width=self.default_button_size * 1.2,
                                 on_click=confirm),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def toggle_training_mode(self, user):
        was_training = self.page.session.get('training')
        now_training = not was_training

        # TODO: hacky but works for now
        if not self.config.production():
            self.page.client_storage.set('training', now_training)

        self.page.session.set('training', now_training)

        self.refresh_training()
        self.informed_refresh()
        self.reset()

    def manager_click(self, e):

        def toggle_training(e):
            dlg.open = False
            self.page.update()

            session = self.app.make_session()
            batch = self.get_current_batch(session, create=False)
            session.close()
            if batch:
                self.show_snackbar("TRANSACTION IN PROGRESS")
                self.reset()

            else:
                # nb. do this just in case we must show login dialog
                # cf. https://github.com/flet-dev/flet/issues/1670
                time.sleep(0.1)

                training = self.page.session.get('training')
                toggle = "End" if training else "Start"
                self.authorized_action('pos.toggle_training', self.toggle_training_mode,
                                       message=f"{toggle} Training Mode")

        def cancel(e):
            dlg.open = False
            self.reset()

        font_size = 32
        toggle = "End" if self.page.session.get('training') else "Start"
        dlg = ft.AlertDialog(
            title=ft.Text("Manager Menu"),
            content=ft.Text("What would you like to do?", size=20),
            actions=[
                self.make_button(f"{toggle} Training",
                                 font_size=font_size,
                                 height=self.default_button_size,
                                 width=self.default_button_size * 2.5,
                                 bgcolor='yellow',
                                 on_click=toggle_training),
                self.make_button("Cancel",
                                 font_size=font_size,
                                 height=self.default_button_size,
                                 width=self.default_button_size * 2.5,
                                 on_click=cancel),
            ])

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def nosale_click(self, e):
        session = self.app.make_session()
        batch = self.get_current_batch(session, create=False)
        session.close()

        if batch:
            self.show_snackbar("TRANSACTION IN PROGRESS", bgcolor='yellow')
            self.page.update()
            return

        self.kick_drawer()

    def refund_click(self, e):
        self.show_snackbar("TODO: handle refund")
        self.page.update()

    def kick_drawer(self):
        self.show_snackbar("TODO: Drawer Kick", bgcolor='yellow')
        self.page.update()

    def add_row_item(self, row, scroll=False):

        # TODO: row types ugh
        if row.row_type not in (self.enum.POS_ROW_TYPE_SELL,
                                self.enum.POS_ROW_TYPE_OPEN_RING,
                                self.enum.POS_ROW_TYPE_TENDER,
                                self.enum.POS_ROW_TYPE_CHANGE_BACK):
            return

        self.items.controls.append(
            ft.Container(
                content=WuttaTxnItem(self.config, row),
                border=ft.border.only(bottom=ft.border.BorderSide(1, 'gray')),
                padding=ft.padding.only(5, 5, 5, 5),
                on_click=self.list_item_click,
                data={'row': row},
                key=row.uuid,
                bgcolor='white',
            ))

        if scroll:
            self.items.scroll_to(offset=-1, duration=100)

    def list_item_click(self, e):
        self.select_txn_item(e.control)

    def select_txn_item(self, item):
        if self.selected_item:
            self.clear_item_selection()

        self.selected_item = item
        self.selected_item.bgcolor = 'blue'
        self.page.update()

    def authorized_action(self, perm, action, cancel=None, message=None):
        auth = self.app.get_auth_handler()

        # current user is assumed if they have the perm
        session = self.app.make_session()
        user = self.get_current_user(session)
        has_perm = auth.has_permission(session, user, perm)
        session.expunge(user)
        session.close()
        if has_perm:
            action(user)
            return

        # otherwise must prompt for different user credentials...

        def login_cancel(e):
            dlg.open = False
            if cancel:
                cancel()
            self.reset()

        def login_failure(e):
            self.show_snackbar("Login failed", bgcolor='yellow')
            self.page.update()

        def authz_failure(user, user_display):
            self.show_snackbar(f"User does not have permission: {user_display}",
                               bgcolor='yellow')
            self.page.update()

        def login_success(user, user_display):
            dlg.open = False
            self.page.update()

            # nb. just in case next step requires a dialog
            # cf. https://github.com/flet-dev/flet/issues/1670
            time.sleep(0.1)

            action(user)
            self.reset()

        title = "Manager Override"
        if message:
            title = f"{title} - {message}"

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Container(
                ft.Column(
                    [
                        ft.Divider(),
                        WuttaLoginForm(self.config,
                                       perm_required=perm,
                                       on_login_success=login_success,
                                       on_login_failure=login_failure,
                                       on_authz_failure=authz_failure),
                    ],
                ),
                height=600,
            ),
            actions=[
                self.make_button("Cancel", on_click=login_cancel,
                                 height=80, width=120),
            ],
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def void_click(self, e):
        session = self.app.make_session()
        batch = self.get_current_batch(session, create=False)
        session.close()

        # nothing to void if no batch
        if not batch:
            self.show_snackbar("NO TRANSACTION", bgcolor='yellow')
            self.reset()
            return

        def confirm(e):
            dlg.open = False
            self.page.update()

            if self.selected_item:

                session = self.app.make_session()
                handler = self.get_batch_handler()
                user = self.get_current_user(session)
                batch = self.get_current_batch(session, user=user)

                # void line
                row = self.selected_item.data['row']
                if row.void:
                    # cannot void an already void line
                    self.show_snackbar("LINE ALREADY VOID", bgcolor='yellow')

                elif row.row_type not in (self.enum.POS_ROW_TYPE_SELL,
                                          self.enum.POS_ROW_TYPE_OPEN_RING):
                    # cannot void line unless of type 'sell'
                    self.show_snackbar("LINE DOES NOT ALLOW VOID", bgcolor='yellow')

                else:
                    # okay, void the line
                    row = session.get(row.__class__, row.uuid)
                    handler.void_row(row, user)
                    session.commit()

                    # refresh display
                    self.selected_item.data['row'] = row
                    self.selected_item.content.row = row
                    self.selected_item.content.refresh()
                    self.clear_item_selection()
                    self.refresh_totals(batch)

                session.close()
                self.reset()

            else: # void txn

                # nb. do this just in case we must show login dialog
                # cf. https://github.com/flet-dev/flet/issues/1670
                time.sleep(0.1)

                self.authorized_action('pos.void_txn', self.void_transaction,
                                       message="Void Transaction")

        def cancel(e):
            dlg.open = False
            self.reset()

        # prompt to void something
        target = 'LINE' if self.selected_item else 'TXN'
        dlg = ft.AlertDialog(
            title=ft.Text("Confirm VOID"),
            content=ft.Text(f"Really VOID {target}?"),
            actions=[
                self.make_button(f"VOID {target}", font_size=self.default_font_size,
                                 height=self.default_button_size,
                                 width=self.default_button_size * 2.5,
                                 bgcolor='red',
                                 on_click=confirm),
                self.make_button("Cancel", font_size=self.default_font_size,
                                 height=self.default_button_size,
                                 width=self.default_button_size * 2.5,
                                 on_click=cancel),
            ])

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def void_transaction(self, user):
        session = self.app.make_session()
        batch = self.get_current_batch(session)
        user = session.get(user.__class__, user.uuid)
        handler = self.get_batch_handler()

        handler.void_batch(batch, user)

        session.commit()
        session.close()
        self.clear_all()
        self.reset()

    def tender_click(self, e):
        session = self.app.make_session()
        handler = self.get_batch_handler()
        user = self.get_current_user(session)
        batch = self.get_current_batch(session, user=user, create=False)
        code = e.control.data['tender_code']
        tender = handler.get_tender(session, code)

        # nothing to do if no transaction
        if not batch:
            session.close()
            self.show_snackbar("NO TRANSACTION", bgcolor='yellow')
            self.reset()
            return

        # nothing to do if zero sales
        if not batch.get_balance():
            session.close()
            self.show_snackbar("NO SALES", bgcolor='yellow')
            self.reset()
            return

        # nothing to do if no amount provided
        if not self.main_input.value:
            session.close()
            self.show_snackbar("MUST SPECIFY AMOUNT", bgcolor='yellow')
            self.reset()
            return

        # nothing to do if amount not valid
        amount = self.require_decimal(self.main_input.value)
        if amount is False:
            session.close()
            self.reset()
            return

        # do nothing if @ quantity present
        if self.set_quantity.data:
            session.close()
            self.show_snackbar(f"QUANTITY NOT ALLOWED FOR TENDER: {self.set_quantity.value}",
                               bgcolor='yellow')
            self.reset()
            return

        # tender / execute batch
        try:

            # apply tender amount to batch
            # nb. this *may* execute the batch!
            # nb. we negate the amount supplied by user
            rows = handler.apply_tender(batch, user, tender or code, -amount)

        except Exception as error:
            session.rollback()
            log.exception("failed to apply tender '%s' for %s in batch %s",
                          code, amount, batch.id_str)
            self.show_snackbar(f"ERROR: {error}", bgcolor='red')

        else:
            session.commit()

            # update screen to reflect new items/balance
            for row in rows:
                self.add_row_item(row, scroll=True)
            self.refresh_totals(batch)

            # executed batch means txn was finalized
            if batch.executed:

                # look for "change back" row, if found then show alert
                last_row = rows[-1]
                if last_row.row_type == self.enum.POS_ROW_TYPE_CHANGE_BACK:

                    def close_bs(e):
                        # user dismissed the change back alert; clear screen
                        bs.open = False
                        bs.update()
                        self.clear_all()
                        self.reset()

                    bs = ft.BottomSheet(
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text("Change Due", size=24,
                                            weight=ft.FontWeight.BOLD),
                                    ft.Divider(),
                                    ft.Text("Please give customer their change:",
                                            size=20),
                                    ft.Text(self.app.render_currency(last_row.tender_total),
                                            size=32, weight=ft.FontWeight.BOLD),
                                    ft.Container(
                                        content=self.make_button("Dismiss", on_click=close_bs,
                                                                 height=80, width=120),
                                        alignment=ft.alignment.center,
                                        expand=1,
                                    ),
                                ],
                            ),
                            bgcolor='green',
                            padding=20,
                        ),
                        open=True,
                        dismissible=False,
                    )

                    # show change back alert
                    # nb. we do *not* clear screen yet
                    self.page.overlay.append(bs)

                else:
                    # txn finalized but no change back; clear screen
                    self.clear_all()

                # kick drawer if accepting any tender which requires
                # that, or if we are giving change back
                first_row = rows[0]
                if ((first_row.tender and first_row.tender.kick_drawer)
                    or last_row.row_type == self.enum.POS_ROW_TYPE_CHANGE_BACK):
                    self.kick_drawer()

        finally:
            session.close()

        self.reset()

    def clear_item_selection(self):
        if self.selected_item:
            self.selected_item.bgcolor = 'white'
            self.selected_item.content.refresh()
            self.selected_item = None

    def clear_all(self):
        self.items.controls.clear()

        self.subtotals.spans.clear()
        self.fs_balance.spans.clear()
        self.balances.spans.clear()
        self.totals_row.bgcolor = None

        self.page.session.set('txn_display', None)
        self.page.session.set('cust_uuid', None)
        self.page.session.set('cust_display', None)
        self.informed_refresh()

    def main_submit(self, e=None):
        if self.main_input.value:
            self.attempt_add_product(record_badscan=True)
        self.reset()
