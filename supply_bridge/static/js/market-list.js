var windowdata = window.appConfig;

function get_row_template(item) {
	return `<tr class="bg-white">
	<td class="p-3 text-sm text-gray-700 whitespace-nowrap">
		<a href="#" class="font-bold text-blue-500 hover:underline"
			>${item.title || "eeeeer"}</a
		>
	</td>

	<td class="p-3 text-sm text-gray-700 whitespace-nowrap">

		<label class="swap swap-flip">
			<!-- this hidden checkbox controls the state -->
			<input type="checkbox" />
			<div class="swap-on">
				<div class="flex">
					<span class="inline-flex items-center px-2 text-sm text-gray-900 bg-gray-200 border border-r-0 border-gray-300 rounded-l-md">
						Measure
					</span>

					<input type="number" min="1" value="${item.price}" step="0.01"
					class="rounded-none bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="0.00">
						
					<select class="rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-white-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
						<option>Choose a Measure</option>
						<option value="kg=">Kilogram</option>
						<option value="TX">Litre</option>
						<option value="WH">Tin-Can</option>
						<option value="WH" class="small text-bg-primary">Not availabele? Create container</option>
					</select>
				</div>
			</div>
			
			<div class="swap-off">
				<div class="flex">
					<span class="inline-flex items-center px-3 text-sm text-gray-900 bg-gray-200 border border-r-0 border-gray-300 rounded-l-md">
						Price
					</span>
					<input type="text" name="currency-field" id="currency-field" pattern="^\$\d{1,3}(,\d{3})*(\.\d+)?$" value="" data-type="currency" class="rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="0.00">			
				</div>
			</div>

		</label>

	</td>


	<td class="p-3 text-sm text-gray-700 whitespace-nowrap">
		<input type="number" min="1"  step="1" data-type="quantity" class="rounded-none bg-gray-50 border text-center text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
			
	</td>

	</tr>`;
}

// new gridjs.Grid({
// 	columns: ["Item", "Price"],
// 	server: {
// 		url: windowdata.url ,
// 		then: data => data.order_items.map(item => [item.title, item.price])
// 	  }
//   }).render(document.getElementById("wrapper"));
async function get_item_data() {
	var url = windowdata.items;
	const response = await fetch(url, {
			method: "GET",
			headers: {
				accept: "application/json",
				"Content-Type": "application/json",
			},
		})
		.then((response) => {
			if (response.status == 200) {
				return response.json();
			}
		})
		// .then((json) => {
		// 	console.log(json);
		// })
		// .catch((error) => {
		// 	console.log(error);
		// });
	return response['order_items']
}
function createSelect(options) {
	const $select = $('<select>', {
		class:'measure-options w-auto rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-white-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
	})

	
	options.forEach(option => {
	  const $optionElement = $('<option>',{
		val:option,
		text:option
	  })
	  $select.append($optionElement);
	});
	
	return $select;}

