# config
cmd_prefix = "!"

# command names
cmd_test = "test"
cmd_help = "help"
cmd_count_questions = "countquestions"
cmd_delete_user = "deleteuser"
cmd_create_user = "createuser"

# cmd usage map
cmd_usages = {
    cmd_help: "{}{}".format(cmd_prefix, cmd_help),
    cmd_count_questions: "{}{} [TOPIC NAME]".format(cmd_prefix, cmd_count_questions),
    cmd_delete_user: "{}{} [USER ID]".format(cmd_prefix, cmd_delete_user),
    cmd_create_user: "{}{} [USERNAME] [optional:PASSWORD] [optional:EMAIL] [optional:FIRSTNAME] [optional:LASTNAME]".format(cmd_prefix, cmd_create_user),
    }

# cmd description map
cmd_descriptions = {
    cmd_help: "Returns a list of commands.",
    cmd_count_questions: "Returns the number of questions categorized as a given topic.",
    cmd_delete_user: "Deletes a user given an ID.",
    cmd_create_user: "Creates a user with the specified parameters",
    }

update_hookstillactive = 3600 # 3 hours between periodic logs

topics = [
    "Algorithm Analysis",
    "AVL Trees",
    "Backtracking",
    "Base Conversion",
    "Binary Trees",
    "Bitwise Operators",
    "Dynamic Memory",
    "Hash Tables",
    "Heaps",
    "Linked Lists",
    "Queues",
    "Recurrence Relations",
    "Recursion",
    "Sorting",
    "Stacks",
    "Summations",
    "Tries",
    ]