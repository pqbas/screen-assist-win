## Safe Exam Browser Overlay

Safe Exam Browser Patches available publicily somehow seem too difficult to use. This repository provides a single-run script that you can use for a setup. Just download the `setup.exe` from releases, run it, and you're good to go.


> [!IMPORTANT]
> This repository is only meant to **expose the unsafe side** of safe exam browser and indirectly give the original developers ideas to make it safer.
>
> The developer is NOT responsible for anyone using this overlay project in any way to cheat in exams and it is NOT open-source. Further details are explicitly stated in the [LICENSE](https://github.com/ShahzaibAhmad05/seb-overlay).


This documentation bellow is 100% manually typed (in this era of LLMs). I appreciate anyone reading. One thing to note is that in some places I have used the acronym SEB which essentially just means **Safe Exam Browser**.


---


## If you are a Teacher

Safe Browser is developed in c#, which can be decompiled and it's code can then be modified and easily used for cheating. On top of that, it's code is publicily available on GitHub [here](https://github.com/SafeExamBrowser/seb-win-refactoring), which proves it is "not safe at all".

But there is one way to prevent cheating at all, which is to have the student sign-in and take the exam in a teacher-owned computer with the latest version of safe-browser installed OR by using the [SEB Windows Verifier Tool](https://github.com/SafeExamBrowser/seb-win-verificator)


---


## What did I do

I came across a challenge to patch Safe Exam Browser. I discovered that most of the [existing patches](https://github.com/topics/seb-bypass) for Safe Exam Browser are either outdated, or only partially work. 

One of the partially working patches that I found was this one: [school-cheating/SEBPatch](https://github.com/school-cheating/SEBPatch). I dived in to discover how it worked and what it was missing.

Welp, for the patch itself, it's UI screen looks like this (for v1.5.2 release as on GitHub):

<br />
<img />
<br />

Its surprisingly well-made, for whoever put effort into it. But it looks like the developer intentionally/unknowingly missed the main purpose there, which was to keep the UI looking like the original. For instance, this is what the UI looks like after applying the patch:

<br />
<img />
<br />

This introduces a lot of problems:

- The original taskbar of the safe exam browser is gone. Any invigilator looking at it would instantly recognize it's a fake.
- There are extra buttons on the UI which we don't need and look fake too.
- SEB on pressing the close button crashes, and takes about 20 seconds to crash too.
- The windows taskbar is visible. Although it can be hidden, it's inconvenient to hide it every time we have an exam. (specifically for students who have quizzes on SEB)
- The patch allows us to use our shortcut keys, but perhaps too many. Imagine accidently pressing the window key right when an invigilator is passing by. I think I don't have to explain what happens next.
- Having to switch to a browser to search for an answer is still not feasible.


These above, and several other reasons are why this repository exists.


---


## What this repository offers

It basically has two modules:

- An Overlay (the important one)

This is exactly what it sounds like. An overlay, a few elements on top of your windows screen using `.png` images. These cover for the visible windows taskbar and the modified buttons on the patch.

As for the shortcut keys, they are temporarily disabled when the script is run. Details for which keys are disabled are [here]().

- MCQ solver using OCR

Since our shortcut keys are disabled, now we have to figure out some way to actually solve an exam without the instructor noticing us pressing a lot of buttons on our keyboards. AND for the sake of an example lets assume our exam to be Multiple Choice Questions (MCQ-based).

A nice way around it would be to use [tesseract OCR]() in a python script to read the question on the screen and use some LLM-based api to solve it. Assuming we all want this to be free I have considered using [Gemini](https://gemini.com) for this task. 

And, for the sake of avoiding pressing/holding a lot I have considered using only two keys of the user's choice (configurable in `config.json`). One takes the OCR of the screen to capture a question, and the other displays the answer to the captured question on the screen.


---


## Setup (this is very complex, trust)

MAKE SURE YOU ARE ON WINDOWS or MacOS and you have python installed!!

> SEB does not run on linux

1) Go to your projects folder, clone this repository and enter it:

```bash
git clone https://github.com/ShahzaibAhmad05/seb-overlay
cd seb-overlay
```

2) Activate a virtual environment and activate it **(optional, skip if you are unfamiliar)**:

```bash
# it will work with older/newer versions as well
# but I have used this one
py -3.13 -m venv .venv
```

3) Install the requirements:

```bash
pip install -r requirements.txt
```

3) Install Safe Exam Browser [VERSION] (the original one) from [here]().

4) Close everything on your desktop and run capture module. This will snip and save images into `/assets`

```bash
python -m capture
```

5) Now it's time to patch SEB. Download the patch [VERSION] from [here](), and run it.

6) Open SEB on your desktop to make sure it is patched. It should look like this:

[IMAGE]

7) Open the `seb-overlay` project again. Run the overlay:

```bash
python -m overlay
```

8) An overlay will popup on the screen. It will stay on the top of the screen by default. There is a key `TOGGLE_OVERLAY` in `config.json`. By default it is set to *Ctrl+Alt+T* which is the safest I could figure out. `Win` key is disabled automatically by this script.

9) Make sure to turn off these shortcuts from windows settings "in the name of safety": 

```txt
Ctrl+Win+ArrowKey -> Changes the desktop view
Three/Four finger swipe -> Opens Task View
```

I prefer not to write an extra 50-line documentation on how to turn these off, so figure it out on runtime. Rest of the steps on the setup are completely optional. 

I would want you to find your own way to solve your exam from here since you have the overlay module running.

10) Now SEB should look real. But since we turned off our VERY useful shortcut keys, we have to use the `mcq` module to be able to solve the exam. First create the `.env` file using the command bellow and put in your Gemini api keys, which you can get from [here]().

```bash
cp .env.example .env
```

11) Now run the `mcq` module:

```bash
python -m mcq
```

12) The default keys for using this script would be `M` for the OCR, and `L` for displaying the answer. You may also need to put your gemini api keys in `.env` 

13) Now when you press `M`, an OCR is taken, and after a time interval of a few seconds, the answer is fetched and saved. When you press `L`, the answer will display at the corner of your screen.

> [!NOTE]
> I hope at this point it is clear how this works. If you have any confusions setting this up, feel free to open an issue here. I would reply.

