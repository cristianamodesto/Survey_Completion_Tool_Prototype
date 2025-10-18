import json
import os
import random
import smtplib
import string
from email.mime.text import MIMEText
from urllib.parse import urlparse
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import requests

"""
Translation of each field into other languages

"""

words_intro = {'en': 'introduction_', 'es': 'introducción_', 'de': 'einführung_',
               'it': 'introduzione_', 'pt': 'introdução_'}
words_for_group_intro = {'en': 'Introduction', 'es': 'Introducción', 'de': 'Einführung',
                         'it': 'Introduzione', 'pt': 'Introdução'}

words_next = {'en': 'Next', 'es': 'Siguiente', 'de': 'Nächste',
              'it': 'Prossima', 'pt': 'Seguinte'}

words_submit_file = {'en': 'Submit', 'es': 'Enviar archivo', 'it': 'Invia file', 'de': 'Datei einreichen',
                     'pt': 'Submeter Ficheiro'}

words_start_survey = {'en': 'Start Survey', 'es': 'Inicio Cuestionario', 'de': 'Start Fragebogen',
                      'it': 'Iniziare il questionario', 'pt': 'Iniciar Questionário'}
words_go_to_first_page = {'en': 'Go to First Page', 'es': 'Ir a la primera página',
                          'de': 'Zur Titelseite gehen', 'it': 'Vai alla prima pagina',
                          'pt': 'Ir para a Primeira Página'}

words_go_to_last_question = {'en': 'Go to Last Question', 'es': 'Ir a la última pregunta',
                             'de': 'Zur letzten Frage gehen', 'it': 'Vai all\'ultima domanda',
                             'pt': 'Ir para a Última Questão'}
words_back = {'en': 'Back', 'es': 'Anterior', 'de': 'Vorherige', 'it': 'Precedente'}
words_question = {'en': 'question_', 'es': 'pregunta_', 'de': 'frage_',
                  'it': 'domanda_', 'pt': 'pergunta_'}
words_type = {'en': 'type_', 'es': 'tipo_', 'de': 'typ_', 'pt': 'tipo_'}
words_options_question = {'en': 'option_', 'fr': 'option_', 'es': 'opción_',
                          'it': 'opzione_', 'pt': 'opção_'}
words_mandatory = {'en': 'mandatory_', 'fr': 'obligatoire_', 'es': 'obligatorio_', 'de': 'zwingend_',
                   'it': 'obbligatorio_', 'pt': 'obrigatório_'}
words_multimedia = {'en': 'multimedia_', 'pt': 'multimédia_'}
words_group = {'en': 'group_', 'fr': 'groupe_', 'de': 'gruppe_', 'it': 'gruppo_',
               'pt': 'grupo_'}
words_hotlink = {'en': 'hotlink_', 'pt': 'dica_', 'en_2': 'tip'}

words_informed_consent = {'en': 'consent', 'es': 'consentimiento',
                          'de': 'zustimmung', 'it': 'consenso', 'pt': 'consentimento'}

extensions = ['.txt', '.json']

words_date = {'en': 'date', 'es': 'fecha', 'de': 'datum', 'it': 'data'}

words_day = {'en': 'day', 'es': 'día', 'de': 'tag', 'it': 'giorno', 'pt': 'dia'}


def loadUploadedFileWithQuestions(uploadInputFileWithQuestions):
    file_extension = os.path.splitext(str(uploadInputFileWithQuestions))[1]
    file_content = uploadInputFileWithQuestions.read().decode('utf-8')

    return file_extension, file_content


def loadLinkFileWithQuestions(insertLinkForFileWithQuestions):
    try:
        file_downloaded = requests.get(insertLinkForFileWithQuestions)
    except requests.RequestException:
        return False, None, False
    file_content = file_downloaded.text

    all_file_name = file_content.split('\n', maxsplit=1)[0]
    file_extension = None
    for ext in extensions:
        if ext in all_file_name:
            final_file_content = file_content.split("\n", maxsplit=1)[1:]
            str_final_file_content = ""
            for line in final_file_content:
                str_final_file_content = str_final_file_content.join(str(line))
            file_extension = ext.strip()
            idx_ext = str(all_file_name).index(str(ext))
            file_name = all_file_name[:idx_ext]
            return file_name, file_extension, str_final_file_content

    if file_extension is None:
        return None, None, None


