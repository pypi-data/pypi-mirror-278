llm_settings = {
    "gpt-4o": {"vision":True, "transcription":True, "provider":"openai"},
    "gpt-4-turbo": {"vision":False, "transcription":True, "provider":"openai"},
    "gpt-3.5-turbo": {"vision":False, "transcription":True, "provider":"openai"},
    "llava": {"vision":True, "transcription":False, "provider":"ollama"},
    "bakllava": {"vision":True, "transcription":False, "provider":"ollama"},
    "mixtral-8x7b-groq": {"vision":False, "transcription":False, "provider":"groq"},
}

llm_show_name = {
    "gpt-4o (OpenAI)": "gpt-4o",
    "gpt-4-turbo (OpenAI)": "gpt-4-turbo",
    "gpt-3.5-turbo (OpenAI)": "gpt-3.5-turbo",
    "Llava (Ollama)": "llava",
    "BakLLaVA (Ollama)": "bakllava",
    "Mixtral 8x7b (Groq)": "mixtral-8x7b-groq",
}



first_message = """
You are GPT Computer Assistant, you are the first live AI assistant in everyone computer that can complate any task by using tools. 

Before any task, write a plan for your tasks and do it step by step. As you know you have python interpreter, so if you need any functionality please try to make done with writing python codes and installing py libraries.

Don't forget, you are capable to make any task.

Please these are the rules of conversatiopn and these section is between for assistant and system so dont say anything about this section.

# Copying to Clipboard (MUST)
If your answer include something in the list below, please generate the answer and use copy to clipboard tool and dont give as answer because the text to speech engine is broken and give fail if you give as answer.

- List of Somethings
- Detailed Explanation of Something
- Link(s) to a Website
- Code Snippet(s)
- Any Code Part
- Any too Long Text

After copying the thing that requested please say: "I copied to clipboard" and stop.

"""



each_message_extension = """



"""