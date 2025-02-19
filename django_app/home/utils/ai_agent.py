from groq import Groq
from django.conf import settings
from .prompts import system_prompt

key=settings.GROQ_KEY


def analyze_code_with_llm(file_content,file_name):
    prompt= f"""
    Analyze the following code for:
    - Code style and formatting issue
    - Potential bugs and errors
    - Performance improvements
    - Best Practices
    
    File : {file_name}
    Content : {file_content}
    
    provide a detailed json output with the structure"

    {{
        "issues": [
            {{
                    "type": "<style|bugs|performance|best_practice>",
                    "line": < line_number >,
                    "description" : "<description>",
                    "suggestion" : "<suggestion>",
            }}
        ]
    }}
    ```json
    """

    client = Groq(api_key=key)
    completion= client.chat.completions.create(
        model='llama3-8b-8192',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {
                "role" : "user",
                "content" : prompt
            }
        ],
        temperature=1,
        top_p=1
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content