def get_list_questions_txt(file_content):
    list_questions = list()
    dict_question = {}
    counter = 0
    counter_question = 0

    for word in file_content.split():
        for word_to_verify in set(words_question.values()):
            if word.__contains__(word_to_verify):
                counter_question += 1

    the_file_content = file_content.strip().splitlines()
    for content in the_file_content:
        if content == '':
            the_file_content.remove(content)

    for word in the_file_content:
        if not word == "\n":
            key, value = word.strip().split(" ", 1)
            if (key in set(words_question.values()) or key in set(
                    words_intro.values()) and 1 <= counter < counter_question - 1):
                list_questions.append(dict_question)
                dict_question = {key: value.strip()}
                counter += 1
            elif key in set(words_question.values()) or key in set(words_intro.values()) and counter == 0:
                counter += 1
                dict_question[key] = value.strip()
            elif key in set(words_question.values()) or key in set(
                    words_intro.values()) and counter == counter_question - 1:
                list_questions.append(dict_question)
                dict_question = {key: value.strip()}
            else:
                dict_question[key] = value.strip()

    list_questions.append(dict_question)
    # print(list_questions)
    return list_questions


def get_type(question):
    type_ = ""
    for key, value in question.items():
        if key in set(words_type.values()):
            _, type_ = type_is_valid(str(value).lower())
    return type_


def validate_file_content(file_content, file_extension, request):
    if file_content and file_extension.__contains__(".txt"):
        list_questions = get_list_questions_txt(file_content)
    elif file_content and file_extension.__contains__(".json"):
        list_questions = json.loads(file_content)
    else:
        return False, "incorrect file type"
    for question in list_questions:
        for key, value in question.items():
            if key in set(words_type.values()):
                is_valid, the_type_ = type_is_valid(str(value).lower())
                if not is_valid and the_type_ is None:
                    return False, "type of question incorrect"

    for question in list_questions:
        for key, value in question.items():
            if key in set(words_question.values()):
                if value == "" and value is None:
                    return False, "no questions"
    for question in list_questions:
        for key, value in question.items():
            if key in set(words_multimedia.values()):
                type_ = get_type(question)
                is_valid = multimedia_is_valid(type_, value)
                if not is_valid:
                    return False, "multimedia incorrect"
    for question in list_questions:
        for key, value in question.items():
            if key in set(words_options_question.values()):
                type_ = get_type(question)
                is_valid = option_is_valid(type_, value)
                if not is_valid:
                    return False, "incorrect answer option"
    return True, ""


