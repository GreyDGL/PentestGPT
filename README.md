# PentestGPT

17/04/2023: Due to the additional verification by OpenAI, you now need to pass the full `cookie` variable into the session. 
You can obtain it from `https://chat.openai.com/api/auth/session`, by examining the HTTP request cookie. Check the updated chatgpt_config_sample.
I'll try to fix this later.


## Introduction
**PentestGPT** is a penetration testing tool empowered by **ChatGPT**. It is designed to automate the penetration testing process. It is built on top of ChatGPT and operate in an interactive mode to guide penetration testers in both overall progress and specific operations.
A sample testing process of **PentestGPT** on a target VulnHub machine (Hackable II) is available at [here](./resources/PentestGPT_Hackable2.pdf).

- Comparison to **Auto-GPT**. 
  - Using [Auto-GPT](https://github.com/Torantulino/Auto-GPT) in security testing is good, but it is not optimized for security-related tasks. 
  - **PentestGPT** is designed for penetration testing with a customized session interaction (see [here](./PentestGPT_design.md) for the detailed design).
  - Currently, **PentestGPT** does not rely on search engine. The "Google-enhanced" version of **PentestGPT** is under development.

## Contribute
- The project is still in its early stage. Feel free to raise any issues when using the tool. 
- This project is for research purpose. Please contact me if you're interested in collaboration.

## Installation
1. Install `requirements.txt` with `pip install -r requirements.txt`
2. (Deprecated: Will update support for non-plus member later.) ~~Install `chatgpt-wrapper` if you're non-plus members: `pip install git+https://github.com/mmabrouk/chatgpt-wrapper`. More details at: https://github.com/mmabrouk/chatgpt-wrapper. Note that the support for non-plus members are not optimized.~~
3. Configure the keys in `config`. You may follow a sample by `cp config/chatgpt_config_sample.py. config/chatgpt_config.py`.



## Usage
1. To start, run `python3 main.py`. 
2. The tool works similar to *msfconsole*. Follow the guidance to perform penetration testing. 
3. In general, PentestGPT intakes commands similar to chatGPT. There are several basic commands.
   1. The commands are: 
      - `help`: show the help message.
      - `next`: key in the test execution result and get the next step.
      - `more`: let **PentestGPT** to explain more details of the current step.
      - `todo`: show the todo list.
      - `discuss`: discuss with the **PentestGPT**.
      - `exit`: exit the tool.
   2. You can use <SHIFT + right arrow> to end your input (and <ENTER> is for next line).
   3. You may always use `TAB` to autocomplete the commands.
   4. When you're given a drop-down selection list, you can use cursor or arrow key to navigate the list. Press `ENTER` to select the item. Similarly, use <SHIFT + right arrow> to confirm selection.


## Design Documentation
The current design is mainly for web penetration testing

### General Design
PentestGPT provides a unified terminal input handler, and backed by three main components:
- A test generation module which generates the exact penetration testing commands or operations for the users to execute.
- A test reasoning module which conducts the reasoning of the test, guiding the penetration testers on what to do next.
- A parsing module which parses the output of the penetration tools and the contents on the webUI.

### Function Design
The handler is the main entry point of the penetration testing tool. It allows pentesters to perform the following operations:
1. (initialize itself with some pre-designed prompts.)
2. Start a new penetration testing session by providing the target information.
3. Ask for todo-list, and acquire the next step to perform.
4. After completing the operation, pass the information to PentestGPT.
   1. Pass a tool output.
   2. Pass a webpage content.
   3. Pass a human description.

## Update history
### v0.3
- Prompt usage optimization.
- Documentation improvements.
### v0.2
- A major update to improve the terminal usage
- Prompt optimization.
