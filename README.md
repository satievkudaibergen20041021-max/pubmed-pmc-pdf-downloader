Welcome everybody! I'm very glad to see you in my first ever repository. 
This project started because of two things, firstly because I was to lazy to search through medical databases manually for my literature review. Abd secondly I was so eager to try out my (almost non-existent) backend dev. skills. 
I hope in the future I could be able to do even more great things in the name of technology and science. 

Anyways, let's cut to the chase. 
First thing first before installing this in your computer you need to create one big folder for everything, and some additional ones. 
The overall structure would look smth like this: 
## Project structure

```text
project/
│
├── downloads/
│   
├── history/
│   ├── europepmc_history/
│   └── pubmed_history/
│  
├── .gitignore
├── pubmed.py
├── europe_pmc.py
├── helpers.py
└── main.py
```
!!! it's very important to name the folders and position them exactly like in the diagram above, otherwise the system will crash. 
NOTE: I will fix this problem in the future. 

About installation... for those who isnt familliar with git or coding at all, you can download a code editor like VS Code and use it to run the files. 
I think that any AI can give you sufficient explanation on what to do next. 

![initialization](images/Screenshot%202026-11-26%20171925.png)
ok, so after you start the programm the terminal will ask you about keywords, you can add multiple keywords, 
BUT 1. separate them with comma 
    2. Enter only RELATED words per line (e.g. NEC, Necrotizing enterocolitis) 

![additional terms, email](images/Screenshot%202026-11-26%20172001.png)
If you dont want to add any more searchwords, just press enter. 
You need to enter your email, in order not to look suspicious for API. 
The programm will nag you until you enter one

![database](images/Screenshot%202026-11-26%20172028.png)
After entering email the programm will ask you about which database you want to explore.
You can choose both. 

![pdf or meta](images/Screenshot%202026-11-26%20172046.png)
Also you can choose whether you want the information about articles or the articles themselfes. 
REMEMBER! Not every article has available pdf version.

![volume](images/Screenshot%202026-11-26%20172100.png)
And finaly, the programm will ask you how may articles do you want.
PLEASE Be cautious ! I advise you against entering any number above 500. We don't want to accidentaly blow up someone's servers 

![slow connection](images/Screenshot%202026-11-26%20172835.png)
One more thing, if your connection is slow, you may get smth like this, dont worry, just restart the programm and try again. 


In the next versions Im planing to add more databases and autocorrection and autosuggestion for keywords. 


Добро пожаловать!
Всем привет! Очень рад видеть вас в своём первом репозитории!

Этот проект появился по двум причинам. Во-первых, мне было слишком лень вручную искать статьи в медицинских базах данных для литературного обзора. Во-вторых, мне очень хотелось попробовать свои силы в backend-разработке (хотя мой опыт в этой области пока практически нулевой).

Надеюсь, в будущем я смогу создавать ещё больше интересных проектов на стыке технологий и науки!
Но давайте перейдём к делу.

## Структура проекта
Прежде чем устанавливать программу на свой компьютер, необходимо создать одну основную папку для проекта и несколько дополнительных папок.

Общая структура должна выглядеть следующим образом:

```text
project/
│
├── downloads/
│
├── history/
│   ├── europepmc_history/
│   └── pubmed_history/
│
├── .gitignore
├── pubmed.py
├── europe_pmc.py
├── helpers.py
└── main.py
```

**ВАЖНО!** Необходимо назвать папки и разместить их именно так, как показано на схеме выше. В противном случае программа может работать некорректно или вовсе завершиться с ошибкой.

Примечание: в будущем я планирую исправить эту проблему.

Установка....
Если вы не знакомы с Git или программированием, можете скачать редактор кода, например VS Code, и использовать его для запуска файлов.
Думаю, любой ИИ сможет достаточно подробно объяснить вам, что делать дальше.

![Инициализация](images/Screenshot%202026-11-26%20171925.png)

После запуска программы терминал попросит вас ввести ключевые слова. Можно указать несколько ключевых слов.
**НО!**
1. Разделяйте их запятыми.
2. Вводите только связанные между собой слова в одной строке (например: NEC, Necrotizing enterocolitis).

![Дополнительные ключевые слова и электронная почта](images/Screenshot%202026-11-26%20172001.png)

Если вы не хотите добавлять дополнительные поисковые слова, просто нажмите Enter.
Также необходимо указать адрес электронной почты, чтобы не выглядеть подозрительно для API.
Программа будет продолжать запрашивать адрес, пока вы его не введёте.

![Выбор базы данных](images/Screenshot%202026-11-26%20172028.png)

После ввода электронной почты программа предложит выбрать базу данных для поиска.
Можно выбрать обе базы данных одновременно.

![Выбор PDF или метаданных](images/Screenshot%202026-11-26%20172046.png)

Также вы можете выбрать, что именно хотите получить: информацию о статьях (метаданные) или сами статьи в формате PDF.
**ПОМНИТЕ!** Не для каждой статьи доступна PDF-версия.

![Количество статей](images/Screenshot%202026-11-26%20172100.png)

