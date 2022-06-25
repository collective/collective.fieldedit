.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://img.shields.io/pypi/v/collective.fieldedit.svg
    :target: https://pypi.python.org/pypi/collective.fieldedit/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.fieldedit.svg
    :target: https://pypi.python.org/pypi/collective.fieldedit
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.fieldedit.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.fieldedit.svg
    :target: https://pypi.python.org/pypi/collective.fieldedit/
    :alt: License


====================
collective.fieldedit
====================

A view to edit selected fields of a content type.


Features
--------

- Useable by simply calling a view with a the fields you want to edit as query-string-parameters
- Select the field or fields you want to edit
- For each field you can choose between input, display and hidden
- Uses the same widgets and validators as the default edit-form
- Respects schema-hints like field-permissions, invariants and widgets
- Nice to use in modals/popups fo allow editing one ore more fields (but not all)

Use it by adding a link to the view ``@@field_edit_form`` and pass the fiels you want to edit as a query-string with up to three parameters separated by a ":" for each field.


Examples
--------

Edit the text of a document::

    http://localhost:8080/Plone/front-page/@@field_edit_form?fields=IRichTextBehavior.text

Edit the fields title and subjects::

    http://localhost:8080/Plone/front-page/@@field_edit_form?fields=IDublinCore.subjects&fields=IDublinCore.title

Display the text and edit the publishing date::

    http://localhost:8080/Plone/front-page/@@field_edit_form?fields=IRichTextBehavior.text:display:0&fields=IRelatedItems.relatedItems

Render a link to edit the title in a modal:

.. code-block::

    <a href="${python:context.absolute_url()}/field_edit_form?fields=IDublinCore.title"
       class="pat-plone-modal"
       data-pat-plone-modal='{"actionOptions": {"reloadWindowOnClose": false, "redirectOnResponse": true, "disableAjaxFormSubmit": true},
                              "buttons": ".formControls > button"'>
        Edit the Title in a modal
    </a>

Edit multiple fields:

.. code-block::

    <a href="${python:context.absolute_url()}/@@field_edit_form?fields=field1&amp;fields=field2&amp;fields=field3"
        Edit some fields.
    </a>

Display one field, edit another"

.. code-block::

    <a href="${python:context.absolute_url()}/@@field_edit_form?fields=field1:display&amp;fields=field2"
        Edit one field, display another.
    </a>

Hide the label:

.. code-block::

    <a href="${python:context.absolute_url()}/@@field_edit_form?fields=field1::0"
        Edit one field, display another.
    </a>

Add a hidden field:

.. code-block::

    <a href="${python:context.absolute_url()}/@@field_edit_form?fields=field1:hidden&amp;fields=field2"
        Edit one field, display another.
    </a>

Behavior-fields need to be prefixed with the Behavior:

.. code-block::

    <a href="${python:context.absolute_url()}/@@field_edit_form?fields=IBasic.title"
        Edit one field, display another.
    </a>


Supported Versions
------------------

collective.fieldedit is tested in Plone 5.1, 5.2 and 6.


Installation
------------

Install collective.fieldedit by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.fieldedit


and then running ``bin/buildout``

Then got to the add-on controlpanel (``/prefs_install_products_form``) to enable it.

Contribute
----------

- Issue Tracker: https://github.com/collective/collective.fieldedit/issues
- Source Code: https://github.com/collective/collective.fieldedit


License
-------

The project is licensed under the GPLv2.
