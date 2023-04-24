# PentestGPT

**We're testing PentestGPT on HackTheBox**. You may follow [this link](https://www.hackthebox.com/home/users/profile/1489431). More details will be released soon.

## Common Questions
- **Q**: What is PentestGPT?
  - **A**: PentestGPT is a penetration testing tool empowered by ChatGPT. It is designed to automate the penetration testing process. It is built on top of ChatGPT and operate in an interactive mode to guide penetration testers in both overall progress and specific operations.
- **Q**: Do I need to be a ChatGPT plus member to use PentestGPT?
  - **A**: Yes. PentestGPT relies on GPT-4 model for high-quality reasoning. Since there is no public GPT-4 API yet, a wrapper is included to use ChatGPT session to support PentestGPT.
- **Q**: Why GPT-4?
  - **A**: After empirical evaluation, we found that GPT-4 performs better than GPT-3.5 in terms of penetration testing reasoning. In fact, GPT-3.5 leads to failed test in simple tasks.
- **Q**: Why not just use GPT-4 directly?
  - **A**: We found that GPT-4 suffers from losses of context as test goes deeper. It is essential to maintain a "test status awareness" in this process. You may check the PentestGPT design [here](./PentestGPT_design.md) for more details.
- **Q**: What about AutoGPT?
  - **A**: AutoGPT is not designed for pentest. It may perform malicious operations. Due to this consideration, we design PentestGPT in an interactive mode. Of course, our end goal is an automated pentest solution.
- **Q**: Future plan?
  - **A**: We're working on a paper to explore the tech details behind automated pentest. Meanwhile, please feel free to raise issues/discussions. I'll do my best to address all of them.


## Introduction
- **PentestGPT** is a penetration testing tool empowered by **ChatGPT**. 
- It is designed to automate the penetration testing process. It is built on top of ChatGPT and operate in an interactive mode to guide penetration testers in both overall progress and specific operations.
- **PentestGPT** is able to solve easy to medium HackTheBox machines, and other CTF challenges. You can check [this](./resources/README.md) example in `resources` where we use it to solve HackTheBox challenge *template*. 
- A sample testing process of **PentestGPT** on a target VulnHub machine (Hackable II) is available at [here](./resources/PentestGPT_Hackable2.pdf).
- A sample usage video is below: (or available here: [Demo](https://youtu.be/h0k6kWWaCEU))

https://user-images.githubusercontent.com/78410652/232327920-7318a0c4-bee0-4cb4-becb-6658b80180ff.mov

## Contribute
- The project is still in its early stage. Feel free to raise any issues when using the tool. 
- Please help to contribute by submitting the vulnerabilities you identified or challenges you solved with **PentestGPT**.
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
      - `google`: search on Google. This function is still under development.
      - `exit`: exit the tool.
   2. You can use <SHIFT + right arrow> to end your input (and <ENTER> is for next line).
   3. You may always use `TAB` to autocomplete the commands.
   4. When you're given a drop-down selection list, you can use cursor or arrow key to navigate the list. Press `ENTER` to select the item. Similarly, use <SHIFT + right arrow> to confirm selection.

## Report
1. After finishing the penetration testing, a report will be automatically generated in `logs` folder (if you quit with `quit` command).
2. The report can be printed in a human-readable format by running `python3 utils/report_generator.py <log file>`. A sample report `sample_pentestGPT_log.txt` is also uploaded.


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

