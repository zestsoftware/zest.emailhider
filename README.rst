Zest emailhider
===============

This document describes the zest.emailhider package.

.. image:: https://secure.travis-ci.org/zestsoftware/zest.emailhider.png?branch=master
  :target: https://travis-ci.org/#!/zestsoftware/zest.emailhider


Dependencies
------------

This package depends on jquery.pyproxy to integrate python code with
jquery code.


Overview
--------

This package provides a mechanism to hide email addresses with
JavaScript.  Or actually: with this package you can hide your email
addresses by default so they are never in the html; with javascript
the addresses are then fetched and displayed.

For every content item in your site you can have exactly one email
address, as we look up the email address for an object by its UID.
For objects for which you want this you should register a simple
adapter to the IMailable interface, so we can ask this adapter for an
``email`` attribute and a ``UID`` method.   The 'emailhider' view is
provided to generate the placeholder link.

Objects display a placeholder link with a ``hidden-email`` class, a
``uid`` rel attribute and a ``email-uid-<some uid>`` class set to the
UID of an object; when the page is loaded some jQuery is run to make a
request for all those links to replace them with a 'mailto' link for
that object.  Using this mechanism the email address isn't visible in
the initial page load, and it requires JavaScript to be seen - so it
is much harder for spammers to harvest.

Special case: when the uid contains 'email' or 'address' it is clearly
no real uid.  In that case we do nothing with the IMailable interface
but we try to get a property with this 'uid' from the property sheet
of the portal.  Main use case is of course the 'email_from_address',
but you can add other addresses as well, like 'info_email'.  If you
want to display the email_from address in for example a static portlet
on any page in the site, use this html code::

  <a class="hidden-email email-uid-email_from_address"
     rel="email_from_address">
     Activate JavaScript to see this address.</a>

You can load the ``test_emailhider`` page to see if this works.


Instructions for your own package
---------------------------------

What do you need to do if you want to use this in your own package,
for your own content type?

First you need to make your content type adaptable to the IMailable
interface, either directly or via an adapter.

If your content type already has a ``UID`` method (like all Archetypes
content types) and an ``email`` attribute, you can use some zcml like
this::

  <class class=".content.MyContentType">
    <implements interface="zest.emailhider.interfaces.IMailable" />
  </class>

If not, then you need to register an adapter for your content type
that has this method and attribute.  For example something like this::

  from zope.component import adapts
  from zope.interface import implements
  from zest.emailhider.interfaces import IMailable
  from your.package.interfaces import IMyContentType

  class MailableAdapter(object):
      adapts(IMyContentType)
      implements(IMailable)

      def __init__(self, context):
          self.context = context

      def UID(self):
          return self.context.my_special_uid_attribute

      @property
      def email(self):
          return self.context.getSomeContactAddress()

Second, in the page template of your content type you need to add code
to show the placeholder text instead of the real email address::

  <span>For more information contact us via email:</span>
  <span tal:replace="structure context/@@emailhider" />

Note that if you want this to still work when zest.emailhider is not
installed, you can use this code instead::

  <span tal:replace="structure context/@@emailhider|context/email" />

This shows the unprotected plain text email when zest.emailhider is is
not available.  When you are using zest.emailhider 2.6 or higher this
works a bit better, as we have introduced an own browser layer: the
@@emailhider page is only available when zest.emailhider is actually
installed in the Plone Site.  This also makes it safe to use
zest.emailhider when you have more than one Plone Site in a single
Zope instance and want emailhider to only be used in one them.

Note that the generated code in the template is very small, so you
can also look at the page template in zest.emailhider and copy some
code from there and change it to your own needs.  As long as your
objects can be found by UID in the uid_catalog and your content type
can be adapted to IMailable to get the email attribute, it should all
work fine.


Note on KSS usage in older releases
-----------------------------------

Older releases (until and including 1.3) used KSS instead of jQuery.
As our functionality should of course also work for anonymous users,
we had to make KSS publicly accessible.  So all javascript that was
needed for KSS was loaded for anonymous users as well.

We cannot undo that automatically, as the package has no way of
knowing if the same change was needed by some other package or was
done for other valid reasons by a Manager.  So you should check the
javascript registry in the ZMI and see if this needs to be undone so
anonymous users no longer get the kss javascripts as they no longer
need that.

For reference, this is the normal line in the Condition field of
``++resource++kukit.js`` (all on one line)::

  python: not
  here.restrictedTraverse('@@plone_portal_state').anonymous() and
  here.restrictedTraverse('@@kss_devel_mode').isoff()

and this is the normal line in the Condition field of
``++resource++kukit-devel.js`` (all on one line)::

  python: not
  here.restrictedTraverse('@@plone_portal_state').anonymous() and
  here.restrictedTraverse('@@kss_devel_mode').ison()


Compatibility
-------------

Version 3.0 should work on Plone 4.1, 4.2, 4.3, 5.0.

For older Plone versions, please stick to the 2.x line.  Latest
release as of writing is 2.7.

Note that on Plone 5.0 we are not completely modern: we register our
css and javascript in the old portal tools, not in the new resource
registry.  So it ends up in the Plone legacy bundle.
