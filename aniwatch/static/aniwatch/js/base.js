// Definitions of event listeners
function searchClicked(){
	let search_li = document.getElementsByClassName("search")[0];
	search_li.getElementsByTagName("img")[0].style.display = "none";
	document.getElementsByClassName("inp")[0].style.display = "block";
}
function backoffSearchBar(){
	//Hide existing search bar
	document.getElementsByClassName("inp")[0].style.display = "none";

	// Restore search icon
	let search_li = document.getElementsByClassName("search")[0];
	search_li.getElementsByTagName("img")[0].style.display = "block";
}
async function notify(msg) {
	let notification_holder = document.createElement('div');
	notification_holder.appendChild(document.createTextNode(msg));
	notification_holder.classList.add('notification')

	document.body.appendChild(notification_holder);
	await setTimeout(function() {
		notification_holder.remove();
	}, 3000);
}
// Attach Event Listeners
window.addEventListener('load', ()=>{
	// Search Bar event listeners
	document.getElementsByClassName("search")[0].addEventListener("click", searchClicked);
	document.getElementsByClassName("search")[0].addEventListener("focusout", backoffSearchBar);

	// Theme button event listeners
	document.getElementsByClassName("theme")[0].addEventListener("click", ()=>{
		notify('Seriously? White Theme? Get a life.')
	});

	// Settings button event listeners
	document.getElementsByClassName("settings")[0].addEventListener("click", ()=>{
		notify('User account feature under construction')
	});
})