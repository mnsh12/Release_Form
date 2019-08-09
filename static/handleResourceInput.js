var resources = [];
var technologies = [];

function Resource(stage, count) {
  this.stage = stage;
  this.count = count;
}


function addTechnology() {
    console.log("add tech start");
    var items = document.getElementById("technology-items");
    var technology = document.getElementById("tech-req").value;

    if(technologies.indexOf(technology) == -1) {
        technologies.push(technology);
        items.innerHTML += "<span id=" + technology + ">" + technology + "</span>";
    }

    console.log("add tech end");
}


function addResource() {
  var items = document.getElementById("resource-items");
  var jobStage = parseInt(document.getElementById("job-stage").value);
  var resCount = parseInt(document.getElementById("res-count").value);
  
  var oldResCount = parseInt(getResourceCountForJobStage(jobStage));
  if(oldResCount >= 0) {
    resCount += oldResCount;
    if(resCount < 0)
      resCount = 0;
    
    var item = document.getElementById("js" + jobStage);
    item.innerHTML = "JS" + jobStage + ": " + resCount;
  }
  else {
    items.innerHTML += "<span id=js" + jobStage + ">JS" + jobStage + ": " + resCount + "</span>";
  }
  
  updateResourceCountForJobStage(jobStage, resCount);
}

function getResourceCountForJobStage(js) {
  for(var i = 0; i < resources.length; ++i) {
    if(resources[i].stage == js)
      return resources[i].count;
  }
  return -1;
}
function myFunction() {
  alert("Hello! I am an alert box!");
}

function updateResourceCountForJobStage(js, count) {
  var found = false;
  for(var i = 0; i < resources.length; ++i) {
    if(resources[i].stage == js) {
      resources[i].count = count;
      found = true;
      break;
    }
  }
  if(!found) {
    resources.push(new Resource(js, count));
  }
}

function submit(data) {

}