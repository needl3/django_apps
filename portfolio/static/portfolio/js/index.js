/* Global variables to store one time animation states' completions */

/*
This is the entry point of the script 
Runs after the window loads completely
*/
window.onload = ()=>{
	ul_container = document.getElementsByTagName("nav")[0].getElementsByTagName("ul")[0];

	/*Assign Event Listeners in nav elements*/
	for(const element of ul_container.getElementsByTagName("li")){
		element.addEventListener("click", ()=>{updateSelection(element.classList[0])})
	}
	/* Assign event listener to bottom arrow */
	move_down_button = document.getElementsByClassName("move_down")[0];
	move_down_button.addEventListener("click", ()=>{
		updateSelection(getNextSelection());
	})
	greet();
}

/* Below are methods to create greeting terminal animation */
function greet(){
	let prompt = "anish@arch-sama ~>";
	let cursor = "█";
	let greeting_prompts = [
		["echo 'Hemlo, Stranger!'", "Hemlo, Stranger!"],
		["whoami", "Anish Chapagai"]
	]

	ul_tag = document.getElementsByClassName('bg_text')[0].getElementsByTagName("ul")[0];
	for(let i=0;i<greeting_prompts.length;i++){
		for(let j=0;j<greeting_prompts.length;j++){
			createGreetingTag(prompt, cursor, greeting_prompts[i][j], ul_tag)
		}
	}
	createGreetingTag(prompt, cursor, "Press the button below to see more", ul_tag, true);
}

function createGreetingTag(prompt, cursor, greeting, container_ul, last=false){
	/* First create a container to append data into */
	li = document.createElement("li");

	/* Append this as last element of container_ul*/
	container_ul.insertAdjacentElement("beforeend", li);
	let s = prompt+" ";
	li.appendChild(document.createTextNode(s));

	/* Create a span element and insert to li from the end */
	let span = document.createElement("span");
	li.insertAdjacentElement("beforeend", span);

	/* Find a way to animate terminal text*/

	for(const a of greeting){
		span.innerHTML += a;
	}
	/* ---------------------------------- */


	if(last){
		let cursor_span = document.createElement("span");
		cursor_span.appendChild(document.createTextNode(cursor));
		cursor_span.classList.add("cursor");
		li.insertAdjacentElement("beforeend", cursor_span);
	}
}

function getSelectedPage(){
	return ul_container.getElementsByClassName("selected")[0].classList[0];
}

function getNextSelection() {
	current_page = getSelectedPage();
	li_elements = ul_container.getElementsByTagName("li")

	let found_selected = false;

	for (const element of li_elements){
		if(found_selected){
			return element.classList[0];
		}
		if (element.classList[0] === current_page){
			found_selected = true;
		}
	}
	return li_elements[0].classList[0];
}

/* Below are methods to update active pages */
function updateSelection(new_selected_class){
	let selected_element = ul_container.getElementsByClassName("selected")[0];
	let new_selected_element = ul_container.getElementsByClassName(new_selected_class)[0];

	selected_element.classList.remove("selected");
	new_selected_element.classList.add("selected");

	/* Add new page first */
	new_selected_page = document.getElementById(new_selected_element.classList[0]);
	new_selected_page.classList.remove("hidden");
	new_selected_page.classList.add("visible");

	/* Scroll to new page */
	new_selected_page.scrollIntoView({
		behavior: 'smooth'
	});

	/* Hide previous page */
	selected_page = document.getElementById(selected_element.classList[0]);
	selected_page.classList.remove("visible");
	selected_page.classList.add("hidden");

}