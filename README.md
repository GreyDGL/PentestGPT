<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Discord][discord-shield]][discord-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/GreyDGL/PentestGPT">
  </a>

<h3 align="center">PentestGPT</h3>

  <p align="center">
    A GPT-empowered penetration testing tool. 
    <br />
    <a href="https://github.com/GreyDGL/PentestGPT"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/GreyDGL/PentestGPT/blob/main/PentestGPT_design.md">Design Details</a>
    ·
    <a href="https://www.youtube.com/watch?v=lAjLIj1JT3c">View Demo</a>
    ·
    <a href="https://github.com/GreyDGL/PentestGPT/issues">Report Bug or Request Feature</a>
    </p>
</div>





<!-- ABOUT THE PROJECT -->
## General Updates
- [Update on 25/03/2024] We're working on the next version of PentestGPT, with online searching, RAGs and more powerful prompting. Stay tuned!
- [Update on 17/11/2023] GPTs for PentestGPT is out! Check this: https://chat.openai.com/g/g-4MHbTepWO-pentestgpt
- [Update on 07/11/2023] GPT-4-turbo is out! Update the default API usage to GPT-4-turbo. 
- Available videos:
  - The latest installation video is [here](https://youtu.be/tGC5z14dE24).
  - **PentestGPT for OSCP-like machine: [HTB-Jarvis](https://youtu.be/lAjLIj1JT3c)**. This is the first part only, and I'll complete the rest when I have time.
  - **PentestGPT on [HTB-Lame](https://youtu.be/Vs9DFtAkODM)**. This is an easy machine, but it shows you how PentestGPT skipped the rabbit hole and worked on other potential vulnerabilities.
- **We're testing PentestGPT on HackTheBox**. You may follow [this link](https://www.hackthebox.com/home/users/profile/1489431). More details will be released soon.
- Feel free to join the [Discord Channel](https://discord.gg/eC34CEfEkK) for more updates and share your ideas!


<!-- Quick Start -->
## Quick Start
1. Create a virtual environment if necessary. (`virtualenv -p python3 venv`, `source venv/bin/activate`)
2. Install the project with `pip3 install git+https://github.com/GreyDGL/PentestGPT`
3. **Ensure that you have link a payment method to your OpenAI account.** Export your API key with `export OPENAI_API_KEY='<your key here>'`,export API base with `export OPENAI_BASEURL='https://api.xxxx.xxx/v1'`if you need.
4. Test the connection with `pentestgpt-connection`
5. For Kali Users: use `tmux` as terminal environment. You can do so by simply run `tmux` in the native terminal.
6. To start: `pentestgpt --logging`


<!-- GETTING STARTED -->
## Getting Started
- **PentestGPT** is a penetration testing tool empowered by **ChatGPT**. 
- It is designed to automate the penetration testing process. It is built on top of ChatGPT and operate in an interactive mode to guide penetration testers in both overall progress and specific operations.
- **PentestGPT** is able to solve easy to medium HackTheBox machines, and other CTF challenges. You can check [this](./resources/README.md) example in `resources` where we use it to solve HackTheBox challenge **TEMPLATED** (web challenge). 
- A sample testing process of **PentestGPT** on a target VulnHub machine (Hackable II) is available at [here](./resources/PentestGPT_Hackable2.pdf).
- A sample usage video is below: (or available here: [Demo](https://youtu.be/h0k6kWWaCEU))

<!-- Common Questions -->
## Common Questions
- **Q**: What is PentestGPT?
  - **A**: PentestGPT is a penetration testing tool empowered by Large Language Models (LLMs). It is designed to automate the penetration testing process. It is built on top of ChatGPT API and operate in an interactive mode to guide penetration testers in both overall progress and specific operations.
- **Q**: Do I need to pay to use PentestGPT?
  - **A**: Yes in order to achieve the best performance. In general, you can use any LLMs you want, but you're recommended to use GPT-4 API, for which you have to [link a payment method to OpenAI](https://help.openai.com/en/collections/3943089-billing?q=API). 
- **Q**: Why GPT-4?
  - **A**: After empirical evaluation, we find that GPT-4 performs better than GPT-3.5 and other LLMs in terms of penetration testing reasoning. In fact, GPT-3.5 leads to failed test in simple tasks.
- **Q**: Why not just use GPT-4 directly?
  - **A**: We found that GPT-4 suffers from losses of context as test goes deeper. It is essential to maintain a "test status awareness" in this process. You may check the [PentestGPT Arxiv Paper](https://arxiv.org/abs/2308.06782) for details.
- **Q**: Can I use local GPT models?
  - **A**: Yes. We support local LLMs with custom parser. Look at examples [here](./pentestgpt/utils/APIs/gpt4all_api.py).


## Installation
PentestGPT is tested under `Python 3.10`. Other Python3 versions should work but are not tested.
### Install with pip
**PentestGPT** relies on **OpenAI API** to achieve high-quality reasoning. You may refer to the installation video [here](https://youtu.be/tGC5z14dE24).
1. Install the latest version with `pip3 install git+https://github.com/GreyDGL/PentestGPT`
   - You may also clone the project to local environment and install for better customization and development
     - `git clone https://github.com/GreyDGL/PentestGPT`
     - `cd PentestGPT`
     - `pip3 install -e .`
2. To use OpenAI API
   - **Ensure that you have link a payment method to your OpenAI account.**
   - export your API key with `export OPENAI_API_KEY='<your key here>'`
   - export API base with `export OPENAI_BASEURL='https://api.xxxx.xxx/v1'`if you need.
   - Test the connection with `pentestgpt-connection`
3. To verify that the connection is configured properly, you may run `pentestgpt-connection`. After a while, you should see some sample conversation with ChatGPT.
   - A sample output is below
   ```
   You're testing the connection for PentestGPT v 0.11.0
   #### Test connection for OpenAI api (GPT-4)
   1. You're connected with OpenAI API. You have GPT-4 access. To start PentestGPT, please use <pentestgpt --reasoning_model=gpt-4>
   
   #### Test connection for OpenAI api (GPT-3.5)
   2. You're connected with OpenAI API. You have GPT-3.5 access. To start PentestGPT, please use <pentestgpt --reasoning_model=gpt-3.5-turbo-16k>
   ```
   - notice: if you have not linked a payment method to your OpenAI account, you will see error messages.
4. The ChatGPT cookie solution is deprecated and not recommended. You may still use it by running `pentestgpt --reasoning_model=gpt-4 --useAPI=False`. 


### Build from Source
1. Clone the repository to your local environment.
2. Ensure that `poetry` is installed. If not, please refer to the [poetry installation guide](https://python-poetry.org/docs/).
3. 

<!-- USAGE EXAMPLES -->

## Usage
1. **You are recommended to run**:
   - (recommended) - `pentestgpt --reasoning_model=gpt-4-turbo` to use the latest GPT-4-turbo API.
   - `pentestgpt --reasoning_model=gpt-4` if you have access to GPT-4 API.
   - `pentestgpt --reasoning_model=gpt-3.5-turbo-16k` if you only have access to GPT-3.5 API.
   
2. To start, run `pentestgpt --args`.
    - `--help` show the help message
    - `--reasoning_model` is the reasoning model you want to use. 
    - `--parsing_model` is the parsing model you want to use. 
    - `--useAPI` is whether you want to use OpenAI API. By default it is set to `True`.
    - `--log_dir` is the customized log output directory. The location is a relative directory.
    - `--logging` defines if you would like to share the logs with us. By default it is set to `False`.
3. The tool works similar to *msfconsole*. Follow the guidance to perform penetration testing. 
4. In general, PentestGPT intakes commands similar to chatGPT. There are several basic commands.
   1. The commands are: 
      - `help`: show the help message.
      - `next`: key in the test execution result and get the next step.
      - `more`: let **PentestGPT** to explain more details of the current step. Also, a new sub-task solver will be created to guide the tester.
      - `todo`: show the todo list.
      - `discuss`: discuss with the **PentestGPT**.
      - `google`: search on Google. This function is still under development.
      - `quit`: exit the tool and save the output as log file (see the **reporting** section below).
   2. You can use <SHIFT + right arrow> to end your input (and <ENTER> is for next line).
   3. You may always use `TAB` to autocomplete the commands.
   4. When you're given a drop-down selection list, you can use cursor or arrow key to navigate the list. Press `ENTER` to select the item. Similarly, use <SHIFT + right arrow> to confirm selection.\
      The user can submit info about:
        * **tool**: output of the security test tool used
        * **web**: relevant content of a web page
        * **default**: whatever you want, the tool will handle it
        * **user-comments**: user comments about PentestGPT operations
5. In the sub-task handler initiated by `more`, users can execute more commands to investigate into a specific problem:
   1. The commands are:
        - `help`: show the help message.
        - `brainstorm`: let PentestGPT brainstorm on the local task for all the possible solutions.
        - `discuss`: discuss with PentestGPT about this local task.
        - `google`: search on Google. This function is still under development.
        - `continue`: exit the subtask and continue the main testing session.

### Report and Logging
1. [Update] If you would like us to collect the logs to improve the tool, please run `pentestgpt --logging`. We will only collect the LLM usage, without any information related to your OpenAI key.
2. After finishing the penetration testing, a report will be automatically generated in `logs` folder (if you quit with `quit` command).
3. The report can be printed in a human-readable format by running `python3 utils/report_generator.py <log file>`. A sample report `sample_pentestGPT_log.txt` is also uploaded.

## Custom Model Endpoints and Local LLMs
PentestGPT now support local LLMs, but the prompts are only optimized for GPT-4.
- To use local GPT4ALL model, you may run `pentestgpt --reasoning_model=gpt4all --parsing_model=gpt4all`.
- To select the particular model you want to use with GPT4ALL, you may update the `module_mapping` class in `pentestgpt/utils/APIs/module_import.py`.
- You can also follow the examples of `module_import.py`, `gpt4all.py` and `chatgpt_api.py` to create API support for your own model.

## Citation
Please cite our paper at:
```
@misc{deng2023pentestgpt,
      title={PentestGPT: An LLM-empowered Automatic Penetration Testing Tool}, 
      author={Gelei Deng and Yi Liu and Víctor Mayoral-Vilches and Peng Liu and Yuekang Li and Yuan Xu and Tianwei Zhang and Yang Liu and Martin Pinzger and Stefan Rass},
      year={2023},
      eprint={2308.06782},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.
The tool is for educational purpose only and the author does not condone any illegal use. Use as your own risk.



<!-- CONTACT -->
## Contact the Contributors!

- Gelei Deng - [![LinkedIn][linkedin-shield]][linkedin-url] - gelei.deng@ntu.edu.sg
- Víctor Mayoral Vilches - [![LinkedIn][linkedin-shield]][linkedin-url2] - v.mayoralv@gmail.com
- Yi Liu - yi009@e.ntu.edu.sg
- Peng Liu - liu_peng@i2r.a-star.edu.sg
- Zhang Jian - jian_zhang@ntu.edu.sg
- Yuekang Li - yuekang.li@unsw.edu.au



<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/GreyDGL/PentestGPT.svg?style=for-the-badge
[contributors-url]: https://github.com/GreyDGL/PentestGPT/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/GreyDGL/PentestGPT.svg?style=for-the-badge
[forks-url]: https://github.com/GreyDGL/PentestGPT/network/members
[stars-shield]: https://img.shields.io/github/stars/GreyDGL/PentestGPT.svg?style=for-the-badge
[stars-url]: https://github.com/GreyDGL/PentestGPT/stargazers
[issues-shield]: https://img.shields.io/github/issues/GreyDGL/PentestGPT.svg?style=for-the-badge
[issues-url]: https://github.com/GreyDGL/PentestGPT/issues
[license-shield]: https://img.shields.io/github/license/GreyDGL/PentestGPT.svg?style=for-the-badge
[license-url]: https://github.com/GreyDGL/PentestGPT/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/gelei-deng-225a10112/
[linkedin-url2]: https://www.linkedin.com/in/vmayoral/
[discord-shield]: https://dcbadge.vercel.app/api/server/eC34CEfEkK
[discord-url]: https://discord.gg/eC34CEfEkK
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
