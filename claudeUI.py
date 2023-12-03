import gradio as gr
import boto3
import json
import random
import time

# Initialize Bedrock Runtime client
brt = boto3.client(service_name='bedrock-runtime')

# Gradio interface setup
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        # Invoke Bedrock model
        body = json.dumps({
            "prompt": f"\n\nHuman: {message}\n\nAssistant:",
            "max_tokens_to_sample": 300,
            "temperature": 0.1,
            "top_p": 0.9,
        })

        model_id = 'anthropic.claude-v2'
        accept = 'application/json'
        content_type = 'application/json'

        # Invoke Bedrock model
        response = brt.invoke_model(body=body, modelId=model_id, accept=accept, contentType=content_type)

        # Parse Bedrock model response
        response_body = json.loads(response.get('body').read())

        # Display chat history
        chat_history.append((message, response_body.get('completion')))
        time.sleep(2)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

# Launch the Gradio interface
demo.launch()
