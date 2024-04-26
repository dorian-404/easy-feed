
// Logique pour gerer le sous-menu de gestion
const dropdown = document.querySelector('.slide-dropdown');
const chevron = document.querySelector('.chevron');
const rapports = document.querySelector('.reports');
let isClick = false;

chevron.addEventListener("click", () => {
      //alert("Vous avez cliquer !");
      if (!isClick) {
           dropdown.style.overflowY = "visible";
           rapports.style.marginTop = "100px";
           isClick = true;
           chevron.style.transform = "rotate(180deg)";
      } else {
           dropdown.style.overflowY = "hidden";
           rapports.style.marginTop = "0px";
           isClick = false;
           chevron.style.transform = "rotate(0deg)";
      }

})

console.log(dropdown.children);
console.log(dropdown.length);

 //const a = item.parentElement.querySelector('a:first-child');
 //console.log(a);

//dropdown.forEach(item=> {
//     const a = item.parentElement.querySelector('a:first-child');
//     a.addEventListener('click', function(e) {
//          e.preventDefault();
//          this.classList.toggle('active');
//     })
//
//})