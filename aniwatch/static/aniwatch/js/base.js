// Definitions of event listeners
function searchClicked(){
	let search_li = document.getElementsByClassName("search")[0];
	search_li.getElementsByTagName("img")[0].style.display = "none";
	document.getElementsByClassName("inp")[0].style.display = "block";
}
function backoffSearchBar(){
	//Remove existing search bar
	document.getElementsByClassName("inp")[0].style.display = "none";

	// Restore search icon
	let search_li = document.getElementsByClassName("search")[0];
	search_li.getElementsByTagName("img")[0].style.display = "block";
}
function themeChanger(){
	alert("Seriously? Who tf uses white theme?")
}
// Attach Event Listeners
window.addEventListener('load', ()=>{
	// Search Bar event listeners
	document.getElementsByClassName("search")[0].addEventListener("click", searchClicked);
	document.getElementsByClassName("search")[0].addEventListener("focusout", backoffSearchBar);

	// Theme button event listeners
	document.getElementsByClassName("theme")[0].addEventListener("click", themeChanger);
})