#%%
import os
import whisper

# Cargar el modelo Whisper
model = whisper.load_model("base")

# Definir directorios de origen y destino
source_dir = r"C:\Users\dameliotomas\experiment_VR\results\sub-06\ses-A\beh\audios"
dest_dir = r"C:\Users\dameliotomas\experiment_VR\results\sub-06\ses-A\beh\transcriptions"

# Verificar si el directorio de origen existe
if not os.path.exists(source_dir):
    print(f"El directorio de origen '{source_dir}' no existe.")
    exit()

# Crear el directorio de destino si no existe
if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)

# Iterar sobre cada archivo .wav en el directorio de origen
for filename in os.listdir(source_dir):
    if filename.endswith(".wav"):
        # Construir la ruta completa del archivo
        full_path = os.path.join(source_dir, filename)
        
        try:
            # Transcribir el archivo de audio especificando el idioma español
            result = model.transcribe(full_path, language="es")
            
            # Extraer el texto transcrito
            transcribed_text = result["text"]
            
            # Crear un archivo .txt para guardar la transcripción
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_full_path = os.path.join(dest_dir, txt_filename)
            
            # Guardar el texto transcrito
            with open(txt_full_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(transcribed_text)
                
            print(f"Transcribed {filename} and saved as {txt_filename}")
            
        except Exception as e:
            print(f"Ocurrió un error al procesar {filename}: {e}")

print("Transcription completed.")

#%%
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk

# Descargar stopwords en español
nltk.download('stopwords')

# Definir directorios de origen y destino
source_dir = r"C:\Users\dameliotomas\experiment_VR\results\sub-06\ses-A\beh\transcriptions"

# Obtener stopwords en español
stop_words = set(stopwords.words('spanish'))

# Añadir palabras específicas a las stopwords
additional_stopwords = {"parece", "después", "video", "da"}
stop_words.update(additional_stopwords)

# Listas para almacenar las transcripciones de estímulos positivos y negativos
positive_transcripts = []
negative_transcripts = []

# Función para limpiar y procesar el texto
def process_text(text):
    # Convertir a minúsculas
    text = text.lower()
    # Quitar puntuación y stopwords
    words = text.split()
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    return ' '.join(filtered_words)

# Iterar sobre cada archivo .txt en el directorio de origen
for filename in os.listdir(source_dir):
    if filename.endswith(".txt"):
        # Construir la ruta completa del archivo
        full_path = os.path.join(source_dir, filename)
        
        try:
            # Leer el archivo de transcripción
            with open(full_path, "r", encoding="utf-8") as file:
                transcribed_text = file.read()
            
            # Determinar si el estímulo es positivo o negativo basado en el nombre del archivo
            probe_number = int(filename.split('probe-')[1].split('.')[0])
            if 1 <= probe_number <= 7:
                positive_transcripts.append(transcribed_text)
            elif 8 <= probe_number <= 14:
                negative_transcripts.append(transcribed_text)
            
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")

#%%
positive_transcripts = ['Bueno, al principio hay una escena en la que se nos muestra nadando bajo el agua, lo cual puede ser relajante pero también muy aburrido porque no pasa mucho. Me aburro porque no ocurre nada interesante. Después aparecen la jirafa bebé y la jirafa adulta, lo que me parece muy tierno y divertido. Lo mismo sucede cuando aparecen otros animales como el elefante; sobre todo cuando hay un elefante me parece muy tierno y divertido. Al final, la cámara vuelve a estar bajo el agua y creo que enfoca a una raya o una mantarraya. Pero me pasa lo mismo que al principio: si bien es relajante, también me aburro un poco y pierdo la atención porque no sucede nada en el video. Así que no sé, me aburro y no me genera tanta emoción como una jirafa.',
 'Bueno, el principio es relajante porque se está viendo la carpa, no hay sal y se encuentra con los amigos. Después van a una fiesta que es un poco más animada, la gente está saltando y me parece divertido. Después se hace de noche, se empieza a ver más gente y todos se van a la fiesta. Ya es como una fiesta tipo "¿qué está pasando?". Me parece que se descontrola demasiado. A mí me gusta estar en lugares cuando hay luz de día, pero bueno, todos están muy contentos y eufóricos, así que bien por ellos. Aunque parece que se drogaron también. No me genera una emoción negativa, más bien como que me divierte y la reacción de la gente me parece divertida.',
 'Bueno, se ve una placa con gente disfrutando, todo muy relajante. Después se vuelve un poco vertiginoso porque la imagen muestra a gente en una especie de canoa o balsa en un río rápido, que parece sucio, como con barro. Ahí van con la balsa, y al final están contentos, lo cual me pone contento también porque parece que sobrevivieron. Después se muestra una montaña que no me genera nada porque es solo una montaña.',
 'Bueno, parece fantástico, muy relajante, el agua es transparente, el sol brilla. Después puede ser un poco preocupante cuando aparece una figura o un perro, pero no parece enojado, así que no es muy intimidante. Toda la escena con los peces parece relajante y me genera una sensación de tranquilidad.',
 'Bueno, hay dos personas surfeando y la segunda persona me da un poco de gracia porque tiene el cabello peinado y parece que no está mojado. En general, toda la escena me resulta alegre porque las personas están disfrutando mucho. Ver a alguien hacer algo que le gusta tanto me transmite una sensación de alegría. Además, parece divertido y todo el video, junto con la música, me da la sensación de que es algo agradable y divertido.',
 'El mundo de los sofandas es un lugar donde hay hogar o el narval y los sofandas. Al principio me da un poco de impresión porque se cae algo y pienso "por favor, que no se haya roto", pero parece esponjoso, así que no creo que se haya roto muy fuerte. Después muestran una ciudad divertida y hay go-karts, lo cual también me parece divertido y relajante. Luego no pasa mucho más, solo muestran algunos edificios y un muellecito, pero ya no me genera ninguna emoción. Es relajante pero me aburro un poco.',
 '¿Te animas? Sí. Y, ciertamente, se me ha quedado el auto del box. No sé, y me ha empezado a dar la vuelta y me parece, a lo largo del video, super divertido. Me generaba una sensación de euforia tipo vértigo, pero en el buen sentido. Me parece super divertido, pero no es mi caso. Es una diversión eufórica. Y después al final, nada, me parece divertido cómo hace girar el auto con menos. Recomendaría verlo en primera persona. A pesar de que me imagina con toda la euforia.']

negative_transcripts = ['¿Cómo que te contaste ahí? Bueno, me parece que es muy relajante andar en auto por ese lugar, pero me enojo cuando sacan el celular porque no deberían hacerlo mientras manejan. Además, me resultan molestas las voces de las mujeres, parecen estúpidas y claramente no se puede confiar en alguien que conduce de esa forma. También me molesta que conduzca mal porque andar rápido por un camino que no es seguro es peligroso. Es obvio que van a chocar, ¿no? Porque ese es el punto del video. En un momento parece que no chocan y eso da un poco de alivio, volviendo a ser relajante. Pero después no sé qué pasa, como que se apaga la luz, supongo que alguien molesta desde atrás y terminan chocando con un tractor. Eso me sorprende porque pensé que ya había pasado el peligro, pero no, chocan con el tractor. Me dio un poco de gracia y pena porque el ruido que hacen es gracioso pero la persona está en el parabrisas y puede estar muerta. No creo que se merezca tanto, pero bueno.',
 '¿Qué es la manera? ¿Cuándo quieres empezar? ¿Estás bien? ¿Estás bien? No me avisa que está con él. Está bien, pero bueno. Entonces al principio se ve a la persona en el agua con las olas entrando y me parece que está muerta, lo cual es triste. Aunque no tanto, porque si se subió a un avión para disparar a la gente, digo, eso es parte del trabajo, no es normal que te caigan. Así que tampoco me da tanto mal. Pero bueno, tampoco es muy divertida la escena. Y después se ve el avión en primera persona y lo mismo, me da un poco de miedo, pero también como que bueno, son cosas que pasan en la guerra. Claramente, la persona sabía a lo que se exponía, así que no me parece tan mal. No es que me genere emociones intensas, más bien una sensación de neutralidad, entendiendo que es una situación peligrosa.',
 'Primero me asusté porque aparece una mujer toda asustada y también me asusté. Luego aparece un payaso y me da mucho miedo y también me genera odio. Sigue pegando obviamente y no sé qué más hace, es muy agresivo. Al final me da alivio porque me doy cuenta que era una actuación, parte de una puesta en escena. Pero aún así, me generó bastante enojo.',
 'Bueno, en tres videos sobre el personaje manejando, el primer video me genera ansiedad porque están tomando y manejando, y eso me da angustia. En el primer video parece que van a chocar por manejar ebrios, pero después resulta que no, que son responsables porque no tuvieron ningún accidente, lo cual me alivia. En el segundo video pisa un bebé, lo cual es horrible y me enoja mucho, porque uno no debe andar manejando distraído. Termina preso y me da satisfacción que haya justicia. En el último video, salen tomando y se estrellan contra un camión por pasarse un semáforo en rojo, lo cual también me enoja. Me causa molestia porque luego otros tienen que limpiar el desastre. Termina el video y siento una mezcla de enojo y alivio por la justicia.',
 'Bueno, es un video bastante aburrido. Primero muestran una perspectiva del suelo y unos bichos que son insectos, supongo que esos quisieron mostrar, pero no me interesa mucho. Después aparecen unos ratones, lo cual me parece simpático pero tampoco pasa mucho en el video. Se ven los ratones comiendo y ocasionalmente mirando a la cámara. Finalmente, lo mismo con unos conejos, que me parecen aún más simpáticos porque hacen ruidos graciosos. Lo único que me molesta un poco es que no se entiende bien lo que son esos bichos. Es un video un poco feo.',
 'Me da miedo porque aparecen víboras, lo cual es preocupante. Me siento incómodo viendo víboras porque me dan miedo. Aunque no hay nada particularmente peligroso en el video, me da ansiedad. Además, los bichos me parecen asquerosos y feos. La escena siempre es la misma, así que no me genera nada nuevo. A veces hacen ruido y eso me da un poco de asco.',
 'Bueno, me intimida tener una casa de noche y me da miedo porque parece que va a pasar algo, típica película de terror. Aparece un viejo con la dentadura en mal estado y me dice que me vaya de la casa, lo cual me da miedo pero también risa porque es un cliché. Después, la otra escena, es como si me estuvieran hechizando. Parece obvio que algo va a pasar con la monja. La sombra de la monja me da ansiedad y cuando finalmente aparece, me da un salto de susto pero también risa porque es obvio. Al final, te muestra la monja para asustarte un poco más, pero ya no es tan efectivo.']

# Procesar los textos de las transcripciones
positive_text = ' '.join([process_text(text) for text in positive_transcripts])
negative_text = ' '.join([process_text(text) for text in negative_transcripts])

#%%
positive_text = 'beginning scene shows swimming underwater can be relaxing boring nothing happens bored nothing happens appear baby giraffe giraffe tender same happens appear animals elephant tender camera returns underwater I think focuses on a stingray same thing happens although it is relaxing I also get bored lose attention nothing happens so I get bored it does not generate much emotion relaxing watching tent no salt meets goes party people jumping gets starts seeing people go party kind of gets out of control I like places daylight happy so good although they got high does not generate emotion it amuses me people reaction sees plaque people becomes vertiginous image shows people kind of canoe raft river they go in the end makes me happy shows mountain generates nothing just water sun can be worrying figure appears so whole scene fish relaxing generates feeling two people surfing second person funny hair styled whole scene cheerful people enjoying seeing someone do what they like gives feeling fun along pleasant feeling world of sofandas place home narwhal beginning impression falls I think so I don\'t think broken they show fun city fun then happens just show buildings generates no relaxing get bored got car started spinning whole super generated euphoria feeling kind of good super fun funny how it spins car would recommend seeing it first even imagine all'

negative_text = 'told relaxing driving car annoyed they take out phone should not do it while annoying voices seem stupid clearly can\'t trust someone driving annoying drives badly driving fast road safe obvious going point moment crash back to being I don\'t know light goes off I guess someone annoys behind ends up crashing surprised I thought passed crash gave funny noise makes funny person windshield can think deserve want let know so beginning sees person water waves coming in although if got on plane shooting part normal so neither neither fun sees plane first person things happen person knew so does not generate emotions well feeling understanding situation first got scared woman appears all scared then clown appears fear generates continues hitting obviously I don\'t know end relief I realize part set still generated quite three videos character first generates anxiety drinking first they are going to crash driving turns out responsible no second steps terrible angry must be driving ends up satisfaction last go out drinking crash truck running red light causes annoyance then clean ends feel mix anger relief quite first shows perspective ground bugs guess wanted interested appear cute nothing happens sees rats eating occasionally looking same appear even cuter make noises only annoying doesn\'t understand well fear appears feel uncomfortable seeing snakes they give although particularly dangerous bugs seem disgusting scene always so generates sometimes makes noise intimidating having house night fear something typical movie old man appears bad teeth tells go fear laugh so obvious going to happen shadow nun anxiety finally jump scare laugh shows nun scare you so'

# Generar nubes de palabras
positive_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_text)
negative_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(negative_text)

