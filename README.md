# <ins>Custom Chat</ins>

![Custom Chat's Logo](./frontend/public/cc_logo.png)

An application that creates a custom AI chatbot for businesses based on documents and finetuning provided.

<ins>**NOTICE**</ins>

At the moment, this app is in development. Thank you for understanding.

## Table of Contents

* <ins>Use Guide</ins>
    * [Getting Started](#getting-started)
    * [How To Start Up](#start-up)
    * [How to Close Down the App](#close-app)
    * [How To Use The App](#use-app)
    * [Things To Be Aware Of](#aware-of)
    * [Ideas for Further Work](#further-work)
    * [Other Dependencies](#other-dependencies)
    * [Contributors & Acknowledgements](#contrib-acknow)
    * [Contribution Guidelines](#contrib-guidelines)
    * [License](#license)
    * [AI Use](#ai-use)

# <ins>Use Guide</ins>

## <a name="#getting-started">Getting Started</a>

.

## <a name="#start-up">How To Start Up</a>

make sure docker is open

supabase start

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --workers 1

## <a name="#close-app">How to Close Down the App</a>

ctrl + c on the uvicorn terminal

supabase stop --no-backup

## <a name="#use-app">How To Use The App</a>


## <a name="#aware-of">Things To Be Aware Of</a>

To test: just run (pytest) or (pytest tests/tests_blank.py)

## <a name="#further-work">Ideas for Further Work</a>

* Add a pdf and docx reader 
* Add a typescript widget to add to websites

## <a name="#other-dependencies">Other Dependencies</a>

Make sure you have docker installed and running when you start up the app

## <a name="#contrib-acknow">Contributors & Acknowledgements</a>

This app was created by myself (BenWrightSWE).

## <a name="#contrib-guidelines">Contribution Guidelines</a>

Follow the license guideline and please message me regarding any changes you may have made. I'd love to hear about them
and implement them in this version after checking them out.

## <a name="#license">License</a>

For this project I am using the AGPL-3.0 license. Please respect this.

If you want further information regarding the license go to the LICENSE file.

## <a name="#ai-use">AI Use</a>

I used a previous project to gain an understanding of how some tools interacted and as an idea of where to go.

From there, I used AI to help me understand how different tools connected, understanding what things were used in which
ways, and just for general understanding. I used it in this way so that I would genuinely comprehend the code I am writing
and what each library or framework I was using, was doing. It was used for templates as well for things I haven't used before.

The main AI used for this was Claude, but ChatGBT was used as well.

