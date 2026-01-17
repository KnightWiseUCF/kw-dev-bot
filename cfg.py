# config
cmd_prefix = "!"

# command names
cmd_test = "test"
cmd_count_questions = "countquestions"

# cmd usage map
usages = {
    cmd_count_questions: "`{}{} [TOPIC NAME]`".format(cmd_prefix, cmd_count_questions)
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