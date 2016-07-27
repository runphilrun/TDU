# Contributing

Building things is fun! Feel free to submit issues, suggest features, and even submit pull requests!

## Getting Started

To contribute to the code base we need some sort of ticket to help communicate the desired changes.

* Make sure you have a [GitHub account](https://github.com/signup/free)
* Submit a ticket for one of the following topics
  * __(fix)__: Describe the issue and include steps to reproduce, include the earliest version that you know has the issue
  * __(feat)ure__: Describe the desired behavior and include any possible solutions
  * __(doc)ument__: Describe which component lacks documentation, not all document changes may require a ticket
  * __(test)__: Describe which component lacks test coverage
  * __(tech)__: Describe what part of the code infrastructure should change

## Making Changes

Once we have a ticket to work off of making changes is a breeze.

* [Fork the repository](https://help.github.com/articles/fork-a-repo/)
* [Create a topic branch](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)
  * Please avoid working directly on the `master` branch
  * `git checkout -b fix/my-fix-name master`
* Make commits of logical units
* Make sure your commit messages are in the following format
```
  ({topic}) {subject}

  {description}
```
__Example:__
```
  (fix:#23) add missing bus control

  No bus control was provided in the original implementation.
  All future components should have a bus control.
```
* Make sure you have added the necessary tests for your changes
* Run __all__ the tests to make sure nothing else was accidentally broken
* [Submit a pull request](https://help.github.com/articles/using-pull-requests/) to the `master` branch
* Once submitted, feedback will be provided and additional changes may have to be made before we can merge it into `master`

# Additional Resources

* [Propulsion](http://www.braeunig.us/space/propuls.htm)
* [Python CLI](https://docs.python.org/2/library/argparse.html)
* [Python testing](https://github.com/pytest-dev/pytest/)
* [Python packaging](http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/quickstart.html)
* [Python dependency management](https://packaging.python.org/requirements/)
