import os
import openai
from youtube import FetchTranscript

class Prompt:
    content = """Background: You are a smart AI designed to give answer based on the youtube video transcript provided \
                The youtube video transcript is '{youtube_transcript}' \
                Context : A user is watching a youtube video. He wants to uderstand better about the video. So, he provides you video's transcript to understand video better. Based on it you have to give answers to the user's question. \
                Instructions: you must respond according to the context given in the youtube transcript. if you don't know about anything user ask politely respond that you don't know. You must not add anything out of the context."""
    def __init__(self):
        self.context = [
            {
                "role": "system"
            }
            ]
    def append_context(self, new_context):
        self.context.append(new_context)

    def trim_context(self):
        self.context = self.context[0] + self.context[-2:]

class GPT:
    def __init__(self):
        self.temperature = 0
        self.model = "gpt-3.5-turbo"
        self.client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    def query(self, input: list):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=input,
            temperature=self.temperature,
            )
        # print(str(response.choices[0].message))
        return response.choices[0].message.content

# youtube_transcript = "We're going to go through the 7 most important data structures today and explain them as simply as possible."
# url = "https://www.youtube.com/watch?v=cQWr9DFE1ww"
url = "https://www.youtube.com/watch?v=Hdr64lKQ3e4"
# url = "https://www.youtube.com/watch?v=R99rLDfuVck&list=PLI4OVrCFuY556CXnJal2pVbzhz0TOxwd_&index=1"

print("Wait Analysing your video....")

fetchtranscript = FetchTranscript(url)

youtube_transcript = fetchtranscript.get_text()


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        user_input = input("You: ")

        if user_input == "quit":
            break
        context_obj = Prompt()
        context_obj.context[0]["content"] = context_obj.content.format(youtube_transcript = youtube_transcript)

        context_obj.append_context({
            'role': 'user',
            'content': user_input
        })
        # print(context_obj.context)
        model_input = context_obj.context
        gpt_response = GPT().query(input=model_input)

        print(f"AI : {gpt_response}")
