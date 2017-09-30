# -*- coding: utf-8 -*-
from collective.fieldedit import _
from plone import api
from plone.autoform.interfaces import READ_PERMISSIONS_KEY
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.dexterity.browser import edit
from plone.dexterity.events import EditFinishedEvent
from plone.dexterity.utils import iterSchemata
from plone.supermodel.utils import mergedTaggedValueDict
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form import interfaces
from zope.component import queryUtility
from zope.event import notify
from zope.security.interfaces import IPermission

import logging


logger = logging.getLogger(__name__)


class FieldEditForm(edit.DefaultEditForm):
    """Edit arbitrary fields of a content.

    Good to be used in modals.
    Has working inline-validation and such :-)
    """

    template = ViewPageTemplateFile('field_edit_form.pt')

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):  # noqa
        # override widget modes to ignore all other fields
        prefix = 'form.widgets.'
        field_ids = [k.split(prefix)[-1] for k in self.request.form.keys()]
        self.request.set('fields', field_ids)
        # set all widgets to display to prevent saving data
        self.set_all_widgets_mode(interfaces.DISPLAY_MODE)

        # change the custom_form_fields to input-mode
        self.set_widgets_mode(field_ids, interfaces.INPUT_MODE)

        # the rest is the original code
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        api.portal.show_message(self.success_message, self.request)
        self.request.response.redirect(self.nextURL())
        notify(EditFinishedEvent(self.context))

    def fields_info(self, fields=None):
        """Get info about the fields and their modes from the query-string.

        Split a query-string into a list if dicts:
        Schema: fieldname:fieldmode:label. mode and label are optional.
        Example:
        @@field_edit_form?fields=somefield&fields=IBasic.title:display:0
        &fields=accountable:hidden&fields=another::no
        Will result in:
        [{'fieldname': 'somefield', 'fieldmode': 'input', 'label': True},
         {'fieldname': 'IBasic.title', 'fieldmode': 'display', 'label': False},
         {'fieldname': 'accountable', 'fieldmode': 'hidden', 'label': True},
         {'fieldname': 'another', 'fieldmode': 'input', 'label': False}]
        """
        results = []
        if not fields:
            return
        if not isinstance(fields, list):
            fields = [fields]
        # Make sure we use the order from the schema
        # This is needed to keep the order during validation-errors
        sorted_fields = []
        for fieldname in self.fields.keys() + fields:
            if fieldname not in sorted_fields and fieldname in fields:
                sorted_fields.append(fieldname)
        for fieldname in sorted_fields:
            fieldmode = interfaces.INPUT_MODE
            label = True
            mode = None
            if ':' in fieldname:
                values = fieldname.split(':')
                if len(values) == 2:
                    fieldname, mode = values
                elif len(values) == 3:
                    fieldname, mode, label = values
                    if label.lower() in ['0', 'false', 'no']:
                        label = False
            if mode and mode in [interfaces.INPUT_MODE, interfaces.DISPLAY_MODE, interfaces.HIDDEN_MODE]:  # noqa
                fieldmode = str(mode)
            results.append({
                'fieldname': fieldname,
                'fieldmode': fieldmode,
                'label': label,
            })
        return results

    def get_widget(self, fieldname=None, fieldmode=None, label=True, autofocus=False):  # noqa
        fieldname = fieldname or self.request.get('fieldname')
        fieldmode = fieldmode or self.request.get('fieldmode') or interfaces.INPUT_MODE  # noqa
        label = label or self.request.get('label')
        if not fieldname:
            return
        widget = self.find_widget(fieldname)
        if widget:
            if fieldmode == interfaces.DISPLAY_MODE \
                    and not check_read_permission(self.context, fieldname):
                # skip if display-mode and cannot view
                return
            if fieldmode in [interfaces.INPUT_MODE, interfaces.HIDDEN_MODE] \
                    and not check_write_permission(self.context, fieldname):
                # skip if edit- or hidden-mode and cannot write
                return
            widget.mode = fieldmode
            fieldclass = widget.klass
            # return wrapped or non-wrapped field element
            if not label:
                widget_view = widget.render
            else:
                widget_view = api.content.get_view(
                    'ploneform-render-widget', widget, self.request)
            # apply autofocus attribute
            if autofocus and fieldclass:
                field_hooks = {
                    'textline-field': 'type=\"text\"',
                    'list-field': 'type=\"text\"',
                    'richtext-field': 'textarea',
                }
                for key in field_hooks.keys():
                    if key in fieldclass:
                        hook = field_hooks[key]
                        widget_view = widget_view()
                        widget_view = widget_view.replace(hook, hook + ' autofocus=\"\"', 1)  # noqa
                        return widget_view
            return widget_view()

    def set_all_widgets_mode(self, mode):
        for widget in self.widgets.values():
            widget.mode = mode
        group_widgets = [widget for group in self.groups for widget
                         in group.widgets.values()]
        for widget in group_widgets:
            widget.mode = mode

    def set_widgets_mode(self, field_ids, mode):
        for field_id in field_ids:
            widget = self.find_widget(field_id.replace('-empty-marker', ''))
            if widget:
                widget.mode = mode

    def find_widget(self, field_id):
        """Return a widget for any field in the schema and behaviors."""
        widget = self.widgets.get(field_id, None)
        if not widget:
            for group in self.groups:
                widget = group.widgets.get(field_id, None)
                if widget:
                    break
        if widget:
            return widget


def check_write_permission(obj, field_id):
    permission = taggedvalue_for_field(obj, field_id, WRITE_PERMISSIONS_KEY)
    if permission:
        return check_permission(permission, obj=obj)
    return True


def check_read_permission(obj, field_id):
    permission = taggedvalue_for_field(obj, field_id, READ_PERMISSIONS_KEY)
    if permission:
        return check_permission(permission, obj=obj)
    return True


def taggedvalue_for_field(obj, field_id, key):
    """Get tagged value for a field by value-key.
    """
    field_id = field_id.split('.')[-1]
    for schema in iterSchemata(obj):
        taggedvalues = mergedTaggedValueDict(schema, key)
        taggedvalue = taggedvalues.get(field_id)
        if taggedvalue:
            return taggedvalue


def check_permission(permission_id, obj=None):
    """Turn a permission-id into a permission and check for it.
    """
    permission = queryUtility(IPermission, name=permission_id)
    if permission:
        return api.user.has_permission(permission.title, obj=obj)
    else:
        logger.info('Permission {0} not found!'.format(permission_id))
