<h1 align="center"><ins>Custom Chat</ins></h1>

<img src="./frontend/public/cc_logo.png" alt="Custon Chat Logo" width="300" height="300" style="display: block; margin-left: auto; margin-right: auto;">

<p align="center">An application that creates a custom AI chatbot for businesses based on documents and finetuning provided.</p>

<h2 align="center">**NOTICE**</h2>

<p align="center"> At the moment, this app is in development. Thank you for understanding. </p>

## Table of Contents

* <ins>Use Guide</ins>
    * [Getting Started](#getting-started)
    * [How To Start Up](#start-up)
    * [How to Close Down the App](#close-app)
    * [How To Use The App](#use-app)
    * [How To Test The App](#test-app)
    * [Things To Be Aware Of](#aware-of)
    * [Other Dependencies](#other-dependencies)
    * [Ideas for Further Work](#further-work)
    * [Contributors & Acknowledgements](#contrib-acknow)
    * [Contribution Guidelines](#contrib-guidelines)
    * [License](#license)
    * [AI Use](#ai-use)

# <ins>Use Guide</ins>

## <a name="#getting-started">Getting Started</a>

Initially you will have to make sure all project requirements are installed.

You can do this by running the following command in the root directory of the project.
```
make init
```
Furthermore, go to the [Other Dependencies](#other-dependencies) tab to find what else you may not have installed, but need.

Before going further make sure to look at the README and .env.example in each of the following:

<b>frontend, backend, embed-service, llm-service</b>

Finally, to be noted, all sets of commands/command sequences are set up in the Makefile! To look at the different 
command sequences you have available to you, use the following command in the root directory of the project.
```
make help
```

## <a name="#start-up">How To Start Up</a>

Before you start up the app, ensure you have the .env file set up similarly to the .env.example set up in each of the 
following: <b>frontend, backend, embed-service, llm-service</b>. For further information look at the 
specific folders .env.example.

After you are done setting up the .env files, we conveniently have a command to start up the actual project. 
All you have to do is run the following command in the root directory!
```
make dev
```
This command starts up all the services, the database, and the frontend for you to use.

After that to test it out, open a browser and open up the following link 
(or the one provided at the end of the dev command sequence):

http://localhost:3000/

## <a name="#close-app">How to Close Down the App</a>

To close down the app it is as simple as using <b>CTRL + C</b> in the terminal <b>make dev</b> was ran,
then running the following command:
```
make stop
```

## <a name="#use-app">How To Use The App</a>

The front end is still in development, but to read more about how to use each individual backend, make sure to read the 
README files in <b>backend, embed-service, and llm-service</b>.

## <a name="#test-app">How To Test The App</a>

### Backend

Before you test the app, ensure you have the .env and .env.test set up for each of the following directories, as shown 
in a similar fomat by the .env.example in each directory:

<b>backend, embed-service, llm-service</b>

After setting up the .env and .env.test files, 
you can run the following command to run all the unit and integration tests:
```
make all-tests
```
If you want to run specific tests, check out the further make commands with:
```
make help
```

## <a name="#aware-of">Things To Be Aware Of</a>

When using this, it will download the Mystral-7B model to your device in the cache.
The model is about 15 gigabytes. 

## <a name="#other-dependencies">Other Dependencies</a>

To run this project you need a few things on your computer:

You need to install supabase locally:
```
brew install supabase
```

Otherwise, you will also need Docker installed on your device.

https://docs.docker.com/get-started/get-docker/

## <a name="#further-work">Ideas for Further Work</a>

### Backend
1. PDF DOCX support
2. Bot optimization
3. Verify bot api key when submitting feedback
3. Delete User, Delete Bot, Delete Doc, clears embeddings & Api key
4. Maybe fix bucket upload logic? might be document/document/{bot_id}/{file_name}
5. Fix for consistent object/dict usage when getting responses from endpoints
6. Fix unit test warnings
7. Docker usage
8. Rate limiting
9. Document endpoint rollback logic (commented in documents endpoint file)

## <a name="#contrib-acknow">Contributors & Acknowledgements</a>

This project was created by myself (BenWrightSWE).

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

