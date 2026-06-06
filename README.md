## Safe Exam Browser Overlay for Windows

Safe Exam Browser Patches available publicily somehow seem too difficult to use. This repository provides a single-run script that you can use for a setup, along with an overlay application that adds images onto the screen to make the patched SEB similar to the original.


> [!IMPORTANT]
> This repository is only meant to **expose the unsafe side** of safe exam browser and indirectly give the original developers ideas to make it safer.
>
> The developer is NOT responsible for anyone using this overlay project in any way to cheat in exams and it is NOT open-source. Further details are explicitly stated in the [LICENSE](https://github.com/ShahzaibAhmad05/seb-overlay).


This documentation bellow is 100% manually typed (in this era of LLMs). I appreciate anyone reading. One thing to note is that in some places I have used the acronym SEB which essentially just means **Safe Exam Browser**.


---


## If you are a Teacher

Safe Browser is developed in c#, which can be decompiled and it's code can then be modified and easily used for cheating. On top of that, it's code is publicily available on GitHub [here](https://github.com/SafeExamBrowser/seb-win-refactoring), which proves it is "not safe at all".

But there is one way to prevent cheating completely, which is to have the student sign-in and take the exam in a teacher-owned computer with the latest version of safe-browser installed OR by using the [SEB Windows Verifier Tool](https://github.com/SafeExamBrowser/seb-win-verificator)


---


## What did I do

I came across a challenge to patch Safe Exam Browser. I discovered that most of the [existing patches](https://github.com/topics/seb-bypass) for Safe Exam Browser are either outdated, or only partially work. 

One of the partially working patches that I found was this one: [school-cheating/SEBPatch](https://github.com/school-cheating/SEBPatch). I dived in to discover how it worked and what it was missing.

Well, for the patch itself, it looks like this (as of [v1.5.2 release](https://github.com/school-cheating/SEBPatch/releases/tag/v1.5.2_3.9.0.787)):

<br />
<img src="https://drive.google.com/uc?export=view&id=1_7e6efYbXPae1CKrw-uqAlHcvqDk4AmN" width="600" />
<br />

Its surprisingly well-made, for the unknown developer who put this much effort into it. But it looks like they intentionally/unknowingly missed the main purpose there, which was to keep the UI looking like the original. For instance, this is what the Safe Browser UI looks like after applying the patch:

<br />
<img src="https://drive.google.com/uc?export=view&id=1ED76lOhexxoib-gRNTV8DGu1BV1cYclH" width="600" />
<br />

This introduces a lot of problems:

- The original taskbar of the safe exam browser is gone. Any invigilator looking at it would instantly recognize it's a fake.
- There are extra buttons on the UI which we don't need and look fake too.
- SEB on pressing the close button crashes, and takes about 20 seconds to crash too.
- The windows taskbar is visible. Although it can be hidden, it's inconvenient to hide it every time we have an exam. (specifically for students who have quizzes on SEB)
- The patch allows us to use our shortcut keys, but perhaps too many. Imagine accidently pressing the window key right when an invigilator is passing by. I think I don't have to explain what happens next.
- Having to switch to another browser to search for an answer is still not feasible.
- Having to install the correct version of SEB confuses many people (judging by the issues in that repository).


These above, and several other reasons are why this repository exists.


---


## What this repository offers

- `setup/`

This module when run allows for installation of the compatible version of Safe Exam Browser, and the latest version of the patch itself. The user just has to follow instructions given in a terminal.


- `overlay/`

Since our shortcut keys are disabled, now we have to figure out some way to actually solve an exam without the instructor noticing us pressing a lot of buttons on our keyboards.

A nice way around it would be to use [tesseract OCR]() in a python script to read the question on the screen and use some LLM-based api to solve it. Assuming we all want this to be free I have considered using [Gemini](https://gemini.com) for this task. 

And, for the sake of avoiding pressing/holding keys a lot I have considered using only two keys of the user's choice (configurable in `config.json`). One takes the OCR of the screen to capture a question, and the other displays the answer to the captured question on the bottom-right corner of the screen.


---


## Setup

Make sure you have python 3.11+ installed before starting from here.

1) Go to your projects folder, clone this repository and enter it:

```bash
git clone https://github.com/ShahzaibAhmad05/seb-overlay
cd seb-overlay
```

3) Install the requirements:

```bash
pip install -r requirements.txt
```

4) Run the setup module and follow the instructions in the terminal:

```bash
python -m setup
```

5) Now run the overlay in a terminal (you'd have to kill this terminal later, because of stubborn keyboard hooks):

```bash
python -m overlay
```

6) An overlay will popup on the screen. It will stay on the top of the screen by default. Try pressing *Ctrl+Alt+T* and the overlay should hide (aka press this shortcut immediately whenever SEB launches). `Win` key is disabled automatically by this script.

7) Make sure to turn off these shortcuts from windows settings "in the name of safety": 

```txt
Ctrl+Win+ArrowKey -> Changes the desktop view
Three/Four finger swipe -> Opens Task View
```

8) There is a half-built question solver module that I put in. It is turned on by default, you basically just press `M` (does OCR and sends the api request to Gemini) and `L` key (displays the answer at a corner of the screen) to use it. If you wish to use it, You may also need to put your gemini api keys in `.env` 


> [!NOTE]
> I hope at this point it is clear how this works. If you have any confusions setting this up, feel free to open an issue here. I would reply.


---


## Contributing

Just make your changes and do a pull request. Explain what you did and how it helps. I turn a PR down only if it smells like its LLM-ed.
