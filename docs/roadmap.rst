.. _roadmap:

Contribute to OGGM-Edu
======================

As of June 2020, the OGGM-Edu platform features:

- 4 interactive web apps
- 8 jupyter notebooks templates in various complexity levels
- a series of glacier graphics
- bits of documentation for teachers about how to use the notebooks and MyBinder

We are proud of simple things, such as the the use of OGGM-Edu for a
class in Peru (`blog post <https://oggm.org/2019/12/06/OGGM-Edu-AGU/>`_),
or the positive feedback about the web applications and the use of MyBinder
as a viable platform to run workshops and tutorials online.

This is great! But we also see that there is room for improvement, and we would
like to use this roadmap as a "working document" to keep track of our
goals for the years to come. OGGM-Edu is meant to be a collaborative platform,
and we welcome any kind of contribution, from a typo correction to a new fully
fledged web app!

**If you want to participate**, here are some pointers to get you started.
Thanks so much for your help!

Help with typos, text, content, etc.
------------------------------------

Everything on this website is written by volunteers and non-native english
speakers. If you find mistakes or things you'd like to change, please do!
You can edit each file by following the "Edit on GitHub" link at the top
of each page, or send us your modification suggestions!

Create new content
------------------

We welcome any new idea you may have: a new graphic, a new notebook, a new app...
You can decide to have it hosted here at edu.oggm.org (ref:`reach out! <title_contact>`), or you can
decide to have it in your own namespace! Follow :ref:`these instructions <user_content>` if you'd
rather do the latter.

Help translate OGGM-Edu
-----------------------

We are seeking to improve the usefulness of OGGM-Edu in non english speaking
groups. It is technically easy to do it (we already have
template - dummy - pages for
`german <https://edu.oggm.org/de/latest/>`_,
`french <https://edu.oggm.org/fr/latest/>`_ and
`spanish <https://edu.oggm.org/es/latest/>`_ and we can easily add any other
language): the hard part is to actually *translate* the content and keep the
translations up to date ;-).

The translation files are located in the `docs/locale <https://github.com/OGGM/oggm-edu/tree/master/docs/locale>`_
folder: these `.po` files are like a dictionary that can be edited with a
simple text editor or dedicated tools (e.g. `poedit <https://poedit.net/>`_).
See `this file <https://github.com/OGGM/oggm-edu/blob/master/docs/locale/fr/LC_MESSAGES/alps_future.po>`_
for an example.

If you would like to help, grab these files and translate were you can! The translation
of even one single page would be very useful. We can provide support and advice with the languages
we can read (spanish, french, german).

Refactoring of the oggm-edu python package
------------------------------------------

This is probably the most involved change.

As it is now, oggm-edu relies mostly on the models and syntax provided by the
core OGGM. They provides the functionality we need, but at the same time the
OGGM numerical models have several issues in the educational context:

- their functionality is tailored for modelers, not students. I.e. certain
  variables are not available and/or hidden, the syntax is clumsy, optimisations
  in code make it less readable
- it is very difficult to change things in OGGM itself because of backwards
  compatibility
- it is complex for new users to find the information in the cluttered OGGM
  namespace

For these reasons, we suggest to **redesign and refactor the OGGM objects in a
more user-friendly, intuitive oggm-edu namespace**.

This will require some thinking, but in short: we should think about (1)
how to name things (very hard) and (2) how do we want the new objects
to behave.

The vision is that people have a one stop shop (the OGGM-Edu documentation)
to learn about the flowline models and what they can do with them, without
having to struggle with OGGM itself. The models
will be more expressive, use rich output in the notebooks, with the goal to
make using the models more fun, intuitive and quantitative.

Website design
--------------

(less important)

ReadTheDocs and Sphinx are great, but they have their limits. If you have
web skills and would like to make OGGM-Edu more appealing,
ref:`reach out! <title_contact>`
