# GPT Learns Counting

![GPT Learns Counting Interface](/imgs/GPT-Interface.jpg)

In comparisson to the official GPT-4o which still gets this wrong.

![GPT Learns Counting Interface](/imgs/GPT-Official.jpg)

## What it does

GPT Learns Counting is an interactive web application that demonstrates the power of AI in performing simple counting tasks. The application allows users to input phrases or words and request various counting operations, such as:

- Counting the occurrences of a specific letter in a word or phrase
- Counting the total number of characters in a given text

## The problem it solves

While counting letters or characters might seem trivial for humans, it's an interesting challenge for AI language models. This project showcases how we can extend the capabilities of large language models like GPT to perform precise counting tasks, which they are not inherently designed to do.

By implementing this functionality, we bridge the gap between natural language processing and exact numerical operations, allowing users to interact with the AI in a more practical and demonstrable way.

## How it uses function calling

The core of this application relies on OpenAI's function calling feature. Here's a brief explanation of how it works:

1. **User Input**: The user submits a query, like "How many 'a's are in 'banana'?"

2. **AI Interpretation**: The AI model (GPT-4) interprets the user's intent and determines which function to call.

3. **Function Calling**: Based on the interpretation, the AI calls one of two custom functions:
   - `count_occurrences(needle, haystack)`: Counts occurrences of a specific letter or word in a phrase.
   - `count_characters(text)`: Counts the total number of characters in a given text.

4. **Result Processing**: The function performs the counting operation and returns the result.

5. **Response Generation**: The application takes the function's result and generates a human-readable response.

6. **Display**: The response is then displayed to the user.

This approach allows the AI to perform exact counting operations while maintaining a natural language interface for the user.

## Try it out!

You can experience GPT Learns Counting live at [https://gmunhoz0810.github.io/GPT-Learns-Counting/](https://gmunhoz0810.github.io/GPT-Learns-Counting/)

Feel free to ask it to count letters, words, or characters in any phrase you can think of!

## Feedback and Contributions

We welcome feedback and contributions to this project. If you have any suggestions or encounter any issues, please open an issue on our GitHub repository.

Happy counting!