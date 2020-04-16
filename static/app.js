handleClick2 = async url => {
	try {
		let res = await fetch(url, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				msg: 'hello',
			}),
		});
		return;
	} catch (err) {
		console.log('fetch error :', err);
	}
};

const handleClick = () => {
	let shipIt = document.getElementById('form-mehh');
	shipIt.submit();
};
