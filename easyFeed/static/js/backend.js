//******************************* Fonctions *******************************************
let nom = "";
let prenom = "";
let email = "";
let password = "";
let password2 = "";

let type_abonnement = "";

let ageFormuler = 0;
let paysFormuler = 0;
let radioButtonManuel = false;
let radioButtonAuto = false;

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

//    // Validation des champs
//    if (password.length < 4){
//    alert("passwords too short");
//        // Il faut creer un span avec l'ID 'password-error' pour afficher les erreurs
////        $('#password-error').text("Le mot de passe doit contenir au moins 4 caractères");
////        $('#password-error').show();
//        return $('#floating_password').focus();
//    } else {
////        $('#password-error').hide();
//    }
//
//    if (password != password2){
////         Il faut creer un span avec l'ID 'password2-error' pour afficher les erreurs
////         $('#password2-error').text("Les mots de passe ne correspondent pas");
////         $('#password2-error').show();
//         return $('#floating_repeat_password').focus();
//    } else {
////         $('#password2-error').hide();
//    }
    alert("Information enregistrées avec succès!!!");
    return $('#mensuel').focus();
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
            password: password,
            titre: type_abonnement,
            prix: (type_abonnement == 'Mensuel') ? PRIX_ABO_MENSUEL : PRIX_ABO_ANNUEL,

            csrfmiddlewaretoken: csrfToken, // donner les permissions (autorison lorsqu'on fait du json en django)
       },
       success: function(data) {
           if (data.result == "ok"){
               alert(data.message);
               window.location.href = url_create;
           }else{
               alert(data.message);
           }
       }
    });
}

//
//  Creer le compte administrateur
//

