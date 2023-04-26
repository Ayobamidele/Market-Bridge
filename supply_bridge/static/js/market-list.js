var windowdata = window.appConfig

// new gridjs.Grid({
// 	columns: ["Item", "Price"],
// 	server: {
// 		url: windowdata.url ,
// 		then: data => data.order_items.map(item => [item.title, item.price])
// 	  } 
//   }).render(document.getElementById("wrapper"));
async function get_item_data(){
var url = windowdata.url
const response = await fetch(url, {
	method: 'GET',
	headers: {
		'accept': 'application/json',
		'Content-Type': 'application/json'
	},
}).then(response => {
	if(response.status == 200){
		return response.json();
	}
}).then(json => {
	console.log(json)
}).catch(error => {
	console.log(error)
})
}  

// $("#countries").change(function () {
// 	console.log(this)
// 	this.disabled = true;
// });

function updateOption(dropdown)
{
    var option_value = dropdown.options[dropdown.selectedIndex].value;
    var option_text = dropdown.options[dropdown.selectedIndex].text;
    // alert('The option value is "' + option_value + '"\nand the text is "' + option_text + '"');
	return option_value, option_text
}

var dropd= document.getElementById("countries").parentNode
dropd.addEventListener('focusin', ev => {
	console.log("focus in", ev.target)
	ev.target.classList.remove('disabled')

	// ev.target.disabled = false
});
dropd.addEventListener('focusout', ev => {
	console.log("focus out", ev.target.parentNode)
	// ev.target.disabled = true
	ev.target.parentNode.classList.add('disabled')
});
dropd.addEventListener('change', ev => {
	console.log("change",ev.target.parentNode)
	updateOption(ev.target)
	// ev.target.blur()
});
dropd.addEventListener('click', ev => {
// ev.target.disabled = false;
if ("disabled" in ev.target.firstElementChild.classList){
	ev.target.firstElementChild.classList.remove('disabled')
}
console.log(ev.target)
});
// $("#countries").on('click', function () {
// 	this.disabled = false
// 	console.log(this.disabled,"click")
// });

// $("#countries").on('focus', function () {
// 	this.disabled = false
// 	console.log(this.disabled,"focus")
// });

// $("#countries").on('blur', function () {
// 	this.disabled = true
// 	console.log(this.disabled,"blur")
// });

// title
// 	-string
// quantiy-
// 	- integer
// -container
// 	- Modal
// price
// 		- integer
// - Active_changes
// 	- modal
// 		- All_active_users_making_changes_to_that_order_item

var order = document.getElementById("order-input")
order.onclick = function (e) {
	console.log(order.value)
	order_value= order.value=""
		// console.log(e)
		//Create order items
		updateTableFromData([order_value, "eee"])
	}