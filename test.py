from gtts import gTTS, lang

"""
tts_langs = lang.tts_langs()
for lang in tts_langs:
    print(lang, tts_langs[lang])
"""

hello = gTTS(text='Hello my name is Akbar', lang='en', slow=False)
hello.save('hello.mp3')
