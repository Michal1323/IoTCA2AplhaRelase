var alive_second = 0;
var heartbeat_rate = 5000;

var myChannel = "IOTCA";


sendEvent("get_auth_key");

pubnub = new PubNub({
        publishKey : "pub-c-4b294d7e-8be1-4dff-9ba7-d18d80953efd",
        subscribeKey : "sub-c-019b1a54-34ce-11eb-99ef-fa1b309c1f97",
        uuid: "ec0f9ad2-37e5-11eb-adc1-0242ac120002"
})

function keep_alive()
{
	var request = new XMLHttpRequest();
	request.onreadystatechange = function(){
		if(this.readyState === 4){
			if(this.status === 200){
				if(this.responseText !== null){
					var date = new Date();
					alive_second = date.getTime();
					var keep_alive_data = this.responseText;
					console.log(keep_alive_data);
					var json_data = this.responseText;
					var json_obj = JSON.parse(json_data);
					if(json_obj.motion == 1){
						document.getElementById("Motion_id").innerHTML = "Intruder Detected";
					}
					else{
						document.getElementById("Motion_id").innerHTML = "All safe";
					}
				}
			}
		}
	};
	request.open("GET","keep_alive", true);
	request.send(null);
	setTimeout('keep_alive()', heartbeat_rate);
}


function time(){
	var d = new Date();
	var current_sec = d.getTime();
	if(current_sec - alive_second > heartbeat_rate + 1000){
		document.getElementById("Connection_id").innerHTML = " Dead";
	}
	else{
		document.getElementById("Connection_id").innerHTML = " Alive";
	}
	setTimeout('time()', 1000);
}

function handleClick(cb){
	if(cb.checked)
	{
		value = true;
	}
	else
	{
		value = false;
	}
	var btnStatus = new Object();
	btnStatus[cb.id] = value;
	var event = new Object();
	event.event = btnStatus;
	console.log("Calling publishUpdate from handleClick");
	publishUpdate(event, myChannel);
}



pubnub.addListener({
        status: function(statusEvent) {
            if (statusEvent.category === "PNConnectedCategory") {
                console.log("Connected to PubNub");
            }
            else
            {
                console.log("Not Connected");
            }
        },
    message: function(message) {
        var msg = message.message;
       console.log(msg);
       document.getElementById("Bedroom_id").innerHTML = msg["Bedroom"];
       document.getElementById("Frontdoor_id").innerHTML = msg["FrontDoor"];
       document.getElementById("Hallway_id").innerHTML = msg["Hallway"];
       document.getElementById("Backdoor_id").innerHTML = msg["Backdoor"];
       sendBackDoorData();
       sendBedroomData();
       sendFrontDoorData();
       sendHallwayData();

    },
    presence: function(presenceEvent) {
            // This is where you handle presence. Not important for now :)
    }
})


function subscribe(){
    pubnub.subscribe({
           channels: [myChannel]
    },
    function(status, response){
    if(status.error)
    {
        console.log("subscribe failed", status)
    }
    else{
        console.log("Subscribe Success", status)
    }
    });
}


function publishUpdate(data, channel){
pubnub.publish({
    channel: channel,
    message: data
    },
    function(status, response){
        if(status.error){
        console.log(status)
        }
         else{
              console.log("Message published with timetoken", response.timetoken)
             }

        }
    );
}

function logout(){

    console.log("Logging out and unsubscribing");
    pubnub.unsubscribe({
        channels: [myChannel]
    });
    location.replace("/logout")

}

function handleButtonClick(b)
{
    var grantUserNameID = b.id.split("-")[1]
    var read_state = document.getElementById("read-"+grantUserNameID).checked
    var write_state = document.getElementById("write-"+grantUserNameID).checked
    sendEvent("grant-"+grantUserNameID+"-"+read_state+"-"+write_state)
}
function sendFrontDoorData()
{
    var front = document.getElementById("Frontdoor_id")
    var pos = "Frontdoor"
    sendEvent("FrontDoor-"+front +"-"+pos)
}
function sendBackDoorData()
{
    var pos2 = "Backdoor"
    var backdoor = document.getElementById("Backdoor_id")
    sendEvent("BackDoor-"+backdoor+"-"+pos2)
}
function sendHallwayData()
{
    var pos3 = "Hallway"
    var hallway = document.getElementById("Hallway_id")
    sendEvent("Hallway-"+hallway+"-"+pos3)
}
function sendBedroomData()
{
    var pos4 = "Bedroom"
    var bedroom = document.getElementById("Bedroom_id")
    sendEvent("Bedroom-"+bedroom+"-"+pos4)
}

function sendEvent(value){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if(this.readyState === 4){
            if(this.status ===200){
                if(this.responseText !== null)
                {
                    try{
                        var json_data = this.responseText;
                        var json_obj = JSON.parse(json_data);
                        if (json_obj.hasOwnProperty("authKey")){
                            pubnub.setAuthKey(json_obj.authKey);
                            pubnub.setCipherKey(json_obj.cipherKey);
                            console.log("Auth key set!" + this.responseText);
                            subscribe();
                        }

                        if(json_obj.hasOwnProperty("access")){
                            if(json_obj.access == "granted"){
                                console.log("access-granted");
                                subscribe();
                            }
                        }
                    }
                    catch(e){
                        console.log("Cant extract the json: " + this.responseText);
                    }
                }
            }
        }
    }
    console.log("Sending ajax " + value);
    request.open("POST", value, true);
    request.send(null);
}
