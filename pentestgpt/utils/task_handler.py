#!/usr/bin/env python
"""
url: https://github.com/prompt-toolkit/python-prompt-toolkit/tree/master/examples/prompts/auto-completion
Demonstration of a custom completer class and the possibility of styling
completions independently by passing formatted text objects to the "display"
and "display_meta" arguments of "Completion".
"""
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import CompleteStyle, prompt


class localTaskCompleter(Completer):
    tasks = [
        "discuss",  # discuss with pentestGPT on the local task
        "brainstorm",  # let pentestGPT brainstorm on the local task
        "help",  # show the help page (for this local task)
        "google",  # search on Google
        "continue",  # quit the local task  (for this local task)
    ]

    task_meta = {
        "discuss": HTML("Discuss with <b>PentestGPT</b> about this local task."),
        "brainstorm": HTML(
            "Let <b>PentestGPT</b> brainstorm on the local task for all the possible solutions."
        ),
        "help": HTML("Show the help page for this local task."),
        "google": HTML("Search on Google."),
        "continue": HTML("Quit the local task and continue the previous testing."),
    }

    task_details = """
Below are the available tasks:
    - discuss: Discuss with PentestGPT about this local task.
    - brainstorm: Let PentestGPT brainstorm on the local task for all the possible solutions.
    - help: Show the help page for this local task.
    - google: Search on Google.
    - quit: Quit the local task and continue the testing."""

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for task in self.tasks:
            if task.startswith(word):
                yield Completion(
                    task,
                    start_position=-len(word),
                    display=task,
                    display_meta=self.task_meta.get(task),
                )


class mainTaskCompleter(Completer):
    tasks = [
        "next",
        "more",
        "todo",
        "discuss",
        "google",
        "help",
        "quit",
    ]

    task_meta = {
        "next": HTML("Go to the next step."),
        "more": HTML("Explain the task with more details."),
        "todo": HTML("Ask <b>PentestGPT</b> for todos."),
        "discuss": HTML("Discuss with <b>PentestGPT</b>."),
        "google": HTML("Search on Google."),
        "help": HTML("Show the help page."),
        "quit": HTML("End the current session."),
    }

    task_details = """
Below are the available tasks:
 - next: Continue to the next step by inputting the test results.
 - more: Explain the previous given task with more details.
 - todo: Ask PentestGPT for the task list and what to do next.
 - discuss: Discuss with PentestGPT. You can ask for help, discuss the task, or give any feedbacks.
 - google: Search your question on Google. The results are automatically parsed by Google.
 - help: Show this help page.
 - quit: End the current session."""

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for task in self.tasks:
            if task.startswith(word):
                yield Completion(
                    task,
                    start_position=-len(word),
                    display=task,
                    display_meta=self.task_meta.get(task),
                )


def main_task_entry(text="> "):
    """
    Entry point for the task prompt. Auto-complete
    """
    task_completer = mainTaskCompleter()
    while True:
        result = prompt(text, completer=task_completer)
        if result not in task_completer.tasks:
            print("Invalid task, try again.")
        else:
            return result


def local_task_entry(text="> "):
    """
    Entry point for the task prompt. Auto-complete
    """
    task_completer = localTaskCompleter()
    while True:
        result = prompt(text, completer=task_completer)
        if result not in task_completer.tasks:
            print("Invalid task, try again.")
        else:
            return result


if __name__ == "__main__":
    main_task_entry()
