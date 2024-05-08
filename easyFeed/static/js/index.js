// Logique pour gerer le sous-menu de gestion
const dropdown = document.querySelector(".slide-dropdown");
const chevron = document.querySelector(".chevron");
const rapports = document.querySelector(".rapports");
let isClick = false;

 // logique pour reduire la largeur de la sidebar à 74px au click sur le hamburger button gestion des valeur des classes sidebar et main-content
 const hamburgerButton = document.querySelector(".hamburger-button");
 const sidebar = document.querySelector(".sidebar");
 const sidemenu = document.querySelector(".side-menu");
 const setting = document.querySelector(".setting");
 const mainContent = document.querySelector(".main-content");
 const tabTitles = document.querySelectorAll(".tab-title"); // Remplacez ".tab-title" par le sélecteur approprié pour vos titres d'onglets


function toggleSidebarClick() {

     sidebar.classList.toggle("sidebar-collapsed");
     mainContent.classList.toggle("main-content-collapsed");

     if (sidebar.classList.contains("sidebar-collapsed")) {
          // Si la sidebar est réduite, définissez --diff-width-sidebar à 176px et masquez les titres d'onglets
          hamburgerButton.style.transform = "rotate(90deg)";
          document.documentElement.style.setProperty("--diff-width-sidebar", "176px");
          tabTitles.forEach(title => title.classList.add("hide-text"));
     } else {
          // Si la sidebar n'est pas réduite, définissez --diff-width-sidebar à 0px et affichez les titres d'onglets
          hamburgerButton.style.transform = "rotate(0deg)";
          document.documentElement.style.setProperty("--diff-width-sidebar", "0px");
          tabTitles.forEach(title => title.classList.remove("hide-text"));
     }
}
     
function toggleSidebarMouseover() {
     if (sidebar.classList.contains("sidebar-collapsed")) {
          document.documentElement.style.setProperty("--diff-width-sidebar", "0px");
          tabTitles.forEach(title => title.classList.remove("hide-text"));
     }
}

function toggleSidebarMouseout() {
     if (sidebar.classList.contains("sidebar-collapsed")) {
          document.documentElement.style.setProperty("--diff-width-sidebar", "176px");
          tabTitles.forEach(title => title.classList.add("hide-text"));
     }
}


document.addEventListener("DOMContentLoaded", (event) => {

     chevron.addEventListener("click", () => {
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