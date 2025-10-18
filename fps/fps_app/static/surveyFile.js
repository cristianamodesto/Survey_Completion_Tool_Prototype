const backgroundAndTextColor = ["background_orange_text_black","background_yellow_text_blue","background_yellow_text_black",
"background_green_text_black","background_blue_text_yellow","background_blue_text_white","background_black_text_yellow",
"background_black_text_green","background_black_text_white","background_white_text_blue","background_white_text_black"]


function construct_date_inputs(){
    let day_obj = document.getElementById("day")
    let day = day_obj.value
    let month_obj = document.getElementById("month")
    let month = month_obj.value
    let year_obj = document.getElementById("year")
    let year = year_obj.value

    for (let i=1;i<=31;i++) {
        let option = document.createElement("option")
        option.value = i.toString()
        option.text = i.toString()
        day_obj.appendChild(option)
    }
    for (let i=1;i<=12;i++) {
        let option = document.createElement("option")
        option.value = i.toString()
        option.text = i.toString()
        month_obj.appendChild(option)
    }
    for (let i=1950;i<=2024;i++) {
        let option = document.createElement("option")
        option.value = i.toString()
        option.text = i.toString()
        year_obj.appendChild(option)
    }

    let v_day_obj = document.getElementById("v_day")
    let v_day = v_day_obj.value
    let v_month_obj = document.getElementById("v_month")
    let v_month = v_month_obj.value
    let v_year_obj = document.getElementById("v_year")
    let v_year = v_year_obj.value

    for (let i=1;i<=31;i++) {
        let option = document.createElement("option")
        option.value = i.toString()
        option.text = i.toString()
        v_day_obj.appendChild(option)
    }
    for (let i=1;i<=12;i++) {
        let option = document.createElement("option")
        option.value = i.toString()
        option.text = i.toString()
        v_month_obj.appendChild(option)
    }
    for (let i=1950;i<=2024;i++) {
        let option = document.createElement("option")
        option.value = i.toString()
        option.text = i.toString()
        v_year_obj.appendChild(option)
    }

    let a_day_obj = document.getElementById("a_day")
    let a_day = a_day_obj.value
    let a_month_obj = document.getElementById("a_month")
    let a_month = a_month_obj.value
    let a_year_obj = document.getElementById("a_year")
    let a_year = a_year_obj.value

    for (let i=1;i<=31;i++) {
        let option = document.createElement("option")
        option.value = i.toString()
        option.text = i.toString()
        a_day_obj.appendChild(option)
    }
    for (let i=1;i<=12;i++) {
        let option = document.createElement("option")
        option.value = i.toString()
        option.text = i.toString()
        a_month_obj.appendChild(option)
    }
    for (let i=1950;i<=2024;i++) {
        let option = document.createElement("option")
        option.value = i.toString()
        option.text = i.toString()
        a_year_obj.appendChild(option)
    }
}


