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
    let matricule = "A"+mois+annee;


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
               sessionStorage.setItem('prenomU', data.prenom);
               sessionStorage.setItem('nomU', data.nom);
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
    mode = ($("#manuel-radio").is(":checked")) ? 'manuel' : 'auto';

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
                let ingredient = "<table border='2' style='margin-right: 5%;'>";

                ingredient += `<thead><tr><th colspan="2">Aliments</th></tr></thead>`;

                for (let i = 0; i < data.x.length; i++) {
                    ingredient += `<tr><td class="space-cell">${data.ing[i]}</td><td>${(data.x[i]*100).toFixed(3)} kg</td></tr>`;
                }

                ingredient += "</table>";

                let nutriments = "<table border='2' style='margin-right:5%;'>";
                nutriments += `<thead><tr><th class="space-cell" colspan="2">Nutriments</th></tr></thead>`;

                for (let i = 0; i < data.nutri.length; i++) {
                    nutriments += `<tr><td class="space-cell">${data.nutri[i]}</td><td>${(data.v_nutri[i]).toFixed(3)}</td></tr>`;
                }

                nutriments += "</table>";


                let ratio = "<center><table border='2'style='margin-right: 5%; margin-left: 5%;'>";

                ratio += "<tr>";
                for (let i = 0; i < data.nom_ratio.length; i++) {
                    ratio += `<th class="space-cell">${data.nom_ratio[i]}</th>`;
                }
                ratio += "</tr>";

                ratio += "<tr>";
                for (let i = 0; i < data.nom_ratio.length; i++) {
                    ratio += `<td class="space-cell">${data.min_ratio[i]}</td>`;
                }
                ratio += "</tr>";

                ratio += "<tr>";
                for (let i = 0; i < data.nom_ratio.length; i++) {
                    ratio += `<td class="space-cell">${data.max_ratio[i]}</td>`;
                }
                ratio += "</tr>";

                ratio += "</table></center><br />";

                let ratioNutriments = "<center><table border='2' style='margin-right: 5%; margin-left:5%;'>";

                ratioNutriments += "<tr><th class='space-cell'>Contraintes</th>";
                for (let i = 0; i < data.nom_nutri.length; i++) {
                    ratioNutriments += `<th>${data.nom_nutri[i]}</th>`;
                }
                ratioNutriments += "</tr>";

                ratioNutriments += "<tr><td class='space-cell'>minimale</td>";
                for (let i = 0; i < data.nom_nutri.length; i++) {
                    ratioNutriments += `<td class="space-cell">${data.min_nutri[i]}</td>`;
                }
                ratioNutriments += "</tr>";

                ratioNutriments += "<tr><td class='space-cell'>maximale</td>";
                for (let i = 0; i < data.nom_nutri.length; i++) {
                    ratioNutriments += `<td class="space-cell">${data.max_nutri[i]}</td>`;
                }
                ratioNutriments += "</tr>";

                ratioNutriments += "</table></center><br />";

//                let ratioNutriments = "<table border='2' style='margin-right: 5%'>";
//
//                for (let i = 0; i < data.nom_nutri.length; i++) {
//                    ratioNutriments += `<th>${data.nom_nutri[i]}</th><tr><td>${data.min_nutri[i]}</td></tr><tr><td>${data.max_nutri[i]}</td></tr>`;
//                }
//
//                ratioNutriments += "</table>";

                $("#ligne-formuler-1").html(ingredient);
                $("#ligne-formuler-1").append(nutriments);
                $("#ligne-formuler-1").append(`
                    <table border='2'>
                        <thead>
                            <tr>
                                <th colspan="2">Valeurs des ratios</th>
                            </tr>
                        </thead>
                        <tr>
                            <td>Ratio EM/Proteine</td>
                            <td>${(data.ratioEMProt).toFixed(2)}</td>
                        </tr>
                        <tr>
                            <td>Ratio Ca/P</td>
                            <td>${(data.ratioCaP).toFixed(2)}</td>
                        </tr>
                        <tr>
                            <td>Ratio Lys/Meth</td>
                            <td>${(data.ratioLysMeth).toFixed(2)}</td>
                        </tr>
                    </table>
                `);
                $("#ligne-formuler-2").append(ratio);
                $("#ligne-formuler-2").append(ratioNutriments);
                $("#ligne-formuler-2").append("<center style='margin-top: 5%; font-family: var(--title-font); color: rgb(0, 66, 20); font-size = 60pt'>Le prix total est " + (data.pt*100).toFixed(2) + " FCFA </center>");
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
    let prenom = sessionStorage.getItem('prenomU');
    let nom = sessionStorage.getItem('nomU');
    // Utiliser les variables prenom et nom comme nécessaire
    $("#username-form").html("Bienvenue " + prenom + " " + nom);
    $("#btn-enregistrer").click(valideInfoClient);
    $("#btn-buy-now").click(saveInfoClient);
    $("#mensuel").click(abonnementMensuel);
    $("#btn-create").click(createAccount);
    $("#btn-login").click(loginClient);
    $("#annuel").click(function() {
        type_abonnement = "Annuel";
    });

                      /************* Gestion des evenements formulation ****************/

    $("#manuel-radio").prop('disabled', true);
    $("#age").change(phaseInfo);             // un age a ete selectionne
    $("#pays").change(paysIngredients);      // un pays a ete selectionne
    $("#manuel-radio").click(manualOptimize); // l'utilisateur a choisi de formuler manuellement
    $("#auto-radio").click(autoOptimize); // l'utilisateur a choisi de formuler automatiquement
    $("#btn-formuler").click(optimize);  // le bouton formuler a ete clique


});


