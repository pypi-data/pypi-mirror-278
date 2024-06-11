.. _dev-git:

Gitlab
......

The official repository for RAM software is the DTU Wind Energy Gitlab installation, either the internal or external server will be used depending on the tool.

The repositories are setup so that the master branch is the "official" branch and is therefore locked from anyone pushing to the branch, and merge requests are used to bring changes into the main branch. It is also required that your merge request passes its pipeline, and before the merge, the :ref:`test_coverage` and :ref:`docs_coverage` will be looked at.

Finally, we are working with a semi-linear history, which will ensure that your change will successfully build when added to the master branch. To facilitate this, you will need to understand how to use ``git rebase``, before performing a merge request.

Git Rebase Workflow
-------------------

Using `git rebase <https://git-scm.com/docs/git-rebase>`_ applies your changes to the tip of another base. In our use case, the other base will be the Master branch. This can be thought of as updating your changes so that they account for any differences to the master branch, before merging. This will require you to repair any conflics.

For this workflow, you will perform the following steps, while on the topic branch:

1. Fetch the latest changes from the upstream "master" branch::

    git fetch origin

2. Rebase the topic branch, this in effect piles all of the commits of the topic branch to the latest tip of the upstream "master" branch::

    git rebase origin/master

3. Push the rebased topic branch to Gitlab::
    git push -u origin topic_branch_name

4. Go to GitLab, verify that the pipeline has passed, and submit merge request.

Squasing commits with rebase
----------------------------

It is common when working on a topic branch that you will create many small commits, and add to them as it goes on. It can be useful to combine some of these to create more appropriate commit messages, and better tracking of the feature development. This can be done through by using ``git rebase`` interactively. See `Git ready <http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html>`_ for an article about this if you are interested in using this.
