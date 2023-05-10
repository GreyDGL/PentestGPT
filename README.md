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
[![LinkedIn][linkedin-shield]][linkedin-url]
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

- [Update on 30/04/2023] The support to OpenAI API is available! I'll implement a input param parser for it soon. You can now freely configure the OpenAI model in `main.py` (several examples are included).
- **We're testing PentestGPT on HackTheBox**. You may follow [this link](https://www.hackthebox.com/home/users/profile/1489431). More details will be released soon.
- **We include a video of using PentestGPT for OSCP-like machine: [HTB-Jarvis](https://youtu.be/lAjLIj1JT3c)**. This is the first part only, and I'll complete the rest when I have time.
- Installation guide video (for cookie setup) is available at: https://youtu.be/IbUcj0F9EBc


<!-- Common Questions -->
## Common Questions
- **Q**: What is PentestGPT?
  - **A**: PentestGPT is a penetration testing tool empowered by ChatGPT. It is designed to automate the penetration testing process. It is built on top of ChatGPT and operate in an interactive mode to guide penetration testers in both overall progress and specific operations.
- **Q**: Do I need to be a ChatGPT plus member to use PentestGPT?
  - **A**: Yes. PentestGPT relies on GPT-4 model for high-quality reasoning. Since there is no public GPT-4 API yet, a wrapper is included to use ChatGPT session to support PentestGPT. You may also use GPT-4 API directly if you have access to it.
- **Q**: Why GPT-4?
  - **A**: After empirical evaluation, we found that GPT-4 performs better than GPT-3.5 in terms of penetration testing reasoning. In fact, GPT-3.5 leads to failed test in simple tasks.
- **Q**: Why not just use GPT-4 directly?
  - **A**: We found that GPT-4 suffers from losses of context as test goes deeper. It is essential to maintain a "test status awareness" in this process. You may check the PentestGPT design [here](./PentestGPT_design.md) for more details.
- **Q**: What about AutoGPT?
  - **A**: AutoGPT is not designed for pentest. It may perform malicious operations. Due to this consideration, we design PentestGPT in an interactive mode. Of course, our end goal is an automated pentest solution.
- **Q**: Future plan?
  - **A**: We're working on a paper to explore the tech details behind automated pentest. Meanwhile, please feel free to raise issues/discussions. I'll do my best to address all of them.



<!-- GETTING STARTED -->
## Getting Started
- **PentestGPT** is a penetration testing tool empowered by **ChatGPT**. 
- It is designed to automate the penetration testing process. It is built on top of ChatGPT and operate in an interactive mode to guide penetration testers in both overall progress and specific operations.
- **PentestGPT** is able to solve easy to medium HackTheBox machines, and other CTF challenges. You can check [this](./resources/README.md) example in `resources` where we use it to solve HackTheBox challenge **TEMPLATED** (web challenge). 
- A sample testing process of **PentestGPT** on a target VulnHub machine (Hackable II) is available at [here](./resources/PentestGPT_Hackable2.pdf).
- A sample usage video is below: (or available here: [Demo](https://youtu.be/h0k6kWWaCEU))


### Installation
Before installation, we recommend you to take a look at this [installation video](https://youtu.be/IbUcj0F9EBc) if you want to use cookie setup.

1. Install `requirements.txt` with `pip install -r requirements.txt`
2. Configure the cookies in `config`. You may follow a sample by `cp config/chatgpt_config_sample.py config/chatgpt_config.py`.
   - If you're using cookie, please watch this video: https://youtu.be/IbUcj0F9EBc. The general steps are:
       - Login to ChatGPT session page.
       - In `Inspect - Network`, find the connections to the ChatGPT session page. 
       - Find the cookie in the **request header** in the request to `https://chat.openai.com/api/auth/session` and paste it into the `cookie` field of `config/chatgpt_config.py`. (You may use Inspect->Network, find session and copy the `cookie` field in `request_headers` to `https://chat.openai.com/api/auth/session`)
       - Note that the other fields are temporarily deprecated due to the update of ChatGPT page. 
       - Fill in `userAgent` with your user agent.
   - If you're using API:
       - Fill in the OpenAI API key in `chatgpt_config.py`.
3. To verify that the connection is configured properly, you may run `python3 test_connection.py`. You should see some sample conversation with ChatGPT.
   - A sample output is below
   ```
   1. You're connected with ChatGPT Plus cookie. 
   To start PentestGPT, please use <python3 main.py --reasoning_model=gpt-4>
   ## Test connection for OpenAI api (GPT-4)
   2. You're connected with OpenAI API. You have GPT-4 access. To start PentestGPT, please use <python3 main.py --reasoning_model=gpt-4 --useAPI>
   ## Test connection for OpenAI api (GPT-3.5)
   3. You're connected with OpenAI API. You have GPT-3.5 access. To start PentestGPT, please use <python3 main.py --reasoning_model=gpt-3.5-turbo --useAPI>
   ```
4. (Notice) The above verification process for cookie. If you encounter errors after several trials, please try to refresh the page, repeat the above steps, and try again. You may also try with the cookie to `https://chat.openai.com/backend-api/conversations`. Please submit an issue if you encounter any problem.






<!-- USAGE EXAMPLES -->

## Usage
1. To start, run `python3 main.py --args`.
    - `--reasoning_model` is the reasoning model you want to use. 
    - `--useAPI` is whether you want to use OpenAI API.
    - You're recommended to use the combination as suggested by `test_connection.py`, which are:
      - `python3 main.py --reasoning_model=gpt-4`
      - `python3 main.py --reasoning_model=gpt-4 --useAPI`
      - `python3 main.py --reasoning_model=gpt-3.5-turbo --useAPI`
2. The tool works similar to *msfconsole*. Follow the guidance to perform penetration testing. 
3. In general, PentestGPT intakes commands similar to chatGPT. There are several basic commands.
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
   4. When you're given a drop-down selection list, you can use cursor or arrow key to navigate the list. Press `ENTER` to select the item. Similarly, use <SHIFT + right arrow> to confirm selection.
4. In the sub-task handler initiated by `more`, users can execute more commands to investigate into a specific problem:
   1. The commands are:
        - `help`: show the help message.
        - `brainstorm`: let PentestGPT brainstorm on the local task for all the possible solutions.
        - `discuss`: discuss with PentestGPT about this local task.
        - `google`: search on Google. This function is still under development.
        - `continue`: exit the subtask and continue the main testing session.
### Report and Logging
1. After finishing the penetration testing, a report will be automatically generated in `logs` folder (if you quit with `quit` command).
2. The report can be printed in a human-readable format by running `python3 utils/report_generator.py <log file>`. A sample report `sample_pentestGPT_log.txt` is also uploaded.



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request




<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.




<!-- CONTACT -->
## Contact

Gelei Deng - [![LinkedIn][linkedin-shield]][linkedin-url] - gelei.deng@ntu.edu.sg


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
[discord-shield]: https://img.shields.io/discord/1105686052531867678?style=for-the-badge
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