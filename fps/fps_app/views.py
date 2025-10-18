import copy
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from .Utils import *
from .models import *


def loadSurvey(request):
    template = loader.get_template('upload_file_by_creator.html')
    context = {}
    return HttpResponse(template.render(context, request))


def possibleRoutes(request):
    template = loader.get_template('possible_routes.html')
    context = {}
    return HttpResponse(template.render(context, request))


def selectSurvey(request):
    # request.session['session_identification'] = random_string_generator(10)
    template = loader.get_template('select_survey_respondent.html')
    context = {}
    return HttpResponse(template.render(context, request))


def save_survey(request):
    email = request.POST.get('email_user')
    allow_prefilled_file_with_answers = request.POST.get('upload_of_file_with_survey_completed')
    if allow_prefilled_file_with_answers == "True":
        allow_prefilled_file_with_answers = True
    else:
        allow_prefilled_file_with_answers = False

    insertLinkForFileWithQuestions = request.POST.get('insertLinkForFileWithQuestions')
    ret = False
    if not request.FILES.getlist('uploadInputFileWithQuestions') and len(insertLinkForFileWithQuestions) == 0:
        ret = None
    elif request.FILES.getlist('uploadInputFileWithQuestions') and len(insertLinkForFileWithQuestions) == 0:
        ret = True
    elif not request.FILES.getlist('uploadInputFileWithQuestions') and len(insertLinkForFileWithQuestions) > 0:
        ret = False
    elif request.FILES.getlist('uploadInputFileWithQuestions') and len(insertLinkForFileWithQuestions) > 0:
        ret = False
    else:
        ret = None
    file_extension = ''
    file_content = ''
    the_file_name = ''
    # Get files extension and content
    if ret is True:
        file_extension, file_content = loadUploadedFileWithQuestions(request.FILES['uploadInputFileWithQuestions'])
        the_file_name = str(request.FILES['uploadInputFileWithQuestions'])
        if str(the_file_name).__contains__(".txt"):
            idx_of_ex = the_file_name.find(".txt")
            the_file_name = the_file_name[:idx_of_ex]
        elif str(the_file_name).__contains__(".json"):
            idx_of_ex = the_file_name.find(".json")
            the_file_name = the_file_name[:idx_of_ex]
        else:
            context = {}
            template = loader.get_template('incorrect_file_type.html')
            return HttpResponse(template.render(context, request))
    elif ret is False:
        the_file_name, file_extension, file_content = loadLinkFileWithQuestions(insertLinkForFileWithQuestions)
        if file_content is None and file_extension is None and the_file_name is None:
            context = {}
            template = loader.get_template('incorrect_file_type.html')
            return HttpResponse(template.render(context, request))
        else:
            context = {}
            template = loader.get_template('incorrect_url.html')
            return HttpResponse(template.render(context, request))
    else:
        context = {}
        template = loader.get_template('no_uploaded_file.html')
        return HttpResponse(template.render(context, request))

    all_correct, text = validate_file_content(file_content, file_extension, request)

    if all_correct is False and text == "type of question incorrect":
        context = {}
        template = loader.get_template('type_of_question_incorrect.html')
        return HttpResponse(template.render(context, request))
    elif all_correct is False and text == "no questions":
        context = {}
        template = loader.get_template('no_questions.html')
        return HttpResponse(template.render(context, request))
    elif all_correct is False and text == "multimedia incorrect":
        context = {}
        template = loader.get_template('multimedia_incorrect.html')
        return HttpResponse(template.render(context, request))
    elif all_correct is False and text == "incorrect answer option":
        context = {}
        template = loader.get_template('incorrect_answer_option.html')
        return HttpResponse(template.render(context, request))
    elif all_correct is False and text == "incorrect file type":
        context = {}
        template = loader.get_template('incorrect_file_type.html')
        return HttpResponse(template.render(context, request))
    else:
        id_survey = ''
        id_of_survey = random_string_generator(4)
        survey = Survey(name_of_survey=the_file_name, id_of_survey=id_of_survey, file_content=file_content,
                        file_extension=file_extension,
                        allow_file_upload_with_answers=allow_prefilled_file_with_answers)
        survey.save()
        id_survey = survey.id
        password = password_generator()
        if User.objects.all().count() == 0:
            user = User(email=email, password=password)
            user.save()
            id_user = user.id
        else:
            if User.objects.filter(email=email).values().count() == 0:
                user = User(email=email, password=password)
                user.save()
                id_user = user.id
            else:
                user = User.objects.filter(email=email).first()
                password = user.password
                id_user = user.id

        if Survey_User.objects.all().count() == 0:
            su = Survey_User.objects.create(id_survey=survey, id_user=user)
            su.save()
            id_su = su.id
        else:
            if Survey_User.objects.filter(id_survey=survey, id_user=user).values().count() == 0:
                su = Survey_User.objects.create(id_survey=survey, id_user=user)
                su.save()
                id_su = su.id
            else:
                id_su = Survey_User.objects.filter(id_survey=survey, id_user=user).first().id
        if not id_survey == '':
            template = loader.get_template('result_upload_template.html')
            str_pass_idsurvey = "Password: " + password + "\n" + "Survey ID: " + survey.id_of_survey
            context = {"str_pass_idsurvey": str_pass_idsurvey,
                       "survey_name": survey.name_of_survey}
            return HttpResponse(template.render(context, request))
        else:
            context = {}
            template = loader.get_template('no_uploaded_file.html')
            return HttpResponse(template.render(context, request))


