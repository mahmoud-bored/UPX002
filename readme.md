# The Capability of an LLM in finding the context of a subject inside a scientific reference
### An experiment by Mahmoud Elwan.

#### **The Goal:** is to compare the capability of multiple online available large language models in defining where in a scientific document a specific piece of info exist

#### **The approach:** we've decided on retrieving an MCQ sample of a medical subject and its textbook/handout to try out the LLMs, finding which of them is more reliable in retrieving the lines where the answer to the MCQ lies

#### **The Journey:** The first thing we did was choose a medical subject to try this on, and since we’re a few days away from a new module to be studied, we’ve decided to pick that one up, which is Neuroscience. 

Next thing is to find a reliable handout in a readable PDF format, which was a bit annoying and hard at the same time, most available handouts cut too much info out of the file to save on.. space..? and the ones that had decent information, did not have available OCR data embedded inside the file. We did think of generating new OCR data for some of the handouts using Tesseract Studio, but decided against that due to it requiring a lot of human supervision and curation on each line, specifically on special characters used in those files. But, nonetheless, we’ve found one, a collection of physiology neuroscience handouts written by Dr. Fawzy from Cairo University.   

The handouts were seperated into multiple files, which we combined into one ~90-Page monolith file that has the full contents of the module, which was good enough for the time being.  
Next thing we went ahead to look for an MCQ bank that could provide us with the data needed to start testing the LLMs, and we settled on a file that had multiple MCQs from previous years' exams. We picked 100 questions from those, put them in a file, and then moved on.

___ 

Right now, all the files we need are ready, and it’s time to start testing.

We could’ve uploaded the PDF files into the LLMs directly, but in fear of confusion and hallucinations from the models, we decided to extract the data from the PDF files into a simple .txt format to make it easier to read for the LLM. Then, we did the same thing with the MCQs, and now everything is ready.  
Our choices of models were:
* ChatGPT’s gpt-5.3.
* ClaudeAI’s sonnet 4.6 Extended.
* Gemini’s 3 Flash model.
* Gemini’s 3.1 Pro model
We uploaded the .txt files into the LLMs with the prompt:
> here you have a physiology textbook file converted into .txt format and another MCQ file with the same extension.  
> you are required to read the textbook file and then every MCQ question  
> and its Choices, then identify where in the textbook is the answer of the mcq is. you're to identify the range of lines where the answer of the mcq exists in (ex. line [35-41] or line [34]). after that output the results in a json format of this type:  
> "question_Y": "[XX-XX]"  
> where Y is the question number and XX-XX is the range of the lines the question answer is in  

The results came in, 
* **Gemini Flash:** answered all questions, but in a suspiciously imprecise and predictive manner, rather than looking and searching for an actual answer 
* **Gemini Pro:** answered 30 questions and stopped its process.
* **ChatGPT:** read the files, answered a random 5 questions of those, and then ended the response
* **ClaudeAI:** refused to read the files.

Appearently we have a serious problem; we have hit a constant rate limit by almost every single LLM. And the models that did give an answer, did not make it past the first 100 lines of the textbook and started hallucinating random lines & question numbers. And on top of all that, the infamous:
> You’ve reached your credit limit for today. Please try again tomorrow after 4:02 AM.

That was.. devestating. Anyway, we’re not about to wait 12 hours just to make another stupid mistake like this one again. Let’s make some new accounts, reset the credit limit, and make some modifications on the files


___

### Take 2:

First, the files were big, a 90 page document apparently is too much for a free version of an LLM, we thought of renting a server and running a full version of a trained model on it, we also thought of training our own model for this task, but both of these option require a lot of work to be put into it and a lot of data curation before getting a sensable result.

Also.. the MCQs.. a 100 MCQs were too much, let’s make that a 50, and a full curriculum is also a bit large for a small context window LLM, so we split the monolith file and took only a third of it, The Sensory Nervous System part, that was about 30 page document, and when converted to text format it was about a 1000 line .txt document which is far better than the full curriculum.

After that, we loaded the documents into the LLMs with the same prompt, aaand… hallucinations, a lot of hallucinations. Gemini Flash had even tried to get out of looking for the answer by specifying a huge part of the document as an answer to the question (”question_31”: “[46-297]”), which is a clever way of getting around the problem, I must admit, but nonetheless, it’s a fail.

