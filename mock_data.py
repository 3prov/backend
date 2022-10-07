from random import randint, choice

from api.control.models import Stage, WeekID
from api.models import User
from api.rus.evaluations.models import (
    EssayCriteria,
    EssayEvaluation,
    EssaySelectionReview,
    RateEssayEvaluation,
)
from api.rus.models import Text, TextKey, Essay
from api.management.commands.init_stage import Command as InitStageCommand
from api.services import all_objects, filter_objects
from api.work_distribution.models import WorkDistributionToEvaluate


class Mock:
    def make(self):
        self._init_stage()
        self._create_users()
        self._create_text()
        self._create_text_keys()
        self._switch_stage_to_S2()
        self._create_essays()
        self._switch_stage_to_S3()
        self._create_evaluations()
        self._switch_stage_to_S4()
        self._create_evaluation_rates()

    @staticmethod
    def _init_stage():
        InitStageCommand().handle()

    @staticmethod
    def _create_users():
        """
        Создаёт пользователей.
        """
        User.objects.create_superuser(username='teacher')  # teacher
        User.objects.create_user(username='panonelag', vkontakte_id=126494354)
        User.objects.create_user(username='atanana', vkontakte_id=673380182)
        User.objects.create_user(username='xiacile', telegram_id=202258695)
        User.objects.create_user(username='wybana', telegram_id=214346353)
        User.objects.create_user(username='zarisiv', telegram_id=660136939)  # volunteer

    @staticmethod
    def _create_text():
        """
        Создаёт текст.
        """
        Text.objects.create(
            body='''(1) Внутри дворца господствовали мрак и тишина. (2) И внутрь прокуратор, как и говорил Афранию, уйти не пожелал. (3) Он велел постель приготовить на балконе, там же, где обедал, а утром вел допрос. (4) Прокуратор лег на приготовленное ложе, но сон не пожелал прийти к нему. (5) Оголенная луна висела высоко в чистом небе, и прокуратор не сводил с нее глаз в течение нескольких часов.
(6) Примерно в полночь сон наконец сжалился над игемоном. (7) Судорожно зевнув, прокуратор расстегнул и сбросил плащ, снял опоясывающий рубаху ремень с широким стальным ножом в ножнах, положил его в кресло у ложа, снял сандалии и вытянулся. (8) Банга поднялся к нему на постель и лег рядом, голова к голове, и прокуратор, положив собаке руку на шею, закрыл наконец глаза. (9) Только тогда заснул и пес.
(10) Ложе было в полутьме, закрываемое от луны колонной, но от ступеней крыльца тянулась к постели лунная лента. (11) И лишь только прокуратор потерял связь с тем, что было вокруг него в действительности, он немедленно тронулся по светящейся дороге и пошел по ней вверх прямо к луне. (12) Он даже рассмеялся во сне от счастья, до того все сложилось прекрасно и неповторимо на прозрачной голубой дороге. (13) Он шел в сопровождении Банги, а рядом с ним шел бродячий философ. (14) Они спорили о чем-то очень сложном и важном, причем ни один из них не мог победить другого. (15) Они ни в чем не сходились друг с другом, и от этого их спор был особенно интересен и нескончаем. (16) Само собой разумеется, что сегодняшняя казнь оказалась чистейшим недоразумением – ведь вот же философ, выдумавший столь невероятно нелепую вещь вроде того, что все люди добрые, шел рядом, следовательно, он был жив. (17) И, конечно, совершенно ужасно было бы даже помыслить о том, что такого человека можно казнить. (18) Казни не было! (19) Не было! (20) Вот в чем прелесть этого путешествия вверх по лестнице луны. (21) Свободного времени было столько, сколько надобно, а гроза будет только к вечеру, и трусость, несомненно, один из самых страшных пороков.(22) Так говорил Иешуа Га-Ноцри. (23) Нет, философ, я тебе возражаю: это самый страшный порок.
(24) Вот, например, не струсил же теперешний прокуратор Иудеи, а бывший трибун в легионе, тогда, в долине дев, когда яростные германцы чуть не загрызли Крысобоя-великана. (25) Но, помилуйте меня, философ! (26) Неужели вы, при вашем уме, допускаете мысль, что из-за человека, совершившего преступление против кесаря, погубит свою карьеру прокуратор Иудеи?
(27) – Да, да, – стонал и всхлипывал во сне Пилат.
(28) Разумеется, погубит. (29) Утром бы еще не погубил, а теперь, ночью, взвесив все, согласен погубить. (З0) Он пойдет на все, чтобы спасти от казни решительно ни в чем не виноватого безумного мечтателя и врача!
(31) – Мы теперь будем всегда вместе, – говорил ему во сне оборванный философ- бродяга, неизвестно каким образом вставший на дороге всадника с золотым копьем.
(32) – Раз один – то, значит, тут же и другой! (ЗЗ) Помянут меня, – сейчас же помянут и тебя! (34) Меня – подкидыша, сына неизвестных родителей, и тебя – сына короля- звездочета и дочери мельника, красавицы Пилы.
(35) – Да, уж ты не забудь, помяни меня, сына звездочета, – просил во сне Пилат.
(36) И, заручившись во сне кивком идущего рядом с ним нищего из Эн-Сарида, жестокий прокуратор Иудеи от радости плакал и смеялся во сне.
(37) Все это было хорошо, но тем ужаснее было пробуждение игемона. (38) Банга зарычал на луну, и скользкая, как бы укатанная маслом, голубая дорога перед прокуратором провалилась. (39) Он открыл глаза, и первое, что вспомнил, – это что казнь была. (40) Первое, что сделал прокуратор, – это привычным жестом вцепился в ошейник Банги, потом больными глазами стал искать луну и увидел, что она немного отошла в сторону и посеребрилась.
''',
            author='по М. А. Булгакову',
            author_description='Михаил Афанасьевич Булгаков (1891—1940) — русский писатель и драматург. Автор романов, повестей, сборников рассказов, фельетонов и около двух десятков пьес.',
            teacher=User.objects.get(username='teacher'),
            week_id=WeekID.get_current(),
        )

    @staticmethod
    def _create_text_keys():
        """
        Создаёт ключи к тексту.
        """
        TextKey.objects.create(
            text=Text.get_current(),
            range_of_problems='Проблема совести. (Что происходит с человеком, если он совершает поступок против своей совести?)',
            authors_position='Человек лишается духовной и душевной гармонии, совершая поступки против собственной совести.',
        )
        TextKey.objects.create(
            text=Text.get_current(),
            range_of_problems='Проблема нравственного выбора человека в сложной жизненной ситуации. (Как поступить в сложной жизненной ситуации, если существует свобода выбора?)',
            authors_position='Находясь в ситуации нравственного выбора, каждый из нас должен руководствоваться собственной совестью, чтобы потом всю оставшуюся жизнь мучительно не сожалеть о содеянном, не имея возможности что-либо исправить. Душевная слабость прокуратора Иудеи проявляется в том, что в критический момент он делает выбор в пользу личного интереса, а не руководствуется нравственным долгом. Поэтому только во сне герой готов пожертвовать своей карьерой ради человека, совершившего преступление против кесаря.',
        )
        TextKey.objects.create(
            text=Text.get_current(),
            range_of_problems='Проблема трусости как одного из самых страшных пороков. (Почему трусость является одним из самых страшных пороков?)',
            authors_position='Боясь кесаря и не желая пожертвовать своей карьерой (лишиться должности прокуратора), Понтий Пилат поступает не по совести, понимая, что обрекает на смерть безвинного человека.',
        )

    @staticmethod
    def _switch_stage_to_S2():
        Stage.switch_stage(Stage.StagesEnum.WORK_ACCEPTING)

    @staticmethod
    def _switch_stage_to_S3():
        Stage.switch_stage(Stage.StagesEnum.EVALUATION_ACCEPTING)

    @staticmethod
    def _switch_stage_to_S4():
        Stage.switch_stage(Stage.StagesEnum.CLOSED_ACCEPT)

    @staticmethod
    def _create_essays():
        """
        Создаёт сочинения.
        """
        Essay.objects.create(
            task=Text.get_current(),
            body='''В чем совершенство и недостаток сна? Эту проблему раскрывает в своем тексте М. А. Булгаков.
Размышляя над проблемой, автор рассказывает нам о прокураторе, которому приснился сон со странником. Он пишет, что во сне игемон "шел в сопровождении Банги, а рядом с ним шел бродячий философ", они спорили о чем-то, но самое главное то, что казни Иешуа не было, Пилат был счастлив. Так писатель показал, что сон дарит человеку положительные эмоции, воплощая его мечты. 
Далее Булгаков отмечает, что, проснувшись, прокуратор Иудеи осознал: "казнь была",  а то был лишь сон, что было ужаснее всего. Через этот пример драматург продемонстрировал, что порой реальность не всегда так же прекрасна, как и сон, который от этого может сделать людям лишь больнее. 
Причинно-следственная связь между этими иллюстрацииями помогает читателю понять, что сон имеет как положительные, так и отрицательные стороны, дает почувствовать эйфорию, радость и наоборот.
Позиция Михаила Афанасьевича Булгакова ясна: совершенство сна в том, что именно в нем человек зачастую чувствует себя комфортно и может позволить себе быть счастливым, однако, пробудившись и поняв, что его ждет жестокая реальность, он может быть морально ранен.
Я согласна с позицией автора, люди всегда верят в лучшее, и во сне часто проявляются их мечты и желания, но действительность не всегда им следует. Я могу подтвердить это на собственном примере. Мне часто снились сны, в которых жизнь была такой, о какой я мечтала, и очень часто, просыпаясь, понимала всю безнадежность ситуации. В такие моменты были лишь две мысли: хотелось, чтобы сон никогда не заканчивался, и противоположная - лучше бы он не снился.
В заключение отмечу, сны - это маленькие вымышленные миры людей, которые чаще всего являются лучшими версиями реальности, а это приводит к тому, что пробуждение не всегда вызывает приятные чувства.
''',
            author=User.objects.get(username='panonelag'),
        )
        Essay.objects.create(
            task=Text.get_current(),
            body='''Какую роль играет совесть в жизни человека? Этой проблеме посвящен текст М.А. Булгакова.
Чтобы привлечь внимание читателей к этому вопросу, автор рассказывает о прокураторе Иудеи Понтии Пилате, который, боясь погубить свою карьеру, обрекает на смерть безвинного философа Иешуа Га-Ноцри, однако Пилат не может поверить в то, что ему придется сделать это. Так писатель указывает на то, что из-за совести человек может испытывать душевные терзания и способен задуматься о верности своих решений.
Кроме того, автор пишет о дальнейших событиях. Во время пробуждения первое, о чем вспоминал Понтий, была казнь. Спя, он видел, что идет со своей любимой собакой, а филосов все еще жив. Пилат отрицал случившееся: "Казни не было! Не было!" Читатель понимает: после определенных событий совесть не отпускает человека, воспоминания преследуют даже во сне.
Примеры дополняют друг друга. Они помогает понять, что чувство нравственной ответственности за своё поведение перед окружающими людьми может не только вызывать душевную боль, но и долго оказывать влияние на человека разными способами.
Позиция автора такова: совесть играет очень важную роль. Она помогает правильно оценивать происходящие события и является самоконтролем для людей, вызывая различные эмоции.
Я согласна с позицией автора, действительно, это так. Например, после того, как моему дедушке пришлось убить человека, он чувствовал нескончаемую боль в сердце, стыд и горечь, потому что это действие было неправильным. Ему постоянно снились сны с участием мертвеца, что было просто ужасно для дедушки.
В заключение хочется сказать, что совесть помогает нам двигаться в правильном напрявление: без насилия и крови.
''',
            author=User.objects.get(username='atanana'),
        )
        Essay.objects.create(
            task=Text.get_current(),
            body='''Как связаны личность человека и его сны? Именно эта проблема находится в центре внимания М.А.Булгакова.
Размшляя над этим вопросом, автор рассказывает о прокураторе, который ложился спать после казни нищего из Эн-Сарида. Смерть этого человека была потрясением для Пилата, но во сне он смог увидеть бродячего философа живым. Прокуратор был рад общаться с мыслителем. Этот пример показывает, что сны позволяют человеку оказаться в ситуациях, невозможных в реальности.
Далее писатель описывает взаимодействие Пилата и нищего: "Они ни в чем не сходились друг с другом, и от этого их спор был особенно интересен и нескончаем". Диалог игемона и мудреца носит философский характер, они дискутируют на тему трусости. Пилат понимает, что он сам совершил порок, потому что не спас философа. Данный пример демонстрирует, что сон может человеку посмотреть на жизнь иначе и понять свои ошибки. Сны также отражают мысли человека, его мечты и страхи.
Примеры дополяют друг друга показывая, что сны имеют сильное влияние на личность. Они позволяют не только побывать в невозможных ситуациях, но и посмотреть на привычные вещи новым взглядом.
Позиция автора такова: сны являются отражением личности, они указывают человеку на его ошибки, помогают убежать от реальности.
Я полностью согласен с позицией автора. Действительно, сны являются отражением личности человека. Так, в произведении И.А.Гончарова "Обломов" есть эпизод сна главного героя. В нем мы можем увидить мечты и представление об идеальной жизни Обломова.
Хочется надеяться, мечты, подаренные снами, не будут разбиваться о суровую действительность.
''',
            author=User.objects.get(username='xiacile'),
        )
        Essay.objects.create(
            task=Text.get_current(),
            body='''Может ли трусливый человек  пойти на поступок? Именно над этой проблемой рассуждает М.А. Булгаков.
В произведении прокуратор Иудеии будучи во сне шел вверх прямо к луне и спорил с философом. Герой твердил себе о том, что никакой казни не было,ведь вот же философ, выдумавший столь невероятно нелепую вещь вроде того, что все люди добрые, шел рядом, следовательно, он был жив. Автор подчеркивает, что для героя совершенно ужасно было бы даже помыслить о том, что такого человека можно казнить. Этот пример показывает , что трусливый человек может только внушать себе то , что реальных событий не было, тем самым мучить себя за содеянное.
Кроме того, игемон соглашается с философом, что трусость- это самый страшный порок. Он утверждает, что погубил бы карьеру прокуратора Иудеии, чтобы  спасти от казни решительно ни в чем не виноватого безумного мечтателя и врача. Стоило только проснутся Пилату, как он опомнился о том, что казнь уже была, и он никак не сможет уберечь Иешуа Га-ноцри . Этот пример показывает. что как трусость человека мешает ему в помощи ни в чем не виновным людям.
Оба примера дополняют друг друга. Трусливый человек упрямо верит, что он его помыслы чисты, что он готов пойти на самопожертвование, но действовать из-за своей несмелости не будет.
Позиция автора выражена чётко. Автор считает, что трусость мешает человеку делать то, что желает именно он. 
Я согласна с позицией автора. Если люди боятся совершить какой- либо по ступок, который , по их мнению, правильный, только потому , что они бояться , что на них это скажется, никогда не смогут совершить его. Так, например, в рассказе А.П. Чехова " Человек в футляре" главный герой боялся всего, он был не решительный. Из-за боязни всего у него не были семьи, любимой работы, он был в неком "куполе", который мешал ему делать то, что хочет именно он.
В заключение, хотелось бы сказать , что трусость - один из человеческих пороков, который мешает человеку для достижения целей.
''',
            author=User.objects.get(username='wybana'),
        )

    @staticmethod
    def _create_evaluations():
        """
        Создаёт проверки сочинений.
        """

        def _make_random_one(evaluator: User):
            for eval_work in filter_objects(
                WorkDistributionToEvaluate.objects, evaluator=evaluator, only=('work',)
            ):
                _essay_criteria_table = dict()
                for i in range(1, 13):
                    _essay_criteria_table[f'k{i}'] = (
                        randint(0, 1) if i not in list(range(5, 11)) else randint(1, 2)
                    )
                print(_essay_criteria_table)
                _essay_criteria = EssayCriteria.objects.create(**_essay_criteria_table)
                a = EssayEvaluation.objects.create(
                    work=eval_work.work,
                    criteria=_essay_criteria,
                    evaluator=evaluator,
                )
                print(f"{a=}")

                _LOREM = 'Задача организации, в особенности же социально-экономическое развитие прекрасно подходит для реализации распределения внутренних резервов и ресурсов. Лишь активно развивающиеся страны третьего мира призывают нас к новым свершениям, которые, в свою очередь, должны быть своевременно верифицированы. Сложно сказать, почему ключевые особенности структуры проекта освещают чрезвычайно интересные особенности картины в целом, однако конкретные выводы, разумеется, разоблачены. Также как высокотехнологичная концепция общественного уклада предполагает независимые способы реализации существующих финансовых и административных условий. Имеется спорная точка зрения, гласящая примерно следующее: действия представителей оппозиции представлены в исключительно положительном свете. Безусловно, синтетическое тестирование не даёт нам иного выбора, кроме определения укрепления моральных ценностей. Для современного мира разбавленное изрядной долей эмпатии, рациональное мышление говорит о возможностях форм воздействия. Высокий уровень вовлечения представителей целевой аудитории является четким доказательством простого факта: социально-экономическое развитие однозначно определяет каждого участника как способного принимать собственные решения касаемо глубокомысленных рассуждений. В целом, конечно, повышение уровня гражданского сознания предполагает независимые способы реализации вывода текущих активов. Кстати, базовые сценарии поведения пользователей объективно рассмотрены соответствующими инстанциями. Кстати, диаграммы связей неоднозначны и будут обнародованы. Разнообразный и богатый опыт говорит нам, что глубокий уровень погружения влечет за собой процесс внедрения и модернизации направлений прогрессивного развития.'
                for char_number in range(
                    0, eval_work.work.chars_count - 50, randint(1, 50)
                ):
                    if randint(0, 7) == 0:
                        EssaySelectionReview.objects.create(
                            evaluator=evaluator,
                            essay=eval_work.work,
                            start_selection_char_index=char_number,
                            selection_length=randint(1, 50),
                            evaluator_comment=choice(_LOREM.split('. ')),
                            mistake_type=choice(
                                list(EssaySelectionReview.MistakesEnum)
                            ),
                        )

        _make_random_one(User.objects.get(username='panonelag'))
        _make_random_one(User.objects.get(username='atanana'))
        _make_random_one(User.objects.get(username='xiacile'))
        _make_random_one(User.objects.get(username='wybana'))

    @staticmethod
    def _create_evaluation_rates():
        """
        Создаёт оценки для рандомных проверок.
        """
        for evaluation in all_objects(EssayEvaluation.objects):
            if randint(0, 3) == 0:
                RateEssayEvaluation.objects.create(
                    score=randint(1, 5),
                    rater=evaluation.work.author,
                    evaluation_criteria=evaluation.criteria,
                )


if __name__ == "__main__":
    Mock().make()
