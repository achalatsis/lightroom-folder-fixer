### Lightroom folder fixer for local accented characters

This script changes certain characters directly in the lightroom database.
Example use case is where accented characters where entered incorrectly and don't map to the current OS.

Switches:

'-d', '--db': lightroom catalog path

'-v', '--verbose': print all changed folders

'-r', '--dry-run': don't commit the changes, only print