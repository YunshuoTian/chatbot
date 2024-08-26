import json, os, time


class Assistant():
    
    def __init__(self, client, doc):
        self.client = client
        self.doc = client.files.create(
        file=open(doc, "rb"),
        purpose="assistants"
        )

    def create_assistant(self):

        assistant = self.client.beta.assistants.create(
            instructions="You will be provided some files please analyze it and response quickly within a few words, no long analysis needed",
            name="Document Helper",
            tools=[{"type": "code_interpreter"}],
            tool_resources={ "code_interpreter": {"file_ids": [self.doc.id]}},
            model='gpt-4o-mini'
        )
        assistant_id = assistant.id

        return assistant_id

    def run_thread(self, thread_id, assistant_id, user_message):
        
        self.client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=user_message
    )

        run_thread = self.client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
        return run_thread

    def get_assistant_message(self, thread):
        conversation = []
        messages = self.client.beta.threads.messages.list(thread_id=thread.id, order="asc")

        for m in messages:
            conversation.append({"role": m.role, "content": m.content[0].text.value})
            if m.role == 'assistant':
                bot_response = m.content[0].text.value
        
        return bot_response, conversation
        
    def wait_on_run(self, run, thread):
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run

class URL_helper():

    def __init__(self, client, urls):
        self.client = client
        self.urls = urls

    def webpage_reader(self):

        urls = self.urls.split(',')
        messages = []

        for url in urls:
            sys_prompt = '''
                You will be provided with url from the internet.
                Your goal will be to summarize the content from the url.
                Here is a description of the parameters:
                - url: the url from user input
                - summary: short description of the website page, no more than 50 words
            '''

            response = self.client.chat.completions.create(
                model = 'gpt-4o-2024-08-06',
                messages = [
                    {"role": "system",
                    "content": sys_prompt
                    },
                    {
                        "role": "user",
                        "content": url
                    }
                ],
                temperature=0,
                response_format = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "summary_output",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "url": {
                                    "type": "string"
                                },
                                "summary": {
                                    "type": "string"
                                }
                            },
                            "required": ["url","summary"],
                            "additionalProperties": False
                        }
                    }
                }
            )

            message = response.choices[0].message.content
            messages.append(message)

        return messages

    def formatted_output(self, messages):

        string_output = ""

        for item in messages:
            json_dict = json.loads(item)

            url = json_dict.get("url")
            summary = json_dict.get("summary")

            string_output += f'<p><strong>For URL <a href="{url}" target="_blank" style="color: #0078d7;">{url}</a>:</strong> {summary}</p>'
            

        return string_output
    

if __name__ == '__main__':

    pass


