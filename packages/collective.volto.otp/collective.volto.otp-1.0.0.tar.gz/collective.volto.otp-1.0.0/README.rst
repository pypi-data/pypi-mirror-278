.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/collective.volto.otp/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/collective.volto.otp/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/collective.volto.otp/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/collective.volto.otp?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/collective.volto.otp/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/collective.volto.otp

.. image:: https://img.shields.io/pypi/v/collective.volto.otp.svg
    :target: https://pypi.python.org/pypi/collective.volto.otp/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.volto.otp.svg
    :target: https://pypi.python.org/pypi/collective.volto.otp
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.volto.otp.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.volto.otp.svg
    :target: https://pypi.python.org/pypi/collective.volto.otp/
    :alt: License


====================
collective.volto.otp
====================

otp validator for emails

Features
--------

- Email validation by otp

RestAPI
=======


@validate-email-address
-----------------------

Send an message to the passed email wit OTP code to verify the address.
Returns a HTTP 204 in case of success or HTTP 400 in case the email is badly composed.::

> curl -i -X POST http://localhost:8080/Plone/my-form/@validate-email-address --data-raw '{"email": "email@email.com", "uid": "ffffffff"}' -H 'Accept: application/json' -H 'Content-Type: application/json'

parameters:

* `email` email address.
* `uid` uid related to email field

@validate-email-token
---------------------

Supposed to validate the OTP code received by the user via email.
Returns HTTP 204 in case of success or HTTP 400 in case of failure ::

> curl -i -X POST http://localhost:8080/Plone/my-form/@validate-email-token --data-raw '{"email": "email@email.com", "otp": "blahblahblah"}' -H 'Accept: application/json' -H 'Content-Type: application/json'

parameters:

* `email` email address
* `uid` uid used to generate the OTP
* `otp` OTP code


Translations
------------

This product has been translated into

- Italian


Installation
------------

Install collective.volto.otp by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.volto.otp


and then running ``bin/buildout``


Authors
-------

RedTurtle


Contributors
------------

Put your name here, you deserve it!

- folix-01


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.volto.otp/issues
- Source Code: https://github.com/collective/collective.volto.otp
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.
