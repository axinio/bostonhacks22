var dict = new Object();
function string2array(data){
    var arr = [];
    var str3 = data;
    while(str3.includes(";")){
        var str1 = str3.substring(0,data.indexOf(";"));
        arr.push(str1);
        var str3 = str3.substring(str3.indexOf(";")+1);
    }
    return arr;
}

function getData(form) {
    var formData = new FormData(form);
    var arr=[];
  
    for (var pair of formData.entries()) {
    if(pair[0]=="classes" && pair[1].includes(";")){
        dict["classes"] = string2array(pair[1])
    }
    else if(pair[0]!="hub"){
        dict[pair[0]] = pair[1];
    }
    else{
        arr.push(pair[1]);
    }
      
    }
    dict["hub"] = arr;
    console.log(dict);
  }
  
  document.getElementById("myForm").addEventListener("submit", function (e) {
    e.preventDefault();
    getData(e.target);
  });
  
const myJSON = JSON.stringify(dict);
let xhr = new XMLHttpRequest();
xhr.open("POST", "");
xhr.setRequestHeader("Accept", "application/json");
xhr.setRequestHeader("Content-Type", "application/json");

xhr.onreadystatechange = function () {
  if (xhr.readyState === 4) {
    console.log(xhr.status);
    console.log(xhr.responseText);
  }};
  xhr.send(myJSON);