def type_is_valid(type_to_check):
    """
    Function to check whether the question types indicated by the user are valid.
    """

    intro = "introduction"
    dict_intro = {'en': 'introduction', 'es': 'introducción',
                  'de': 'Einführung', 'it': 'introduzione',
                  'pt': 'introdução'}

    video_with_intro = "video with introduction"
    dict_video_with_intro = {'en': 'video with introduction', 'fr': 'vidéo d\'introduction',
                             'es': 'vídeo con introducción', 'de': 'Einführungsvideo',
                             'it': 'video con introduzione', 'pt': 'vídeo com introdução'}
    audio_with_intro = "audio with introduction"
    dict_audio_with_intro = {'en': 'audio with introduction', 'fr': 'audio d\'introduction',
                             'es': 'audio con introducción', 'de': 'Audio-Einleitung',
                             'it': 'audio con introduzione', 'pt': 'áudio com introdução'}

    choose_digital_image = "choose one of the digital images"
    dict_choose_digital_image = {'en': 'choose one of the digital images',
                                 'fr': "choisissez l'une des images numériques",
                                 'es': 'elija una de las imágenes digitales',
                                 'de': 'wählen sie eines der digitalen bilder',
                                 'it': 'scegli una delle immagini digitali',
                                 'pt': 'escolha uma das imagens digitais'
                                 }
    numerical_scales = "numerical scales"
    dict_numerical_scales = {'en': 'numerical scales', 'fr': 'échelles numériques', 'es': 'escalas numéricas',
                             'de': 'numerische skalen', 'it': 'scale numeriche', 'pt': 'escalas numéricas'}
    image_numerical_scales = "images with numerical scales as visual aids"
    dict_images_numerical_scales = {'en': 'images with numerical scales as visual aids',
                                    'fr': 'images avec des échelles numériques comme aides visuelles',
                                    'es': 'imágenes con escalas numéricas como ayudas visuales',
                                    'de': 'bilder mit numerischen skalen als visuelle hilfsmittel',
                                    'it': 'immagini con scale numeriche come ausili visivi',
                                    'pt': 'imagens com escalas numéricas como recursos visuais',
                                    }
    graphics_likert_scale = "graphics for response options using likert-type scales"
    dict_graphics_likert_scale = {'en': 'graphics for response options using likert-type scales',
                                  'fr': "graphiques pour les options de réponse à l'aide d'échelles de type likert",
                                  'es': 'gráficos para opciones de respuesta utilizando escalas de tipo likert',
                                  'de': 'grafiken für antwortoptionen unter verwendung von skalen vom typ likert',
                                  'it': 'grafici per le opzioni di risposta utilizzando scale di tipo likert',
                                  'pt': 'gráficos para opções de resposta usando escalas do tipo likert'
                                  }

    multiple_choice = "multiple choice"
    dict_multiple_choice = {'en': 'multiple choice', 'fr': 'choix multiple', 'es': 'multiple choice',
                            'de': 'multiple-choice-raster', 'it': 'scelta multipla', 'pt': 'escolha múltipla'
                            }
    single_option = "single option answer"
    dict_single_option_answer = {'en': 'single option answer', 'fr': 'réponse à option unique',
                                 'es': 'respuesta de opción única', 'de': 'single-option-antwort',
                                 'it': 'risposta a opzione singola', 'pt': 'uma só opção de resposta'
                                 }
    yes_no_maybe = "yes/no/maybe"
    dict_yes_no_maybe = {'en': 'yes/no/maybe', 'fr': 'oui/non/peut-être ', 'es': 'sí/no/quizá ',
                         'de': 'ja, nein, oder vielleicht', 'it': 'con me', 'pt': 'sim — não — talvez'}
    date_ = "date"
    dict_date = {'en': 'date', 'fr': 'date', 'es': 'fecha', 'de': 'datum', 'it': 'data,', 'pt': 'data'}

    number_ = "number"
    dict_number = {'en': 'number', 'fr': 'nombre', 'es': 'número', 'de': 'nummer', 'it': 'numero', 'pt': 'número'}

    written_answer_short = "short written answer"
    dict_written_answer_short = {'en': 'short written answer', 'fr': 'courte réponse écrite',
                                 'es': 'respuesta escrita breve', 'de': 'kurze schriftliche antwort',
                                 'it': 'breve risposta scritta', 'pt': 'resposta escrita curta'}

    written_answer_long = "long written answer"
    dict_written_answer_long = {'en': 'long written answer', 'fr': 'longue réponse écrite',
                                'es': 'respuesta escrita larga', 'de': 'lange schriftliche antwort',
                                'it': 'lunga risposta scritta', 'pt': 'resposta escrita longa'}

    video_with_long_written_answer = "video with long written answer"
    dict_video_with_long_written_answer = {'en': 'video with long written answer',
                                           'fr': 'vidéo avec réponse écrite longue',
                                           'es': 'vídeo con respuesta larga por escrito',
                                           'de': 'video mit langer schriftlicher antwort',
                                           'it': 'video con risposta scritta lunga',
                                           'pt': 'vídeo com resposta longa por escrito'}

    video_with_short_written_answer = "video with short written answer"
    dict_video_with_short_written_answer = {'en': 'video with short written answer',
                                            'fr': 'vidéo avec réponse écrite courte',
                                            'es': 'vídeo con respuesta breve por escrito',
                                            'de': 'video mit kurzer schriftlicher antwort',
                                            'it': 'video con breve risposta scritta',
                                            'pt': 'vídeo com resposta curta por escrito'}

    video_with_number = "video with number"
    dict_video_with_number = {'en': 'video with number', 'fr': 'vidéo avec numéro', 'es': 'vídeo con número',
                              'de': 'video mit nummer', 'it': 'video con numero', 'pt': 'vídeo com número'}

    video_with_date = "video with date"
    dict_video_with_date = {'en': 'video with date', 'fr': 'vidéo avec date', 'es': 'vídeo con fecha',
                            'de': 'video mit datum', 'it': 'video con data', 'pt': 'vídeo com data'}

    video_with_yes_no_maybe = "video with yes/no/maybe"
    dict_video_with_yes_no_maybe = {'en': 'video with yes/no/maybe', 'fr': 'vidéo avec oui/non/peut-être',
                                    'es': 'vídeo con sí/no/tal vez', 'de': 'video mit ja/nein/vielleicht',
                                    'it': 'video con sì/no/forse', 'pt': 'vídeo com sim/não/talvez'}

    video_with_single_option_answer = "video with single option answer"
    dict_video_with_single_option_answer = {'en': 'video with single option answer',
                                            'fr': 'vidéo avec une seule option de réponse',
                                            'es': 'vídeo con respuesta de una sola opción',
                                            'de': 'video mit single-option-antwort',
                                            'it': 'video con risposta a opzione singola',
                                            'pt': 'vídeo com resposta de opção única'}

    video_with_multiple_choice = "video with multiple choice"
    dict_video_with_multiple_choice = {'en': 'video with multiple choice', 'fr': 'vidéo à choix multiples',
                                       'es': 'vídeo con opción múltiple', 'de': 'video mit mehrfachauswahl',
                                       'it': 'video a scelta multipla', 'pt': 'vídeo com múltipla escolha'}

    video_with_graphics_response_options_using_likert_scales = "video with graphics response options using likert scales"
    dict_video_with_graphics_response_options = {'en': 'video with graphics response options using likert scales',
                                                 'fr': "vidéo avec options de réponse graphique à l'aide d'échelles de similarité",
                                                 'es': 'vídeo con opciones de respuesta gráfica utilizando escalas likert',
                                                 'de': 'video mit grafischen antwortoptionen unter verwendung von likert-skalen',
                                                 'it': 'video con opzioni di risposta grafica utilizzando scale likert',
                                                 'pt': 'vídeo com opções de resposta gráfica usando escalas likert'}

    video_with_images_with_numerical_scales_as_visual_aids = "video with images with numerical scales as visual aids"
    dict_video_with_images_with_numerical_scales_as_visual_aids = {
        'en': 'video with images with numerical scales as visual aids',
        'fr': 'vidéo avec des images avec des échelles numériques comme aides visuelles',
        'es': 'vídeo con imágenes con escalas numéricas como ayudas visuales',
        'de': 'video mit bildern mit numerischen skalen als visuelle hilfsmittel',
        'it': 'video con immagini con scale numeriche come ausili visivi',
        'pt': 'vídeo com imagens com escalas numéricas como recursos visuais'}

    video_with_numerical_scales = "video with numerical scales"
    dict_video_with_numerical_scales = {'en': 'video with numerical scales', 'fr': 'vidéo avec échelles numériques',
                                        'es': 'vídeo con escalas numéricas', 'de': 'video mit numerischen skalen',
                                        'it': 'video con scale numeriche', 'pt': 'vídeo com escalas numéricas'}

    video_with_choose_one_of_the_digital_images = "video with choose one of the digital images"
    dict_video_with_choose_one_of_the_digital_images = {'en': 'video with choose one of the digital images',
                                                        'fr': "vidéo avec choisir l'une des images numériques",
                                                        'es': 'vídeo con elegir una de las imágenes digitales',
                                                        'de': 'video mit einem der digitalen bilder auswählen',
                                                        'it': 'video con scelta di una delle immagini digitali',
                                                        'pt': 'vídeo com escolha uma das imagens digitais'}
    audio_with_long_written_answer = "audio with long written answer"
    dict_audio_with_long_written_answer = {'en': 'audio with long written answer',
                                           'fr': 'audio avec réponse écrite longue',
                                           'es': 'audio con respuesta larga por escrito',
                                           'de': 'audio mit langer schriftlicher antwort',
                                           'it': 'audio con risposta scritta lunga',
                                           'pt': 'áudio com resposta longa por escrito'}

    audio_with_short_written_answer = "audio with short written answer"
    dict_audio_with_short_written_answer = {'en': 'audio with short written answer',
                                            'fr': 'audio avec réponse écrite courte',
                                            'es': 'audio con respuesta escrita corta',
                                            'de': 'audio mit kurzer schriftlicher antwort',
                                            'it': 'audio con breve risposta scritta',
                                            'pt': 'áudio com resposta escrita curta'}

    audio_with_number = "audio with number"
    dict_audio_with_number = {'en': 'audio with number', 'fr': 'audio avec numéro', 'es': 'audio con número',
                              'de': 'audio mit nummer', 'it': 'audio con numero', 'pt': 'áudio com número'}

    audio_with_date = "audio with date"
    dict_audio_with_date = {'en': 'audio with date', 'fr': 'audio avec date', 'es': 'audio con fecha',
                            'de': 'audio mit datum', 'it': 'audio con data', 'pt': 'áudio com data'}

    audio_with_yes_no_maybe = "audio with yes/no/maybe"
    dict_audio_with_yes_no_maybe = {'en': 'audio with yes/no/maybe', 'fr': 'audio avec oui/non/peut-être',
                                    'es': 'audio con sí/no/tal vez', 'de': 'audio mit ja/nein/vielleicht',
                                    'it': 'audio con sì/no/forse', 'pt': 'áudio com sim/não/talvez'}

    audio_with_single_option_answer = "audio with single option answer"
    dict_audio_with_single_option_answer = {'en': 'audio with single option answer',
                                            'fr': 'audio avec une seule option de réponse',
                                            'es': 'audio con respuesta de una sola opción',
                                            'de': 'audio mit single-option-antwort',
                                            'it': 'audio con risposta a opzione singola',
                                            'pt': 'áudio com resposta de opção única'}

    audio_with_multiple_choice = "audio with multiple choice"
    dict_audio_with_multiple_choice = {'en': 'audio with multiple choice', 'fr': 'audio à choix multiples',
                                       'es': 'audio con opción múltiple', 'de': 'audio mit mehrfachauswahl',
                                       'it': 'audio a scelta multipla', 'pt': 'áudio com múltipla escolha'}

    audio_with_graphics_response_options_using_likert_scales = "audio with graphics response options using likert scales"
    dict_audio_with_graphics_response_options = {'en': 'audio with graphics response options using likert scales',
                                                 'fr': "audio avec options de réponse graphique à l'aide d'échelles de similarité",
                                                 'es': 'audio con opciones de respuesta gráfica utilizando escalas likert',
                                                 'de': 'audio mit grafik-response-optionen unter verwendung von likert-skalen',
                                                 'it': 'audio con opzioni di risposta grafica utilizzando scale likert',
                                                 'pt': 'áudio com opções de resposta gráfica usando escalas likert'}

    audio_with_images_with_numerical_scales_as_visual_aids = "audio with images with numerical scales as visual aids"
    dict_audio_with_images_with_numerical_scales_as_visual_aids = {
        'en': 'audio with images with numerical scales as visual aids',
        'fr': 'audio avec des images avec des échelles numériques comme aides visuelles',
        'es': 'audio con imágenes con escalas numéricas como ayudas visuales',
        'de': 'audio mit bildern mit numerischen skalen als visuelle hilfsmittel',
        'it': 'audio con immagini con scale numeriche come ausili visivi',
        'pt': 'áudio com imagens com escalas numéricas como recursos visuais'}

    audio_with_numerical_scales = "audio with numerical scales"
    dict_audio_with_numerical_scales = {'en': 'audio with numerical scales', 'fr': 'audio avec échelles numériques',
                                        'es': 'audio con escalas numéricas', 'de': 'audio mit numerischen skalen',
                                        'it': 'audio con scale numeriche', 'pt': 'áudio com escalas numéricas'}

    audio_with_choose_one_of_the_digital_images = "audio with choose one of the digital images"
    dict_audio_with_choose_one_of_the_digital_images = {'en': 'audio with choose one of the digital images',
                                                        'fr': "audio avec choisissez l'une des images numériques",
                                                        'es': 'audio con elegir una de las imágenes digitales',
                                                        'de': 'audio mit einem der digitalen bilder auswählen',
                                                        'it': 'audio con scelta di una delle immagini digitali',
                                                        'pt': 'áudio com escolha uma das imagens digitais'}

    if type_to_check in dict_choose_digital_image.values():
        return True, choose_digital_image
    elif type_to_check in dict_numerical_scales.values():
        return True, numerical_scales
    elif type_to_check in dict_images_numerical_scales.values():
        return True, image_numerical_scales
    elif type_to_check in dict_graphics_likert_scale.values():
        return True, graphics_likert_scale
    elif type_to_check in dict_written_answer_short.values():
        return True, written_answer_short
    elif type_to_check in dict_written_answer_long.values():
        return True, written_answer_long
    elif type_to_check in dict_multiple_choice.values():
        return True, multiple_choice
    elif type_to_check in dict_single_option_answer.values():
        return True, single_option
    elif type_to_check in dict_yes_no_maybe.values():
        return True, yes_no_maybe
    elif type_to_check in dict_date.values():
        return True, date_
    elif type_to_check in dict_number.values():
        return True, number_
    elif type_to_check in dict_video_with_long_written_answer.values():
        return True, video_with_long_written_answer
    elif type_to_check in dict_video_with_short_written_answer.values():
        return True, video_with_short_written_answer
    elif type_to_check in dict_video_with_number.values():
        return True, video_with_number
    elif type_to_check in dict_video_with_date.values():
        return True, video_with_date
    elif type_to_check in dict_video_with_yes_no_maybe.values():
        return True, video_with_yes_no_maybe
    elif type_to_check in dict_video_with_single_option_answer.values():
        return True, video_with_single_option_answer
    elif type_to_check in dict_video_with_multiple_choice.values():
        return True, video_with_multiple_choice
    elif type_to_check in dict_video_with_graphics_response_options.values():
        return True, video_with_graphics_response_options_using_likert_scales
    elif type_to_check in dict_video_with_images_with_numerical_scales_as_visual_aids.values():
        return True, video_with_images_with_numerical_scales_as_visual_aids
    elif type_to_check in dict_video_with_numerical_scales.values():
        return True, video_with_numerical_scales
    elif type_to_check in dict_video_with_choose_one_of_the_digital_images.values():
        return True, video_with_choose_one_of_the_digital_images
    elif type_to_check in dict_audio_with_long_written_answer.values():
        return True, audio_with_long_written_answer
    elif type_to_check in dict_audio_with_short_written_answer.values():
        return True, audio_with_short_written_answer
    elif type_to_check in dict_audio_with_number.values():
        return True, audio_with_number
    elif type_to_check in dict_audio_with_date.values():
        return True, audio_with_date
    elif type_to_check in dict_audio_with_yes_no_maybe.values():
        return True, audio_with_yes_no_maybe
    elif type_to_check in dict_audio_with_single_option_answer.values():
        return True, audio_with_single_option_answer
    elif type_to_check in dict_audio_with_multiple_choice.values():
        return True, audio_with_multiple_choice
    elif type_to_check in dict_audio_with_graphics_response_options.values():
        return True, audio_with_graphics_response_options_using_likert_scales
    elif type_to_check in dict_audio_with_images_with_numerical_scales_as_visual_aids.values():
        return True, audio_with_images_with_numerical_scales_as_visual_aids
    elif type_to_check in dict_audio_with_numerical_scales.values():
        return True, audio_with_numerical_scales
    elif type_to_check in dict_audio_with_choose_one_of_the_digital_images.values():
        return True, audio_with_choose_one_of_the_digital_images
    elif type_to_check in dict_intro.values():
        return True, intro
    elif type_to_check in dict_video_with_intro.values():
        return True, video_with_intro
    elif type_to_check in dict_audio_with_intro.values():
        return True, audio_with_intro
    else:
        return False, None


