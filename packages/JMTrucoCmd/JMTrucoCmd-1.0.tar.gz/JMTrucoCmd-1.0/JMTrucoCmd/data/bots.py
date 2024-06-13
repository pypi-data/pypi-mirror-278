from JMTrucoCmd.schemas.bot import BotInit
bots_data = {
    'Jesus' : BotInit(
        name='Jesus',
        aggressive=3,
        liar=1,
        fisherman=10,
        phrases={
            "Envido": [
                "Mi corazón puro como el agua del Jordán, Envido.",
                "Deja que tu fe guíe tus cartas, Envido.",
                "Como el buen pastor te digo, Envido.",
                [
                "Donde hay fe y hay amor,",
                "hay Envido y hay valor."
                ]
            ],
            "Real Envido": [
                "Con la verdad que te libera, Real Envido.",
                "Que la luz del Espíritu ilumine tus cartas, Real Envido.",
                "Como el maná que cae del cielo, Real Envido.",
                [
                "La fe mueve montañas,",
                "tambien altera mis cartas",
                "asi que un Real Envido se alza."
                ]
            ],
            "Falta Envido": [
                [
                "Al que cree",
                "todo le es posible",
                "asi que Falta Envido"
                ],
                "Que tu fe sea más grande que tu temor, Falta Envido.",
                ["Como el milagro del vino", "Falta Envido divino."],
                [
                "Si tienes fe y confías,",
                "Falta Envido y alegrías."
                ]
            ],
            "Truco": [
                ["Como el buen pastor cuida a sus ovejas", "yo cuido mis cartas", "Truco"],
                "Con la sabiduría obtenida, Truco.",
                [
                "El amor es paciente y bondadoso,",
                "pero en este juego", "Truco."
                ],
                [
                "Con la fuerza del Espíritu Santo,",
                "te canto este Truco y me planto."
                ]
            ],
            "Retruco": [
                ["Así como resucité al tercer día", "te levanto el Truco","y te Retruco."],
                "Con la fuerza de la fe que mueve montañas, Retruco.",
                "Si crees en el milagro, Retruco es algo.",
                [
                "En el nombre del Padre y del Hijo,",
                "te canto Retruco",
                "amen"
                ]
            ],
            "Vale Cuatro": [
                ["Como el milagro de los panes y los peces", "esto se multiplica", "Vale Cuatro."],
                "Con la certeza del cielo, Vale Cuatro.",
                [
                "Por los caminos de Nazaret,",
                "Vale Cuatro."
                ]
            ],
            "Quiero": [
                "Como el amor del Padre, Quiero.",
                "Con la confianza de un niño, Quiero.",
                [
                "Donde dos o más se reúnen,",
                "Quiero y a nadie confunden."
                ]
            ],
            "No Quiero": [
                "No tentarás al Señor tu Dios, No Quiero.",
                "Con la prudencia del buen samaritano, No Quiero.",
                [
                "Como el que guarda silencio,",
                "No Quiero y sin lamento."
                ]
            ],
            "Victoria": [
                "He vencido al mundo, esta es mi Victoria.",
                "Con la gloria del Reino de los Cielos, Victoria.",
                [
                "En el nombre del Señor,",
                "Victoria y honor."
                ]
            ],
            "Derrota": [
                "En la humildad está la grandeza, acepto mi Derrota.",
                "Aprendo y crezco, aún en la Derrota.",
                [
                "El que muere en la cruz",
                "Murio de vuelta..."
                ]
            ]
        }
    ),
    'Papa Noel':BotInit(
        name= "Papa Noel",
        aggressive= 2,
        liar= 3,
        fisherman= 7,
        phrases= {
            "Envido": [
                "Ho ho ho, Envido y navidad!",
                "Con la magia de la Navidad, Envido.",
                "En el trineo llevo cartas, Envido.",
                [
                    "Como los regalos en la nochebuena,",
                    "Envido llega sin pena."
                ]
            ],
            "Real Envido": [
                "En el Polo Norte hace frío, por lo que acéptame este Real Envido.",
                "Como un regalo bien envuelto, Real Envido.",
                [
                    "La nieve cae suavemente,",
                    "Real Envido, claramente."
                ]
            ],
            "Falta Envido": [
                ["Mercado Libre dice que se extravió mi envío", "digo...", "Falta Envido"],
                "Con la magia que nunca falla, Falta Envido.",
                "Si crees en mí, Falta Envido aquí.",
                [
                    "Como los niños esperan su regalo,",
                    "Falta Envido, apurado."
                ]
            ],
            "Truco": [
                ["Si seguís portándote así", "te voy a regalar un...", "¡Truco!"],
                ["Te doy 2 elfos si me aceptas un...", "Truco!"],
                "Con el saco lleno de sorpresas, Truco.",
                [
                    "Como en la noche de Navidad,",
                    "el Truco te va a encantar."
                ]
            ],
            "Retruco": [
                "Con la fuerza del Polo Norte, Retruco.",
                "Levanto con el espíritu navideño, Retruco.",
                [
                    "Si crees en la magia de la Navidad,",
                    "Retruco con gran calidad."
                ]
            ],
            "Vale Cuatro": [
                "Con la alegría de los niños, Vale Cuatro.",
                "La Navidad lo merece, Vale Cuatro.",
                [
                    "Con el brillo de las luces,",
                    "Vale Cuatro y muchas dulces."
                ]
            ],
            "Quiero": [
                "Como a las galletas y la leche, Quiero!",
                ["Estas por ganarte carbón...", "Quiero."],
                [
                    "Noche de paz, noche de amor,",
                    "todos quieren alrededor", "si, Quiero."
                ]
            ],
            "No Quiero": [
                ["Peor que los que me dejan galletita de agua", "No Quiero"],
                "Te estás por ganar más carbón para Navidad... No Quiero.",
                [
                    "Con la prudencia de un buen Santa,",
                    "No Quiero", "y eso me encanta."
                ]
            ],
            "Victoria": [
                "Yo soy mi mejor regalo, Victoria Navideña.",
                "Nunca subestimes la magia de la Navidad, Ho ho ho.",
                [
                    "Hoy invito las birras navideñas,",
                    "si los elfos despiertos me esperan",
                    "Ho ho ho, Victoria"
                ]
            ],
            "Derrota": [
                "Hasta los duendes se equivocan... Derrota.",
                "La navidad también aprende, bien jugado",
                [
                    "Aprendo y sigo adelante,",
                    "Derrota, pero no va a ser constante."
                ]
            ]
        }
    ),
    'Gucci' : BotInit(
        name='Gucci',
        aggressive=4,
        liar=6,
        fisherman=7,
        phrases={
            "Truco": [
                ["Que colorida","Truco"],
                "Truco man",
                ["Te haces el vivo y te parto de un tackle", "Truco!"],
                "Dale man, Truco"
            ],
            "Retruco":[
                'Retruco!',
                'Retruco Rugbier',
                'Retruco callado',
                'Timido Retruco',
            ],
            "Vale Cuatro":[
                ['Soy una bestiaaaaa','quiero Vale Cuatro'],
                ["Cuidado que tengo el macho...",'Vale Cuatro'],
                ["Mato gente en boliches", "pensas que tendria miedo??",'Vale Cuatro'],
                ['Uhhhh no se eh','Vale cuatro']
            ],
            "Envido":[
                ["No man", "Que buenas cartas", "Envido"],
                "Envido o tackle",
                ["No man", "estoy re atrevido", "Envido"],
            ],
            "Real Envido":[
                "Dale no cagonees man, Real Envido",
                ["Gris","muy gris","demasiado gris","Nah mentira, Real Envido"]
            ],
            "Falta Envido":[
                ["La tablada, es una garchada", "ellos Falta Envidio", "no me aceptaban"],
                ["Maaaannnn mira estos puntos", "Falta Envido"]
            ],
            "Quiero":[
                ["Buenísimo man", "Quiero"],
                ["Con estas cartas como no voy a querer??","Si si, Quiero"],
                ["Tengo cartas mas lindas que la remera del Tala", "Quiero"],
                ["Que si quiero laburo?", "Si, Quiero"],
                "Buenísimas man, Quiero"
            ],
            "No Quiero":[
                ["Que gris la veo...", "No Quiero"],
                "No man, No Quiero",
                ["Gris","muy gris","demasiado gris", "No Quiero"]
            ],
            "Victoria":[
                "Guccibot >>> Gucci",
                ["MANNN","NO PUEDO SER TAN BUENO"]
            ],
            "Derrota":[
                'Man el wifi man... fue eso',
                ['SE ME FUE EL WIFI',"AAAAAAAAAAAAAAAAAAAHHHH"],
                "Si tuviera manos te ganaria...",
                ["Ya no es mas gris man...","ahora es negro :("],
                ['Oh man',"no me toca nada","que bronca"]
            ]
        }
    ),
    'Gato':BotInit(
        name='Cat',
        aggressive=4,
        liar=4,
        fisherman=10,
        phrases={
            "Envido": [
                "Miau miau miau miau miau miau miau, miau.",
                "Miau miau tu miau miau miau miau.",
                "Miau miau miau miau miau miauuuu.",
                [
                    "Miau miau miau", "miau miau",
                    "miau miau miauuu."
                ]
            ],
            "Real Envido": [
                "Miau la miau que te miau",
                "Miau la miau del miau miau tus miau",
                "Miau el miau miau cae del miau",
                [
                    "Miau miau miau miau,",
                    "miau miau miau miau",
                    "miau miau."
                ]
            ],
            "Falta Envido": [
                [
                    "Miau miau miau miau",
                    "miau miau miau",
                    "miau"
                ],
                "Miau miau miau miau miau miau miau, miau",
                ["Miau miau miau", "miau miau miau."],
                [
                    "Miau miau miau miau,",
                    "miau miau miau."
                ]
            ],
            "Truco": [
                ["Miau miau miau miau miau", "miau miau", "miau"],
                "Miau miau miau",
                'Miau!!',
                [
                    "Miau miau miau miau?",
                    "miau miau miau?", "miau"
                ],
                [
                    "Miau miau miau miau",
                    "miau miau miau miau ¡miau!"
                ]
            ],
            "Retruco": [
                ["Miau miau miau miau miau", "miau miau?","miau"],
                "Miau miau miau miau miau",
                "Miau miau miau miau.",
                [
                    "Miau...",  "miau miau miau...",
                    "miau miau",
                    "miau?"
                ]
            ],
            "Vale Cuatro": [
                ["Miau miau miau miau", "miau miau!"],
                "Miau miau miau, MIAUUUUU",
                [
                    "Miau miau miau,",
                    "¡¡¡MIAUUUU!!!"
                ]
            ],
            "Quiero": [
                "Miau miau miau, miau.",
                [
                    "Miau miau", "miau",
                    "miau... miau miau."
                ]
            ],
            "No Quiero": [
                "Miau miau miau miau, miau...",
                "Miau miau miau miau miau",
                [
                    "Miau miau miau,",
                    "miau"
                ]
            ],
            "Victoria": [
                "Miau miau miau miau",
                "Miau miau miau miau, MIAU.",
                [
                    "Miau miau miau,",
                    "miau miau miau miau."
                ]
            ],
            "Derrota": [
                "Miau... miau miau, miau, miau miau",
                "Miau miau, miau miau miau.",
                [
                    "Miau miau miau miau,",
                    "miau."
                ]
            ]
        }
    ),
    'Javier Milei': BotInit(
        name='Javier Milei',
        aggressive=9,
        liar=7,
        fisherman=3,
        phrases={
            "Envido": [
                "Con la fuerza de la libertad, Envido.",
                "Envido Libertario!!!.",
                [
                    "Con la economía en mi mente,",
                    "el Envido siempre de frente."
                ]
            ],
            "Real Envido": [
                "Sin trampa ni cartón, Real Envido de corazón.",
                "Con el rigor de un economista, Real Envido",
                [
                    "La realidad es dura,",
                    "Real Envido"
                ]
            ],
            "Falta Envido": [
                [
                    "Envidio", "Pa' fuera",
                    "Real Envidio", "Pa' fuera",
                    "Falta Envido", "No, vos si quédate",
                ],
                [
                    "Con la falta de un buen plan,",
                    "Falta Envido, te vas a encontrar."
                ]
            ],
            "Truco": [
                ["A vos pedazo de zurdo", "te va a entrar todo este truco"],
                ["Como mi amigo Elon Musk me dijo...", "Trucaishion mi amigo"],
                ["A vos pedazo de zurdo", "te va a entrar todo este Truco"],
                ["Preparate porque la vas a pasar mal", "Truco"],
            ],
            "Retruco": [
                "Retruco libertario!",
                "La libertad Retruca, Retruco.",
                "Para boludeces estan los zurdos, yo quiero Retruco.",
            ],
            "Vale Cuatro": [
                ["21 Ministerios??!!", "Nah, Vale Cuatro"],
                "Voy con todo, sin miedo, Vale Cuatro.",
                [
                    "La libertad avanza!",
                    "Vale Cuatro."
                ]
            ],
            "Quiero": [
                'Tendrias que hacer como la casta y dar un paso al costado, ¡Quiero!',
                'Quiero!!!!',
                "Con la certeza de un plan, Quiero.",
                "Dolarizacion??, si Quiero.",
                [
                    "El leon quiere?",
                    "si",
                    "si Quiere"
                ]
            ],
            "No Quiero": [
                'No Quiero.',
                "No tengo nada, o sea digamos, no, o sea digamos No Quiero.",
                "Mmmm opinion de un economista, No Quiero.",
                [
                    "Si tus cartas no son fuertes",
                    "No Quiero, PA' FUERA."
                ]
            ],
            "Victoria": [
                "ZURDOS HIJOS DE PUTA, TIEMBLEN",
                [
                    "NO HAY PLATA",
                    "Solo esta mi victoria"
                ]
            ],
            "Derrota": [
                "Nos vamos a ver en el ballotage.",
                "En 4 años te espero en elecciones.",
            ]
        }
    )
}