async function load_items(){
	const items = await get_item_data();
	console.log(items)
	  
	items.forEach(item => {
		console.log(item)
	const $tr = $('<tr>',{
		class: "bg-white",
	});
	
	const $nameTd = $('<td>',{
		class: "p-3 ed-cell text-gray-700 whitespace-nowrap",
	})
	const $nameP = $('<p>', {
		class: "text-slate-500 hover:text-primary-focus/100 fs-5 font-bold",
	}).text(item['title']);
	$nameTd.append($nameP);
	$tr.append($nameTd);
  

	const $quantityTd = $('<td>',{
		class: "p-3 text-sm text-gray-700 whitespace-nowrap"
	});
		const $quantityInput = $('<input>', {
			type:"number",
			min:"1",
			step:"1",
			data_type:"quantity",
			class: "rounded-none bg-gray-50 border text-center text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
		});
		$quantityTd.append($quantityInput)
		
		$tr.append($quantityTd);

	
	const $measurementTd = $('<td>')
	if (item['measurement_type'] == "measure"){
		const $measurementMeasure = $('<div>',{
			data_id:"222",
			class: "swap swap-flip swap-container",
		})
		const $measurementMeasureContent_SwapOn = $('<div>', {
			class: "swap-on"
		})
		$measurementMeasure.append($measurementMeasureContent_SwapOn)
		const $measurementMeasureContent_Flex = $('<div>', {
			class: "flex"
		})
		$measurementMeasureContent_SwapOn.append($measurementMeasureContent_Flex)

		// Inside Flex
		const $measurementMeasureContent_Span = $('<span>', {
			class:"swap-controller inline-flex items-center px-2 text-sm text-gray-900 bg-gray-200 border border-r-0 border-gray-300 rounded-l-md",
		}).text("Measure")
		$measurementMeasureContent_Flex.append($measurementMeasureContent_Span)
		// Inside Flex
		const $measurementMeasureContent_Input = $('<input>', {
			type:"number",
			min:"1",
			step:"0.01",
			class:"rounded-none bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
			placeholder:"0.00"
		})
		$measurementMeasureContent_Flex.append($measurementMeasureContent_Input)

		async function get_options_details (){

			var url = windowdata.measure;
			const response = await fetch(url, {
				method: "GET",
				headers: {
					accept: "application/json",
					"Content-Type": "application/json",
				},
			})
			.then((response) => {
				if (response.status == 200) {
					return response.json();
				}
			})
			.then((json) => {
				let result = json.map(({ name }) => name);
				
				
				const $measurementMeasureContent_Select = createSelect(result)
				const $measurementMeasureContent_Option = $('<option>',{
					value:"create",
					class:"small px-2 text-bg-primary"
				}).text("Not availabele? Create container");
				$($measurementMeasureContent_Select).append($measurementMeasureContent_Option);
				$measurementMeasureContent_Flex.append($measurementMeasureContent_Select);
				$measurementTd.append($measurementMeasure)
				
				



				const $measurementMeasureContent_SwapOff = $('<div>', {
					class: "swap-off"
				})
				const $measurementMeasureContent_SwapOff_Flex = $('<div>', {
					class: "flex"
				})
				// $measurementMeasureContent_SwapOff.append($measurementMeasureContent_Flex)
		
				// Inside Flex
				const $measurementMeasureContent_Span = $('<span>', {
					class:"swap-controller inline-flex items-center px-2 text-sm text-gray-900 bg-gray-200 border border-r-0 border-gray-300 rounded-l-md",
				}).text("Price")
				$measurementMeasureContent_SwapOff_Flex.append($measurementMeasureContent_Span)
				// Inside Flex
				const $measurementMeasureContent_Input = $('<input>', {
					type:"text",
					name:"currency-field",
					pattern:"^\$\d{1,3}(,\d{3})*(\.\d+)?$",
					value:"",
					data_type:"currency",
					class:"rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
					placeholder:"0.00",
				})
				$measurementMeasureContent_SwapOff_Flex.append($measurementMeasureContent_Input)

				$measurementMeasureContent_SwapOff.append($measurementMeasureContent_SwapOff_Flex)
				$measurementMeasure.append($measurementMeasureContent_SwapOff)


				
				$tr.append($measurementTd)


			});
		}
		get_options_details()
		// Inside Flex
		 
		// Add inside measurementMeasureContent_Select
		
		$measurementMeasure.toggleClass("swap-active");
		
	} else{
		const $measurementMeasure = $('<div>',{
			data_id:"222",
			class: "swap swap-flip swap-container",
		})
		const $measurementMeasureContent_SwapOff = $('<div>', {
			class: "swap-off"
		})
		$measurementMeasure.append($measurementMeasureContent_SwapOff)
		const $measurementMeasureContent_SwapOff_Flex = $('<div>', {
			class: "flex"
		})
		$measurementMeasureContent_SwapOff.append($measurementMeasureContent_SwapOff_Flex)

		// Inside Flex
		const $measurementMeasureContent_SwapOff_Span = $('<span>', {
			class:"swap-controller inline-flex items-center px-2 text-sm text-gray-900 bg-gray-200 border border-r-0 border-gray-300 rounded-l-md",
		}).text("Price")
		$measurementMeasureContent_SwapOff_Flex.append($measurementMeasureContent_SwapOff_Span)
		// Inside Flex
		const $measurementMeasureContent_SwapOff_Input = $('<input>', {
			type:"text",
			name:"currency-field",
			pattern:"^\$\d{1,3}(,\d{3})*(\.\d+)?$",
			value:"",
			data_type:"currency",
			class:"rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
			placeholder:"0.00",
		})
		$measurementMeasureContent_SwapOff_Flex.append($measurementMeasureContent_SwapOff_Input)



		




		const $measurementMeasureContent_SwapOn = $('<div>', {
			class: "swap-on"
		})
		$measurementMeasure.append($measurementMeasureContent_SwapOn)
		const $measurementMeasureContent_Flex = $('<div>', {
			class: "flex"
		})
		$measurementMeasureContent_SwapOn.append($measurementMeasureContent_Flex)

		// Inside Flex
		const $measurementMeasureContent_Span = $('<span>', {
			class:"swap-controller inline-flex items-center px-2 text-sm text-gray-900 bg-gray-200 border border-r-0 border-gray-300 rounded-l-md",
		}).text("Measure")
		$measurementMeasureContent_Flex.append($measurementMeasureContent_Span)
		// Inside Flex
		const $measurementMeasureContent_Input = $('<input>', {
			type:"number",
			min:"1",
			step:"0.01",
			class:"rounded-none bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
			placeholder:"0.00"
		})
		$measurementMeasureContent_Flex.append($measurementMeasureContent_Input)

		async function get_options_details (){

			var url = windowdata.measure;
			const response = await fetch(url, {
				method: "GET",
				headers: {
					accept: "application/json",
					"Content-Type": "application/json",
				},
			})
			.then((response) => {
				if (response.status == 200) {
					return response.json();
				}
			})
			.then((json) => {
				let result = json.map(({ name }) => name);
				
				
				const $measurementMeasureContent_Select = createSelect(result)
				const $measurementMeasureContent_Option = $('<option>',{
					value:"create",
					class:"small px-2 text-bg-primary"
				}).text("Not availabele? Create container");
				$($measurementMeasureContent_Select).append($measurementMeasureContent_Option);
				$measurementMeasureContent_Flex.append($measurementMeasureContent_Select);
				
				$measurementTd.append($measurementMeasure)
				
				
				
				$tr.append($measurementTd)


			});
		}
		get_options_details()



		// $measurementTd.append($measurementMeasure)
		// $tr.append($measurementTd)
	}
	
	
	
	$('#tbody').append($tr);
	});
	  

}