# Mostrar las nubes de palabras
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Positive Stimuli")
plt.imshow(positive_wordcloud, interpolation='bilinear')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Negative Stimuli")
plt.imshow(negative_wordcloud, interpolation='bilinear')
plt.axis('off')

plt.show()



# %%
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re

# Función para procesar texto y eliminar palabras no deseadas
def process_text(text):
    # Convertir texto a minúsculas
    text = text.lower()
    # Eliminar palabras no deseadas
    text = re.sub(r'\b(parece|después|video|da)\b', '', text)
    return text

positive_transcripts = [
    'Bueno, al principio hay una escena en la que se nos muestra nadando bajo el agua, lo cual puede ser relajante pero también muy aburrido porque no pasa mucho. Me aburro porque no ocurre nada interesante. Después aparecen la jirafa bebé y la jirafa adulta, lo que me parece muy tierno y divertido. Lo mismo sucede cuando aparecen otros animales como el elefante; sobre todo cuando hay un elefante me parece muy tierno y divertido. Al final, la cámara vuelve a estar bajo el agua y creo que enfoca a una raya o una mantarraya. Pero me pasa lo mismo que al principio: si bien es relajante, también me aburro un poco y pierdo la atención porque no sucede nada en el video. Así que no sé, me aburro y no me genera tanta emoción como una jirafa.',
    'Bueno, el principio es relajante porque se está viendo la carpa, no hay sal y se encuentra con los amigos. Después van a una fiesta que es un poco más animada, la gente está saltando y me parece divertido. Después se hace de noche, se empieza a ver más gente y todos se van a la fiesta. Ya es como una fiesta tipo "¿qué está pasando?". Me parece que se descontrola demasiado. A mí me gusta estar en lugares cuando hay luz de día, pero bueno, todos están muy contentos y eufóricos, así que bien por ellos. Aunque parece que se drogaron también. No me genera una emoción negativa, más bien como que me divierte y la reacción de la gente me parece divertida.',
    'Bueno, se ve una placa con gente disfrutando, todo muy relajante. Después se vuelve un poco vertiginoso porque la imagen muestra a gente en una especie de canoa o balsa en un río rápido, que parece sucio, como con barro. Ahí van con la balsa, y al final están contentos, lo cual me pone contento también porque parece que sobrevivieron. Después se muestra una montaña que no me genera nada porque es solo una montaña.',
    'Bueno, parece fantástico, muy relajante, el agua es transparente, el sol brilla. Después puede ser un poco preocupante cuando aparece una figura o un perro, pero no parece enojado, así que no es muy intimidante. Toda la escena con los peces parece relajante y me genera una sensación de tranquilidad.',
    'Bueno, hay dos personas surfeando y la segunda persona me da un poco de gracia porque tiene el cabello peinado y parece que no está mojado. En general, toda la escena me resulta alegre porque las personas están disfrutando mucho. Ver a alguien hacer algo que le gusta tanto me transmite una sensación de alegría. Además, parece divertido y todo el video, junto con la música, me da la sensación de que es algo agradable y divertido.',
    'El mundo de los sofandas es un lugar donde hay hogar o el narval y los sofandas. Al principio me da un poco de impresión porque se cae algo y pienso "por favor, que no se haya roto", pero parece esponjoso, así que no creo que se haya roto muy fuerte. Después muestran una ciudad divertida y hay go-karts, lo cual también me parece divertido y relajante. Luego no pasa mucho más, solo muestran algunos edificios y un muellecito, pero ya no me genera ninguna emoción. Es relajante pero me aburro un poco.',
    '¿Te animas? Sí. Y, ciertamente, se me ha quedado el auto del box. No sé, y me ha empezado a dar la vuelta y me parece, a lo largo del video, super divertido. Me generaba una sensación de euforia tipo vértigo, pero en el buen sentido. Me parece super divertido, pero no es mi caso. Es una diversión eufórica. Y después al final, nada, me parece divertido cómo hace girar el auto con menos. Recomendaría verlo en primera persona. A pesar de que me imagina con toda la euforia.'
]

