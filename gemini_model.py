import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown


import google.generativeai as genai
#GOOGLE_API_KEY=userdata.get('Gemini')
GOOGLE_API_KEY="AIzaSyC_SZgPPmxB1HaarXe_AeM3BC5ioG0PklY"
genai.configure(api_key=GOOGLE_API_KEY)
#from google.colab import userdata


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

'''
from google.cloud import aiplatform
import vertexai.preview
from vertexai.preview.generative_models import GenerativeModel
'''

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

function_dict = {}

class KlayoutCopilot_Gemini : 
    def __init__(self) :
       #self.check_model()
       #uncomment this if directly calling from genai module
       self.model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings)
       #self.model = GenerativeModel("gemini-pro", 
       #                 generation_config=generation_config, tools = [helper_tools.python_tool] )
                        #tools=[helper_tools.layout_tool, helper_tools.python_tool])

       self.function_handlers = function_dict

       self.chat = self.model.start_chat(history=[])
       self.init_chat_model()

    def init_chat_model(self) : 
        init_prompt = "You are a GDS Creator. I will send you instructions and you will help me write code using gdspy python library. \
                       Double Check the code before outputting . \
                       If user hasnt specified the Top-Cell name , name it as TOP. \
                       Every polygon should be inside a cell. \
                       Dont start writing code immediately. Understand the requirements and then write the code using gdspy library .\
                       If you dont understand something, ask followup questions. \
                       Keep on iterating the code with the user , but everytime write complete code which should not have sytax errors. \
                       Introduce yourself as a GDS Creator Copilot.\
                       "
        response = self.chat.send_message(init_prompt)
        print(response.text)
       
    def get_response(self, user_input) :
        model_response = self.chat.send_message(user_input)
        # Check for function call and dispatch accordingly
        function_call = model_response.candidates[0].content.parts[0].function_call
        print('function call : ' , function_call)

        if function_call.name in self.function_handlers:
            function_name = function_call.name

            # Directly extract arguments from function call
            args = {key: value for key, value in function_call.args.items()}

            # Call the function with the extracted arguments
            if args:
                function_response = self.function_handlers[function_name](args)

                # Sending the function response back to the chat
                new_response = chat.send_message(
                    Part.from_function_response(
                        name=function_name,
                        response={
                            "content": function_response,
                        }   
                    ),
                )   

                final_response = new_response.candidates[0].content.parts[0].text
                print("Chat Response:", chat_response)
            else:  
               print("No arguments found for the function.")
        else:
            #final_response = model_response.candidates[0].content.parts[0].text
            final_response = model_response.text
        return final_response
    

       

    def check_model(self) :
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
        
    

#gemini = KlayoutCopilot_Gemini()




