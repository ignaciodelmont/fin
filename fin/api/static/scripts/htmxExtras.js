// htmxs doesn't emit the formData event, so I have to intercept the request and add the form data as request parameters
// stolen from https://github.com/bigskysoftware/htmx/issues/1323

document.addEventListener('htmx:configRequest', (event) => {
    if (event.target.tagName === "FORM") {
	const formData = new FormData(event.target);

	// add the form data as request parameters
	for (const pair of formData.entries()) {
	    const name = pair[0];
	    const value = pair[1];

	    const parameters = event.detail.parameters;

	    // for multivalued form fields, FormData.entries() may contain multiple entries with the same name
	    if (parameters[name] == null) {
		parameters[name] = [value]; // single element array
	    } else if (Array.isArray(parameters[name]) && !parameters[name].includes(value)) {
		parameters[name].push(value);
	    }
	}
    }
});

