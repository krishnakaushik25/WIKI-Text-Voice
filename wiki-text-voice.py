
# Core Pkgs
import streamlit as st 
st.set_page_config(page_title="Wikepedia Text-To-Voice", page_icon="https://cdn.embed.ly/providers/logos/megafono.png", layout='centered', initial_sidebar_state='auto')


# Articles Pkgs
#import nltk
import nltk_download_utils
#nltk.download('punkt')
from newspaper import Article

import wikipedia



# Translation Pkg
from google_trans_new import google_translator

# TTS Pkg
from gtts import gTTS

# Email Pkg
import smtplib


def translation(text, lang):

	translator = google_translator()
	return translator.translate(text, lang_tgt=lang)



def main():
    """App for Web Articles and Wikipedia Pages Retrieval and Summarization.
    Articles are coverted to MP3 files via Text-To-Speech and sent by email"""

    title_templ = """
    <div style="background-color:blue;padding:8px;">
    <h1 style="color:salmon">Wikepedia Text-To-Voice</h1>
    </div>
    """

    st.markdown(title_templ,unsafe_allow_html=True)

    subheader_templ = """
    <div style="background-color:salmon;padding:8px;">
    <h3 style="color:blue">Save and Play MP3 of your favourite Articles!</h3>
    </div>
    """

    st.markdown(subheader_templ,unsafe_allow_html=True)

    st.sidebar.image("https://cdn.embed.ly/providers/logos/megafono.png", use_column_width=True)

    translator = google_translator()


    activity = ["Wikipedia","Play Audio", "Email", "About"]
    choice = st.sidebar.selectbox("Menu",activity)

    lang_dict = {'Telugu':'te','Hindi':'hi','Bengali':'bn','English':'en','Italian':'it'}


    if choice == 'Wikipedia':

        st.subheader("Article from Wikipedia")

        lang = st.sidebar.selectbox('Select a language for the search',('Telugu', 'Hindi','Bengali','English','Italian'))

        lan = lang_dict[lang]

        wikipedia.set_lang(lan)

        topic = st.sidebar.text_area("Topic to Search For","Topic...")
        
        if st.sidebar.checkbox("Search"):
            if len(topic) == 0:
            	st.warning("Enter a Topic...")
            else:
            	wiki_articles  = wikipedia.search(topic, results=3)

            	if len(wiki_articles) == 0:
            		st.warning("No Matches on Wikipedia")
            	else:
            		text = str(len(wiki_articles)) + " articles found on Wikipedia"
            		st.info(text)

            		#st.json(wiki_articles)

            		wiki = st.selectbox("Select an Article",wiki_articles)

            		try:
            			wiki_nlp = wikipedia.page(wiki)
            			st.success("Article Title - " + wiki_nlp.title)
            			st.success("Article URL - " + wiki_nlp.url[:15] + (wiki_nlp.url[15:] and '..'))
            			st.info("Article Summary (MP3 file available)")
            			summary = wiki_nlp.summary
            			st.write(summary)

            			tts = gTTS(summary,lang=lang_dict[lang])
            			tts.save('article.mp3')
            		except:
            			st.warning("No Match any Page, Select another one...")



    elif choice == 'Play Audio':

    	st.subheader("Play Your MP3 Article")

    	st.info("Click 'Play' to reproduce your Article")

    	#if st.button("Play"):

    	try:
    		audio_file = open('article.mp3', 'rb')
    		audio_bytes = audio_file.read()
    		st.audio(audio_bytes, format='audio/mp3')

    	except:
    		st.warning("Select the Article and make the Summary first, please...")



    elif choice == 'Email':

    	st.subheader("Send Your MP3 Article by Email")

    	sender = st.text_input("Type sender's email address")
    	password = st.text_input("Type sender's password", type="password")
    	receiver = st.text_input("Type receiver's email address")

    	if sender != "" and password != "" and receiver != "":
    		if st.button("EMAIL"):

    			from os.path import basename
    			from email.mime.text import MIMEText
    			from email.mime.multipart import MIMEMultipart
    			from email.mime.application import MIMEApplication

    			msg = MIMEMultipart()

    			msg['Subject'] = 'MP3 from Wikepedia Text-To-Voice APP'
    			msg['From'] = sender
    			msg['To'] = receiver

    			filename = 'article.mp3'
    			with open(filename, 'rb') as f:
    				part = MIMEApplication(f.read(), Name=basename(filename))

    			part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
    			msg.attach(part)

    			user = sender
    			password = password

    			with smtplib.SMTP('smtp.gmail.com', 587) as server:

    				try:
	    				server.starttls()
	    				server.login(user, password)
	    				server.sendmail(sender, receiver, msg.as_string())
	    				st.info("Email Successfully Sent!")
	    			except:
	    				st.warning("Please Check Your Account...")

    	else:
    		st.warning("sender address, password or receiver address missing...")


            
    # About CHOICE
    else:
        st.subheader("About")

        st.write("")
        st.write("")

        st.markdown("""
        ### Wikepedia Text-To-Voice (Text To Speech App with Streamlit)
        
        ##### By
        + **[Krishna Kaushik](https://github.com/krishnakaushik25)**
        + [Reference Repository](https://github.com/rosariomoscato/VoiceArticles)
        """)





if __name__ == '__main__':
	main()