function on_date_change() {
    let day_obj = document.getElementById("day_js")
    let day = day_obj.value

    let v_day_obj = document.getElementById("v_day_js")
    let v_day = v_day_obj.value

    let a_day_obj = document.getElementById("a_day_js")
    let a_day = a_day_obj.value

    let month_obj = document.getElementById("month_js")
    let month = month_obj.value

    let v_month_obj = document.getElementById("v_month_js")
    let v_month = v_month_obj.value

    let a_month_obj = document.getElementById("a_month_js")
    let a_month = a_month_obj.value

    let year_obj = document.getElementById("year_js")
    let year = year_obj.value

    let v_year_obj = document.getElementById("v_year_js")
    let v_year = v_year_obj.value

    let a_year_obj = document.getElementById("a_year_js")
    let a_year = a_year_obj.value

    if (!is_leap_year(year) && month === "2" && day === "29") {
        send_message("O ano " + year + " não é bissexto. Pelo que, não ocorreu o dia 29 de fevereiro neste ano.")
        year_obj.value = 1950
        day_obj.value = 1

    }else if (!is_leap_year(v_year) && v_month === "2" && v_day === "29"){
        send_message("O ano " + v_year + " não é bissexto. Pelo que, não ocorreu o dia 29 de fevereiro neste ano.")
        v_year_obj.value = 1950
        v_day_obj.value = 1

    }else if (!is_leap_year(a_year) && a_month === "2" && a_day === "29"){
        send_message("O ano " + v_year + " não é bissexto. Pelo que, não ocorreu o dia 29 de fevereiro neste ano.")
        v_year_obj.value = 1950
        v_day_obj.value = 1

    } else if (month==="2" && day>29) {
        send_message("Dia inválido para o mês de fevereiro.")
        day_obj.value = 1
    } else if (v_month==="2" && v_day>29){
        send_message("Dia inválido para o mês de fevereiro.")
        v_day_obj.value=1
    } else if (a_month==="2" && a_day>29){
        send_message("Dia inválido para o mês de fevereiro.")
        a_day_obj.value=1
    } else if (month==="4" || month==="6" || month==="9" || month==="11"){
        let error_message = ""
        if (day>30){
            switch (month) {
                case "4":
                    error_message = "Dia inválido para o mês de abril."
                    break;
                case "6":
                    error_message = "Dia inválido para o mês de junho."
                    break;
                case "9":
                    error_message = "Dia inválido para o mês de setembro."
                    break;
                case "11":
                    error_message = "Dia inválido para o mês de novembro."
                    break;
            }
            send_message(error_message)
            month_obj.value=1
            day_obj.value=1
        }


    } else if (v_month==="4" || v_month==="6" || v_month==="9" || v_month==="11"){
        let error_message = ""
        if (v_day>30){
            switch (v_month) {
                case "4":
                    error_message = "Dia inválido para o mês de abril."
                    break;
                case "6":
                    error_message = "Dia inválido para o mês de junho."
                    break;
                case "9":
                    error_message = "Dia inválido para o mês de setembro."
                    break;
                case "11":
                    error_message = "Dia inválido para o mês de novembro."
                    break;
            }
            send_message(error_message)
            v_month_obj.value=1
            v_day_obj.value=1
        }

    } else if (a_month==="4" || a_month==="6" || a_month==="9" || a_month==="11"){
        let error_message = ""
        if (a_day>30){
            switch (v_month) {
                case "4":
                    error_message = "Dia inválido para o mês de abril."
                    break;
                case "6":
                    error_message = "Dia inválido para o mês de junho."
                    break;
                case "9":
                    error_message = "Dia inválido para o mês de setembro."
                    break;
                case "11":
                    error_message = "Dia inválido para o mês de novembro."
                    break;
            }
            send_message(error_message)
            a_month_obj.value=1
            a_day_obj.value=1
        }


    }

}

function send_message(message_to_send){
    let div_of_message = document.getElementById("alert_message")
    let btn_to_close = document.getElementById("close_btn")
    btn_to_close.style.display="block"
    div_of_message.style.display="block"
    let paragraph_of_message = document.getElementById("error_message")
    paragraph_of_message.textContent=message_to_send
}
function is_leap_year(year){
    return ((year%4==0) && (year%100!=0)) || (year%400==0)
}

function changeBackgroundColor(){//possibilidade de alterar a cor do texto e a do background, por via de color pickers
    var backgroundColor = document.getElementById("background_color").value;
    console.log("background_color "+background_color);
    document.body.style.backgroundColor = backgroundColor;
}
function changeTextColor(){//possibilidade de alterar a cor do texto e a do background, por via de color pickers
    var textColor = document.getElementById("text_color").value;
    var the_question = document.getElementById("the_question")
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


function process_checkboxes(name){
    let checkboxes = document.getElementsByName(name)

    for (let i=0; i<checkboxes.length; i++){
        checkboxes[i].removeAttribute("required")
    }



}
/*
window.onload = function() {
    let select_view = sessionStorage.getItem("view")
    console.log(select_view)
    let selection_item = document.getElementById("view_type_js")
    selection_item.value = select_view
    change_view(select_view)
};
/*
function change_view(select_view){
    if (select_view === "None"){
        select_view = document.getElementById("view_type_js").value
        sessionStorage.setItem("view", select_view)
    }
    let the_videos = document.getElementsByTagName("video")
    let the_color_selection = document.getElementById("backgroundAndTextColor")
    if (select_view === "0"){
        for (let i=0; i<the_videos.length; i++){
            the_videos[i].style.display = "block"
        }
        the_color_selection.style.display = "block"
    } else if (select_view === "1") {
        for (let i=0; i<the_videos.length; i++){
            the_videos[i].style.display = "none"
        }
        the_color_selection.style.display = "block"
    } else if (select_view === "2"){
        the_color_selection.style.display = "none"
        for (let i=0; i<the_videos.length; i++){
            the_videos[i].style.display = "block"
        }
    } else if (select_view === "3"){
        for (let i=0; i<the_videos.length; i++){
            the_videos[i].style.display = "none"
        }
        the_color_selection.style.display = "none"
    }

}

 */
function submit_or_not(event){
    event.preventDefault();
    let btn_to_submit = document.getElementById("hidden_submit_button");
    if (confirm("Tem a certeza que quer submeter as respostas dadas ao questionário?"))
        btn_to_submit.click();


}