def processSelectedSurvey(request):
    # Definition of variables to be used throughout the function, which correspond to survey components
    global email, list_questions, list_types, list_options_questions, list_mandatory, list_multimedia, list_groups, the_type_, multimedia, answer_option, group, the_mandatory, the_file_name, hotlink, type
    # Get language selected by the user
    multimedia = answer_option = group = the_mandatory = hotlink = None
    language = request.POST.get('language')
    if "boxes_for_view" in request.POST.keys():
        boxes_selected = request.POST.getlist('boxes_for_view')
        selected_view = define_selected_view(boxes_selected)
    else:
        selected_view = "3"
    # Obtain survey by its id
    id_of_survey = request.POST['id_of_survey']
    if id_of_survey == '':
        context = {}
        template = loader.get_template('incorrect_id_of_survey.html')
        return HttpResponse(template.render(context, request))
    # Obtain file content, extension, name for the survey selected
    survey = Survey.objects.filter(id_of_survey=id_of_survey).first()
    if survey is None:
        context = {}
        template = loader.get_template('incorrect_id_of_survey.html')
        return HttpResponse(template.render(context, request))
    su = Survey_User.objects.filter(id_survey=survey).first()

    user = su.id_user
    file_content = survey.file_content
    file_extension = survey.file_extension
    file_name = survey.name_of_survey
    # Get if the creator allows a pre-filled file with the answers to the survey questions
    allow_prefilled_file_with_answers = survey.allow_file_upload_with_answers
    if file_content and file_extension.__contains__(".txt"):
        idx_txt = int(str(file_name).find(".txt"))
        the_file_name = str(file_name)[:idx_txt]
        list_questions = get_list_questions_txt(file_content)

    elif file_content and file_extension.__contains__(".json"):
        idx_json = int(str(file_name).find(".json"))
        the_file_name = str(file_name)[:idx_json]
        list_questions = json.loads(file_content)

    # Save and Retrieve survey structure from the database

    list_survey = []
    list_user = []
    list_id_types = list()
    list_id_questions = list()
    list_id_options = list()
    list_id_multimedia = list()
    list_id_question_multimedia = list()
    list_id_survey_question = list()
    list_id_question_option = list()
    list_id_groups = list()
    list_id_hotlink = list()
    list_id_question_hotlink = list()
    for question in list_questions:
        for key, value in question.items():
            if key in set(words_type.values()):
                is_valid, the_type_ = type_is_valid(str(value).lower())
                if Type_question.objects.all().count() == 0:
                    type = Type_question(type_question=the_type_)
                    type.save()
                    id_type = type.id
                    list_id_types.append(id_type)
                else:
                    if Type_question.objects.filter(type_question=the_type_).values().count() == 0:
                        type = Type_question(type_question=the_type_)
                        type.save()
                        id_type = type.id
                        list_id_types.append(id_type)
                    else:
                        type = Type_question.objects.filter(type_question=the_type_).first()
                        id_type = type.id
                        list_id_types.append(id_type)
        for key, value in question.items():
            if key in set(words_group.values()):
                if Group.objects.all().count() == 0:
                    group = Group(group_name=value)
                    group.save()
                    id_group = group.id
                    list_id_groups.append(id_group)

                else:
                    if Group.objects.filter(group_name=value).values().count() == 0:
                        group = Group(group_name=value)
                        group.save()
                        id_group = group.id
                        list_id_groups.append(id_group)
                    else:
                        group = Group.objects.filter(group_name=value).first()
                        id_group = group.id
                        list_id_groups.append(id_group)

        if group is None:
            if type.type_question == "introduction" or type.type_question == "video with introduction" or type.type_question == "audio with introduction":
                if Group.objects.filter(group_name="Introdução").values().count() == 0:
                    group = Group(group_name="Introdução")
                    group.save()
                    id_group = group.id
                    list_id_groups.append(id_group)
                else:
                    group = Group.objects.filter(group_name="Introdução").first()
                    id_group = group.id
                    list_id_groups.append(id_group)
            else:
                group = Group.objects.filter(group_name="Outras").first()
                id_group = Group.objects.filter(group_name="Outras").first().id
                list_id_groups.append(id_group)

        for key, value in question.items():
            if key in set(words_mandatory.values()):
                the_mandatory = value
        if the_mandatory is None:
            the_mandatory = False
        for key, value in question.items():
            if key in set(words_question.values()) or key in set(words_intro.values()):
                if Question.objects.all().count() == 0:
                    the_question = Question(question=value, mandatory=bool(the_mandatory), id_type_question=type,
                                            id_survey=survey, id_group=group)
                    the_question.save()
                    id_question = the_question.id
                    list_id_questions.append(id_question)
                else:
                    if Question.objects.filter(question=value, mandatory=the_mandatory,
                                               id_type_question=type,
                                               id_survey=survey, id_group=group).values().count() == 0:
                        the_question = Question(question=value, mandatory=bool(the_mandatory),
                                                id_type_question=type,
                                                id_survey=survey, id_group=group)
                        the_question.save()
                        id_question = the_question.id
                        list_id_questions.append(id_question)
                    else:
                        the_question = Question.objects.filter(question=value, mandatory=bool(the_mandatory),
                                                               id_type_question=type,
                                                               id_survey=survey, id_group=group).first()
                        id_question = the_question.id
                        list_id_questions.append(id_question)
        for key, value in question.items():
            if key in set(words_options_question.values()):
                if Answer_Option.objects.all().count() == 0:
                    answer_option = Answer_Option(answer_option=value)
                    answer_option.save()
                    id_option = answer_option.id
                    list_id_options.append(id_option)
                else:
                    if Answer_Option.objects.filter(answer_option=value).values().count() == 0:
                        answer_option = Answer_Option(answer_option=value)
                        answer_option.save()
                        id_option = answer_option.id
                        list_id_options.append(id_option)
                    else:
                        answer_option = Answer_Option.objects.filter(answer_option=value).first()
                        id_option = answer_option.id
                        list_id_options.append(id_option)
        for key, value in question.items():
            if key in set(words_multimedia.values()):
                if Multimedia.objects.all().count() == 0:
                    multimedia = Multimedia(multimedia=value)
                    multimedia.save()
                    id_multimedia = multimedia.id
                    list_id_multimedia.append(id_multimedia)
                else:
                    if Multimedia.objects.filter(multimedia=value).values().count() == 0:
                        multimedia = Multimedia(multimedia=value)
                        multimedia.save()
                        id_multimedia = multimedia.id
                        list_id_multimedia.append(id_multimedia)
                    else:
                        multimedia = Multimedia.objects.filter(multimedia=value).first()
                        id_multimedia = multimedia.id
                        list_id_multimedia.append(id_multimedia)
        for key, value in question.items():
            if key in set(words_hotlink.values()):
                if Hotlink.objects.all().count() == 0:
                    hotlink = Hotlink(hotlink=value)
                    hotlink.save()
                    id_hotlink = hotlink.id
                    list_id_hotlink.append(id_hotlink)
                else:
                    if Hotlink.objects.filter(hotlink=value).values().count() == 0:
                        hotlink = Hotlink(hotlink=value)
                        hotlink.save()
                        id_hotlink = hotlink.id
                        list_id_hotlink.append(id_hotlink)
                    else:
                        hotlink = Hotlink.objects.filter(hotlink=value).first()
                        id_hotlink = hotlink.id
                        list_id_hotlink.append(id_hotlink)
        if multimedia is not None:
            if Question_Multimedia.objects.all().count() == 0:

                qm = Question_Multimedia(id_question=the_question, id_multimedia=multimedia)
                qm.save()
                id_qm = qm.id
                list_id_question_multimedia.append(id_qm)
            else:
                if Question_Multimedia.objects.filter(id_question=the_question,
                                                      id_multimedia=multimedia).values().count() == 0:
                    qm = Question_Multimedia(id_question=the_question, id_multimedia=multimedia)
                    qm.save()
                    id_qm = qm.id
                    list_id_question_multimedia.append(id_qm)
                else:
                    qm = Question_Multimedia.objects.filter(id_question=the_question, id_multimedia=multimedia).first()
                    id_qm = Question_Multimedia.objects.filter(id_question=the_question,
                                                               id_multimedia=multimedia).first().id
                    list_id_question_multimedia.append(id_qm)
        if Survey_Question.objects.all().count() == 0:
            sq = Survey_Question(id_survey=survey, id_question=the_question)
            sq.save()
            id_sq = sq.id
            list_id_survey_question.append(id_sq)
        else:
            if Survey_Question.objects.filter(id_survey=survey, id_question=the_question).values().count() == 0:
                sq = Survey_Question(id_survey=survey, id_question=the_question)
                sq.save()
                id_sq = sq.id
                list_id_survey_question.append(id_sq)
            else:
                sq = Survey_Question.objects.filter(id_survey=survey, id_question=the_question).first()
                id_sq = Survey_Question.objects.filter(id_survey=survey, id_question=the_question).first().id
                list_id_survey_question.append(id_sq)
        if hotlink is not None:
            if Question_Hotlink.objects.all().count() == 0:
                qh = Question_Hotlink(id_hotlink=hotlink, id_question=the_question)
                qh.save()
                id_qh = qh.id
                list_id_question_hotlink.append(id_qh)
            else:
                if Question_Hotlink.objects.filter(id_hotlink=hotlink, id_question=the_question).values().count() == 0:
                    qh = Question_Hotlink(id_hotlink=hotlink, id_question=the_question)
                    qh.save()
                    id_qh = qh.id
                    list_id_question_hotlink.append(id_qh)
                else:
                    qh = Question_Hotlink.objects.filter(id_hotlink=hotlink, id_question=the_question).first()
                    id_qh = qh.id
                    list_id_question_hotlink.append(id_qh)

        if answer_option is not None:
            if Question_Answer_Option.objects.all().count() == 0:
                qo = Question_Answer_Option(id_question=the_question, id_answer_option=answer_option)
                qo.save()
                id_qo = qo.id
                list_id_question_option.append(id_qo)
            else:
                if Question_Answer_Option.objects.filter(id_question=the_question,
                                                         id_answer_option=answer_option).values().count() == 0:
                    qo = Question_Answer_Option(id_question=the_question, id_answer_option=answer_option)
                    qo.save()
                    id_qo = qo.id
                    list_id_question_option.append(id_qo)
                else:
                    qo = Question_Answer_Option.objects.filter(id_question=the_question,
                                                               id_answer_option=answer_option).first()
                    id_qo = Question_Answer_Option.objects.filter(id_question=the_question,
                                                                  id_answer_option=answer_option).first().id
                    list_id_question_option.append(id_qo)
        multimedia = type = answer_option = group = the_mandatory = hotlink = None
    """
    Gathering and organizing all the data needed to construct the survey
    """
    dict_question_hotlink = dict()
    if list_id_question_hotlink.__sizeof__() > 0:
        questions_hotlinks = Question_Hotlink.objects.filter(pk__in=list_id_question_hotlink)
        for qh in questions_hotlinks:
            dict_question_hotlink[qh.id_question.pk] = qh.id_hotlink.hotlink
    types = Type_question.objects.filter(pk__in=list_id_types)

    groups = Group.objects.filter(pk__in=list_id_groups)
    new_groups = list()
    gr_i_c = None
    for gr in groups:
        for key, value in words_informed_consent.items():
            if value in str(gr.group_name).lower():
                new_groups.append(gr)
                gr_i_c = gr
                break
    if gr_i_c is not None:
        for gr in groups:
            if not gr.pk == gr_i_c.pk:
                new_groups.append(gr)
    else:
        for gr in groups:
            new_groups.append(gr)

    questions_ = Question.objects.filter(pk__in=list_id_questions)

    questions = questions_.order_by("id_group")

    new_questions = list()
    for gr in new_groups:
        for q in questions:
            if q.id_group.pk == gr.pk:
                new_questions.append(q)
    intro_quest = None

    has_intro = False
    for q in new_questions:
        if str(q.id_type_question.type_question).__contains__("intro"):
            intro_quest = q
            new_questions.remove(q)
            new_questions.insert(0, intro_quest)
            has_intro = True

    options = Answer_Option.objects.filter(pk__in=list_id_options)

    multimedia = Multimedia.objects.filter(pk__in=list_id_multimedia)

    dict_question_option = dict()
    if list_id_question_option.__sizeof__() > 0:
        question_option = Question_Answer_Option.objects.filter(pk__in=list_id_question_option)
        for qo in question_option:
            if qo.id_question.id_type_question.type_question == 'numerical scales' or qo.id_question.id_type_question.type_question == 'video with numerical scales' or qo.id_question.id_type_question.type_question == 'audio with numerical scales':
                lst_temp = list()
                scale = str(qo.id_answer_option.answer_option).strip().split(";")[0]
                idx_start = str(scale).find("[")
                idx_end = str(scale).find("]")
                idx_middle = str(scale).find("-")
                idx_x = scale[idx_start + 1:idx_middle]
                idx_y = scale[idx_middle + 1:idx_end]
                for i in range(int(idx_x), int(idx_y) + 1):
                    lst_temp.append(i)
                dict_question_option[qo.id_question.pk] = lst_temp
            else:
                dict_question_option[qo.id_question.pk] = str(qo.id_answer_option.answer_option).split(";")
    dict_question_multimedia = dict()
    dict_videos = dict()
    dict_audios = dict()
    if list_id_question_multimedia.__sizeof__() > 0:
        question_multimedia = Question_Multimedia.objects.filter(pk__in=list_id_question_multimedia)
        dict_temp = dict()
        for qm in question_multimedia:
            dict_question_multimedia[qm.id_question.pk] = str(qm.id_multimedia.multimedia).split(";")
        for key, element in dict_question_multimedia.items():
            quest = Question.objects.filter(pk=key).first()
            if (quest.id_type_question.type_question == 'choose one of the digital images' or
                    quest.id_type_question.type_question == 'images with numerical scales as visual aids'):
                for item in element:
                    lst_temp = item.split(",")
                    dict_temp[lst_temp[0].strip()] = lst_temp[1].strip()
                dict_question_multimedia[key] = dict_temp
                dict_temp = dict()

            elif quest.id_type_question.type_question == 'graphics for response options using likert-type scales':
                for item in element:
                    lst_temp = item.split(",")
                    dict_temp[lst_temp[0].strip()] = [lst_temp[1].strip(), lst_temp[2].strip()]
                dict_question_multimedia[key] = dict_temp
                dict_temp = dict()

            elif quest.id_type_question.type_question == "video with choose one of the digital images" or quest.id_type_question.type_question == "video with images with numerical scales as visual aids" or quest.id_type_question.type_question == "audio with choose one of the digital images" or quest.id_type_question.type_question == "audio with images with numerical scales as visual aids":
                counter = 0
                for item in element:
                    if counter == 0:
                        if quest.id_type_question.type_question == "audio with choose one of the digital images" or quest.id_type_question.type_question == "audio with images with numerical scales as visual aids":
                            dict_audios[key] = item.strip()
                        else:
                            dict_videos[key] = item.strip()
                        counter += 1
                    else:
                        lst_temp = item.split(",")
                        dict_temp[lst_temp[0].strip()] = lst_temp[1].strip()
                dict_question_multimedia[key] = dict_temp
                # if quest.id_type_question.type_question == "audio with choose one of the digital images" or quest.id_type_question.type_question == "audio with images with numerical scales as visual aids":
                #     if key in dict_question_hotlink.keys():
                #         dict_question_multimedia[key] = zip(dict_temp.items(), dict_audios[key][2:])
                #     else:
                #         dict_question_multimedia[key] = zip(dict_temp.items(), dict_audios[key][1:])
                # else:
                #     if key in dict_question_hotlink.keys():
                #         dict_question_multimedia[key] = zip(dict_temp.items(), dict_videos[key][2:])
                #     else:
                #         dict_question_multimedia[key] = zip(dict_temp.items(), dict_videos[key][1:])
                dict_temp = dict()

            elif quest.id_type_question.type_question == "video with graphics response options using likert scales" or quest.id_type_question.type_question == "audio with graphics response options using likert scales":
                counter = 0
                for item in element:
                    if counter == 0:
                        if quest.id_type_question.type_question == ("audio with graphics response options using likert "
                                                                    "scales"):
                            dict_audios[key] = item.strip()
                        else:
                            dict_videos[key] = item.strip()
                        counter += 1
                    else:
                        lst_temp = item.split(",")
                        dict_temp[lst_temp[0].strip()] = [lst_temp[1].strip(), lst_temp[2].strip()]
                dict_question_multimedia[key] = dict_temp
                # if quest.id_type_question.type_question == "audio with graphics response options using likert scales":
                #     if key in dict_question_hotlink.keys():
                #         dict_question_multimedia[key] = zip(dict_temp.items(), dict_audios[key][2:])
                #     else:
                #         dict_question_multimedia[key] = zip(dict_temp.items(), dict_audios[key][1:])
                # else:
                #     if key in dict_question_hotlink.keys():
                #         dict_question_multimedia[key] = zip(dict_temp.items(), dict_videos[key][2:])
                #     else:
                #         dict_question_multimedia[key] = zip(dict_temp.items(), dict_videos[key][1:])
                dict_temp = dict()
    # for key, value in dict_question_multimedia.items():
    #     lst_temp_ = []
    #     if isinstance(value, zip):
    #         for (imgdet1, imgdet2), med in value:
    #             lst_temp_.append([imgdet1, imgdet2, med])
    #         dict_question_multimedia[key] = lst_temp_
    for key, value in dict_question_option.items():
        lst_temp_ = []
        quest = Question.objects.filter(pk=key).first()
        if (quest.id_type_question.type_question == 'video with single option answer' or quest.id_type_question.
                type_question == 'audio with single option answer' or quest.id_type_question.type_question == 'video with multiple choice' or
                quest.id_type_question.type_question == 'audio with multiple choice'):
            counter = 1
            for item in value:
                lst_temp_.append([str(item).strip(), dict_question_multimedia[key][counter]])
                counter += 1
            dict_question_option[key] = lst_temp_

    survey_question = Survey_Question.objects.filter(pk__in=list_id_survey_question)
    id_of_respondent = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    respondent = define_respondent(id_of_respondent)

    str_survey_questions = "".join("\"\t" + survey.name_of_survey + "\t\"\n")

    dict_questions_answers = dict()

    dict_numberquestion_questionpk = dict()
    number_of_questions = 0
    for q in new_questions:
        dict_questions_answers[str(q.pk)] = ""
        number_of_questions += 1
        dict_numberquestion_questionpk[str(number_of_questions)] = str(q.pk)
    request.session['dict_questions_answers'] = dict_questions_answers
    request.session['dict_numberquestion_questionpk'] = dict_numberquestion_questionpk
    if allow_prefilled_file_with_answers:
        for g in new_groups:
            if g.group_name not in words_for_group_intro.values():
                str_survey_questions += "\n" + "---\t" + str(g.group_name).upper() + "---\t" + "\n"
            for q in new_questions:
                if q.id_group == g:
                    if q.mandatory:
                        str_survey_questions += "Q: \t" + q.question + "*\n"
                    else:
                        if not q.id_type_question.type_question == "introduction" and not q.id_type_question.type_question == "video with introduction" and not q.id_type_question.type_question == "audio with introduction":
                            #     str_survey_questions += "«\t" + q.question+"\t»" + "\n"
                            # else:
                            str_survey_questions += "Q: \t" + q.question + "\n"
                    str_survey_questions += "\n"

                    # if dict_videos.keys().__contains__(q.pk):
                    #     str_survey_questions += "Video:\t" + dict_videos[q.pk] + "\n"
                    #     str_survey_questions += "\n"
                    # if dict_audios.keys().__contains__(q.pk):
                    #     str_survey_questions += "Audio:\t" + dict_audios[q.pk] + "\n"
                    #     str_survey_questions += "\n"
                    #
                    if dict_question_hotlink.keys().__contains__(q.pk):
                        str_survey_questions += dict_question_hotlink[q.pk] + "\n"
                        str_survey_questions += "\n"
                    if dict_question_multimedia.keys().__contains__(q.pk):
                        if (q.id_type_question.type_question == "choose one of the digital images"
                                or q.id_type_question.type_question == "images with numerical scales as visual aids"
                                or q.id_type_question.type_question == "video with choose one of the digital images"
                                or q.id_type_question.type_question == "video with images with numerical scales as visual aids"
                                or q.id_type_question.type_question == "audio with choose one of the digital images"
                                or q.id_type_question.type_question == "audio with images with numerical scales as visual aids"):

                            dict_link_txt_alt = dict_question_multimedia[q.pk]
                            for key, value in dict_link_txt_alt.items():
                                _txt = value
                                str_survey_questions += str(_txt) + "\n"  # + "\t" + str(link)
                        elif (
                                q.id_type_question.type_question == "graphics for response options using likert-type scales"
                                or q.id_type_question.type_question == "video with graphics response options using "
                                                                       "likert scales"
                                or q.id_type_question.type_question == "audio with graphics response options using "
                                                                       "likert scales"):
                            dict_link_legend_and_txt_alt = dict_question_multimedia[q.pk]

                            for key, value in dict_link_legend_and_txt_alt.items():
                                _txt = value[1]
                                str_survey_questions += str(_txt) + "\n"  # + "\t" + str(link)
                        else:
                            # lst_multimedia = dict_question_multimedia[q]
                            # for multi in lst_multimedia:
                            #     if str(q.id_type_question.type_question).__contains__("video"):
                            #         str_survey_questions += "Video:\t" + multi + "\n"
                            #     elif str(q.id_type_question.type_question).__contains__("audio"):
                            #         str_survey_questions += "Audio:\t" + multi + "\n"
                            #     else:
                            #         str_survey_questions += multi + "\n"
                            lst_options = list()
                            if dict_question_option.keys().__contains__(q.pk):
                                lst_options = dict_question_option[q.pk]
                            if len(lst_options) > 0:
                                for lst_option in lst_options:
                                    if q.id_type_question.type_question == "video with multiple choice" or q.id_type_question.type_question == "audio with multiple choice" or q.id_type_question.type_question == "video with single option answer" or q.id_type_question.type_question == "audio with single option answer":
                                        str_survey_questions += str(lst_option[0]) + "\n"
                                    else:
                                        str_survey_questions += str(lst_option) + "\n"
                    if dict_question_option.keys().__contains__(
                            q.pk) and not dict_question_multimedia.keys().__contains__(
                        q.pk):
                        lst_options = dict_question_option[q.pk]
                        for lst_option in lst_options:
                            str_survey_questions += str(lst_option) + "\n"
                    str_survey_questions += "\n"
                    if str(q.id_type_question.type_question).__contains__("date"):
                        str_survey_questions += "R:DD/MM/YYYY"
                    elif str(q.id_type_question.type_question).__contains__("intro"):
                        str_survey_questions += "\t"
                    else:
                        str_survey_questions += "R:"
                    str_survey_questions += "\n\n\n"

        str_survey_questions += "\n-----------------------------------"
    questions_with_pk = list()
    for q in new_questions:
        questions_with_pk.append(q.pk)
    new_dict_question_multimedia = {str(key): value for key, value in dict_question_multimedia.items()}
    new_dict_question_option = {str(key): value for key, value in dict_question_option.items()}
    new_dict_videos = {str(key): value for key, value in dict_videos.items()}
    new_dict_audios = {str(key): value for key, value in dict_audios.items()}
    context_survey_file = {
        'survey': survey.pk,
        'survey_name': survey.name_of_survey,
        'allow_prefilled_file_with_answers': bool(allow_prefilled_file_with_answers),
        'respondent': respondent.id_of_respondent,
        'questions_hotlinks': dict_question_hotlink,
        'questions': questions_with_pk,
        'str_survey_questions': str_survey_questions,
        'number_of_pages': int(number_of_questions),
        'question_multimedia': new_dict_question_multimedia,
        'question_option': new_dict_question_option,
        'user': user.pk,
        'the_videos': new_dict_videos,
        'the_audios': new_dict_audios,
        'has_intro': has_intro,
        'selected_view': selected_view
    }
    request.session['context_survey_file'] = context_survey_file
    request.session['first_time_on_first_page'] = True
    context = formulate_context(request, context_survey_file, 1, None, True)
    template = loader.get_template('surveyFile_new_version.html')
    return HttpResponse(template.render(context, request))


