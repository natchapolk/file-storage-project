function handleLogout(){
window.localStorage.removeItem("DES424");
window.location.href = "index.html";
}

function handleUploadFile(){
var data = new FormData()
data.append('files', document.getElementById("file").files[0]);
var path = "/file";
var option = {
method: 'POST',
headers: {
'Authorization': 'Bearer '+window.localStorage.getItem("DES424")
},
body: data
}
fetch(path, option)
.then(function(response){
if (response.status == 201){
response.json().then(function(json){
alert(json['result']);
document.getElementById("file").value = null;
showContent();
})
return;
}
})
}

function showContent(){
fetch("/file", {
headers: {
'Content-Type': 'application/json',
'Authorization': 'Bearer '+window.localStorage.getItem("DES424")
},
})
.then(function(response){
if (response.status == 403){
handleLogout();
return;
}
response.json().then(function(json){
document.getElementById("file_list").innerHTML = "";
var list = document.createElement("ul");
for (var i=0;i<json.length;i++){
var div = document.createElement("div");
div.innerHTML = json[i][1]
var buttonDiv = document.createElement("div");
var button = document.createElement("button");
button.setAttribute("id", json[i][0]);
button.setAttribute("onClick", "handleDownload("+json[i][0]+")");
button.innerHTML = "download";
buttonDiv.appendChild(button);
var button = document.createElement("button");
button.setAttribute("id", json[i][0]);
button.setAttribute("onClick", "handleDeleteFile("+json[i][0]+")");
button.innerHTML = "Remove";
buttonDiv.appendChild(button);
div.appendChild(buttonDiv);
list.appendChild(div);
}

document.getElementById("file_list").appendChild(list);
})
})
}

function handleDownload(id){
window.location.href = "/file/"+id;
}

function handleDeleteFile(id){
fetch("/file/"+id, {
method: "DELETE",
headers: {
"Content-Type": "application/json",
"Authorization": "Bearer "+window.localStorage.getItem("DES424")
}
})
.then(function(response){
if (response.status == 403){
handleLogout();
return;
}
response.json().then(function(json){
alert(json['result']);
showContent();
})
})
}