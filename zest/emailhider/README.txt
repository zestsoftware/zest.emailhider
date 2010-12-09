Zest emailhider
===============

This document describes the zest.emailhider package.


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
``email`` and a ``uid`` attribute.   The 'emailhider' view is
provided to generate the placeholder link.

Objects display a placeholder link with a ``hidden-email`` class, a
``uid`` rel attribute and a ``email-uid-<some uid>`` class set to the
UID of an object; when the page is loaded some jQuery is run to make a
request for all those links to replace them with a 'mailto' link for
that object.  Using this mechanism the email address isn't visible in
the initial page load, and it requires JavaScript to be seen - so it
is much harder for spammers to harvest.

Special case: when the uid is 'email_from_address', we do nothing with
the IMailable interface but just get the email_from_address from the
portal property.  If you want to display this address in for example a
static portlet, use this html code::

  <a class="hidden-email email-uid-email_from_address"
     href="mailto:nowhere" rel="email_from_address">
     Activate JavaScript to see this address.</a>


Note on KSS usage in older releases
-----------------------------------

Older releases (until and including 1.3) used KSS instead of jQuery.
As our functionality should of course also work for anonymous users,
we had to make KSS publicly accessible.  So all javascript that was
needed for KSS was loaded for anonymous users as well.

So you should check the javascript and kss registry and see if this
needs to be undone so anonymous users no longer get the kss
javascripts as they no longer need that.