def formulate_context(request, context_survey_file, number_of_page, action, first_time_on_first_page=False):
    """
    Function that considers if the user wants to go to the previous or to the next question, gathering the information needed to load that question
    """
    if not first_time_on_first_page:
        request.session['first_time_on_first_page'] = False
    questions = context_survey_file["questions"]
    context = copy.deepcopy(context_survey_file)
    context.pop('user')
    new_number_of_page = 0
    if action is not None:
        if action in words_next.values() or action in words_start_survey.values() and number_of_page < int(
                context['number_of_pages']):
            new_number_of_page = context['number_of_page'] = number_of_page + 1
        elif action in words_go_to_first_page.values() and number_of_page == int(
                context['number_of_pages']):
            new_number_of_page = context['number_of_page'] = 1
        elif action in words_back.values() and number_of_page > 1:
            new_number_of_page = context['number_of_page'] = number_of_page - 1
        elif action in words_go_to_last_question.values() and number_of_page == 1:
            new_number_of_page = context['number_of_page'] = context['number_of_pages']
    else:
        new_number_of_page = int(number_of_page)
    question = questions[new_number_of_page - 1]
    the_question = Question.objects.filter(pk=question).first()
    group_name = the_question.id_group.group_name
    context['q'] = the_question
    context['group_name'] = group_name
    context['number_of_page'] = new_number_of_page
    context['first_time_on_first_page'] = request.session.get('first_time_on_first_page', False)
    d_q_a = request.session.get('dict_questions_answers')
    if the_question.id_type_question.type_question == "date" or the_question.id_type_question.type_question == "video with date" or the_question.id_type_question.type_question == "audio with date":
        context['question'] = d_q_a[str(question)].split("/")
    else:
        context['question'] = d_q_a[str(question)]
    return context


