code_structure_list = [
    {
        "code": """from bedrock_util.bedrock_genai_util.TextCompletionUtil import generate_text_completion
from bedrock_util.bedrock_genai_util.prompt_service import run_service
import boto3

bedrock_client = boto3.client(service_name='bedrock-runtime')

def lambda_handler(event, context):
    \"""
    This block of code demonstrates how to invoke methods for generating text completions
    and running a prompt service flow based on service ID which it verifies from prompt_store.yaml file.


    example:

    If we want to directly use the FM API
    print(generate_text_completion(bedrock_client, event['model'], event['prompt']))

    If we want to use existing prompt flow
    if "prompt_input" in event:
        print(run_service(bedrock_client, "getMathDetails", event['model'], event["prompt_input"]))


    1. The first line generates a text completion using the model and prompt provided in the event,
       and prints the result.
    2. The if-statement checks if the 'prompt_input' key exists in the event.
       If it does, it runs the 'getMathDetails' service using the model and prompt input from the event,
       and prints the result.    

    \"""



    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }""",
        "file_name": "lambda_function.py",
    },
    {
        "code": """from bedrock_util.bedrock_genai_util.TextCompletionUtil import generate_text_completion
from bedrock_util.bedrock_genai_util.prompt_service import run_service
import boto3

bedrock_client = boto3.client(service_name='bedrock-runtime')

\"""
    This block of code demonstrates how to invoke methods for generating text completions
    and running a prompt service flow based on service ID which it verifies from prompt_store.yaml file.


    example:

    If we want to directly use the FM API , use - generate_text_completion

    If we want to use prompt service framework - run_service 

\"""
""",
        "file_name": "bedrock_app.py",
    },
    {
        "code": """##############################################################################################
#   Create YAML file content for prompt service flow. Example:                               #
#                                                                                            #
#  PromptServices:                                                                           #
#                                                                                            #
#    getMathDetails:                                                                         #
#      prompt: |                                                                             #
#        You are an expert math teacher. Based on user input below provide assistance.       #
#                                                                                            #
#        input: {input}                                                                      #
#      inputVariables:                                                                       #
#        - input                                                                             # 
#      guardrailIdentifier: "test"                                                             #
#      guardrailVersion:"1"                                                                    #
#      allowedFoundationModelProviders:                                                      #
#        - Amazon                                                                            #
#        - Meta                                                                              #
#        - Anthropic                                                                         #
#        - Mistral AI                                                                        #
#        - Cohere                                                                            #
##############################################################################################""",
        "file_name": "prompt_store.yaml",
    },
]