function createAccount(){
    let nom = $("#floating_last_name").val();
    let prenom = $("#floating_first_name").val();
    let ddn = $("#floating_birthdate").val();
    let telephone = $("#floating_phone").val();
    let adresse = $("#floating_company").val();
    let email = $("#floating_email").val();
    let dde = new Date().toISOString().slice(0,10);
    let [annee, mois, jour] = dde.split("-");
    let methode = "POST";
    alert(`Année: ${annee}, Mois: ${mois}, Jour: ${jour}`);
    alert(annee);
    let matricule = "A"+mois+annee;
    alert(matricule);
    alert(url_create);
    alert(url_login);


    $.ajax({
        url: url_create,  // url est une variable declaree dans le fichier .html
        type: 'POST',
        dataType: "json",
        data: {
            nom: nom,
            prenom: prenom,
            email: email,
            telephone: telephone,
            adresse: adresse,
            ddn: ddn,
            password: password,
            method: methode,

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


//
//  Se connecter a son compte
//

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

                    /* fonctions pour la formulation */

//
//  Afficher les contraintes d'une phase de developpement
//

function phaseInfo() {
    id_phase = $("#age").val();
    activerDesactiverFormuler();

    if (id_phase != -1){
            $.ajax({
                url: url_phase,  // url est une variable declaree dans le fichier .html
                type: "GET",
                dataType: "json",
                data: {
                    id_phase: id_phase,
                    csrfmiddlewaretoken: '{{ csrf_token }}', // donner les permissions (autorison lorsqu'on fait du json en django)
                },
                success: function(data) {   // data : contient les nutriments
//                    let tableau = "";
//                    $("#phase-table-body").empty();
//                    for (let key in data) {
//                        tableau += `<tr><td>${key}</td><td>${data[key]}</td></tr>`;
//                    };
//                    $("#phase-table-header1").html("Contraintes de la phase");
//                    $("#phase-table-header2").html("Nom contraintes");
//                    $("#phase-table-header3").html("Valeurs");
//                    $("#phase-table-body").html(tableau);
                }
            });
    }else{
//        $("#phase-table-body").empty();
    }
}

//
//  Afficher les ingredients lies a un pays
//

function paysIngredients() {
    code_pays = $("#pays").val();
    alert(code_pays);
    activerDesactiverFormuler();

    if (code_pays != -1){ // un pays a ete selectionne
        $("#manuel-radio").prop('disabled', false);
        $.ajax({
            url: url_pays,
            type: "GET",
            dataType: "json",
            data: {
                code_pays: code_pays,
                csrfmiddlewaretoken: '{{ csrf_token }}', // donner les permissions (autorison lorsqu'on fait du json en django)
            },
            success: function(data) {   // data : contient les ingredients sous la forme d'un dictionnaire
                    $("#table").empty();   // Vider le contenu de la liste des ingredients
                    let count = 0;
                    let valeurs = "<tr>";
                    $.each(data, function(key, value) {
                        let idValue = value.replace(/[ ']+/g, '-').replace(/%$/, ''); // Replace spaces with hyphens
                        valeurs += `<td><input type='checkbox' id='${idValue}' name='${idValue}' value=''><label for='${value}'>${value}</label></td>`;
                        count++;

                        // === compare à la fois le type et la valeur.
                        // En JavaScript, === est l'opérateur de comparaison stricte
                        if (count === 3) {
                            valeurs += "</tr><tr>";
                            count = 0;
                        }
                    });
                    valeurs += "</tr>";

                    // ajouter les valeurs a la table
                    $('#table').html(valeurs);
            }
        });
    }
    else{  // Aucun pays n'a ete selectionne

    }
}


//
//  Option de formulation manuelle
//

function manualOptimize(){
    activerDesactiverFormuler();

    if ($("#manuel-radio").is(":checked")){
        $(".card-choice-ingredient").show();
        $("#p-formuler").empty();
    }else{
        $(".card-choice-ingredient").hide();
    }
}

//
//  Option de formulation automatique
//

function autoOptimize(){
    activerDesactiverFormuler();

    if ($("#manuel-radio").is(":checked")){
        $(".card-choice-ingredient").show();
    }else{
        $(".card-choice-ingredient").hide();
    }
}

//
//  activer ou desactiver le bouton formuler
//

function activerDesactiverFormuler(){
    ageFormuler = $("#age").val();
    paysFormuler = $("#pays").val();
    radioButtonManuel = $("#manuel-radio").is(":checked");
    radioButtonAuto = $("#auto-radio").is(":checked");

    if ((ageFormuler != -1 && paysFormuler != -1) && (radioButtonAuto || radioButtonManuel)){
        $("#btn-formuler").prop('disabled', false);
    }else{
        $("#btn-formuler").prop('disabled', true);
    }
}

//
//  calculer la recette optimale
//

function optimize() {
//    alert("oups");
alert("id_phase: " + id_phase + " code_pays: " + code_pays);
    mode = ($("#manuel-radio").is(":checked")) ? 'manuel' : 'auto';
    alert("mode: " + mode);

    $.ajax({
        url: url_formuler,  // url est une variable declaree dans le fichier .html
        type: 'GET',
        dataType: "json",
        data: {
            id_phase: id_phase,
            code_pays: code_pays,
            mode: mode,
            csrfmiddlewaretoken: '{{ csrf_token }}', // donner les permissions (autorison lorsqu'on fait du json en django)
        },
        success: function(data) {
            console.log("L'optimisation a réussi: " + data.success);
            console.log("Message: " + data.message);
            console.log("Valeur minimale de la fonction objectif: " + data.fun);
            console.log("Point qui minimise la fonction objectif: " + data.x);

            if(mode == 'auto'){
                // Creer une liste HTML pour afficher les valeurs de solution.x
                let ingredient = "<ul>";

                for (let i = 0; i < data.x.length; i++) {
                    ingredient += `<li>${data.ing[i]} : ${(data.x[i]*100).toFixed(3)} kg</li>`;
                }

                ingredient += "</ul><br />";

                let nutriments = "<ul>";
                for (let i = 0; i < data.nutri.length; i++) {
                    nutriments += `<li>${data.nutri[i]} : ${(data.v_nutri[i]).toFixed(3)}</li>`;
                }

                nutriments += "</ul><br />";

                let ratio = "<table border='2'>";

                for (let i = 0; i < data.nom_ratio.length; i++) {
                    ratio += `<th>${data.nom_ratio[i]}</th><tr><td>${data.min_ratio[i]}</td></tr><tr><td>${data.max_ratio[i]}</td></tr>`;
                }

                ratio += "</table><br />";

                let ratioNutriments = "<table border='2'>";

                for (let i = 0; i < data.nom_nutri.length; i++) {
                    ratioNutriments += `<th>${data.nom_nutri[i]}</th><tr><td>${data.min_nutri[i]}</td></tr><tr><td>${data.max_nutri[i]}</td></tr>`;
                }

                ratioNutriments += "</table><br />";

                $("#p-formuler").html(ingredient);
                $("#p-formuler").append(nutriments);
                $("#p-formuler").append(`Valeurs des ratios : <br/> Ratio EM/Proteine: ${(data.ratioEMProt).toFixed(2)}<br/>Ratio Ca/P:${(data.ratioCaP).toFixed(2)} <br/>Ratio Lys/Meth: ${(data.ratioLysMeth).toFixed(2)}`);
                $("#p-formuler").append(ratio);
                $("#p-formuler").html(ratioNutriments);
                $("#p-formuler").append("Le prix total est " + (data.pt*100).toFixed(2) + " FCFA");
            }

        },
        error: function(error) {
            console.log("Une erreur s'est produite lors de l'optimisation: " + error);
        }
    });
}


//************************* Gestion des evenements *****************************
$(document).ready(function () {
    activerDesactiverFormuler();
    abonnementMensuel();
    $("#btn-enregistrer").click(valideInfoClient);
    $("#btn-buy-now").click(saveInfoClient);
    $("#mensuel").click(abonnementMensuel);
    $("#btn-create").click(createAccount);
    $("#btn-login").click(loginClient);
    $("#annuel").click(function() {
        type_abonnement = "annuel";
    });

                      /************* Gestion des evenements formulation ****************/

    $("#manuel-radio").prop('disabled', true);
    $("#age").change(phaseInfo);             // un age a ete selectionne
    $("#pays").change(paysIngredients);      // un pays a ete selectionne
    $("#manuel-radio").click(manualOptimize); // l'utilisateur a choisi de formuler manuellement
    $("#auto-radio").click(autoOptimize); // l'utilisateur a choisi de formuler automatiquement
    $("#btn-formuler").click(optimize);  // le bouton formuler a ete clique


});



//alert("success");
////                    let valeurs = "";
//                    $("#liste").empty();   // Vider le contenu de la liste des ingredients
//                    let count = 0;
//                    let valeurs = "<tr>";
//                    $.each(json, function(key, value) {
//                        let idValue = value.replace(/[ ']+/g, '-').replace(/%$/, ''); // Replace spaces with hyphens
//                        valeurs += `<td><input type='checkbox' id='${idValue}' name='${idValue}' value=''><label for='${value}'>${value}</label></td>`;
//                        count++;
//                        if (count === 3) {
//                            valeurs += "</tr><tr>";
//                            count = 0;
//                        }
//                    });
//                    valeurs += "</tr>";
//
//                    // Add the values to the HTML table
//                    $('#table').html(valeurs);

//                    for (let key in json) {
//                        let idValue = json[key].replace(/[ ']+/g, '-').replace(/%$/, ''); // Remplace les espaces par des traits d'union
//                        valeurs += `<tr><td><input type='checkbox' id='${idValue}' name='${idValue}' value=''><label for='${json[key]}'>${json[key]}</label></td></tr>`;
//                    }
//                        $("#liste").html(valeurs);
//                    if (estCoche){
//                        $("#chkbox").html(valeurs);
//                    }


//let valeurs = "";
//                    $("#liste").empty();   // Vider le contenu de la liste des ingredients
//                    for (let key in data) {
//                        let idValue = data[key].replace(/[ ']+/g, '-').replace(/%$/, ''); // Remplace les espaces par des traits d'union
//                        valeurs += `<label id='${idValue}' style='display: flex; align-items: center;'><input type='checkbox'>${data[key]}</label><br />`;
//                    }
//                    $("#liste").html(valeurs);