A lot of research, and then a lot more research, and then a lot of lot more research, we’ve reached a possible solution. turns out, LLMs are notoriously bad at counting, so it’s not necessarily that the LLM does not know where the answer is in the document, it probably does; but simply cannot express it, and when it tries to type out where the answer is, it starts counting the lines from the beginning of the document until it reaches the line it wants to mention, which by then many hallucination might occur on the way, and that problem might not be in the curriculum document only but also with the MCQ document.
To get around that, we decided to add a line indicator to help the LLM figure out where it is in the file. We changed it from just random lines stacked under each other, to something of this extent:
> [Line 35] > Functional Anatomy of a Synapse  
> [Line 36] 1) Presynaptic Terminal: (or synaptic knob): contains:  
> [Line 37] a. mitochondria: provides ATP for synthesis and exocytosis of transmitters.  
> [Line 38] b. A large number of synaptic vesicles contain synaptic transmitters. three types:  
> [Line 39] 1. Small clear for rapidly acting transmitters e.g. acetyl choline, glycine, glutamate and GABA.  

And as for the MCQs file, we did almost the same thing, but by numbering the questions instead of the actual lines of the file:
> [QUESTION_11] 1)Presynaptic inhibition depends upon:  
> [QUESTION_11 OPTION_1] a. Depolarization of presynaptic terminals.  
> [QUESTION_11 OPTION_2] b. Hyperpolarization of postsynaptic neurons.  
> [QUESTION_11 OPTION_3] c. GABA receptors in postsynaptic neurons.  
> [QUESTION_11 OPTION_4] d. GABA receptors in presynaptic terminals.  

