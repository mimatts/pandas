# Report for assignment 4

This is a template for your report. You are free to modify it as needed.
It is not required to use markdown for your report either, but the report
has to be delivered in a standard, cross-platform format.

## Project

Name: Pandas

URL: https://github.com/pandas-dev/pandas

One or two sentences describing it

## Onboarding experience

Did you choose a new project or continue on the previous one? we chose a new project

If you changed the project, how did your experience differ from before?

## Effort spent

For each team member, how much time was spent in

1. plenary discussions/meetings;

2. discussions within parts of the group;

3. reading documentation;

4. configuration and setup;

5. analyzing code/output;

6. writing documentation;

7. writing code;

8. running code?

For setting up tools and libraries (step 4), enumerate all dependencies
you took care of and where you spent your time, if that time exceeds
30 minutes.

## Overview of issue(s) and work done.

Title: Default negative location in pandas insert

URL: https://github.com/pandas-dev/pandas/issues/49496

Summary in one or two sentences

Previously, specifying the index for a new column was mandatory when inserting data. In order to improve the functionality, an enhancement was made to modify the insertion process. This enhancement enables the insertion of arguments without the need for a specified index and by default, the data set will be added at the end.

Scope (functionality and code affected).

## Requirements for the new feature or requirements affected by functionality being refactored

Optional (point 3): trace tests to requirements.
1. The insertion function needs to be reworked to make the parameter index optional.
2. To ensure that the added column is placed at the last index, tests should be created. 
3. Additionally, previous tests should be modified to accommodate the new parameter layout in the insertion function. 

## Code changes

### Patch

(copy your changes or the add git command to show them)

git diff ...

Optional (point 4): the patch is clean.

Optional (point 5): considered for acceptance (passes all automated checks).

## Test results

Overall results with link to a copy or excerpt of the logs (before/after
refactoring).

## UML class diagram and its description

### Key changes/classes affected

Optional (point 1): Architectural overview.

Optional (point 2): relation to design pattern(s).

## Overall experience

What are your main take-aways from this project? What did you learn?

How did you grow as a team, using the Essence standard to evaluate yourself?

Optional (point 6): How would you put your work in context with best software engineering practice?

Optional (point 7): Is there something special you want to mention here?
