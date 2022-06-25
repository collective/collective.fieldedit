# -*- coding: utf-8 -*-
from collective.fieldedit.field_edit_form import check_permission
from collective.fieldedit.field_edit_form import check_write_permission
from collective.fieldedit.testing import (  # noqa: E501
    COLLECTIVE_FIELDEDIT_FUNCTIONAL_TESTING,
)
from collective.fieldedit.testing import COLLECTIVE_FIELDEDIT_INTEGRATION_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.textfield.value import RichTextValue
from plone.testing.z2 import Browser

import transaction
import unittest


try:
    from Products.CMFPlone.factory import PLONE52MARKER  # noqa: F401

    RICHTEXT = "IRichTextBehavior"
except ImportError:
    # before Plone 5.2:
    RICHTEXT = "IRichText"


class TestFieldEditForm(unittest.TestCase):

    layer = COLLECTIVE_FIELDEDIT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        login(self.portal, SITE_OWNER_NAME)
        self.doc = api.content.create(
            container=self.portal,
            type="Document",
            id="welcome_page",
            title=u"Willkommen",
            text=RichTextValue(u"Söme Täxt", "text/html", "text/x-html-safe"),
        )

    def test_get_widget_markup(self):
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        html = view.get_widget(fieldname="{}.text".format(RICHTEXT))
        self.assertIn(' name="form.widgets.{}.text"'.format(RICHTEXT), html)

    def test_get_widget_markup_display(self):
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        html = view.get_widget(fieldname="IDublinCore.title", fieldmode="display")
        self.assertNotIn(' name="form.widgets.IDublinCore.title"', html)
        self.assertIn(' id="form-widgets-IDublinCore-title"', html)

    def test_get_widget_from_request(self):
        self.request["fieldname"] = "IDublinCore.title"
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        html = view.get_widget(fieldname="IDublinCore.title")
        self.assertIn(' name="form.widgets.IDublinCore.title"', html)

    def test_field_edit_form_render(self):
        self.request["fields"] = ["IDublinCore.title"]
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        html = view.render()
        self.assertIn(' name="form.widgets.IDublinCore.title"', html)
        self.assertIn("welcome_page/@@field_edit_form", html)

    def test_field_edit_form_render_display(self):
        self.request["fields"] = ["IDublinCore.title:display"]
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        html = view.render()
        self.assertNotIn(' name="form.widgets.IDublinCore.title"', html)
        self.assertIn(' id="form-widgets-IDublinCore-title"', html)
        self.assertIn("welcome_page/@@field_edit_form", html)

    def test_field_edit_form_submit(self):
        self.assertEqual(self.doc.title, u"Willkommen")
        new_title = u"Huhuhu"
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        view.request.form["form.widgets.IDublinCore.title"] = new_title
        view.handleApply(view, None)
        self.assertEqual(self.doc.title, new_title)

    def test_field_edit_form_submit_with_behavior_field(self):
        self.assertFalse(self.doc.table_of_contents)
        self.request["fields"] = ["ITableOfContents.table_of_contents"]
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        view.request.form[
            "form.widgets.ITableOfContents.table_of_contents"
        ] = u"selected"  # noqa: E501
        view.handleApply(view, None)
        self.assertTrue(self.doc.table_of_contents)

    def test_field_edit_form_validation(self):
        self.assertFalse(self.doc.table_of_contents)
        self.request["fields"] = ["IDublinCore.effective"]
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        html = view.render()
        self.assertIn(' name="form.widgets.IDublinCore.effective"', html)
        self.assertNotIn('>Required input is missing.<', html)
        view.request.form["form.widgets.IDublinCore.effective"] = u"unexpected"
        view.handleApply(view, None)
        self.assertEqual(view.status, u"There were some errors.")
        html = view.render()
        self.assertIn(' name="form.widgets.IDublinCore.effective"', html)
        self.assertIn(
            '>The system could not process the given value.<',
            html,
        )  # noqa: E501

    def test_field_edit_form_required(self):
        self.request["fields"] = ["IDublinCore.title"]
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        view.request.form["form.widgets.IDublinCore.title"] = u""
        view.handleApply(view, None)
        self.assertEqual(view.status, u"There were some errors.")
        html = view.render()
        self.assertIn('>Required input is missing.<', html)

    def test_multifield_edit_form_submit(self):
        self.assertEqual(self.doc.title, u"Willkommen")
        self.assertEqual(self.doc.description, u"")
        new_title = u"Huhuhu"
        new_desc = u"hahaha"
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        view.request.form["form.widgets.IDublinCore.title"] = new_title
        view.request.form["form.widgets.IDublinCore.description"] = new_desc
        view.handleApply(view, None)
        self.assertEqual(self.doc.title, new_title)
        self.assertEqual(self.doc.description, new_desc)

    def test_multifield_edit_form_render(self):
        self.request["fields"] = ["IDublinCore.title", "IDublinCore.description"]
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        html = view.render()
        self.assertIn(' name="form.widgets.IDublinCore.title"', html)
        self.assertIn(' name="form.widgets.IDublinCore.description"', html)
        self.assertIn("welcome_page/@@field_edit_form", html)

    def test_multifield_edit_form_label(self):
        self.request["fields"] = [
            "IShortName.id:input:yes",
            "IDublinCore.subjects",
        ]
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        html = view.render()
        self.assertIn(' name="form.widgets.IShortName.id"', html)
        self.assertIn(' name="form.widgets.IDublinCore.subjects"', html)
        self.assertIn(' for="form-widgets-IShortName-id"', html)
        self.assertIn(' for="form-widgets-IDublinCore-subjects"', html)
        self.assertNotIn(
            '<span id="form-widgets-IShortName-id" class="text-widget asciiline-field">welcome_page</span>',
            html,
        )  # noqa: E501
        self.assertNotIn(
            '<span id="form-widgets-IDublinCore-subjects" class="text-widget tuple-field">',
            html,
        )  # noqa: E501
        self.assertIn("welcome_page/@@field_edit_form", html)

        self.request["fields"] = [
            "IShortName.id::false",
            "IDublinCore.subjects::no",
        ]
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        html = view.render()
        self.assertIn(' name="form.widgets.IShortName.id"', html)
        self.assertIn(' name="form.widgets.IDublinCore.subjects"', html)
        self.assertNotIn(' for="form-widgets-IShortName-id"', html)
        self.assertNotIn(' for="form-widgets-IDublinCore-subjects"', html)
        self.assertNotIn(
            '<span id="form-widgets-IShortName-id" class="text-widget asciiline-field">welcome_page</span>',
            html,
        )  # noqa: E501
        self.assertNotIn(
            '<span id="form-widgets-IDublinCore-subjects" class="text-widget tuple-field">',
            html,
        )  # noqa: E501

        self.request["fields"] = [
            "IShortName.id:display:false",
            "IDublinCore.subjects:display:0",
        ]
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        html = view.render()
        self.assertNotIn(' name="form.widgets.IShortName.id"', html)
        self.assertNotIn(' name="form.widgets.IDublinCore.subjects"', html)
        self.assertNotIn(' for="form-widgets-IShortName-id"', html)
        self.assertNotIn(' for="form-widgets-IDublinCore-subjects"', html)
        self.assertIn(
            '<span id="form-widgets-IShortName-id" class="text-widget asciiline-field">welcome_page</span>',
            html,
        )  # noqa: E501
        self.assertIn(
            '<span id="form-widgets-IDublinCore-subjects" class="text-widget tuple-field">',
            html,
        )  # noqa: E501

        self.request["fields"] = ["nofield"]
        view = api.content.get_view("field_edit_form", self.doc, self.request)
        view.update()
        html = view.render()
        self.assertNotIn("nofield", html)


