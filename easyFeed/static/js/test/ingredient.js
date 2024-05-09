//******************************* Fonctions *******************************************
let estCoche = false;   // Variable pour verifier si la case a cocher
                        //pour la visibilite de la liste des ingredients lies a un pays est cochee

let id_phase = 0;          // Variable pour stocker l'identifiant de la phase de developpement
let code_pays = "";          // Variable pour stocker l'identifiant de la phase de developpement
/*
    Note:
    la fonction isJSON(str) est une fonction qui prend une chaîne str en entrée
    et renvoie true si la chaîne est une représentation JSON valide. Sinon, elle renvoie false.
    La fonction utilise la méthode $.parseJSON(str) pour essayer de convertir la chaîne en un objet JSON.
    Elle vérifie ensuite si la chaîne n'est pas vide en utilisant l'opérateur de conversion de type !!str.
    Il est important de noter que !!str renvoie true si str n'est pas une chaîne vide.
    Aussi, isJSON(str) renvoie false si la méthode $.parseJSON(str) renvoie une erreur,
    ou si la chaîne str est vide et si elle reçoit un objet JSON.
    En conclusion: isJSON(str) s'attend à recevoit une chaîne de caractères JSON en entrée et pas un objet JSON.
*/

function isJSON(str){
    try {
        return $.parseJSON(str) && !!str;  // <-- equivalent js est : JSON.parse(str) &&  !!str;
    }catch(e){
        return false;
    }
}

//
// Afficher les nutriments contenus dans un ingredient
//

function ingredientInfo() {
    let ingredient = $("#select-ingredient").val();

    if (ingredient != -1){  // un ingredient a ete selectionne
        $.ajax({

            /*
                Note:
                js ne reconnait pas le langage template de django
                donc il faut declarer une variable pour l'url dans une balise
                script dans le fichier .html. cette variable sera par la suite
                appelee dans mon fichier .js a l'emplacement desire
                D'ou url: url dans le code ci-bas
            */

            url: url,   // url est une variable declaree dans le fichier .html
            type: "GET",
            dataType: "html",
            data: {
                ingredient: ingredient,
                csrfmiddlewaretoken: '{{ csrf_token }}',   // donner les permissions (autorison lorsqu'on fait du json en django)
            },
            success: function(data) {   // data : contient la réponse du serveur (les nutriments)
                console.log(data);
                if (isJSON(data)){
                    let json = $.parseJSON(data);    // <-- equivalent js est: JSON.parse(data);
                    console.log(json);
                    let tableau = "";
                    $("#nutriment-table-body").empty();
                    for (let key in json) {
                        tableau += `<tr><td>${key}</td><td>${json[key]}</td></tr>`;
                    };
                    $("#nutriment-table-header1").html("Valeurs nutritives");
                    $("#nutriment-table-header2").html("Nom nutriments");
                    $("#nutriment-table-header3").html("Valeurs");
                    $("#nutriment-table-body").html(tableau);
                }
            }
        });
    }else{
        $("#nutriment-table-body").empty();
    }
}

//
//  Afficher les ingredients lies a un pays
//

function paysIngredients() {
    let chkbox_af_liste = $("#chkbox-af-liste");
    code_pays = $("#select-pays").val();

    if (code_pays != -1){ // un pays a ete selectionne
        $.ajax({
            url: url_pays,
            type: "GET",
            dataType: "html",
            data: {
                code_pays: code_pays,
                csrfmiddlewaretoken: '{{ csrf_token }}', // donner les permissions (autorison lorsqu'on fait du json en django)
            },
            success: function(data) {   // data : contient les nutriments
                if (isJSON(data)){
                    let json = $.parseJSON(data);    // <-- equivalent js est: JSON.parse(data);
                    let valeurs = "";
                    $("#chkbox").empty();   // Vider le contenu de la liste des ingredients
                    for (let key in json) {
                        let idValue = json[key].replace(/[ ']+/g, '-').replace(/%$/, ''); // Remplace les espaces par des traits d'union
                        valeurs += `<label id='${idValue}' style='display: flex; align-items: center;'><input type='checkbox'>${json[key]}</label><br />`;
                    }
                    if (estCoche){
                        $("#chkbox").html(valeurs);
                    }
                }
            }
        });
    }else{  // Aucun pays n'a ete selectionne
        $("#chkbox").empty();
    }
}

//
//  Afficher rendre visible la listes des ingredients lies a un pays
//

function rendreVisibleListeIngredients(){
    let chkbox_af_liste = $("#chkbox-af-liste");

    if (chkbox_af_liste.prop("checked")){
        $("#chkbox").css('visibility','visible');
        estCoche = true;
    }else{
        $("#chkbox").css('visibility','hidden');
        estCoche = false;
    }
    paysIngredients();  // Appel de la fonction paysIngredients
}

//
//  Afficher les contraintes d'une phase de developpement
//

function phaseInfo() {
    id_phase = $("#select-age").val();

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
                    let tableau = "";
                    $("#phase-table-body").empty();
                    for (let key in data) {
                        tableau += `<tr><td>${key}</td><td>${data[key]}</td></tr>`;
                    };
                    $("#phase-table-header1").html("Contraintes de la phase");
                    $("#phase-table-header2").html("Nom contraintes");
                    $("#phase-table-header3").html("Valeurs");
                    $("#phase-table-body").html(tableau);
                }
            });
    }else{
        $("#phase-table-body").empty();
    }
}

//
//  Faire la formulation
//

function optimize() {
//alert("oups");
    $.ajax({
        url: url_formuler,  // url est une variable declaree dans le fichier .html
        type: 'GET',
        dataType: "json",
        data: {
            id_phase: id_phase,
            code_pays: code_pays,
            csrfmiddlewaretoken: '{{ csrf_token }}', // donner les permissions (autorison lorsqu'on fait du json en django)
        },
        success: function(data) {
            console.log("L'optimisation a réussi: " + data.success);
            console.log("Message: " + data.message);
            console.log("Valeur minimale de la fonction objectif: " + data.fun);
            console.log("Point qui minimise la fonction objectif: " + data.x);

            // Creer une liste HTML pour afficher les valeurs de solution.x
            let solution = "<ul>";

            for (let i = 0; i < data.x.length; i++) {
                solution += `<li>${data.x[i]}</li>`;
            }

            solution += "</ul>";
            $("#p-formuler").html(solution);
        },
        error: function(error) {
            console.log("Une erreur s'est produite lors de l'optimisation: " + error);
        }
    });
}

//************************* Gestion des evenements *****************************
$(document).ready(function () {
    $("#select-ingredient").change(ingredientInfo); // un ingredient a ete selectionne
    $("#select-age").change(phaseInfo);             // un age a ete selectionne
    $("#select-pays").change(paysIngredients);      // un pays a ete selectionne
    $("#chkbox-af-liste").click(rendreVisibleListeIngredients)  // la case a cocher la visibilite des ingredients a ete cliquee
    $("#btn-formuler").click(optimize);  // le bouton formuler a ete clique
});