def update_view(request):
    number_of_page = request.POST.get('actual_number_of_page')
    c_s_f = request.session.get('context_survey_file')
    if "boxes_for_view" in request.POST.keys():
        boxes_selected = request.POST.getlist('boxes_for_view')
        selected_view = define_selected_view(boxes_selected)
    else:
        selected_view = "3"
    c_s_f["selected_view"] = selected_view
    request.session['context_survey_file'] = c_s_f
    context = formulate_context(request=request, context_survey_file=c_s_f, number_of_page=number_of_page, action=None)
    template = loader.get_template('surveyFile_new_version.html')
    return HttpResponse(template.render(context, request))

def get_recommendations(request):
    context = {}
    template = loader.get_template('recommendations_for_building_accessible_surveys.html')
    return HttpResponse(template.render(context, request))
def render_surveyFile(request):
    """
    Function responsible for loading each of the survey questions, one per page
    """
    number_of_page = int(request.POST.get('actual_number_of_page'))
    lst_keys_req = list(request.POST.keys())
    c_s_f = request.session.get('context_survey_file')
    action = submit_file_answers = None
    if "action" in lst_keys_req:
        action = request.POST.get('action')
    elif "submit_file_answers" in lst_keys_req:
        submit_file_answers = request.POST.get('submit_file_answers')
    user = c_s_f['user']
    the_user = User.objects.filter(pk=user).first()
    survey_pk = c_s_f['survey']
    survey = Survey.objects.filter(pk=int(survey_pk)).first()
    respondent = c_s_f['respondent']
    lst_keys_req_files = list(request.FILES.keys())
    request.session['context_survey_file'] = c_s_f
    if "survey_file" in lst_keys_req_files and not request.FILES['survey_file'] == '':
        survey_file = request.FILES['survey_file']
        all_saved, context = process_survey_file(request, survey_file)
        if all_saved and not context == "":
            request.session.flush()
            template = loader.get_template('result_template.html')
            return HttpResponse(template.render(context, request))
        elif not all_saved and context == "incorrect date":
            context = {}
            template = loader.get_template('incorrect_date.html')
            return HttpResponse(template.render(context, request))
        elif not all_saved and context == "incorrect questions order":
            context = {}
            template = loader.get_template('incorrect_questions_order.html')
            return HttpResponse(template.render(context, request))
        elif not all_saved and context == "incorrect file type":
            context = {}
            template = loader.get_template('incorrect_file_type_for_respondents.html')
            return HttpResponse(template.render(context, request))
        elif not all_saved and context == "mandatory response non given":
            context = {}
            template = loader.get_template('mandatory_response_non_given.html')
            return HttpResponse(template.render(context, request))
    elif "survey_file" not in lst_keys_req_files and submit_file_answers in words_submit_file.values():
        context = {}
        template = loader.get_template('no_uploaded_response_file.html')
        return HttpResponse(template.render(context, request))
    else:
        all_correctly_saved, error_explanation = process_response(request, request.POST)
        if all_correctly_saved and error_explanation == "":
            if "submit_answers" in lst_keys_req:
                selected_view = c_s_f['selected_view']
                context = save_answers_to_db(request, the_user, survey, respondent, selected_view)
                if context == 'incorrect questions order':
                    context = {}
                    template = loader.get_template('incorrect_questions_order.html')
                    return HttpResponse(template.render(context, request))
                else:
                    request.session.flush()
                    template = loader.get_template('result_template.html')
                    return HttpResponse(template.render(context, request))
            else:
                c_s_f = request.session.get('context_survey_file')
                context = formulate_context(request, c_s_f, number_of_page, action)
                template = loader.get_template('surveyFile_new_version.html')
                return HttpResponse(template.render(context, request))

        elif not all_correctly_saved and error_explanation == "incorrect answer format":
            context = {}
            template = loader.get_template('incorrect_answer_format.html')
            return HttpResponse(template.render(context, request))

        elif not all_correctly_saved and error_explanation == "incorrect date":
            context = {}
            template = loader.get_template('incorrect_date.html')
            return HttpResponse(template.render(context, request))


