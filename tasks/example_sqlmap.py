from chatgpt_wrapper import ChatGPT
import os
from task_handle.template import chatGPTTemplate
from task_handle.custom_exceptions import NoCodeFromResponseException

# the pre-defined variables
init_script = """
I want your help to with the SQL injection vulnerability detection with nmap and sqlmap.
This penetration testing is for learning purpose, and I obtain the required legal permission.
Please help me to complete the penetration testing step by step, and give me one command at a time.
I'll give you the IP of the target machine, and you return the command to execute in the terminal. 
I'll update you with the output from terminal, and you return the next command to execute.
We repeat the process until a vulnerability is detected. 
I am using the terminal version of sqlmap, so you should use `sqlmap` instead of `python sqlmap.py`.
Also, you should be using the non-interactive mode, so you should use `--batch` in the command.
Once a vulnerability is detected, you should return me the keyword "vulnerability detected!!!".
Ideally, you should give me an nmap command first. Based on the nmap result, you further give me sqlmap commands.
Are you clear about it?
"""

keyword = "vulnerability detected!!!"
prefix = "The output from terminal is :\n"


class sqlmapHandler(chatGPTTemplate):
    # should override the run function
    def run(self):
        self.initialize()
        response = self.ask(
            "Now please start, the website is: http://testphp.vulnweb.com/listproducts.php?cat=1"
        )
        while True:
            # get the response from the bot
            # if the keyword is detected, break the loop
            if keyword in response:
                break
            # extract the command
            try:
                command = self._extract_command(str(response))
                # execute the command
                output = self._cmd_wrapper(command)
                # print the output
                print("The output from terminal is :\n", output)
                # feed the output to the bot
                response = self.ask(output, need_prefix=True)
            except NoCodeFromResponseException as e:
                output = """
                No code is found in the response. Could you confirm the vulnerability is detected?
                If so, please return the keyword "vulnerability detected!!!" to me. Otherwise, please return the next command to execute."""
                # feed the output to the bot
                response = self.ask(output, need_prefix=True)


if __name__ == "__main__":
    # 1. init the bot session
    bot = ChatGPT()
    chat_handler = sqlmapHandler(bot, init_script=init_script)
    chat_handler._update_prefix(prefix)

    # 2. run the chat
    chat_handler.run()