И наконец, программа спросит, сколько статей вы хотите получить.
**ПОЖАЛУЙСТА, БУДЬТЕ ОСТОРОЖНЫ!** Я не рекомендую указывать число больше 500. Не стоит случайно перегружать чужие серверы.

![Медленное интернет-соединение](images/Screenshot%202026-11-26%20172835.png)

И ещё один момент: если у вас медленное интернет-соединение, вы можете столкнуться с подобной ошибкой. Не переживайте: просто перезапустите программу и попробуйте ещё раз.

## Что планируется в будущем?
В следующих версиях я планирую добавить новые базы данных, а также функции автоматического исправления и автодополнения ключевых слов.

# Қош келдіңіздер!

Баршаңызға сәлем! Менің алғашқы репозиторийіме қош келдіңіздер!
Бұл жобаны жасауыма екі себеп болды. Біріншіден, әдеби шолу жасау үшін медициналық дерекқорлардан мақалаларды қолмен іздеуге еріндім. Екіншіден, backend әзірлеу саласында (әзірге тәжірибем өте аз болса да) өзімді сынап көргім келді.
Болашақта технология мен ғылымды біріктіретін бұдан да көп қызықты жобалар жасай аламын деп үміттенемін!
Ал енді негізгі мәселеге көшейік.

## Жоба құрылымы

Бағдарламаны компьютеріңізге орнатпас бұрын, жобаға арналған негізгі бір бума және бірнеше қосымша бума жасауыңыз қажет.
Жобаның жалпы құрылымы төмендегідей болуы керек:

```text
project/
│
├── downloads/
│
├── history/
│   ├── europepmc_history/
│   └── pubmed_history/
│
├── .gitignore
├── pubmed.py
├── europe_pmc.py
├── helpers.py
└── main.py
```

**МАҢЫЗДЫ!** Бумалардың атаулары мен орналасуы жоғарыдағы сызбада көрсетілгендей болуы керек. Әйтпесе бағдарлама дұрыс жұмыс істемеуі немесе қате беруі мүмкін.
Ескерту: болашақта бұл мәселені шешуді жоспарлап отырмын.

## Орнату

Егер Git немесе бағдарламалау саласымен таныс болмасаңыз, VS Code сияқты код редакторын жүктеп алып, бағдарламаны сол арқылы іске қоса аласыз.
Әрі қарай не істеу керектігін кез келген жасанды интеллект жеткілікті түрде түсіндіріп бере алады деп ойлаймын.

![Бағдарламаны іске қосу](images/Screenshot%202026-11-26%20171925.png)

Бағдарламаны іске қосқаннан кейін терминал сізден кілт сөздерді енгізуді сұрайды. Бірнеше кілт сөз енгізуге болады.
**БІРАҚ!**
1. Кілт сөздерді үтір арқылы бөліңіз.
2. Бір жолға тек өзара байланысты сөздерді енгізіңіз (мысалы: NEC, Necrotizing enterocolitis).

![Қосымша кілт сөздер және электрондық пошта](images/Screenshot%202026-11-26%20172001.png)

Егер қосымша іздеу сөздерін енгізгіңіз келмесе, Enter пернесін басыңыз.
Сондай-ақ электрондық пошта мекенжайыңызды енгізу қажет. Бұл API сұраныстары кезінде сіздің сұраныстарыңыздың күмәнді болып көрінбеуі үшін керек.
Бағдарлама электрондық пошта мекенжайын енгізгенше қайта-қайта сұрай береді.

![Дерекқорды таңдау](images/Screenshot%202026-11-26%20172028.png)

Электрондық поштаңызды енгізгеннен кейін бағдарлама сізге іздеу жүргізетін дерекқорды таңдауды ұсынады.
Екі дерекқорды да бір уақытта таңдауға болады.

![PDF немесе метадеректерді таңдау](images/Screenshot%202026-11-26%20172046.png)

Сонымен қатар, сізге мақалалар туралы ақпаратты (метадеректерді) немесе мақалалардың өзін PDF форматында жүктеп алу керектігін таңдауға болады.
**ЕСТЕ САҚТАҢЫЗ!** Әрбір мақаланың PDF нұсқасы бола бермейді.

![Мақалалар санын таңдау](images/Screenshot%202026-11-26%20172100.png)

Соңында бағдарлама сізден қанша мақала қажет екенін сұрайды.
**ӨТІНІШ, АБАЙ БОЛЫҢЫЗ!** 500-ден жоғары сан енгізуді ұсынбаймын. Басқа біреудің серверлеріне шамадан тыс жүктеме түсіріп алғымыз келмейді.

![Интернет байланысының баяулығы](images/Screenshot%202026-11-26%20172835.png)

Тағы бір ескеретін жайт: интернет байланысыңыз баяу болса, осындай қате пайда болуы мүмкін. Уайымдамаңыз, бағдарламаны қайта іске қосып, тағы бір рет көріңіз.

## Болашақ жоспарлар
Келесі нұсқаларда қосымша дерекқорларды қосуды, сондай-ақ кілт сөздерді автоматты түрде түзету және толықтыру функцияларын енгізуді жоспарлап отырмын.