def login(request):
    """
    render login page
    """
    show_message = False
    message = ""
    context = {"show_message": show_message, "message": message}
    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


def process_login(request):
    """
    if login fails the user is redirected to a page where the user is informed that the login was unsuccessful and is
    given the opportunity to log in again
    on the other hand, if the login is successful, the user is taken to a page where can consult the answers given to the surveys that has built
    """
    email = request.POST['email']
    password = request.POST['password']
    if User.objects.filter(email=email, password=password).values().count() == 0:
        context = {}
        template = loader.get_template('login_failed.html')
        return HttpResponse(template.render(context, request))
    else:
        user = User.objects.filter(email=email, password=password).first()
        dsa = Display_Answers.objects.filter(id_user=user).order_by('id_survey', 'id_respondent')
        unique_surveys_ids = set(dsa.values_list('id_survey', flat=True).distinct())
        unique_surveys_list = Survey.objects.filter(pk__in=unique_surveys_ids)
        context = {"display_answers": dsa, "unique_surveys_list": unique_surveys_list}
        template = loader.get_template('display_answers.html')
        return HttpResponse(template.render(context, request))


def define_respondent(id_of_respondent):
    """
    function that ensures that each respondent has an id that corresponds only to them
    """
    if Respondent.objects.all().count() == 0:
        respondent = Respondent(id_of_respondent=id_of_respondent)
        respondent.save()
        return respondent
    else:
        if Respondent.objects.filter(id_of_respondent=id_of_respondent).values().count() == 0:
            respondent = Respondent(id_of_respondent=id_of_respondent)
            respondent.save()
            return respondent
        else:
            id_of_respondent = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            define_respondent(id_of_respondent)


