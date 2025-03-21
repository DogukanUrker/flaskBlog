
// function to count visitors time spend time on post
// store in seconds in database
let initailSpendTime = 0;

// check visitorID is not null then perform fetch operation and increment
if (visiorID != null) {

    setInterval(() => {
        // increase initial spend time on every interval with 5 
        initailSpendTime += 5;

        const data = {
            visitorID: visiorID,
            spendTime: initailSpendTime,
        };
        // send data on every 5 second to store on database of visitor

        // send post request to server and update visitors time spend duration 
        fetch("/api/v1/timeSpendsDuration", {
            method: "POST",
            headers: { 'X-CSRFToken': csrfToken, "Content-Type": "application/json" },
            body: JSON.stringify(data),
            keepalive: true
        });
    }, 5000);
};