def contains_options_and_returns_them(option_or_multimedia):
    """
    Function that checks whether multimedia content or options inherent to a question have been correctly indicated
    """
    if str(option_or_multimedia).__contains__(";"):
        ret = str(option_or_multimedia).split(";")
        return True, ret
    else:
        return False, None


def option_is_valid(type, option):
    """
    Function that evaluates options and their arrangement, according to the type of question
    """

    if_contains_semicolon, options = contains_options_and_returns_them(option)

    if type == "choose one of the digital images" or type == "video with choose one of the digital images" or type == "audio with choose one of the digital images" or type == "graphics for response options using likert-type scales" or type == "video with graphics response options using likert scales" or type == "audio with graphics response options using likert scales" and option == 'None' or option == '':
        return False
    elif type == "numerical scales" or type == "video with numerical scales" or type == "audio with numerical scales" and is_numerical_scale_correct(
            option):
        return True
    elif type == "images with numerical scales as visual aids" or type == "video with images with numerical scales as visual aids" or type == "audio with images with numerical scales as visual aids" and is_numerical_scale_correct(
            option):
        return True
    elif (
            type == "short written answer" or type == "video with short written answer" or type == "audio with short written answer" or type == "long written answer"
            or type == "video with long written answer" or type == "audio with long written answer" or type == "date"
            or type == "video with date" or type == "audio with date" or type == "number" or type == "video with number" or type == "audio with number"
            and option == 'None' or option == ''):
        return False
    elif type == "multiple choice" or type == "video with multiple choice" or type == "audio with multiple choice" and if_contains_semicolon and options is not None:
        return True
    elif type == "single option answer" or type == "video with single option answer" or type == "audio with single option answer" and if_contains_semicolon and options is not None:
        return True
    elif type == "yes/no/maybe" or type == "video with yes/no/maybe" or type == "audio with yes/no/maybe" and if_contains_semicolon and options is not None:
        return True
    else:
        return False


