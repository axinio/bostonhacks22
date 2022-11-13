var dict = new Object();
function string2array(data){
  var arr = [];
  var str3 = data.split(" ").join("");
  while(str3.includes(",")){
      var str1 = str3.substring(0,data.indexOf(","));
      arr.push(str1);
      str3 = str3.substring(str3.indexOf(",")+1);
  }
  if(str3.length>0){
      arr.push(str3);
  }
  return arr;
}

function getData(form) {
    var formData = new FormData(form);
    var arr=[];
  
    for (var pair of formData.entries()) {
    if(pair[0]=="classes" && pair[1].includes(",")){
        dict["classes"] = string2array(pair[1])
    }
    else if(pair[0]=="taken_classes" && pair[1].includes(",")){
        dict["taken_classes"] = string2array(pair[1])
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
    sendRequest()
  
  });
  document.getElementById("myClear").addEventListener("clear", function(e) {
    e.preventDefault;
    clearFields();
  })
  
function clearFields(){
  const pninput = document.getElementById("number");
  pninput.value = "";
  const m1input = document.getElementById("majordesired");
  m1input.value = "";
  const h1input = document.getElementById("hubdesired");
  h1input.value = "";
  const m2input = document.getElementById("major");
  m2input.value = "";
  const cinput = document.getElementById("classes");
  cinput.value = "";
  const c2input = docume.getElementById("taken_classes")
  c2input.value = "";
  let elements = document.getElementsByName("hub");
  for(let i = 0; i< elements.length;i++){
      elements[i].checked = false;
  }
}

function sendRequest(){
  const myJSON = JSON.stringify(dict);
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:5000/api");
  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("Access-Control-Allow-Private-Network", "true");

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      console.log(xhr.status);
      console.log(xhr.responseText);
    }};
    xhr.send(myJSON);
    /* DEBUG USE, DOWNLOADS JSON ONTO COMPUTER WHEN SUBMIT IS CLICKED
    let dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(myJSON);
    let exportFileDefaultName = 'data.json';

    let linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click()
    */
}