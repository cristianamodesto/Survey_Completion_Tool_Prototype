const backgroundAndTextColor = ["background_orange_text_black","background_yellow_text_blue","background_yellow_text_black",
"background_green_text_black","background_blue_text_yellow","background_blue_text_white","background_black_text_yellow",
"background_black_text_green","background_black_text_white","background_white_text_blue","background_white_text_black"]


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

function download_answers(answers, survey_name){
    console.log(answers)
    console.log(survey_name)
    let file_name = ""
    if (survey_name==""){
        file_name = "answers.txt"
    }else{

    }
    file_name = survey_name+".txt"
    /*let the_answers = answers.split("    ")
    console.log(the_answers)
    let final_answer = ""
    for (let i=0; i<the_answers.length;i++){
       final_answer += final_answer.concat(answers[0]+"\n")
    }*/
    let element = document.createElement('a');
    element.setAttribute('href',
        'data:text/plain;charset=utf-8, '
        + encodeURIComponent(answers.toString()));
    element.setAttribute('download', file_name);
    document.body.appendChild(element);
    element.click();

    document.body.removeChild(element);
}