def process_response(request, query_dict):
    """
    save temporarily the responses given to the survey
    """
    error_explanation = ""
    c_s_f = request.session.get('context_survey_file')
    key_not_there = False
    for key in query_dict.keys():
        if not key == "csrfmiddlewaretoken" and not key == "actual_number_of_page" and not key == "action" and not key == "survey_file":
            key_not_there = True
    if not key_not_there:
        return True, error_explanation
    elif bool(c_s_f["has_intro"]) and int(request.POST.get('actual_number_of_page')) == 1:
        return True, error_explanation
    answer_to_db = ""
    d_nq_qpk = request.session.get('dict_numberquestion_questionpk')
    d_q_a = request.session.get('dict_questions_answers')
    for key, values in query_dict.lists():
        if not key == "csrfmiddlewaretoken" and not key == "actual_number_of_page" and not key == "action" and not key == "survey_file":
            counter = 0
            quest_pk = d_nq_qpk[str(key)]
            question = Question.objects.filter(pk=quest_pk).first()
            for value in values:
                if len(values) > 1 and question.id_type_question.type_question == "date" or question.id_type_question.type_question == "video with date" or question.id_type_question.type_question == "audio with date":
                    if counter < 2:
                        answer_to_db += str(value).strip() + "/"
                        counter += 1
                    else:
                        answer_to_db += str(value).strip()
                        counter = 0
                        is_valid_date = validate_date(answer_to_db, question.mandatory)
                        if not is_valid_date and not validate_date(d_q_a[str(quest_pk)], question.mandatory):
                            error_explanation = "incorrect date"
                            return False, error_explanation
                else:
                    if counter < len(values) - 1:
                        answer_to_db += str(value).strip() + ";"
                        counter += 1
                    else:
                        answer_to_db += str(value).strip()
                        counter = 0
            if not answer_to_db == '' and not answer_to_db == ' ' and not answer_to_db == '0/0/0000':
                d_q_a[str(quest_pk)] = answer_to_db
                request.session['dict_questions_answers'] = d_q_a
            return True, error_explanation
    error_explanation = "incorrect answer format"
    return False, error_explanation


