//******************************* Fonctions *******************************************
let nom = "";
let prenom = "";
let email = "";
//    let telephone = 0;
//    let adresse = "";
//    let ville = "";
//    let code_postal = "";
//    let pays = "";
let password = "";
let password2 = "";

let type_abonnement = "";

//
//  Valider les informations du client
//

function valideInfoClient() {
    nom = $("#floating_last_name").val();
    prenom = $("#floating_first_name").val();
    email = $("#floating_email").val();
//    telephone = $("#floating_telephone").val();
//    adresse = $("#floating_adresse").val();
//    ville = $("#floating_ville").val();
//    code_postal = $("#floating_code_postal").val();
//    pays = $("#floating_pays").val();
      password = $("#floating_password").val();
      password2 = $("#floating_repeat_password").val();

    // Validation des champs
    if (password.length < 4){
    alert("passwords too short");
        // Il faut creer un span avec l'ID 'password-error' pour afficher les erreurs
//        $('#password-error').text("Le mot de passe doit contenir au moins 4 caractères");
//        $('#password-error').show();
        return $('#floating_password').focus();
    } else {
//        $('#password-error').hide();
    }

    if (password != password2){
//         Il faut creer un span avec l'ID 'password2-error' pour afficher les erreurs
//         $('#password2-error').text("Les mots de passe ne correspondent pas");
//         $('#password2-error').show();
         return $('#floating_repeat_password').focus();
    } else {
//         $('#password2-error').hide();
    }
}

//
//  choisir un abonnement mensuel
//

function abonnementMensuel(){
    type_abonnement = "Mensuel";
}

//
//  Enregistrer les informations du client
//

function saveInfoClient(){
    const PRIX_ABO_MENSUEL = 100.0;
    const PRIX_ABO_ANNUEL = 950.0;

    $.ajax({
        url: url_signup,  // url est une variable declaree dans le fichier .html
        type: 'POST',
        dataType: "json",
        data: {
            nom: nom,
            prenom: prenom,
            email: email,
//          telephone: telephone,
//          adresse: adresse,
//          ville: ville,
//          code_postal: code_postal,
//          pays: pays,
            password: password,
            titre: type_abonnement,
            prix: (type_abonnement == 'Mensuel') ? PRIX_ABO_MENSUEL : PRIX_ABO_ANNUEL,

            csrfmiddlewaretoken: csrfToken, // donner les permissions (autorison lorsqu'on fait du json en django)
       },
       success: function(data) {
           if (data.result == "ok"){
               alert(data.message);
               window.location.href = url_login;
           }else{
               alert(data.message);
           }
       }
    });
}

function loginClient(){
    let email = $("#username").val();
    let password = $("#password").val();
    $.ajax({
        url: url_login,  // url est une variable declaree dans le fichier .html
        type: 'GET',
        dataType: "json",
        data: {
            email: email,
            password: password,
            csrfmiddlewaretoken: '{{ csrf_token }}', // donner les permissions (autorison lorsqu'on fait du json en django)
       },
       success: function(data) {
           if (data.result == "ok"){
               alert(data.message );
               window.location.href = url_dashboard;
           }else{
               alert(data.message);
               return;
           }

       },
         error: function(jqXHR, textStatus, errorThrown) {
            console.log("AJAX error: " + textStatus + ' : ' + errorThrown);
    }
    });
}
//************************* Gestion des evenements *****************************
$(document).ready(function () {
    abonnementMensuel();
    $("#btn-save").click(valideInfoClient);
    $("#btn-buy-now").click(saveInfoClient);
    $("#mensuel").click(abonnementMensuel);
    $("#btn-login").click(loginClient);
    $("#annuel").click(function() {
        type_abonnement = "annuel";
    });
});