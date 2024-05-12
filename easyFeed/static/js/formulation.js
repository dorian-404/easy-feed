
// Declaration des variables
let radioManuel = document.querySelector("#manuel-radio");
let radioAuto = document.querySelector("#auto-radio");
let cardChoiceIngredient = document.querySelector(".card-choice-ingredient");

let formulerButton = document.querySelector(".formuler-button");
let cardResultat = document.querySelector(".card-resultat");
let selectAge = document.querySelector(".age-select");
let selectPays = document.querySelector(".pays-select");
let isC

// faire apparaitre ou disparaitre la cardChoiceIngredient en fonction du choix de l'utilisateur
radioManuel.addEventListener('click', function() {
    cardChoiceIngredient.style.display = 'block';
});

radioAuto.addEventListener('click', function() {
    cardChoiceIngredient.style.display = 'none';
});

// faire apparaitre la cardResultat lorsque l'utilisateur clique sur formuler
formulerButton.addEventListener('click', function() {


    // si les select et les radio ne sont pas remplis, afficher un message d'erreur
    if (selectAge.value === 0 || selectPays.value === "" || (radioManuel.checked === false && radioAuto.checked === false)) {
        alert("Veuillez remplir tous les champs nécessaire pour formuler votre recette");
    }
    else
    {
        alert("Votre recette a bien été formulée !");
    }
});