negative_transcripts = [
    '¿Cómo que te contaste ahí? Bueno, me parece que es muy relajante andar en auto por ese lugar, pero me enojo cuando sacan el celular porque no deberían hacerlo mientras manejan. Además, me resultan molestas las voces de las mujeres, parecen estúpidas y claramente no se puede confiar en alguien que conduce de esa forma. También me molesta que conduzca mal porque andar rápido por un camino que no es seguro es peligroso. Es obvio que van a chocar, ¿no? Porque ese es el punto del video. En un momento parece que no chocan y eso da un poco de alivio, volviendo a ser relajante. Pero después no sé qué pasa, como que se apaga la luz, supongo que alguien molesta desde atrás y terminan chocando con un tractor. Eso me sorprende porque pensé que ya había pasado el peligro, pero no, chocan con el tractor. Me dio un poco de gracia y pena porque el ruido que hacen es gracioso pero la persona está en el parabrisas y puede estar muerta. No creo que se merezca tanto, pero bueno.',
    '¿Qué es la manera? ¿Cuándo quieres empezar? ¿Estás bien? ¿Estás bien? No me avisa que está con él. Está bien, pero bueno. Entonces al principio se ve a la persona en el agua con las olas entrando y me parece que está muerta, lo cual es triste. Aunque no tanto, porque si se subió a un avión para disparar a la gente, digo, eso es parte del trabajo, no es normal que te caigan. Así que tampoco me da tanto mal. Pero bueno, tampoco es muy divertida la escena. Y después se ve el avión en primera persona y lo mismo, me da un poco de miedo, pero también como que bueno, son cosas que pasan en la guerra. Claramente, la persona sabía a lo que se exponía, así que no me parece tan mal. No es que me genere emociones intensas, más bien una sensación de neutralidad, entendiendo que es una situación peligrosa.',
    'Primero me asusté porque aparece una mujer toda asustada y también me asusté. Luego aparece un payaso y me da mucho miedo y también me genera odio. Sigue pegando obviamente y no sé qué más hace, es muy agresivo. Al final me da alivio porque me doy cuenta que era una actuación, parte de una puesta en escena. Pero aún así, me generó bastante enojo.',
    'Bueno, en tres videos sobre el personaje manejando, el primer video me genera ansiedad porque están tomando y manejando, y eso me da angustia. En el primer video parece que van a chocar por manejar ebrios, pero después resulta que no, que son responsables porque no tuvieron ningún accidente, lo cual me alivia. En el segundo video pisa un bebé, lo cual es horrible y me enoja mucho, porque uno no debe andar manejando distraído. Termina preso y me da satisfacción que haya justicia. En el último video, salen tomando y se estrellan contra un camión por pasarse un semáforo en rojo, lo cual también me enoja. Me causa molestia porque luego otros tienen que limpiar el desastre. Termina el video y siento una mezcla de enojo y alivio por la justicia.',
    'Bueno, es un video bastante aburrido. Primero muestran una perspectiva del suelo y unos bichos que son insectos, supongo que esos quisieron mostrar, pero no me interesa mucho. Después aparecen unos ratones, lo cual me parece simpático pero tampoco pasa mucho en el video. Se ven los ratones comiendo y ocasionalmente mirando a la cámara. Finalmente, lo mismo con unos conejos, que me parecen aún más simpáticos porque hacen ruidos graciosos. Lo único que me molesta un poco es que no se entiende bien lo que son esos bichos. Es un video un poco feo.',
    'Me da miedo porque aparecen víboras, lo cual es preocupante. Me siento incómodo viendo víboras porque me dan miedo. Aunque no hay nada particularmente peligroso en el video, me da ansiedad. Además, los bichos me parecen asquerosos y feos. La escena siempre es la misma, así que no me genera nada nuevo. A veces hacen ruido y eso me da un poco de asco.',
    'Bueno, me intimida tener una casa de noche y me da miedo porque parece que va a pasar algo, típica película de terror. Aparece un viejo con la dentadura en mal estado y me dice que me vaya de la casa, lo cual me da miedo pero también risa porque es un cliché. Después, la otra escena, es como si me estuvieran hechizando. Parece obvio que algo va a pasar con la monja. La sombra de la monja me da ansiedad y cuando finalmente aparece, me da un salto de susto pero también risa porque es obvio. Al final, te muestra la monja para asustarte un poco más, pero ya no es tan efectivo.'
]