def save_answers_to_db(request, user, survey, respondent, selected_view):
    """
    Saves answers to the database after the survey has been submitted
    """
    list_id_question_answer = list()
    counter = 1
    d_q_a = request.session.get('dict_questions_answers')
    d_nq_qpk = request.session.get('dict_numberquestion_questionpk')
    the_respondent = Respondent.objects.filter(id_of_respondent=respondent).first()
    intro = None
    for quest_nr, answer_to_db in d_q_a.items():
        quest_pk = d_nq_qpk[str(counter)]
        if quest_nr == quest_pk:
            question = Question.objects.filter(pk=int(quest_pk)).first()
            counter += 1
        else:
            return "incorrect questions order"
        if question.id_group.group_name not in words_for_group_intro.values():
            if Answer.objects.all().count() == 0:
                the_answer = Answer(answer=answer_to_db)
                the_answer.save()
            else:
                if Answer.objects.filter(answer=answer_to_db).values().count() == 0:
                    the_answer = Answer(answer=answer_to_db)
                    the_answer.save()
                else:
                    the_answer = Answer.objects.filter(answer=answer_to_db).first()
            if Display_Answers.objects.all().count() == 0:
                display_answer = Display_Answers(id_survey=survey, id_user=user, id_question=question,
                                                 id_answer=the_answer, id_respondent=the_respondent)
                display_answer.save()
            else:
                if Display_Answers.objects.filter(id_survey=survey, id_user=user, id_question=question,
                                                  id_respondent=the_respondent).values().count() > 0:
                    display_answer = Display_Answers.objects.filter(id_survey=survey, id_user=user,
                                                                    id_question=question,
                                                                    id_respondent=the_respondent).first()
                    display_answer.id_answer = the_answer
                    display_answer.save()
                elif Display_Answers.objects.filter(id_survey=survey, id_user=user, id_question=question,
                                                    id_answer=the_answer,
                                                    id_respondent=the_respondent).values().count() == 0:
                    display_answer = Display_Answers(id_survey=survey, id_user=user, id_question=question,
                                                     id_answer=the_answer,
                                                     id_respondent=the_respondent)
                    display_answer.save()
            if User_Answer.objects.all().count() == 0:
                user_answer = User_Answer(id_user=user, id_answer=the_answer)
                user_answer.save()
            else:
                if User_Answer.objects.filter(id_user=user, id_answer=the_answer).values().count() == 0:
                    user_answer = User_Answer(id_user=user, id_answer=the_answer)
                    user_answer.save()
            if Question_Answer.objects.all().count() == 0:
                question_answer = Question_Answer(id_question=question, id_answer=the_answer)
                question_answer.save()
            else:
                if Question_Answer.objects.filter(id_question=question, id_answer=the_answer).values().count() == 0:
                    question_answer = Question_Answer(id_question=question, id_answer=the_answer)
                    question_answer.save()
                    list_id_question_answer.append(question_answer.pk)
                else:
                    question_answer = Question_Answer.objects.filter(id_question=question, id_answer=the_answer).first()
                    id_question_answer = question_answer.id
                    list_id_question_answer.append(id_question_answer)
        else:
            intro = question
    display_answers = Display_Answers.objects.all()
    questions_answers = Question_Answer.objects.filter(pk__in=list_id_question_answer)
    if intro is not None:
        str_to_return = "".join("\t" + survey.name_of_survey + "\t\n\n" + intro.question + "\n\n\n")
    else:
        str_to_return = "".join("\t" + survey.name_of_survey + "\t\n\n")
    for qa in questions_answers:
        # if str(qa.id_question.id_group.group_name) not in words_for_group_intro.values():
        str_to_return += qa.id_question.question + " " + qa.id_answer.answer + "\n"
    context = {
        'text_to_return': str_to_return,
        'survey_name': survey.name_of_survey,
        'selected_view': selected_view
    }
    return context


