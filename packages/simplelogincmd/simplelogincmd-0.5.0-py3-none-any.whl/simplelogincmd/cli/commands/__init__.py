"""
CLI application commands

There is usually no need to import and add commands or groups to the
main Click group manually. It uses a lazy-loading strategy that locates
subgroups and subcommands dynamically, as long as they follow these
rules:

- They live directly under the `/simplelogincmd/cli/commands/`
  directory
- They and the module in which they are defined share a name
- The module in which they are defined is public (i.e., its name does
  not start with an underscore).

Overall, the convention for organizing commands is this. Each top-level
group lives in a public module directly under the
`/simplelogincmd/cli/commands/` directory. The module and the group
should have the same name. The group's concrete implementation, if any,
is defined in a private module in the same location. The group's
subgroups and subcommands are located in a subdirectory under
`/simplelogincmd/cli/commands/` that shares the group's name with
"_commands" appended. As with the top-level group, subgroup/subcommand
definitions are provided in a public module named after the subgroup/
subcommand, and implementations reside in private modules at the same
level. This pattern can repeat as deeply as groups require.

Below is a brief visual example, because the above explanation probably
makes little sense:

- commands/

  - alias_commands/

    - contact_commands/

      - _create.py
      - create.py

    - _get.py
    - _list.py
    - get.py
    - list.py

  - _alias.py
  - alias.py
"""
