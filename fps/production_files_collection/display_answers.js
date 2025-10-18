const backgroundAndTextColor = ["background_orange_text_black", "background_yellow_text_blue", "background_yellow_text_black",
"background_green_text_black","background_blue_text_yellow","background_blue_text_white","background_black_text_yellow",
"background_black_text_green","background_black_text_white","background_white_text_blue","background_white_text_black"]

const tableBorderColor = ["table_border_black", "table_border_blue", "table_border_yellow", "table_border_white", "table_border_green"]

function changeBackgroundColor(){//possibilidade de alterar a cor do texto e a do background, por via de color pickers
    let backgroundColor = document.getElementById("background_color").value;
    console.log("background_color "+background_color);
    document.body.style.backgroundColor = backgroundColor;

}
function changeTextColor(){//possibilidade de alterar a cor do texto e a do background, por via de color pickers
    let textColor = document.getElementById("text_color").value;
    document.body.style.color = textColor;
    let tables = document.getElementsByTagName("table")
    for (let i=0;i<tables.length;i++){
        tables[i].style.borderColor=""
        tables[i].style.borderColor="1px solid "+textColor
    }
}

function changeBackgroundAndTextColorBySelect(){//possibilidade de alterar a cor do texto e a do background mantendo o contraste adequado com o mesmo, por via de um select
    let selectBackgroundAndTextColor = document.getElementById("selectBackgroundAndTextColor");
    let tables = document.getElementsByTagName("table")
    let idx= selectBackgroundAndTextColor.selectedIndex;
    let selectedClass = backgroundAndTextColor[idx];
    for (let i=0;i<tables.length;i++){
        tables[i].className=''
        tables[i].style.backgroundColor=''
        tables[i].style.color=''
    }


    for (let i=0;i<tables.length;i++){
        console.log("for in select")
        console.log(selectedClass.includes("text_black"))
        if (selectedClass.includes("text_black")){
            tables[i].className=tableBorderColor[0]
        }else if (selectedClass.includes("text_blue")){
            tables[i].className=tableBorderColor[1]
        }else if (selectedClass.includes("text_yellow")){
            tables[i].className=tableBorderColor[2]
        }else if (selectedClass.includes("text_white")){
            tables[i].className=tableBorderColor[3]
        }else if (selectedClass.includes("text_green")){
            tables[i].className=tableBorderColor[4]
        }else{
            tables[i].className=tableBorderColor[0]
        }
        console.log(tables[i])
    }

    document.body.className='';
    document.body.style.backgroundColor = '';
    document.body.style.color = '';
    console.log("selectedClass" + selectedClass);
    document.body.classList.add(selectedClass);



}
