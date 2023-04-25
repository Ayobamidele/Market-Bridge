var windowdata = window.appConfig

// new gridjs.Grid({
// 	columns: ["Item", "Price"],
// 	server: {
// 		url: windowdata.url ,
// 		then: data => data.order_items.map(item => [item.title, item.price])
// 	  } 
//   }).render(document.getElementById("wrapper"));

var grid = new gridjs.Grid({
	columns: ["Item", "Price"],
	server: {
		url: windowdata.url ,
		then: data => data.order_items.map(item => [item.title, item.price])
		} 
}).render(document.getElementById("wrapper"));

function updateTable(){
	// lets update the config
	grid.updateConfig({
		data: [
			['John', '(353) 01 222 3333'],
			['Mark', '(01) 22 888 4444'],
		],
	}).forceRender();
	setTimeout( updateTable, 1000);
}
	
// updateTable()


var order = document.getElementById("order-input")
order.onclick = function (e) {
	console.log(order.value)
	order.value=""
		console.log(e)
		//Create order items
	}