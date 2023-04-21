$(".connect").on('click', async function (event) {
	event.stopPropagation();
	event.stopImmediatePropagation();
	const data = {
		"connect": true,
		"user": event.target.dataset.id,
	}
	var url = Flask.url_for("friends", {"title": window.appConfig.title, "username": window.appConfig.username })
	const response = await fetch(url, {
		method: 'POST',
		headers: {
			'accept': 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(data)
	}).then(response => {
		if(response.status == 200){
			return response.json();
		}
	}).then(json => {
		event.target.className=json.style
		$(event.target).html(`<span>${json.text}</span>`)
		// $(event.target).html(`<span> ${json.text}</span> <svg class="svg-loader stroke-info flex-shrink-0 w-6 h-6" viewBox="-2000 -1000 4000 2000"><path id="inf" d="M354-354A500 500 0 1 1 354 354L-354-354A500 500 0 1 0-354 354z"></path><use xlink:href="#inf" stroke-dasharray="1570 5143" stroke-dashoffset="6713px"></use></svg>`)
	}).catch(error => {
		console.log(error)
	})
});

var body = document.getElementsByTagName('body')
body[0].classList.add('bg-base-200/25')