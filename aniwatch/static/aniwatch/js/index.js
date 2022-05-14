function splashscreen(){
	let splashscreen = document.createElement('div');
	splashscreen.appendChild(document.createTextNode('Aniwatch'));
	splashscreen.classList.add('splashscreen')

	document.documentElement.appendChild(splashscreen)

	setTimeout(()=>{
		splashscreen.remove()
	}, 2000);
}
splashscreen()