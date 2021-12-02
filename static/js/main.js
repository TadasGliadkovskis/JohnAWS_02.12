var aliveSecond = 0;
var heartbeatRate = 5000;

var my_channel = "tadas-pi-channel"

function keepAlive()
{
	var request = new XMLHttpRequest();
	request.onreadystatechange = function(){
		if(this.readyState === 4){
			if(this.status === 200){
				if(this.responseText !== null){
					var date = new Date();
					aliveSecond = date.getTime();
					var keepAliveData = this.responseText;
					//convert string to JSON
				}
			}
		}
	};
	request.open("GET", "keep_alive", true);
	request.send(null);
	setTimeout('keepAlive()', heartbeatRate);
}

pubnub = new PubNub({
            publishKey : "pub-c-46fbdcc7-699c-43e3-a9a3-d6a5ef9068f2",
            subscribeKey : "sub-c-73bed68a-3c06-11ec-b886-526a8555c638",
            uuid: "f2904319-88d0-424b-9ca5-8523c26d84b6"
        })

pubnub.addListener({
        status: function(statusEvent) {
            if (statusEvent.category === "PNConnectedCategory") {
                console.log("Success connected PubNub main.js");
                publishSampleMessage();
            }
        },
        message: function(msg) {
            console.log(msg.message.title);
            console.log(msg.message.description);
        },
        presence: function(presenceEvent) {
            // This is where you handle presence. Not important for now :)
        }
    })


function time()
{
	var d = new Date();
	var currentSec = d.getTime();
	if(currentSec - aliveSecond > heartbeatRate + 1000)
	{
		document.getElementById("Connection_id").innerHTML = "DEAD";
	}
	else
	{
		document.getElementById("Connection_id").innerHTML = "ALIVE";
	}
	setTimeout('time()', 1000);
}

pubnub.subscribe({channels: [my_channel]});

function publishUpdate(data, channel) {
    pubnub.publish({
    channel: channel,
    message: data
    },
    function(status,response){
        if(status.error){
            console.log(status);
	  }
        else{
            console.log("Message published with timetoken",response.timetoken)
        }
    }
    );
}

function handleClick(cb)
{
	if(cb.checked)
	{
		value = "ON";
	}
	else
	{
		value = "OFF";
	}
	var ckbStatus = new Object();
	ckbStatus[cb.id] = value;
	var event = new Object();
	event.event = ckbStatus;
	publishUpdate(event, my_channel);
}

function logout()
{
    console.log("Logging out and unsubscribing");
    pubnub.unsubscribe({
    channels: [my_channel]
    })
    location.replace("/logout")
}