class TestDecisionFieldEditForm(unittest.TestCase):

    layer = COLLECTIVE_FIELDEDIT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

    def test_field_permissions_are_observed(self):
        login(self.portal, SITE_OWNER_NAME)
        from plone.autoform.interfaces import READ_PERMISSIONS_KEY
        from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
        from plone.dexterity.schema import SCHEMA_CACHE
        from plone.namedfile import NamedBlobFile

        file_schema = SCHEMA_CACHE.get("File")

        file_schema.setTaggedValue(
            WRITE_PERMISSIONS_KEY,
            {
                "title": u"cmf.ReviewPortalContent",
                "file": u"cmf.ManagePortal",
            },
        )
        file_schema.setTaggedValue(
            READ_PERMISSIONS_KEY, {"file": u"cmf.ReviewPortalContent"}
        )

        item = api.content.create(
            container=self.portal,
            type="File",
            id="testfile",
            title=u"I have a secret file!",
            description=u"The description",
            file=NamedBlobFile(filename=u"testfile.txt", data="Data"),
        )
        logout()

        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ["Editor", "Reviewer", "Manager"])
        self.assertTrue(
            api.user.has_permission(
                "Modify portal content", username=TEST_USER_NAME, obj=item
            )
        )  # noqa: E501
        self.assertTrue(
            api.user.has_permission(
                "Review portal content", username=TEST_USER_NAME, obj=item
            )
        )  # noqa: E501
        self.assertTrue(
            api.user.has_permission("Manage portal", username=TEST_USER_NAME, obj=item)
        )  # noqa: E501
        self.assertTrue(check_write_permission(item, "title"))
        self.assertTrue(check_write_permission(item, "description"))
        self.assertTrue(check_write_permission(item, "file"))

        self.assertIsNone(check_permission("mich_gibs_nich"))
        self.request["fields"] = ["title", "description", "file"]
        view = api.content.get_view("field_edit_form", item, self.request)
        html = view()
        self.assertIn(
            u'value="I have a secret file!" type="text" />',
            html,
        )  # noqa: E501
        self.assertIn(
            u'>The description</textarea>',
            html,
        )  # noqa: E501
        self.assertIn(
            'name="form.widgets.file"',
            html,
        )  # noqa: E501

        setRoles(self.portal, TEST_USER_ID, ["Editor", "Reviewer"])
        self.assertTrue(
            api.user.has_permission(
                "Modify portal content", username=TEST_USER_NAME, obj=item
            )
        )  # noqa: E501
        self.assertTrue(
            api.user.has_permission(
                "Review portal content", username=TEST_USER_NAME, obj=item
            )
        )  # noqa: E501
        self.assertFalse(
            api.user.has_permission("Manage portal", username=TEST_USER_NAME, obj=item)
        )  # noqa: E501
        self.assertTrue(check_write_permission(item, "title"))
        self.assertTrue(check_write_permission(item, "description"))
        self.assertFalse(check_write_permission(item, "file"))
        view = api.content.get_view("field_edit_form", item, self.request)
        html = view()
        self.assertIn(
            u'value="I have a secret file!" type="text" />',
            html,
        )  # noqa: E501
        self.assertIn(
            u'>The description</textarea>',
            html,
        )  # noqa: E501
        self.assertNotIn(
            'name="form.widgets.file"',
            html,
        )  # noqa: E501

        setRoles(self.portal, TEST_USER_ID, ["Editor"])
        self.assertTrue(
            api.user.has_permission(
                "Modify portal content", username=TEST_USER_NAME, obj=item
            )
        )  # noqa: E501
        self.assertFalse(
            api.user.has_permission(
                "Review portal content", username=TEST_USER_NAME, obj=item
            )
        )  # noqa: E501
        self.assertFalse(
            api.user.has_permission("Manage portal", username=TEST_USER_NAME, obj=item)
        )  # noqa: E501
        self.assertFalse(check_write_permission(item, "title"))
        self.assertTrue(check_write_permission(item, "description"))
        self.assertFalse(check_write_permission(item, "file"))
        view = api.content.get_view("field_edit_form", item, self.request)
        html = view()
        self.assertNotIn(
            u'value="I have a secret file!"',
            html,
        )  # noqa: E501
        self.assertIn(
            u'>The description</textarea>',
            html,
        )  # noqa: E501
        self.assertNotIn(
            'name="form.widgets.file"',
            html,
        )  # noqa: E501


