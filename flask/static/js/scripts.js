function error(type) {
  alert(type);
}

function rerun() {
  window.location.replace("/");
}

function savePath() {
  $.post({
    type: "POST",
    url: "/settings",
    data: {
      "pythonPath": $("#settings-pypath").val(),
      "projectPath": $("#settings-projectpath").val(),
      "trainPath": $("#settings-trainpath").val(),
      "exportPath": $("#settings-exportpath").val(),
      "convertPath": $("#settings-convertpath").val(),
      "dataPath": $("#settings-datapath").val(),
      "configPath": $("#settings-configpath").val(),
      "preprocessPath": $("#settings-preprocesspath").val(),
      "resultPath": $("#settings-resultpath").val()
    },
    success(response){
      var status = JSON.parse(response)["status"];
      if (status === "Save successful") {
        alert(status);
        window.location.replace("/");
      }
      else { error(status); }
    }
  });  
}

function run() {
  $.post({
    type: "POST",
    url: "/",
    data: {
      "branch": $("#settings-branch").val(),
      "modelType": $("#settings-model-type").val(),
      "width": $("#settings-image-width").val(),
      "height": $("#settings-image-height").val(),
      "batch": $("#settings-batch").val(),
      "epochs": $("#settings-epochs").val(),
      "halfPrecision": $("#settings-half-precision").val(),
      "message": $("#settings-message").val(),
      "resultName": $("#settings-name").val(),
      "extraArgs":  $("#settings-extra").val()
    },
    success(response){
      var status = JSON.parse(response)["status"];
      if (status === "Run successful") { window.location.replace("/success"); }
      else { error(status); }
    }
  });
}


// Open or Close mobile & tablet menu
// https://github.com/jgthms/bulma/issues/856
$("#navbar-burger-id").click(function () {
  if($("#navbar-burger-id").hasClass("is-active")){
    $("#navbar-burger-id").removeClass("is-active");
    $("#navbar-menu-id").removeClass("is-active");
  }else {
    $("#navbar-burger-id").addClass("is-active");
    $("#navbar-menu-id").addClass("is-active");
  }
});