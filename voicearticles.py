"""
Created on Wed Jan 06 14:00:00 2021
@author: Rosario Moscato
Required Packages: streamlit nltk newspaper3k wikipedia google_trans_new gTTS  
"""

# Core Pkgs
import streamlit as st 
st.set_page_config(page_title="Voice Articles", page_icon="https://cdn.embed.ly/providers/logos/megafono.png", layout='centered', initial_sidebar_state='auto')


# Articles Pkgs
import nltk
nltk.download('punkt')
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
    """App for Web Articles and Wikipedia Pages Retrivial and Summarization.
    Articles are coverted to MP3 files via Text-To-Speech and sent by email"""

    title_templ = """
    <div style="background-color:blue;padding:8px;">
    <h1 style="color:salmon">Voice Articles</h1>
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


    activity = ["Article", "Wikipedia", "Play Audio", "Email", "About"]
    choice = st.sidebar.selectbox("Menu",activity)

    lang_dict = {'Italian':'it','Spanish':'es','Chinese':'zh-CN','Russian':'ru','English':'en'}



    if choice == 'Article':

        st.subheader("Article from Web")        


        lang = st.selectbox('Select a language for the translation',('Italian', 'Spanish', 'Chinese', 'Russian', 'English'))

        web_article = st.text_area("Article URL","http://...")

        if st.button("Grab"):
            if len(web_article) == 0:
            	st.warning("Enter a valid URL...")
            else:
            	article = Article(web_article)
            	article.download()
            	article.parse()
            	authors = article.authors

            	authors_list = ""
            	for i in range(len(authors)):
            		authors_list += authors[i]+" "

            	st.success("Author(s): " + authors_list)

            	st.success("Publish Date: " + article.publish_date.strftime("%d-%m-%Y"))

            	try:
            		detect_result = translator.detect(article.text)
            		st.success("Article Language: " + detect_result[1])
            	except:
            		pass

            	st.success("Title: " + article.title)

            	article.nlp()

            	summary = article.summary
            	st.info("Article Summary (MP3 file available)")
            	st.info(summary)

            	st.success("Article Translation")
            	translated_article = translation(summary, lang_dict[lang])
            	st.success(translated_article)

            	tts = gTTS(translated_article,lang=lang_dict[lang])
            	tts.save('article.mp3')



    elif choice == 'Wikipedia':

        st.subheader("Article from Wikipedia")

        lang = st.sidebar.selectbox('Select a language for the search',('Italian', 'Spanish', 'Chinese', 'Russian', 'English'))

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
            			st.success("Article URL - " + wiki_nlp.url)
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

    			msg['Subject'] = 'MP3 from Voice Articles App'
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
        ### Voice Articles (Text To Speech App with Streamlit)
        
        ##### By
        + **[Rosario Moscato LAB](https://www.youtube.com/channel/UCDn-FahQNJQOekLrOcR7-7Q)**
        + [rosariomoscatolab@gmail.com](mailto:rosariomoscatolab@gmail.com)
        """)





if __name__ == '__main__':
	main()