function updateOption(dropdown) {
	var option_value = dropdown.options[dropdown.selectedIndex].value;
	var option_text = dropdown.options[dropdown.selectedIndex].text;
	// alert('The option value is "' + option_value + '"\nand the text is "' + option_text + '"');
	return option_value, option_text;
}

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
var needsValueUpdate;

$("#tbody").on('click', ".swap-controller", function () {
		$(this).offsetParent().toggleClass("swap-active");
		// update measurement type
});

$("#tbody").on('click', ".measure-options", function () {
	if (this.value === "create") {
		console.log("create");
		$("#measure-modal").prop("checked", true);
		needsValueUpdate = this;
	}
}
);

function getOptions() {
	var values = [];

	$(".measure-options option").each(function () {
		var value = $(this).val();
		if (values.indexOf(value) === -1) {
			values.push(value);
		}
	});
	return values;
}

function addOption(text, value) {
	var option = $("<option></option>").text(text).val(value);
	$(".measure-options").each(function () {
		$(this).find("option").eq(-2).before(option.clone());
	});
}

async function updateSelect() {
	// Get the new options
	var url = windowdata.measure;
	const response = await fetch(url, {
			method: "GET",
			headers: {
				accept: "application/json",
				"Content-Type": "application/json",
			},
		})
		.then((response) => {
			if (response.status == 200) {
				return response.json();
			}
		})
		.then((json) => {
			json.forEach(function (option) {
				// Update only
				if (!getOptions().includes(option["name"])) {
					addOption(option["name"], option["name"]);
				}
			});
		});
}