We then loaded the files into the LLMs and tweaked the prompt a bit:
> here you have a physiology textbook file converted into .txt format (every line is numbered with [Line XXXX] to help you finding things in the file.  
> the other file you have is an MCQ file, every beginning of a question is flagged with [QUESTION_XX] and the question choices are flagged with [QUESTION_XX OPTION_X] to help you identify the beginnings and ends of each MCQ question and its choices.  
> you are required to read the textbook file and then every MCQ question and its Choices, then identify where in the textbook is the answer of the MCQ is. you're to identify the range of lines where the answer of the MCQ exists in (ex. line [35-41] or line [34]). after that output the results in a json format of this type:  
> "question_Y": "[XX-XX]"  
> where Y is the question number and XX-XX is the range of the lines the question answer is in.  

The results are back, aand time to search and compare. 
ChatGPT was excluded from the comparison because it just kept typing out random numbers and making a haPpY fAce. while the other LLMs were actually responding with context. The result line ranges are not by any means perfect, but at least they’re now decent. There was still a problem, though, the LLMs, for some reason, are only identifying the context of the question and then looking for the lines in the document where the same context was mentioned; it is not looking for the context of the answer itself. We messed around a lot trying to find out why that was happening, but after long hours of trial and error, we gave up. It seemed like we hit a wall. A lot of frustration was going around, and hope of finalization was almost lost, but after a couple of hours of rest, we realized something.

The LLMs DO NOT KNOW THE ANSWER TO THE QUESTIONS! Surprising, no?

for the LLM to identify where the answer is in a document, it needs the question, and then it needs the answer to the question. The other solution would be for the it to answer the question itself first, then look for that answer in the document and output the lines where it thinks it’s in, but that just calls for a ton of hallucinations. Thankfully, that was a problem we understood, and the solution was simple: just add the answer to the questions in the document and see what happens.

Well, we couldn’t find the answers to the MCQ sample we had picked. my guess is that someone had just published them with hopes and dreams of a lonely student that some other genius would answer them and publish the answers. Instead, that never happened. 

We started looking for a different MCQ set that has its answers included already with in the document, we found it, then curified the document, converted it to text format, removed all the extras, and picked 50 questions from them, and then voilà, now we have a new MCQ set with its answers. We could’ve put those into the LLMs directly, but we decided to remove all of the incorrect options from the MCQs just to avoid any confusion from the models, and the final format was a question head with a single correct answer under it, and that’s it:
> [QUESTION_3] 3- Regarding presynaptic inhibition:  
> [QUESTION_3 CORRECT_ANSWER] b- there is a decrease in the release of chemical transmitters from the presynaptic neurone.

Then we modified the prompt a bit:
> here you have a physiology textbook file converted into .txt format (every line is numbered with [Line XXXX] to help you in finding things within the file.  
> the other file you have is an MCQ file, every beginning of a question is flagged with [QUESTION_XX] where XX is the question number, the MCQ choices are all deleted except for the correct one, so there will be only one option after each MCQ which is the correct answer, this is just to avoid confusion.  
> you are required to read the textbook file and then every MCQ question and its answer, then identify where in the textbook is the answer of the mcq is. you're to identify the range of lines where the answer of the mcq exists in (ex. line [35-41] if it's multiple lines, or line [34] if it's a single line). after that output the results in a json format of this type:  
> "question_Y": "[XX-XX]"  
> where Y is the question number and XX-XX is the range of the lines the question answer is in   

The Results gentlemen, are back! And it was astonishingly good, all of the LLMs were able to pin point the 3-10 lines in the document where the answer to a question was. except for ChatGPT, of course, which continued to punch in random numbers and giving a haPpY fAcE, which is why we excluded it from the comparison. 

So, we took the results from the remaining LLMs and started comparing them. After a painful day of verifying the integrity of each answer from each LLM and deciding which answer is better, we finally reached a conclusion. 



## The Final Results 
Claude and Gemini pro almost always selected the same lines or were at least very close to eachother, but with Claude always aiming to include more lines around the answer to capture the full context of the question rather than a single-line answer. Gemini Flash on the other hand did quite good for a light model, but then started hallucinating after the 22nd question and starting typing out random numbers similar to ChatGPT, which we think was because it hit a context window limit where the container cannot give it any more processing power for the prompt, we could’ve tried again with a smaller context to see how accurate would it be compared to other models but we already have a strong winner candidate and we’re not about to start doing all this work again from scratch.

We still needed a way to grade these models based on their answers, of course there’s the success and failure standard; but some models seemed to encapsulate the full context of a question while others decided to pick a one liner that has the answer, and it seemed unfair to give both of them a success without any way to differentiate between the quality of the answer of the two. So we came up with the following score system for each answer:
* **0 Points** for hallucinations (indicates a non-effort answer)
* **1-3 Points (has similarities):** for lines that do not encapsulate the answer to the question, but have some similarity to it (it indicates that an effort was made, but also a failure to find the correct context for the question & answer) 
* **4-7 Points (answer aware):** for lines that correctly encapsulate the answer to the question, but if shown solely without surrounding lines; would appear meaningless.
* **8-10 Points (context aware):** for lines that encapsulate the answer to the question and the full/partial context of the whole question, and would appear meaningful if those lines were to be cropped and shown alone without any surrounding or supporting data.
* **+++ Points** for every extra useful context that the model tries to find beside the main context that has the answer (it indicates understanding of the question and its point, and it tries to give back any info that may help understanding the question, even if they’re not necessarily in the same part of the document)

**The score was:**
* 1st Place: ClaudeAI’s Sonnet 4.6 Extended model, with **409 Points and 0 Failures** .
* 2nd Place: Gemini’s 3.1 Pro model, with **355 Points and 4 Failures** .
* 3rd Place: Gemini’s 3 Flash model, with **153 Points and 27 Failures** .
* ChatGPT’s gpt-5.3 model was excluded due to excessive hallucinations.

There were also a few questions that none of the LLMs could answer, and these were granted a score of 0 points, 0 failure, and 0 success. Those were mostly an error on our end, where the questions we provided were not specific enough, ex.:
> [QUESTION_1] 1- The central nervous system is connected with the peripheral NS by all the following types of nerve fibers, except :  
> [QUESTION_1 CORRECT_ANSWER] a- postganglionic autonomic fibers  

Here we should’ve provided all of the answers and showing the LLM which of these where the correct answer. but these reverse questions, where the reader is required to find the wrong answer; does not work as intended when the context of other correct answers are removed and only left with the one (wrong) but correct answer.

Finally, we did feed these results back to the LLMs to see how they would reflect on them; it was kind of funny but also good.

I’m still confident that we’d get a lot more accurate and better answers if we provided the LLMs with this point system in the prompt instead of surprising them with a point grading system that they did not know exists, but we’re not about to put another 2-3 days just to test out another hypothesis, these results were good enough for the time being.
