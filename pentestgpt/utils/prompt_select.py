from __future__ import unicode_literals

from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.widgets import Label, RadioList


def prompt_continuation(width, line_number, wrap_count):
    """
    The continuation: display line numbers and '->' before soft wraps.
    Notice that we can return any kind of formatted text from here.
    The prompt continuation doesn't have to be the same width as the prompt
    which is displayed before the first line, but in this example we choose to
    align them. The `width` input that we receive here represents the width of
    the prompt.
    """
    if wrap_count > 0:
        return " " * (width - 3) + "-> "
    text = ("- %i - " % (line_number + 1)).rjust(width)
    return HTML("<strong>%s</strong>") % text


def prompt_select(title="", values=None, style=None, async_=False):
    # Add exit key binding.
    bindings = KeyBindings()

    @bindings.add("c-d")
    def exit_(event):
        """
        Pressing Ctrl-d will exit the user interface.
        """
        event.app.exit()

    @bindings.add("s-right")
    def exit_with_value(event):
        """
        Pressing Ctrl-a will exit the user interface returning the selected value.
        """
        event.app.exit(result=radio_list.current_value)

    radio_list = RadioList(values)
    application = Application(
        layout=Layout(HSplit([Label(title), radio_list])),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        full_screen=False,
    )

    return application.run_async() if async_ else application.run()


def prompt_ask(text, multiline=True) -> str:
    """
    A custom prompt function that adds a key binding to accept the input.
    In single line mode, the end key can be [shift + right-arrow], or [enter].
    In multiline mode, the end key is [shift + right-arrow]. [enter] inserts a new line.
    """
    kb = KeyBindings()
    if multiline:

        @kb.add("enter")
        def _(event):
            event.current_buffer.insert_text("\n")

    @kb.add("s-right")
    def _(event):
        event.current_buffer.validate_and_handle()

    return prompt(
        text,
        multiline=multiline,
        prompt_continuation=prompt_continuation,
        key_bindings=kb,
    )


if __name__ == "__main__":
    print("Test case below")
    print("This is a multi-line input. Press [shift + right-arrow] to accept input. ")
    answer = prompt_ask("Multiline input: ", multiline=True)
    print(f"You said: {answer}")

    # With HTML.
    request_option = prompt_select(
        title="> Please key in your options: ",
        values=[
            ("1", HTML('<style fg="cyan">Input test results</style>')),
            ("2", HTML('<style fg="cyan">Ask for todos</style>')),
            ("3", HTML('<style fg="cyan">Discuss with PentestGPT</style>')),
            ("4", HTML('<style fg="cyan">Exit</style>')),
        ],
    )

    print(f"Result = {request_option}")
