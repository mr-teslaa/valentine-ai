function updateClock1() {
	let date = new Date();
	let nyWeekday = date.toLocaleString("en-US", {
		timeZone: "America/New_York",
		weekday: "long",
	});
	let nyTime = date.toLocaleString("en-US", {
		timeZone: "America/New_York",
		hour: "numeric",
		minute: "numeric",
		second: "numeric",
		hour12: true,
	});
	document.getElementById("nyWeekday").innerHTML = nyWeekday;
	document.getElementById("nytime").innerHTML = nyTime;
}

function updateClock2() {
	let date = new Date();
	let bdWeekday = date.toLocaleString("en-US", {
		timeZone: "Asia/Dhaka",
		weekday: "long",
	});
	let bdTime = date.toLocaleString("en-US", {
		timeZone: "Asia/Dhaka",
		hour: "numeric",
		minute: "numeric",
		second: "numeric",
		hour12: true,
	});
	document.getElementById("bdWeekday").innerHTML = bdWeekday;
	document.getElementById("bdtime").innerHTML = bdTime;
}

setInterval(updateClock1, 1000);
setInterval(updateClock2, 1000);
