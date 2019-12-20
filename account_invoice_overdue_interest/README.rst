.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
Overdue Interest for Invoices
=============================

* Enables setting overdue interest rate percents for customers as well as
  individual invoices

Configuration
=============

* Set the default interest rate in Accounting -> Configuration -> Settings
* Optional: define custom interest rates for specific partners in Sales 
  -> Customers

Usage
=====

* Create a new invoice. If a partner has a custom interest rate, that one is
  suggested. Otherwise, the default one is suggested.

Known issues / Roadmap
======================

* Note that this module only provides an extra field to be used with PDF 
  prints, accounting integrations etc. It has no functionality related to e.g. 
  creating reminder invoices with increased totals, if the original invoice was
  not paid in time.

Credits
=======

Contributors
------------
* Timo Talvitie <timo.talvitie@tawasta.fi>
* Oskars Zālītis <oskars.zalitis@avoin.systems>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.