
const backgroundAndTextColor = ["background_orange_text_black","background_yellow_text_blue","background_yellow_text_black",
"background_green_text_black","background_blue_text_yellow","background_blue_text_white","background_black_text_yellow",
"background_black_text_green","background_black_text_white","background_white_text_blue","background_white_text_black"]
/*
const text = "introdução_ \ntipo_ \nmultimédia_ \n \n"
    + "pergunta_ \ntipo_ \nopção_ \nobrigatório_ \nmultimédia_ \ngrupo_ \ndica_ \n \n"
    + "pergunta_ \ntipo_ \nopção_ \nobrigatório_ \nmultimédia_ \ngrupo_ \ndica_ \n \n"
    + "pergunta_ \ntipo_ \nopção_ \nobrigatório_ \nmultimédia_ \ngrupo_ \ndica_ \n \n";

const json = "[\n" +
    "{\"introdução_\": \"\", \n"+
    "\"tipo_\":\"\", \n" +
    "\"multimédia_\":\"\"}, \n" +
    "\n" +
    "{\"pergunta_\": \"\", \n" +
    "\"tipo_\":\"\", \n" +
    "\"opção_\":\"\", \n" +
    "\"obrigatório_\":\"\", \n" +
    "\"multimédia_\":\"\", \n" +
    "\"grupo_\":\"\", \n" +
    "\"dica_\":\"\"}, \n" +
    "\n" +
    "{\"pergunta_\": \"\", \n" +
    "\"tipo_\":\"\", \n" +
    "\"opção_\":\"\", \n" +
    "\"obrigatório_\":\"\", \n" +
    "\"multimédia_\":\"\", \n" +
    "\"grupo_\":\"\", \n" +
    "\"dica_\":\"\"}, \n" +
    "\n" +
    "{\"pergunta_\": \"\", \n" +
    "\"tipo_\":\"\", \n" +
    "\"opção_\":\"\", \n" +
    "\"obrigatório_\":\"\", \n" +
    "\"multimédia_\":\"\", \n" +
    "\"grupo_\":\"\", \n" +
    "\"dica_\":\"\"} \n" +
    "]";
*/

function handleUploadFile(){//mecanismo para não se passar a próxima pagina sem antes inserir o txt ou JSON com o Survey
    var submitBtnUpload = document.getElementById("submitBtnUpload")
    var uploadBtnFileWithQuestions = document.getElementById("uploadInputFileWithQuestions")

    if (uploadBtnFileWithQuestions.files.length>0){
        submitBtnUpload.style.visibility='visible'
    }else{
        submitBtnUpload.style.visibility='hidden'
    }
}

function handleUploadFile_answers(){//mecanismo para não se passar a próxima pagina sem antes inserir o txt ou JSON com o Survey
    var submitBtnUpload = document.getElementById("submit_answers")
    var uploadBtnFileWithQuestions = document.getElementById("survey_file")

    if (uploadBtnFileWithQuestions.files.length>0){
        submitBtnUpload.style.visibility='visible'
    }else{
        submitBtnUpload.style.visibility='hidden'
    }
}

function handleInsertLink(){ //mecanismo para não se passar a próxima pagina sem antes inserir o link para o Survey
    var submitBtnUpload = document.getElementById("submitBtnUpload")
    var insertLinkForFileWithQuestions = document.getElementById("insertLinkForFileWithQuestions")
    var url = insertLinkForFileWithQuestions.value
    try {
        new URL(url)
        send_message("A ligação indicada é válida.", "info")
        submitBtnUpload.style.visibility='visible'
    } catch (error) {
        send_message("A ligação indicada não é válida. Por favor, tente novamente.", "error")
        submitBtnUpload.style.visibility='hidden'
    }
}

function send_message(message_to_send, type){
    let div_of_message = document.getElementById("alert_message")
    let btn_close = document.getElementById("close_btn")
    let validate_link = document.getElementById("validate_link")
    if (validate_link.checked===true){
        validate_link.checked=false
    }
    if (type==="error"){
        div_of_message.className = ''
        div_of_message.classList.add("alert")
    }else if (type==="info"){
        div_of_message.className = ''
        div_of_message.classList.add("info")
    }
    btn_close.style.display="block"
    btn_close.classList.add("close_btn")
    div_of_message.style.display="block"
    let paragraph_of_message = document.getElementById("message")
    paragraph_of_message.textContent=message_to_send
}

/* function adjustInput(){
    console.log("adjustInput()")
    var insertLinkForFileWithQuestions = document.getElementById("insertLinkForFileWithQuestions")

    var urlSize = insertLinkForFileWithQuestions.length

    var urlMininumSize = 50

    if(urlSize>urlMininumSize){
        insertLinkForFileWithQuestions.size = urlSize
    }else{
        insertLinkForFileWithQuestions.size = 50
    }
} */

function changeBackgroundColor(){//possibilidade de alterar a cor do texto e a do background, por via de color pickers
    var backgroundColor = document.getElementById("background_color").value;
    console.log("background_color "+background_color);
    document.body.style.backgroundColor = backgroundColor;

}
function changeTextColor(){//possibilidade de alterar a cor do texto e a do background, por via de color pickers
    var textColor = document.getElementById("text_color").value;
    console.log("text_color "+text_color);
    document.body.style.color = textColor;

}

function changeBackgroundAndTextColorBySelect(){//possibilidade de alterar a cor do texto e a do background mantendo o contraste adequado com o mesmo, por via de um select
    var selectBackgroundAndTextColor = document.getElementById("selectBackgroundAndTextColor");
    var idx= selectBackgroundAndTextColor.selectedIndex;
    var selectedClass = backgroundAndTextColor[idx];
    document.body.className='';
    document.body.style.backgroundColor = '';
    document.body.style.color = '';
    console.log("selectedClass" + selectedClass);
    document.body.classList.add(selectedClass);

}

/*
function download_json_file(){
    var file_name = "modelo.json"
    var element = document.createElement('a');
    element.setAttribute('href',
        'data:application/json;charset=utf-8, '
        + encodeURIComponent(json));
    element.setAttribute('download', file_name);
    document.body.appendChild(element);
    element.click();

    document.body.removeChild(element);
}
function download_text_file(){
    var file_name = "modelo.txt"
    var element = document.createElement('a');
    element.setAttribute('href',
        'data:text/plain;charset=utf-8, '
        + encodeURIComponent(text));
    console.log(encodeURIComponent(text))
    element.setAttribute('download', file_name);
    document.body.appendChild(element);
    element.click();

    document.body.removeChild(element);
}

function detectlanguage(){
    var browser_lang = navigator.language || navigator.userlanguage;
    var choose_file = document.getelementbyid("uploadinputfilewithquestions")
    choose_file.lang= browser_lang
    var change_color_text_background = document.getelementbyid("selectbackgroundandtextcolor")
    change_color_text_background.lang= browser_lang
    var change_color_text = document.getelementbyid("text_color")
    change_color_text.lang = browser_lang
    var change_color_background = document.getelementbyid("background_color")
    change_color_background.lang = browser_lang
}
*/
/*
function on_change_view(event){
    event.preventDefault();
    let view_chosen = document.getElementById("view_type_js")
    let view = view_chosen.value
    sessionStorage.setItem("view", view)
    let btn_to_submit = document.getElementById("submit_chosen_survey");
    btn_to_submit.click();
}
*/