class TestFieldEditFormFunctional(unittest.TestCase):

    layer = COLLECTIVE_FIELDEDIT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.browser = Browser(self.layer["app"])
        self.browser.handleErrors = False
        self.browser.addHeader(
            "Authorization",
            "Basic {0}:{1}".format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        login(self.portal, SITE_OWNER_NAME)
        self.doc = api.content.create(
            container=self.portal,
            type="Document",
            id="welcome_page",
            title=u"Willkommen",
            text=RichTextValue(u"Söme Täxt", "text/html", "text/x-html-safe"),
        )
        transaction.commit()

    def test_render_form(self):
        doc_url = self.doc.absolute_url()
        self.doc.subject = (u"Krazy Keyword",)
        self.browser.open(
            doc_url
            + "/@@field_edit_form?fields=IDublinCore.title&fields={}.text&autofocus=True".format(RICHTEXT)  # noqa W503
        )  # noqa: E501
        self.assertEqual(
            self.browser.getControl(
                name="form.widgets.IDublinCore.title"
            ).value,  # noqa: E501
            "Willkommen",
        )
        self.browser.getControl(
            name="form.widgets.IDublinCore.title"
        ).value = "Was ist das?"  # noqa: E501
        self.browser.getControl(
            name="form.widgets.{}.text".format(RICHTEXT)
        ).value = "<p>Warum?</p>"  # noqa: E501
        self.browser.getControl(name="form.buttons.save").click()
        self.assertEqual(self.doc.title, u"Was ist das?")
        self.assertEqual(self.doc.text.raw, u"<p>Warum?</p>")

        self.browser.open(
            doc_url
            + "/@@field_edit_form?fields={}.text:display&fields=IDublinCore.description".format(RICHTEXT)  # noqa W503
        )  # noqa: E501
        with self.assertRaises(LookupError):
            self.browser.getControl(name="form.widgets.{}.text".format(RICHTEXT))
        self.assertIn("Warum?", self.browser.contents)
        self.assertIn(
            'data-fieldname="form.widgets.{}.text"'.format(RICHTEXT),
            self.browser.contents,
        )

        qs = "?fields=ITableOfContents.table_of_contents:hidden&fields=IDublinCore.subjects:input"  # noqa: E501
        self.browser.open(doc_url + "/@@field_edit_form" + qs)
        with self.assertRaises(LookupError):
            self.browser.getControl(
                name="form.widgets.ITableOfContents.table_of_contents"
            )  # noqa: E501

        self.browser.getControl(
            name="form.widgets.IDublinCore.subjects"
        ).value = "Some Keyword;Another"  # noqa: E501
        self.browser.getControl(name="form.buttons.save").click()
        self.assertEqual(self.doc.subject, (u"Some Keyword", u"Another"))

    def test_render_form_with_validationerror(self):
        doc_url = self.doc.absolute_url()
        self.doc.subject = (u"Krazy Keyword",)
        self.browser.open(
            doc_url
            + "/@@field_edit_form?fields=IDublinCore.title&fields={}.text".format(RICHTEXT) # noqa W503
        )  # noqa: E501
        self.assertEqual(
            self.browser.getControl(
                name="form.widgets.IDublinCore.title"
            ).value,  # noqa: E501
            "Willkommen",
        )
        self.browser.getControl(
            name="form.widgets.IDublinCore.title"
        ).value = ""  # noqa: E501
        self.browser.getControl(
            name="form.widgets.{}.text".format(RICHTEXT)
        ).value = "<p>Warum?</p>"  # noqa: E501
        self.browser.getControl(name="form.buttons.save").click()
        self.assertIn(
            '>Required input is missing.<', self.browser.contents
        )  # noqa: E501
        self.assertEqual(
            self.browser.url, "http://nohost/plone/welcome_page/@@field_edit_form"
        )  # noqa: E501

        self.browser.getControl(
            name="form.widgets.IDublinCore.title"
        ).value = ""  # noqa: E501
        self.browser.getControl(name="form.buttons.save").click()
        self.assertIn(
            '>Required input is missing.<', self.browser.contents
        )  # noqa: E501
        self.assertEqual(
            self.browser.url, "http://nohost/plone/welcome_page/@@field_edit_form"
        )  # noqa: E501

        self.browser.getControl(
            name="form.widgets.IDublinCore.title"
        ).value = "äöü"  # noqa: E501
        self.browser.getControl(name="form.buttons.save").click()
        self.assertEqual(self.doc.title, u"äöü")
        self.assertEqual(self.doc.text.raw, u"<p>Warum?</p>")
