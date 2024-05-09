// Déclaration des variables pour les éléments du DOM
const dropdown = document.querySelector(".slide-dropdown"); // Element à dérouler pour afficher le sous-menu de gestion
const dropdownGestion = document.querySelector(".dropdown-gestion"); // Element qui déclenche le déroulement du sous-menu de gestion
const chevron = document.querySelector(".chevron"); // Icone chevron pour indiquer si le sous-menu de gestion est déroulé ou non
const rapports = document.querySelector(".rapports"); // Element à déplacer vers le bas lorsque le sous-menu de gestion est déroulé
let isClick = false; // Variable pour suivre si le sous-menu de gestion est déroulé ou non

const hamburgerButton = document.querySelector(".hamburger-button"); // Bouton hamburger pour réduire ou agrandir la sidebar
const sidebar = document.querySelector(".sidebar"); // Sidebar à réduire ou agrandir
const sidemenu = document.querySelector(".side-menu");
const setting = document.querySelector(".setting");
const sidebarCollapsedResponsive = document.querySelector(".sidebar-collapsed-responsive");
let isSidebarCollapsed = false; // Variable pour suivre si la sidebar est réduite ou non au clic sur le hamburger button



function toggleSidebarClick() {

     if (sidebar.classList.contains("sidebar-collapsed")) {
          // Si la sidebar est réduite, définissez --diff-width-sidebar à 176px et masquez les titres d'onglets
          sidebar.classList.toggle("sidebar-collapsed");
          hamburgerButton.style.transform = "rotate(90deg)";
          document.documentElement.style.setProperty("--diff-width-sidebar", "176px");
          isSidebarCollapsed = true;
     } else {
          // Si la sidebar n'est pas réduite, définissez --diff-width-sidebar à 0px et affichez les titres d'onglets
          sidebar.classList.toggle("sidebar-collapsed");
          hamburgerButton.style.transform = "rotate(0deg)";
          document.documentElement.style.setProperty("--diff-width-sidebar", "0px");
          isSidebarCollapsed = false;
     }
}

function toggleSidebarMouseover() {
     //verifie que la sidebar est réduite au click sur le hamburger button
     if (isSidebarCollapsed) {
          document.documentElement.style.setProperty("--diff-width-sidebar", "0px");
     }
}

function toggleSidebarMouseout() {
     //verifie que la sidebar est réduite au click sur le hamburger button
     if (isSidebarCollapsed) {
          document.documentElement.style.setProperty("--diff-width-sidebar", "176px");
     }
}

document.addEventListener("DOMContentLoaded", (event) => { // Attend que le DOM soit chargé pour exécuter le code

     dropdownGestion.addEventListener("click", () => {
          isClick = !isClick;
          dropdown.style.overflowY = isClick ? "visible" : "hidden";
          rapports.style.marginTop = isClick ? "100px" : "0px";
          chevron.style.transform = isClick ? "rotate(180deg)" : "rotate(0deg)";
    });

     hamburgerButton.addEventListener("click", toggleSidebarClick);

     // Lorsque la souris survole le sideMenu, si la sidebar est réduite, la dérouler
     sidemenu.addEventListener("mouseover", toggleSidebarMouseover);

     // Lorsque la souris quitte le sidemenu, si la sidebar est réduite, la réduire à nouveau
     sidemenu.addEventListener("mouseout", toggleSidebarMouseout);

     // Lorsque la souris survole le setting, si la sidebar est réduite, la dérouler
     setting.addEventListener("mouseover", toggleSidebarMouseover);

     // Lorsque la souris quitte le setting, si la sidebar est réduite, la réduire à nouveau
     setting.addEventListener("mouseout", toggleSidebarMouseout);

 });



