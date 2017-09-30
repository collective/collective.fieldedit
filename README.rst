.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

====================
collective.fieldedit
====================

A flexible form to edit selected fields of a content type.


Features
--------

- Nice to use In popups
- Select the field or fields you want to edit
- You can also add fields to display or hidden
- Use the same widgets and validators as the default edit-form
- Respects schema-hints like field-permissions, invariants and widgets.

Use it by adding a link to the view ``@@field_edit_form`` and pass the fiels you want to edit as a query-string with up to three parameters separated by a ":" for each field.


Examples
--------

A link that opens the view to edit the title of this object in a modal:

.. code-block:: html

    <a href="${python:context.absolute_url()}/field_edit_form?fields=IBasic.title"
       class="pat-plone-modal"
       data-pat-plone-modal='{"actionOptions": {"reloadWindowOnClose": false, "redirectOnResponse": true},
                              "buttons": ".formControls > button",
                              "content": "#content-core"}'>
        Edit the Title in a modal
    </a>

Edit multiple fields:

.. code-block:: html

    <a href="${python:context.absolute_url()}/@@field_edit_form?fields=field1&amp;fields=field2&amp;fields=field3"
        Edit some fields.
    </a>

Display one field, edit another"

.. code-block:: html

    <a href="${python:context.absolute_url()}/@@field_edit_form?fields=field1:display&amp;fields=field2"
        Edit one field, display another.
    </a>

Hide the label:

.. code-block:: html

    <a href="${python:context.absolute_url()}/@@field_edit_form?amp;fields=field1::0"
        Edit one field, display another.
    </a>

Add a hidden field:

.. code-block:: html

    <a href="${python:context.absolute_url()}/@@field_edit_form?fields=field1:hidden&amp;fields=field2"
        Edit one field, display another.
    </a>

Behavior-fields need to be prefixed with the Bahavior:

.. code-block::

    <a href="${python:context.absolute_url()}/@@field_edit_form?fields=IBasic.title"
        Edit one field, display another.
    </a>


Documentation
-------------

TODO



Installation
------------

Install collective.fieldedit by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.fieldedit


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.fieldedit/issues
- Source Code: https://github.com/collective/collective.fieldedit


License
-------

The project is licensed under the GPLv2.
