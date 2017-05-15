# Contributing to Dora

*Dora, the explorer* is an open source project and a volunteer effort.
Dora welcomes contribution from everyone.

## Contributions

Contributions to Dora should be made in the form of [GitHub pull requests][pr].
Each pull request will be reviewed by a core contributor (someone with permission to land patches) and either landed in
the main tree or given feedback for changes that would be required before it can be merged. All contributions should
follow this format, even those from core contributors.

## Not All Commits Need CI Builds

Sometimes all you are changing is the `README.md`, some documentation or other things which have no effect on the tests.
In this case, you may not want a build to be created for that commit. To do this, all you need to do is to add `[ci skip]`
somewhere in the commit message.

Commits that have `[ci skip]` anywhere in the commit messages will be ignored. `[ci skip]` does not have to appear on the
first line, so it is possible to use it without polluting your project's history.

Alternatively, you can also use `[skip ci]`.

## Questions & Support

*We only accept bug reports, new feature requests and pull requests in GitHub*.
For questions regarding the usage of Dora, the explorer or support requests please visit the
[official forums][forum].

## Getting Support

If you have a question about how to use Dora, please see the [support page][support].

## Requesting Features

If you have a change or new feature in mind, please fill an [NFR][nfr].

Thanks! <br />
Dora Team

[pr]: https://help.github.com/articles/using-pull-requests/
[forum]: https://forum.dora.cc/
[srt]: https://github.com/jorge-matricali/dora/wiki/Submit-Reproducible-Test
[gb]: https://github.com/jorge-matricali/dora/wiki/Generating-a-backtrace
[support]: https://www.dora.cc/support
[nfr]: https://github.com/jorge-matricali/dora/wiki/New-Feature-Request---NFR
