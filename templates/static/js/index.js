$('document').ready(function() {
	// add class .default to input element to focus keyboard cursor on page load
	// not actually used so I havent tested this yet.. :)
	defaultInputEl = $(':input.default').first();
	if (defaultInputEl) {
		defaultInputEl.focus();
	}
});