def is_numerical_scale_correct(option):
    """
    Function that evaluates whether a numerical scale was correctly indicated
    """
    if option is None:
        return False
    else:
        try:
            idx_start = str(option).find("[")
            idx_end = str(option).find("]")
            idx_middle = str(option).find("-")
            if idx_start == -1 and idx_end == -1 and idx_middle == -1:
                return False
            else:
                idx_x = int(option[idx_start + 1:idx_middle])
                idx_y = int(option[idx_middle + 1:idx_end])
                if 0 <= idx_x <= 10 and 0 <= idx_y <= 10:
                    return True
                else:
                    return False
        except ValueError or TypeError:
            return False


def contains_multimedia(multimedia, video_or_audio):
    if str(multimedia).__contains__(";"):
        ret = str(multimedia).split(";")
        counter = 0
        for element in ret:
            if counter == 0 and video_or_audio:
                counter += 1
                continue
            else:
                if not str(element).__contains__(","):
                    return False, None
        return True, ret
    else:
        return False, None


def multimedia_is_valid(the_type, multimedia):
    """
        Function that evaluates links to multimedia content and their arrangement, according to the type of question
    """
    if_contains_semicolon, multimedia_ = contains_multimedia(multimedia, False)

    if the_type == "choose one of the digital images":
        if_contains_semicolon, multimedia_ = contains_multimedia(multimedia, False)
        if if_contains_semicolon and multimedia_ is not None:
            return True
    elif the_type == "video with choose one of the digital images" or the_type == "audio with choose one of the digital images":
        if_contains_semicolon, multimedia_ = contains_multimedia(multimedia, True)
        if if_contains_semicolon and multimedia_ is not None and validate_link_video_or_audio(multimedia_[0]):
            return True
    elif the_type == "images with numerical scales as visual aids":
        if_contains_semicolon, multimedia_ = contains_multimedia(multimedia, False)
        if if_contains_semicolon and multimedia_ is not None:
            return True
    elif the_type == "video with images with numerical scales as visual aids" or the_type == "audio with images with numerical scales as visual aids":
        if_contains_semicolon, multimedia_ = contains_multimedia(multimedia, True)
        if if_contains_semicolon and multimedia_ is not None and validate_link_video_or_audio(multimedia_[0]):
            return True
    elif the_type == "graphics for response options using likert-type scales":
        if_contains_semicolon, multimedia_ = contains_multimedia(multimedia, False)
        if if_contains_semicolon and multimedia_ is not None:
            return True
    elif the_type == "video with graphics response options using likert scales" or the_type == "audio with graphics response options using likert scales":
        if_contains_semicolon, multimedia_ = contains_multimedia(multimedia, True)
        if if_contains_semicolon and multimedia_ is not None and validate_link_video_or_audio(multimedia_[0]):
            return True
    elif ((the_type == "short written answer" or the_type == "long written answer"
           or the_type == "date" or the_type == "number"
           or the_type == "multiple choice" or the_type == "single option answer"
           or the_type == "yes/no/maybe" or the_type == "numerical scales")
          and (multimedia == 'None' or multimedia == "")):
        return False
    elif ((the_type == "video with short written answer" or the_type == "video with long written answer"
           or the_type == "video with long written answer" or the_type == "video with date" or the_type == "video with number"
           or the_type == "video with multiple choice" or the_type == "video with single option answer" or the_type == "video with yes/no/maybe" or the_type == "video with numerical scales" or
           the_type == "audio with short written answer" or the_type == "audio with long written answer"
           or the_type == "audio with long written answer" or the_type == "audio with date" or the_type == "audio with number"
           or the_type == "audio with multiple choice" or the_type == "audio with single option answer" or the_type == "audio with yes/no/maybe" or the_type == "audio with numerical scales"
          )
          and (multimedia is not None and validate_link_video_or_audio(multimedia))):
        return True
    elif the_type == "video with introduction" or the_type == "audio with introduction" and (multimedia is not None and
                                                                                             validate_link_video_or_audio(
                                                                                                 multimedia)):
        return True
    else:
        return False


