
const backgroundAndTextColor = ["background_orange_text_black","background_yellow_text_blue","background_yellow_text_black",
"background_green_text_black","background_blue_text_yellow","background_blue_text_white","background_black_text_yellow",
"background_black_text_green","background_black_text_white","background_white_text_blue","background_white_text_black"]

const text = "pergunta_: \ntipo_: \nopção_: \nobrigatório_: \nmultimédia_: \ngrupo_: \n \n"
    + "pergunta_: \ntipo_: \nopção_: \nobrigatório_: \nmultimédia_: \ngrupo_: \n \n"
    + "pergunta_: \ntipo_: \nopção_: \nobrigatório_: \nmultimédia_: \ngrupo_: \n \n";

const json = "[ \n" +
    "{\"pergunta_\": \"\", \n" +
    "\"tipo_\":\"\", \n" +
    "\"opção_\":\"\", \n" +
    "\"obrigatório_\":\"\", \n" +
    "\"multimédia_\":\"\", \n" +
    "\"grupo_\":\"\"}, \n" +
    "\n" +
    "{\"pergunta_\": \"\", \n" +
    "\"tipo_\":\"\", \n" +
    "\"opção_\":\"\", \n" +
    "\"obrigatório_\":\"\", \n" +
    "\"multimédia_\":\"\", \n" +
    "\"grupo_\":\"\"}, \n" +
    "\n" +
    "{\"pergunta_\": \"\", \n" +
    "\"tipo_\":\"\", \n" +
    "\"opção_\":\"\", \n" +
    "\"obrigatório_\":\"\", \n" +
    "\"multimédia_\":\"\", \n" +
    "\"grupo_\":\"\"} \n" +
    "]";

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
}*/
