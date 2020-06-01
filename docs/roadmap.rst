.. _roadmap:

Roadmap
=======

:Authors: Fabien Maussion
:Status: Draft
:Created: 04.10.2019
:Updated: 01.06.2020

The OGGM-Edu platform will soon be 2 years old (first commit on Sep 21, 2018!).
We have made tremendous progress in one year: we created this website,
added new content, enabled interactivity via MyBinder and hub.oggm.org,
supported the creation of a workshop for a class in Peru, secured
funding to continue the platform's development...

It is now time to make a step back and have a look at what we achieved, and
brainstorm about what we want to realize in the future.

Intro
-----

As of June 2020, we have on the platform:

- 4 interactive web apps
- 8 jupyter notebooks templates in various complexity levels
- a series of glacier graphics
- bits of documentation for teachers about how to use the notebooks and MyBinder

So far, our biggest achievements are (subjective opinion):

- our notebooks were used for a class in Peru (`blog post <https://oggm.org/2019/12/06/OGGM-Edu-AGU/>`_)
- the uprecedented web applications
- the use of MyBinder and hub.oggm.org as viable platforms to run
  workshops and tutorials
- securing of funding for the platform, indicating that other people
  see potential in the project as well.

This is great! But we also see that there is room for improvement, and we would
like to use this roadmap as a "working document" to keep track of our
goals for the year to come.

Feel to comment or edit this file on GitHub!


Refactoring of the oggm-edu python package
------------------------------------------

This is probably the most involved and most important change.

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

This will require some thinking, but at the core, we should think about (1)
how to name things (very hard) and (2) how do we want the new objects
to behave.

The vision is that people have a centralized place (the OGGM-Edu documentation)
to learn about the flowline models and what they can do with them. The models
will be more expressive, use rich output in the notebooks, with the goal to
make using the models more fun, intuitive and quantitative.

Website design
--------------

(less important)

I'm not a big fan of using sphinx and ReadTheDocs anymore. We could have a
fancy Jekyll website hosted on Netlify instead!
