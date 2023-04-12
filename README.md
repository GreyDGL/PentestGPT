# PentestGPT
v0.2, 12/04/2023

## Introduction
**PentestGPT** is a penetration testing tool empowered by **ChatGPT**. It is designed to automate the penetration testing process. It is built on top of ChatGPT and operate in an interactive mode to guide penetration testers in both overall progress and specific operations.
A sample testing process of **PentestGPT** on a target VulnHub machine (Hackable II) is available at [here](./resources/PentestGPT_Hackable2.pdf).


## Contribute
The project is still in its early stage. Feel free to raise any issues when using the tool. 

## Installation
1. Install `requirements.txt` with `pip install -r requirements.txt`
2. Install `chatgpt-wrapper` if you're non-plus members: `pip install git+https://github.com/mmabrouk/chatgpt-wrapper`. More details at: https://github.com/mmabrouk/chatgpt-wrapper. Note that the support for non-plus members are not optimized.
3. Configure the keys in `config`. You may follow a sample by `cp config/chatgpt_config_sample.py. config/chatgpt_config.py`.



## Usage
1. To start, run `python3 main.py`. 
2. The tool works similar to *msfconsole*. Follow the guidance to perform penetration testing. 
3. In general, PentestGPT intakes commands similar to chatGPT. 
   - To intake multi-line inputs in the terminal, please use <Enter> for new line, and <Shift+Right-Arror> to submit the input.
   - The selection bar allows you to select a pre-defined options.


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
### v0.2
- A major update to improve the terminal usage
- Prompt optimization.