function updateNeedsValueUpdate(name) {
	$(needsValueUpdate).val(name).change();
	updateSelect();
	console.log(name);
	$(needsValueUpdate).val(name).change();
}

// setInterval(updateSelect, 3000)

$("#submit-measure").on({
	click: async function (e) {
		e.preventDefault();

		var url = windowdata.create;
		const response = await fetch(url, {
				method: "POST",
				body: JSON.stringify({
					action: "create",
					type: "measure",
					name: $("#measure-input").val(),
				}),
				headers: {
					accept: "application/json",
					"Content-Type": "application/json",
				},
			})
			.then((response) => {
				if (response.status == 200) {
					$("#measure-input").val("");
					$("#cancel-measure").trigger("click");
					return response.json();
				}
			})
			.then((json) => {
				var updated = updateSelect();
				$.when(updated).done(function () {
					console.log(json);
					updateNeedsValueUpdate(json["name"]);
				});
			});
		// .catch((error) => {
		// 	console.log(error);
		// });
	},
});

$("table").on("click", ".ed-cell", function (e) {
	if ($(this).find("input").length > 0) {
        return;
    }
	var p = $(this).find("p");
	if ( p.text() == "You haven't added a name yet." ){
		p.textContent = ""
	}
	var input = $("<input>", {
		val: p.text().trim(),
		type: "text",
		maxlength: "35",
		placeholder:"Don't forget to Add the items name",
		class: "rounded bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
	});
    p.replaceWith(input);
	input.on("blur", function () {
		if (!this.value.replace(/\s/g, '').length) {
		console.log('string only contains whitespace (ie. spaces, tabs or line breaks)');
		this.value = "You haven't added a name yet."
		}
		var newP = $("<p></p>",{
			class:"text-slate-500 hover:text-primary-focus/100 fs-5 font-bold",
		}).text(this.value.trim());
        $(this).replaceWith(newP);
	});
	input.focus();
});

//Create order items
$("#order-input").on({
	keyup: function (e) {
		if (e.keyCode === 13) {
			console.log(e.target.value);
			var item = {
				title: e.target.value,
				price: "550.99",
			};
			$("#tbody").append(get_row_template(item));
		}
	},
});

// Jquery Dependency

$("input[data-type='currency']").on({
	keyup: function () {
		formatCurrency($(this));
	},
	blur: function () {
		formatCurrency($(this), "blur");
	},
});

function formatNumber(n) {
	// format number 1000000 to 1,234,567
	return n.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function formatCurrency(input, blur) {
	// appends $ to value, validates decimal side
	// and puts cursor back in right position.

	// get input value
	var input_val = input.val();

	// don't validate empty input
	if (input_val === "") {
		return;
	}

	// original length
	var original_len = input_val.length;

	// initial caret position
	var caret_pos = input.prop("selectionStart");

	let input_currency = "₦";

	// check for decimal
	if (input_val.indexOf(".") >= 0) {
		// get position of first decimal
		// this prevents multiple decimals from
		// being entered
		var decimal_pos = input_val.indexOf(".");

		// split number by decimal point
		var left_side = input_val.substring(0, decimal_pos);
		var right_side = input_val.substring(decimal_pos);

		// add commas to left side of number
		left_side = formatNumber(left_side);

		// validate right side
		right_side = formatNumber(right_side);

		// On blur make sure 2 numbers after decimal
		if (blur === "blur") {
			right_side += "00";
		}

		// Limit decimal to only 2 digits
		right_side = right_side.substring(0, 2);

		// join number by .
		input_val = input_currency + left_side + "." + right_side;
	} else {
		// no decimal entered
		// add commas to number
		// remove all non-digits
		input_val = formatNumber(input_val);
		input_val = input_currency + input_val;

		// final formatting
		if (blur === "blur") {
			input_val += ".00";
		}
	}

	// send updated string to input
	input.val(input_val);

	// put caret back in the right position
	var updated_len = input_val.length;
	caret_pos = updated_len - original_len + caret_pos;
	input[0].setSelectionRange(caret_pos, caret_pos);
}



load_items()