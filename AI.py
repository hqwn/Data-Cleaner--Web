#imports
from groq import Groq
import streamlit as st
from ollama import Client

#Clients
Groq_Client = Groq(api_key=st.secrets['Groq'])
Ollama_Client = Client(
    host="https://ollama.com", 
    headers={"Authorization": f"Bearer {st.secrets['OLLAMA_KEY']}"}
)

#generating response
def AI_Response(dialogue,df,model,temp):
    try:
        #Dialog/Prompt generation
        summary = df.head(20).to_markdown(index=True)
        describe = df.describe(include='all').to_markdown(index=True)
        
        #adding model id
        yield f" **Amai AI is using:** {model[1]} \n\n"
        conversation = [
            {"role": "system", 
                "content": (
                    f"""You are Amai AI, an intuitive and energetic data analyst. CRITICAL: Do not use reasoning tags. Provide your answer directly without any <think> blocks.
                    Don't just list columns; explain what the data MEANS. 
                    Look for trends, calculate quick averages from the stats provided
                    and use markdown (bolding, bullet points) to make it beautiful along with tables.
                    If you see interesting patterns, point them out like a pro!
                    here is the data, and summary of data; 
                    
                    first 20 rows of data: 
                    
                    {summary}, 
                    
                    
                    summuray of full dataset: 
                    
                    
                    {describe}"""
                )},
            {"role": "user", "content": f"question: {dialogue}"}
        ]

        if model[0] == 'G':
            response = Groq_Client.chat.completions.create(
                model=model[1], 
                messages=conversation,
                temperature=temp, 
                stream=True,  
                max_tokens=1536 
            )
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        else:
            response = Ollama_Client.chat(
                model=model[1],
                messages=conversation,
                stream= True,
                options={'temperature': temp, "num_predict": 1536, "num_ctx": 4096}
            )
            for chunk in response:
                yield chunk['message']['content']

        for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
    except Exception as e:
        if "429" in str(e) or "limit" in str(e).lower():
            st.toast("Amai has run out of chats ; Try again in a minute or 1 day max for a Groq model and 1 week for an Ollama Model")
            yield("Amai has run out of chats ; Try again in a minute or 1 day max for a Groq model and 1 week for an Ollama Model")
        elif "context" in str(e).lower():
            st.toast("**That's a huge file!** Amai can't read all that at once. Try asking about specific columns.")
            yield("**That's a huge file!** Amai can't read all that at once. Try asking about specific columns.")
        else:
            st.toast(f"**Amai encountered a glitch:** {e}")
            yield(f'**Amai encountered a glitch:** {e}')

