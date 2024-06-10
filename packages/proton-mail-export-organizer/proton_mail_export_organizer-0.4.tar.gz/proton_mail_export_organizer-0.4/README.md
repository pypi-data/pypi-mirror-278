# Proton mail export organizer

This is a tool to sort emails from a proton-mail-export directory into folders.

I used it to import my proton-mail-export into thunderbird using
[ImportExportTools
NG](https://addons.thunderbird.net/en-US/thunderbird/addon/importexporttools-ng/).


## Quick usage

The program only takes a single parameter: the export directory, so:

- First run [proton-mail-export-cli](https://proton.me/support/proton-mail-export-tool) to download your emails.
- It should create a directory like `username@protonmail.com/mail_YYYYMMDD_HHMMSS/`.
- `pip install proton-mail-export-organizer`
- `proton-mail-export-organizer username@protonmail.com/mail_YYYYMMDD_HHMMSS` (Replace the username and date to match **your** export).


You're done, your emails has been ordered in a hierarchy that should match the one you had in Protonmail.


## I'm not happy with the result

It works for me.

But I bet we're not all using emails the same
way. Feel free to doodle around with the code.

You can run it multiple times to see the effect of your changes in the
hierarchy.

The only thing that may be surprising is that I do not delete empty
directories if all emails are moved out of them.

If you're happy with your changes, don't hesitate to open a PR.
