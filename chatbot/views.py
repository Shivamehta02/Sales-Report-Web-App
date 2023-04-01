from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import openai,os
from dotenv import load_dotenv
load_dotenv()
# Create your views here.

api_key = os.getenv("OPENAI_KEY",None)
openai.api_key = api_key

@login_required
def index(request):
    chatbot_response = None
    if api_key is not None and  request.method =='POST':
        user_input = request.POST.get('user_input')
        prompt = user_input
        # prompt = f"if the question is related to sales or buisness or greetings- answer it:{user_input}, else say - I can only answer sales or buisness related queries"
        
        
        response = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt = prompt,
            max_tokens = 256,
            # stop = "."
            temperature = 0.5
        )
        # print(response)
        chatbot_response= response["choices"][0]["text"]
    return render(request, "chatbot/index.html",{"response":chatbot_response})
