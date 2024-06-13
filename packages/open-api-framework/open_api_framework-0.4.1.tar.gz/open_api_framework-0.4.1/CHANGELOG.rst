Changelog
=========

0.4.1 (2024-06-13)
------------------

**Bugfixes**

* Add ``ordered_model`` to ``INSTALLED_APPS`` (required for ``django-admin-index``)
* Add ``two_factor.plugins.webauthn`` to ``INSTALLED_APPS`` (required for ``maykin_2fa``)

0.4.0 (2024-06-06)
------------------

**New features**

* Add django-setup-configuration to deps
* Add ELASTIC_APM_TRANSACTION_SAMPLE_RATE

0.3.0 (2024-05-17)
------------------

**New features**

* [#14] Add django-log-outgoing-requests to deps
* [open-zaak/open-zaak#1629] Add generic base settings file


0.2.0 (2024-03-22)
------------------

**New features**

* Add support for python 3.10
* Upgrade to Django 4.2
* Add maykin-2fa


0.1.0 (2024-01-30)
------------------

* Initial release as a metapackage to pin several dependencies
