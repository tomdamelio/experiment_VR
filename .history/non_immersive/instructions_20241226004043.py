# file for writing the instrucitons of the task

non_immersive_instructions_text = {

    # WELCOME Y BASELINE VAN JUNTAS AL MOMENTO DE GRABAR LOS AUDIOS

    'welcome_text': "¡Te damos la bienvenida a este experimento, \n\n"
        "con el que vamos a estudiar como nuestras emociones cambian en tiempo real!\n",
        #"Presioná la barra espaciadora para continuar.",
     
    'baseline_instructions_text': "Antes de empezar con las tareas principales,\n"
        "te vamos a pedir que te relajes y que mires la cruz que aparece en el centro de la pantalla. \n\n"
        "Tratá de no moverte y no hablar de ser posible durante los próximos 5 minutos\n"
        "para garantizar la precisión de la recolección de datos.\n\n"
        "Esto vale para todo el experimento, en particular cuando estes viendo los distintos videos mas tarde."
        "Cualquier de estos momivientos durante el experimento puede afectar las mediciones que estamos haciendo.\n\n"
        "Ahora vamos a empezar.\n\n",
        #"Presioná la barra espaciadora para continuar (y aguardá unos segundos).",


    'valence_practice_instructions_text': "¡Listo! Vamos a empezar con alugnos videos de práctica del experimento.\n\n"
        "Te vamos a pedir que uses el joystick que tenes delante tuyo para reportar\n"
        "tu nivel de valencia emocional mientras ves un video, en tiempo real,\n"
        "en una dimensión que va desde 'negativo' a 'positivo'.\n"
        "Al reportar en el extremo izquierdo, sentis infelicidad,\n"
        "molestia, insatisfacción, melancolía, desesperación, aburrimiento.\n"
        "Al reportar en el extremo derecho, sentis felicidad plena, alegría,\n"
        "satisfacción, bienestar y esperanza.\n\n"
        "Podés representar niveles intermedios ubicándote en cualquier otro punto de la escala con el joystick,\n"
        "indicando así cómo te sentís en tiempo real al ver el video.\n\n"
        "Recorda: negativo a izquierda y positivo a derecha\n\n",
        #"Presioná la barra espaciadora para continuar.",

    'arousal_practice_instructions_text': "Ahora vas a tener que reportar tu nivel de activación emocional mientras ves un video,\n"
        "en una dimensión que va desde 'calmado' a 'emocionado'.\n\n"
        "Reportando en el extremo izquierdo de la escala, sentis relajación, tranquilidad,\n"
        "inactividad, aburrimiento, somnolencia, o ausencia de excitación.\n\n"
        "Reportando en el extremo derecho, sentis estimulación completa,\n"
        "emoción intensa, frenesí, nerviosismo, alerta y mayor activación.\n\n"
        "Podés representar niveles intermedios posicionándote en cualquier otro punto de la escala con el joystick,\n"
        "indicando así cómo te sentís en tiempo real al ver el video.\n\n"
        "Recorda: calmado a izquierda y emocionado a derecha\n\n",
        #"Presioná la barra espaciadora para continuar.",

    'post_stimulus_self_report_text_1': "Después de cada video, vas a tener que indicar tus niveles de \n"
        "valencia, activación emocional, preferencia, atencion, familiaridad,\n"
        "y las emociones básicas que experimentaste durante el vídeo, asi como tambien tus niveles de mareo que experimentaste.\n\n"
        "Vas a reportar esto de forma verbal, en una escala que va de una a 1 a 9, luego de que te nombre cada emocion.\n\n",
        #"Presioná la barra espaciadora para continuar.",

   # 'post_stimulus_self_report_text_2': "Entonces, las dos primeras dimensiones son:\n"
   #     "'valencia', que refiere a cuán positiva o negativa fue tu experiencia emocional, y \n"
   #     "'activación', que indica cuán emocionado/a o calmado/a te encontrabas. \n\n"
   #     "Por otro lado, abajo vas a encontrar casillas de 'emociones básicas'\n"
   #     "son aquellas emociones primarias como \n"
   #     "alegría, tristeza, ira, etc., que pudiste haber sentido.\n\n"
   #     "Presiona la barra espaciadora para continuar.",

    #'post_stimulus_self_report_text_2_draft': "Recordá que:\n\n"
    #    "'valencia' se refiere a cuán negativa o positiva fue tu experiencia emocional,\n\n"
    #    "'activación emocional' indica cuán calmado o emocionado te encontrabas;\n\n"
    #    "'preferencia' muestra cuánto te gustó el estímulo;\n\n"
    #    "'atencion' refleja tu nivel de atención en el ensayo anterior;\n\n"
    #    "'familiaridad' indica si el video te resultó conocido o no;\n\n\n"
    #    "y 'emociones básicas' son aquellas emociones primarias como \n"
    #    "alegría, tristeza, ira, etc., que pudiste haber sentido.\n\n",
        
        
    #'motion_sickness_report_text': "Por favor, evaluá tu nivel de mareo por movimiento utilizando la escala de \n"
    #    "1 (sin síntomas) a 9 (síntomas extremadamente severos).\n\n",
    
'post_stimulus_self_report_practice': 
    "Ahora te voy a nombrar distintas emociones. Y para cada una, "
    "quiero que indiques verbalmente con un número entero del 1 al 9 cómo fue tu experiencia durante el video.\n\n"
    "Podés representar valores intermedios dicendo otros numeros de esa escala.\n\n"
    "Empezamos\n\n"

    "1) *Valencia emocional*: \n"
    "   - 1 = totalmente negativo \n"
    "   - 9 = totalmente positivo\n\n"

    "2) *Activación emocional*: \n"
    "   - 1 = totalmente calmado \n"
    "   - 9 = totalmente emocionado\n\n"

    "3) *Preferencia*: \n"
    "   - 1 = completo desagrado del video\n"
    "   - 9 = completo agrado del video\n\n"

    "4) *Atención*: \n"
    "   - 1 = no presté atención al video \n"
    "   - 9 = presté completa atención al video \n\n"

    "5) *Familiaridad*: \n"
    "   - 1 = nunca había visto este video antes \n"
    "   - 9 = conozco este video muy bien\n\n"

    "6) *Mareo*: \n"
    "   - 1 = sin síntomas de mareo \n"
    "   - 9 = CON síntomas extremadamente severos de mareo\n\n"

    "Para las siguientes emociones básicas, la escala del 1 al 9 indica la "
    "intensidad con la que sentiste cada una:\n\n"

    "7) *Asco*:\n"
    "   - 1 = ausencia de la emoción \n"
    "   - 9 = intensidad máxima\n\n"

    "8) *Felicidad*:\n"
    "   - 1 = ausencia de la emoción \n"
    "   - 9 = intensidad máxima\n\n"

    "9) *Sorpresa*:\n"

    "10) *Enojo*:\n"
    
    "11) *Miedo*:\n"

    "12) *Tristeza*:\n"

    "13) *Neutral*:\n",
    
'post_stimulus_self_report': 
    "Ahora vamos con el reporte de las distintas emociones que sentiste durante el video, en la escala del 1 al 9\n\n"

    "1) *Valencia emocional*: \n"

    "2) *Activación emocional*: \n"
    
    "3) *Preferencia*: \n"

    "4) *Atención*: \n"

    "5) *Familiaridad*: \n"

    "6) *Mareo*: \n"

    "7) *Asco*:\n"

    "8) *Felicidad*:\n"

    "9) *Sorpresa*:\n"

    "10) *Enojo*:\n"
    
    "11) *Miedo*:\n"

    "12) *Tristeza*:\n"

    "13) *Neutral*:\n",
    

    #'post_stimulus_self_report_text_3': "Para dar tu respuesta en las escalas \n"
    #    "no tenés que arrastrar el círculo como hacés en el resto de los ensayos. \n\n"
    #    "En lugar de eso, hacé click con el mouse en el punto exacto \n"
    #    "de la escala que mejor represente tu estado afectivo después de ver el video.\n\n"
    #    "Por otro lado, te recuerdo que es importante que estas respuestas sean lo más\n"
    #    "precisas posibles de acuerdo a como vos te sentiste al ver los videos.\n\n"
    #    "¿Estás listo/a?\n\n"
    #    "Presioná la barra espaciadora para continuar (y aguardá unos segundos).",

    'luminance_practice_instructions_text': "Algunos videos van a ser simplemente una pantalla que cambia de color, \n"
        "en un rango que va de verde sin brillo a verde brillante.\n"
        "Tu tarea es reportar tu percepción de cómo cambia \n"
        "el brillo en la pantalla en tiempo real, en una dimensión \n"
        "que va desde 'bajo brillo' a izquierda 'alto brillo' a derecha.\n\n"
        "Podés representar niveles intermedios de brillo posicionándote en cualquier \n"
        "punto de la escala, de acuerdo con cómo percibas el brillo del video en tiempo real.\n\n"
        "¿Estás listo/a?\n\n"
        "Rercorda: bajo brillo a la izquierda y alto brillo a la derecha.\n\n",
        #"Presioná la barra espaciadora para continuar con la explicación.",
        
    'luminance_instructions_direct':  "Ahora vas a reportar cómo cambia \n"
        "el brillo en la pantalla en tiempo real, en una dimensión \n"
        "que va desde 'bajo brillo' a izquierda 'alto brillo' a derecha.\n\n",

    'luminance_instructions_inverse':  "Ahora vas a reportar cómo cambia \n"
        "el brillo en la pantalla en tiempo real, en una dimensión \n"
        "que va desde 'alto brillo' a izquierda 'bajo brillo' a derecha.\n\n",

    #'left_right_alternance_instructions_text': "Tené en cuenta que el orden de los\n\n"
    #    "a la izquierda y derecha de l,\n\n"
        #"y también deberás alternar la mano con la que reportas según\n\n"
        #"se te indicará antes de cada ensayo.\n\n\n"
        #"Presioná la barra espaciadora para continuar.",

    #'post_stimulus_verbal_report_practice': "En algunos momentos vas a tener reportar verbalmente \n"
    #    "las emociones que experimentaste durante el vídeo que acabas de ver.\n\n\n"
    #    "Presioná la barra espaciadora para continuar con la explicación.",
    
    'post_stimulus_verbal_report': "Ahora vas a tener que reportar verbalmente como te sentiste al ver el video. \n\n"
        "Describí esta experiencia en orden cronológico, de principio a fin del video \n"
        "y con el mayor detalle posible, haciendo foco en tus emociones.\n\n",
        #"Presioná la barra espaciadora y esperá unos segundos para comenzar\n",

    #'post_stimulus_stop_verbal_report': "¡Listo! Ahora vamos a pasar al próximo ensayo.\n\n\n",
     #   "Presiona la barra espaciadora para comenzar.",

    # END PRACTICE E INITIAL RELAXATION SE GRABAN JUNTOS
    'end_practice': "¡Terminamos con los ensayos de práctica!\n\n"
        "Llamá el evaluador para preguntar si ya está todo listo \n\n"
        "para comenzar el experimento.\n\n",

    'initial_relaxation_video_text': "Antes de comenzar con las tareas principales,\n"
        "te vamos a mostrar un video relajante.\n\n"
        "Durante este vídeo, simplemente relajate y enfocate en el video. \n\n"
        "No es necesario realizar ningún reporte.\n\n"
        "Recordá que durante las mediciones quedarte lo mas quieto/a posible\n\n",
        
    'block_1_text': 
        "Vamos a empezar un nuevo bloque del experimento, compuesto por 3 o 4 videos.\n"
        "Durante los distintos videos de este bloque, vas a tener que reportar en tiempo real tu activación emocional con el joystick\n"
        "en una dimensión que va desde 'calmado' a 'emocionado'.\n\n"
        "Reportando en el extremo izquierdo de la escala, sentis relajación, tranquilidad,\n"
        "inactividad, aburrimiento, somnolencia, o ausencia de excitación.\n\n"
        "Reportando en el extremo derecho, sentis estimulación completa,\n"
        "emoción intensa, frenesí, nerviosismo, alerta y mayor activación.\n\n"
        "Podés representar niveles intermedios posicionándote en cualquier otro punto de la escala con el joystick,\n"
        "indicando así cómo te sentís en tiempo real al ver el video.\n\n"
        "Es importante evitar movimientos ajenos al joystick mientras ves los videos para garantizar la precisión de las mediciones.\n"
        "¡Empezamos! Recordá: calmado a la izquierda y emocionado a la derecha.\n\n",

    'block_2_text': 
        "Vamos a empezar un nuevo bloque del experimento, compuesto por 3 o 4 videos.\n"
        "Durante los distintos videos de este bloque, vas a reportar en tiempo real tu activación emocional con el joystick\n"
        "en una dimensión que va desde 'emocionado' a 'calmado'.\n\n"
        "Al posicionarte en el extremo izquierdo de la escala, sentis una estimulación completa,\n"
        "emoción intensa, frenesí, nerviosismo, alerta y mayor activación.\n"
        "Al posicionarte en el extremo derecho, se experimenta relajación, tranquilidad,\n"
        "inactividad, aburrimiento, somnolencia y ausencia de excitación.\n\n"
        "Podés representar niveles intermedios ubicándote en cualquier otro punto de la escala con el joystick,\n"
        "mostrando así cómo te sentís en tiempo real al ver el video.\n\n"
        "Es importante evitar movimientos ajenos al joystick mientras ves los videos para garantizar la precisión de las mediciones.\n"
        "¡Empezamos! Recordá: emocionado a la izquierda y calmado a la derecha.\n\n",

    'block_3_text': 
        "Vamos a empezar un nuevo bloque del experimento, compuesto por 3 o 4 videos.\n"
        "Durante los distintos videos de este bloque, vas a reportar en tiempo real la valencia emocional con el joystick\n"
        "en una dimensión que va desde 'negativo' a 'positivo'.\n\n"
        "Al reportar en el extremo izquierdo, sentis infelicidad,\n"
        "molestia, insatisfacción, melancolía, desesperación, aburrimiento.\n"
        "Al reportar en el extremo derecho, sentis felicidad plena, alegría,\n"
        "satisfacción, bienestar y esperanza.\n\n"
        "Podés representar niveles intermedios ubicándote en cualquier otro punto de la escala con el joystick,\n"
        "indicando así cómo te sentís en tiempo real al ver el video.\n\n"
        "Es importante evitar movimientos ajenos al joystick mientras ves los videos para garantizar la precisión de las mediciones.\n"
        "¡Empezamos! Recordá: negativo a la izquierda y positivo a la derecha.\n\n",
        
    'block_4_text': 
        "Vamos a empezar un nuevo bloque del experimento, compuesto por 3 o 4 videos.\n"
        "Durante los distintos videos de este bloque, vas a reportar en tiempo real la valencia emocional con el joystick\n"
        "en una dimensión que va desde 'positivo' a 'negativo'.\n\n"
        "Al reportar en el extremo izquierdo, sentis felicidad, alegría,\n"
        "satisfacción, bienestar y esperanza.\n\n"
        "Mientras que al reportar en el extremo derecho, sentis infelicidad,\n"
        "molestia, insatisfacción, melancolía, desesperación, aburrimiento.\n"
        "Podés representar niveles intermedios ubicándote en cualquier otro punto de la escala con el joystick,\n"
        "indicando así cómo te sentís en tiempo real al ver el video.\n\n"
        "Es importante evitar movimientos ajenos al joystick mientras ves los videos para garantizar la precisión de las mediciones.\n"
        "¡Empezamos! Recordá: positivo a la izquierda y negativo a la derecha.\n\n",
    
    'rest_suprablock_text': "¡Felicitaciones, terminaste la primera mitad del experimento!\n\n"
        "Podés tomarte unos minutos antes de continuar \n"
        "con la segunda mitad.\n\n",
        #"Presioná la barra espaciadora para continuar.",
        

    'block_5_text': 
        "Vamos a empezar un nuevo bloque.\n"
        "Vas a reportar valencia emocional,\n"
        "en una dimensión que va desde 'positivo' a la izquierda, hasta 'negativo' a la derecha.\n"
        "Es importante evitar movimientos ajenos al joystick mientras ves los videos para garantizar la precisión de las mediciones.\n"
        "¡Empezamos! Recordá: positivo a la izquierda y negativo a la derecha.\n\n",

    'block_6_text': 
        "Vamos a empezar un nuevo bloque.\n"
        "Vas a reportar valencia emocional,\n"
        "en una dimensión que va desde 'negativo' a la izquierda, hasta 'positivo' a la derecha.\n"
        "Es importante evitar movimientos ajenos al joystick mientras ves los videos para garantizar la precisión de las mediciones.\n"
        "¡Empezamos! Recordá: negativo a la izquierda y positivo a la derecha.\n\n",

    'block_7_text': 
        "Vamos a empezar un nuevo bloque.\n"
        "Vas a reportar activación emocional,\n"
        "en una dimensión que va desde 'emocionado' a la izquierda, hasta 'calmado' a la derecha.\n"
        "Es importante evitar movimientos ajenos al joystick mientras ves los videos para garantizar la precisión de las mediciones.\n"
        "¡Empezamos! Recordá: emocionado a la izquierda y calmado a la derecha.\n\n",

    'block_8_text': 
        "Vamos a empezar un nuevo bloque.\n"
        "Vas a reportar activación emocional,\n"
        "en una dimensión que va desde 'calmado' a la izquierda, hasta 'emocionado' a la derecha.\n"
        "Es importante evitar movimientos ajenos al joystick mientras ves los videos para garantizar la precisión de las mediciones.\n"
        "¡Empezamos! Recordá: calmado a la izquierda y emocionado a la derecha.\n\n",
        
    'final_relaxation_video_text': "¡Ya estamos terminando el experimento!\n"
        "Para terminar, te vamos a mostrar otro vídeo relajante. \n"
        "Como antes, simplemente relajate y disfrutá del vídeo sin realizar reportes. \n\n"
        "Recordá durante las mediciones no hacer movimientos en lo posible\n\n",

    'experiment_end_text': "¡Gracias por participar en nuestro experimento!\n\n\n"
        "De verdad, tu participacion nos ayuda muchísimo a entender cómo experimentamos nuestras emociones en tiempo real."
        "Si te quedan energias y tenes ganas, podes decirle al evaluador que te muestre algunos juegos con el casco de realidad virtual! Te lo ganaste!"
}
