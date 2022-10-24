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
})
return;
}
})
}