def process_survey_file(request, survey_file):
    """
    processes the file with the answers to the survey after its submission
    """
    context = ""
    if "survey_file" not in request.FILES.keys():
        context = 'no uploaded response file'
        return False, context
    c_s_f = request.session.get('context_survey_file')
    respondent = c_s_f["respondent"]
    the_respondent = Respondent.objects.filter(id_of_respondent=respondent).first()
    survey_pk = c_s_f["survey"]
    survey = Survey.objects.filter(pk=int(survey_pk)).first()
    user = c_s_f["user"]
    the_user = User.objects.filter(pk=user).first()
    dict_quest_ans = dict()
    list_id_question_answer = list()
    lst_temp_questions = list()
    file_extension, file_content = loadUploadedFileWithQuestions(survey_file)
    intro = retrieve_intro(c_s_f["questions"])
    if file_content and file_extension.__contains__(".txt"):
        the_file_content = str(file_content).strip().split(sep="\n")
        the_new_file_content = list()
        for content in the_file_content:
            if content.__contains__("Q: \t") or content.__contains__("R:"):
                the_new_file_content.append(content)

        counter = 1
        for line in the_new_file_content:
            if line.__contains__("Q: \t"):
                _, q = line.strip().split(" \t", 1)
                if q.__contains__("*"):
                    q = str(q).replace("*", "")
                lst_temp_questions.append(q)

            elif line.__contains__("R:"):
                _, a = line.strip().split("R:", 1)
                question = c_s_f["questions"][counter]
                the_question = Question.objects.filter(pk=question).first()
                if the_question.question == lst_temp_questions[-1]:
                    is_there = False
                    for key, value in words_date.items():
                        if value in str(the_question.question).lower():
                            is_valid = validate_date(str(a).strip(), the_question.mandatory)
                            if is_valid:
                                is_there = True
                                dict_quest_ans[the_question] = a
                                counter += 1
                            else:
                                context = "incorrect date"
                                return False, context

                    for key, value in words_day.items():
                        if value in str(the_question.question).lower():
                            is_valid = validate_date(str(a).strip(), the_question.mandatory)
                            if is_valid:
                                is_there = True
                                dict_quest_ans[the_question] = a
                                counter += 1
                            else:
                                context = "incorrect date"
                                return False, context
                    if not is_there:
                        dict_quest_ans[the_question] = a
                        counter += 1
                else:
                    context = "incorrect questions order"
                    return False, context
    else:
        context = "incorrect file type"
        return False, context
    for question, ans in dict_quest_ans.items():
        if question.mandatory and ans == "" or ans == " ":
            return False, "mandatory response non given"
        if Answer.objects.all().count() == 0:
            the_answer = Answer(answer=ans)
            the_answer.save()
        else:
            if Answer.objects.filter(answer=ans).values().count() == 0:
                the_answer = Answer(answer=ans)
                the_answer.save()
            else:
                the_answer = Answer.objects.filter(answer=ans).first()

        if Display_Answers.objects.all().count() == 0:
            display_answer = Display_Answers(id_survey=survey, id_user=the_user, id_question=question,
                                             id_answer=the_answer, id_respondent=the_respondent)
            display_answer.save()
        else:
            if Display_Answers.objects.filter(id_survey=survey, id_user=the_user, id_question=question,
                                              id_respondent=the_respondent).values().count() > 0:
                display_answer = Display_Answers.objects.filter(id_survey=survey, id_user=the_user,
                                                                id_question=question,
                                                                id_respondent=the_respondent).first()
                display_answer.id_answer = the_answer
                display_answer.save()
            elif Display_Answers.objects.filter(id_survey=survey, id_user=the_user, id_question=question,
                                                id_answer=the_answer,
                                                id_respondent=the_respondent).values().count() == 0:
                display_answer = Display_Answers(id_survey=survey, id_user=the_user, id_question=question,
                                                 id_answer=the_answer,
                                                 id_respondent=the_respondent)
                display_answer.save()
        if User_Answer.objects.all().count() == 0:
            user_answer = User_Answer(id_user=the_user, id_answer=the_answer)
            user_answer.save()
        else:
            if User_Answer.objects.filter(id_user=the_user, id_answer=the_answer).values().count() == 0:
                user_answer = User_Answer(id_user=the_user, id_answer=the_answer)
                user_answer.save()

        if Question_Answer.objects.all().count() == 0:
            question_answer = Question_Answer(id_question=question, id_answer=the_answer)
            question_answer.save()
        else:
            if Question_Answer.objects.filter(id_question=question, id_answer=the_answer).values().count() == 0:
                question_answer = Question_Answer(id_question=question, id_answer=the_answer)
                question_answer.save()
                list_id_question_answer.append(question_answer.pk)
            else:
                question_answer = Question_Answer.objects.filter(id_question=question, id_answer=the_answer).first()
                id_question_answer = question_answer.id
                list_id_question_answer.append(id_question_answer)
    questions_answers = Question_Answer.objects.filter(pk__in=list_id_question_answer)
    if intro is not None:
        str_to_return = "".join("\t" + survey.name_of_survey + "\t\n\n" + intro.question + "\n\n\n")
    else:
        str_to_return = "".join("\t" + survey.name_of_survey + "\t\n\n")
    for qa in questions_answers:
        # if str(qa.id_question.id_group.group_name) not in words_for_group_intro.values():
        str_to_return += qa.id_question.question + " " + qa.id_answer.answer + "\n"
    context = {
        'text_to_return': str_to_return,
        'survey_name': survey.name_of_survey,
        'selected_view': c_s_f['selected_view']
    }
    return True, context


def retrieve_intro(questions: list):
    for q in questions:
        quest = Question.objects.filter(pk=q).first()
        if str(quest.id_group.group_name) in words_for_group_intro.values():
            return quest
    return None
