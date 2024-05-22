from odoo.tests.common import TransactionCase


class TestOverdueInterest(TransactionCase):
    # Test overdue interest

    def setUp(self):
        super().setUp()

        # Set default overdue interest
        self.env["res.company"].search([]).write({"overdue_interest": 11.5})

        self.ResPartner = self.env["res.partner"]

        # Set up partners with and without overdue interest
        self.partner1 = self.ResPartner.create(
            dict(name="Yritys Oy", overdue_interest="10.0")
        )

        self.partner2 = self.ResPartner.create(dict(name="Firma Oy"))

    def test_overdue_interest(self):
        inv = self.env["account.move"].create({"partner_id": self.partner1.id})
        # This should use the partner-spesific overdue interest
        self.assertEqual(inv.overdue_interest, 10.0)

    def test_default_overdue_interest(self):
        inv = self.env["account.move"].create({"partner_id": self.partner2.id})
        # This should use the default overdue interest from company
        self.assertEqual(inv.overdue_interest, 11.5)
