import base64

code_str='ZnJvbSBkamFuZ28uZGIgaW1wb3J0IG1vZGVscwoKCmNsYXNzIEN1cnJlbmN5\nKG1vZGVscy5Nb2RlbCk6CiAgICBjb2RlID0gbW9kZWxzLkNoYXJGaWVsZCht\nYXhfbGVuZ3RoPTMsIHVuaXF1ZT1UcnVlKQogICAgbmFtZSA9IG1vZGVscy5D\naGFyRmllbGQobWF4X2xlbmd0aD0yMCkKICAgIHN5bWJvbCA9IG1vZGVscy5D\naGFyRmllbGQobWF4X2xlbmd0aD0xMCkKCiAgICBkZWYgX19zdHJfXyhzZWxm\nKToKICAgICAgICByZXR1cm4gc2VsZi5uYW1lCgpjbGFzcyBDdXJyZW5jeUV4\nY2hhbmdlUmF0ZShtb2RlbHMuTW9kZWwpOgogICAgc291cmNlX2N1cnJlbmN5\nID0gbW9kZWxzLkZvcmVpZ25LZXkoQ3VycmVuY3ksIHJlbGF0ZWRfbmFtZT0n\nc291cmNlX2V4Y2hhbmdlcycsIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSkK\nICAgIGV4Y2hhbmdlZF9jdXJyZW5jeSA9IG1vZGVscy5Gb3JlaWduS2V5KEN1\ncnJlbmN5LCByZWxhdGVkX25hbWU9J3RhcmdldF9leGNoYW5nZXMnLCBvbl9k\nZWxldGU9bW9kZWxzLkNBU0NBREUpCiAgICB2YWx1YXRpb25fZGF0ZSA9IG1v\nZGVscy5EYXRlRmllbGQoKQogICAgcmF0ZV92YWx1ZSA9IG1vZGVscy5EZWNp\nbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9NikKCiAg\nICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5z\nb3VyY2VfY3VycmVuY3l9IHRvIHtzZWxmLmV4Y2hhbmdlZF9jdXJyZW5jeX0g\nb24ge3NlbGYudmFsdWF0aW9uX2RhdGV9OiB7c2VsZi5yYXRlX3ZhbHVlfSI=\n'

print(base64.b64decode(code_str).decode())

from groq import Groq

key = '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'


def analyze_code_with_llm(file_content, file_name):
    prompt = f"""
    Analyze the following code for:
    - Code style and formatting issues
    - Potential bugs or errors
    - Performance improvements
    - Best practices

    File: {file_name}
    Content:
    {file_content}

    Provide a detailed JSON output with the structure:
    {{
        "issues": [
            {{
                "type": "<style|bug|performance|best_practice>",
                "line": <line_number>,
                "description": "<description>",
                "suggestion": "<suggestion>"
            }}
        ]
    }}
    ``json
    """


    client = Groq(api_key=key)
    completion = client.chat.completions.create(
        model='llama3-8b-8192',
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        top_p=1
    )
    print(completion.choices[0].message.content)

analyze_code_with_llm((base64.b64decode(code_str).decode()),'model.py')