def validate_link_video_or_audio(link):
    """
    Function that validates a link and evaluates its extension. It applies to links to audios or videos.
    """
    try:
        urlparse(link)
        ends_with_mp4 = str(link).__contains__(".mp4")
        ends_with_mp3 = str(link).__contains__(".mp3")
        ends_with_ogg = str(link).__contains__(".ogg")
        return ends_with_mp4 or ends_with_mp3 or ends_with_ogg
    except Exception:
        return False


def validate_date(date_string: str, question_mandatory) -> bool:
    """
    Function used to validate a date input
    """
    if date_string == "":
        return False
    date_elements = date_string.split("/")
    if question_mandatory and (date_elements[0] == "DD" and date_elements[1] == "MM" and date_elements[2] == "YYYY" or date_elements[0] == "0" and date_elements[1] == "0" and date_elements[2] == "0000"):
        return False
    if date_elements[0] == "DD" and date_elements[1] == "MM" and date_elements[2] == "YYYY":
        return True
    day = int(date_elements[0])
    month = int(date_elements[1])
    year = int(date_elements[2])
    if not is_leap_year(year) and month == 2 and day == 29:
        return False
    elif month == 2 and day > 29:
        return False
    elif (month == 4 or month == 6 or month == 9 or month == 11) and day > 30:
        return False
    else:
        return True


def is_leap_year(year):
    """
    Function used to verify if a year is a leap year
    """
    return ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0)


def random_string_generator(number_of_characters: int) -> str:
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    chars = lower + upper + digits
    str_to_ret = ""
    for i in range(number_of_characters):
        str_to_ret += random.choice(chars)
    return str_to_ret


def password_generator():
    """
    Function used to generate a random password
    """
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    chars = lower + upper + digits
    password = ""
    for i in range(1, 13):
        password += random.choice(chars)
    return password


def remove_spaces_on_dict_values(dictionary: dict) -> dict:
    for key, value in dictionary.items():
        dictionary[key] = str(value).strip()
    return dictionary


def define_selected_view(boxes_selected: list):
    selected_view = None
    if "select_colors" in boxes_selected and "videos_lgp" in boxes_selected:
        selected_view = "0"
    elif "select_colors" in boxes_selected and "videos_lgp" not in boxes_selected:
        selected_view = "1"
    elif "select_colors" not in boxes_selected and "videos_lgp" in boxes_selected:
        selected_view = "2"
    elif "select_colors" not in boxes_selected and "videos_lgp" not in boxes_selected:
        selected_view = "3"
    else:
        selected_view = "0"

    return selected_view
