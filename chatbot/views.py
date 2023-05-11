from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import QAPair
from profiles.models import Profile
import openai,os
from dotenv import load_dotenv
from django.contrib.auth import get_user
load_dotenv()
# Create your views here.

api_key = os.getenv("OPENAI_KEY",None)
openai.api_key = api_key

@login_required
def index(request):
    profile=Profile.objects.get(user=request.user)
    chatbot_response = None
    prompt = None
    if api_key is not None and  request.method =='POST':
        user_input = request.POST.get('user_input')
        try:
            qa_pair = QAPair.objects.get(question__iexact=user_input)
            prompt = user_input
            chatbot_response = qa_pair.answer
            chatbot_lines = chatbot_response.splitlines()
            # Remove empty lines
            chatbot_lines = [line for line in chatbot_lines if line.strip()]
            # Convert lines to list of paragraphs
            chatbot_paragraphs = ['<p>{}</p>'.format(line) for line in chatbot_lines]
            # Join paragraphs into a string
            chatbot_response = ''.join(chatbot_paragraphs)
        except QAPair.DoesNotExist:
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
            chatbot_lines = chatbot_response.splitlines()
            # Remove empty lines
            chatbot_lines = [line for line in chatbot_lines if line.strip()]
            # Convert lines to list of paragraphs
            chatbot_paragraphs = ['<p>{}</p>'.format(line) for line in chatbot_lines]
            # Join paragraphs into a string
            chatbot_response = ''.join(chatbot_paragraphs)
    username = request.user.get_username()
            
    context = {
                "response":chatbot_response,
                "prompt":prompt,
              "username":username,
              "profile":profile,
            } 
        
    return render(request, "chatbot/index.html",context)