# Procesar los textos de las transcripciones
positive_text = ' '.join([process_text(text) for text in positive_transcripts])
negative_text = ' '.join([process_text(text) for text in negative_transcripts])

positive_text = 'beginning scene shows swimming underwater can be relaxing boring nothing happens bored nothing happens appear baby giraffe giraffe tender same happens appear animals elephant tender camera returns underwater I think focuses on a stingray same thing happens although it is relaxing I also get bored lose attention nothing happens so I get bored it does not generate much emotion relaxing watching tent no salt meets goes party people jumping gets starts seeing people go party kind of gets out of control I like places daylight happy so good although they got high does not generate emotion it amuses me people reaction sees plaque people becomes vertiginous image shows people kind of canoe raft river they go in the end makes me happy shows mountain generates nothing just water sun can be worrying figure appears so whole scene fish relaxing generates feeling two people surfing second person funny hair styled whole scene cheerful people enjoying seeing someone do what they like gives feeling fun along pleasant feeling world of sofandas place home narwhal beginning impression falls I think so I don't think broken they show fun city fun then happens just show buildings generates no relaxing get bored got car started spinning whole super generated euphoria feeling kind of good super fun funny how it spins car would recommend seeing it first even imagine all'

negative_text = 'told relaxing driving car annoyed they take out phone should not do it while annoying voices seem stupid clearly can't trust someone driving annoying drives badly driving fast road safe obvious going point moment crash back to being I don't know light goes off I guess someone annoys behind ends up crashing surprised I thought passed crash gave funny noise makes funny person windshield can think deserve want let know so beginning sees person water waves coming in although if got on plane shooting part normal so neither neither fun sees plane first person things happen person knew so does not generate emotions well feeling understanding situation first got scared woman appears all scared then clown appears fear generates continues hitting obviously I don't know end relief I realize part set still generated quite three videos character first generates anxiety drinking first they are going to crash driving turns out responsible no second steps terrible angry must be driving ends up satisfaction last go out drinking crash truck running red light causes annoyance then clean ends feel mix anger relief quite first shows perspective ground bugs guess wanted interested appear cute nothing happens sees rats eating occasionally looking same appear even cuter make noises only annoying doesn't understand well fear appears feel uncomfortable seeing snakes they give although particularly dangerous bugs seem disgusting scene always so generates sometimes makes noise intimidating having house night fear something typical movie old man appears bad teeth tells go fear laugh so obvious going to happen shadow nun anxiety finally jump scare laugh shows nun scare you so'

#%%
# Función para generar colores en tonos verdes menos brillantes
def green_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(100, 50%%, %d%%)" % random_state.randint(30, 60)

# Función para generar colores en tonos rojos menos brillantes
def red_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 50%%, %d%%)" % random_state.randint(30, 60)

# Generar nubes de palabras
positive_wordcloud = WordCloud(width=800, height=400, background_color='white', color_func=green_color_func).generate(positive_text)
negative_wordcloud = WordCloud(width=800, height=400, background_color='white', color_func=red_color_func).generate(negative_text)

# Mostrar las nubes de palabras
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Positive videos", fontsize=15)
plt.imshow(positive_wordcloud, interpolation='bilinear')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Negative videos", fontsize=15)
plt.imshow(negative_wordcloud, interpolation='bilinear')
plt.axis('off')

plt.show()
# %%
