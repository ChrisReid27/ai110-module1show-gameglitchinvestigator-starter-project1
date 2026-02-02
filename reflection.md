# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
The ranges for easy/normal/hard mode should be 20/100/50 but in the actual game it is always 1 to 100. The attempt system for each mode is also bugged and entering guesses only works if you if you click submit, even though there is a prompt saying you can press the enter key.
The hint sytem for going higher or lower is not working correctly. If the answer is 72 and I put 90 it should not be returning Go Higher. 
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion you accepted and why.
- Give one example of an AI suggestion you changed or rejected and why.
I used Copilot and Gemini on this project. I accepted most of the changes like the
changes for attempt logic and game reset issue fixes. I did not accept an initial version of tests from Copilot and I switched to Gemini to see if there was a cleaner way to go about it. The Copilot version of the tests for attempt logic and attempt history didn't match what I expected.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
I would frequently rerun the actual streamlit app and try different scenarios specifically to see if bugs had been fixed. I ran my test for submission method using pytest and it showed that it was at ~90% passing. The app now accepts enter key or submit button click properly. AI helped me understand my tests, specifically for the bugs that were hard to initially pin down like submission method. I asked copilot about certain lines and what they were meant for.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?
Every run or reload of streamlit gives a new secret number because the entire code runs over again each time. Reruns literally restart the script from scratch. Session states are like storage for values so that they stay stable if say a script is ran again from scratch. I changed random.randint(1, 100) to (low, hig).
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I want to make sure to start a new chat for different issues because if you forget to do that, the llm will incorporate previous issue with your new prompt which is most times not what you want. I want to next time ask multiple models on improvements earlier in the process, so I can compare there suggestions to eachother. This project made me think that AI generated code is very much cookie cutter and if you have a certain way of coding, implementing it's very plain, standard, code into yours can 1 make readability weird and 2, actually mess up the code.