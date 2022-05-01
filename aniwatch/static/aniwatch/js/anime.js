selected_ep = null
async function activatePlayer(cName){
	// Fetch new goload.pro embed link for No. "cName" episode
	let orig_anime_url = document.getElementsByClassName("associated_url")[0].getAttribute("data-url")
	let anime = orig_anime_url.split("/category/")[1]
	do{
		alert(cName+" != "+url+". So fetching again.")
		await fetch(document.location.origin+"/aniwatch/query/"+anime+"/episode/"+cName.split("_")[1]).then(response=>{
		  response.text().then(response=>{
		  	// Global 'url' variable
		      url = JSON.parse(JSON.parse(response)).Url;
		  	})
		})
	}while(!url.includes(cName.split("_")[1]));
	// Hide main class
	document.getElementsByClassName('main')[0].style.display = "none";

	// Update new episode in iframe	
	let player = document.getElementsByClassName('player')[0]
	player.style.display = "flex";
	player.style.justifyContent = "center"
	player.getElementsByTagName('iframe')[0].src = url
	if(selected_ep != null){
		document.getElementsByClassName(selected_ep)[0].classList.remove('selected')
	}
	selected_ep = cName;
	document.getElementsByClassName(selected_ep)[0].classList.add('selected')
}
/*episodes=document.getElementsByClassName('list')[0].getElementsByTagName('li')
for (const episode of episodes)
{
	episode.addEventListener("click",function(){activatePlayer(episode.className)})
}*/