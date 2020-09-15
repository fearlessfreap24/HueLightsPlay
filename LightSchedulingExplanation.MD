A little explanation on how the schduling worked.
<hr>
<p>I had made a schedule with the iOS app that was controlling the on/off time. At first, 
I started to try to manipulate the rules that the app created, but the off time never worked.</p>

<p>here is a snippet from the rules:<br>
Rule for on<br>
    <code>{'conditions': 
        [
            {
                'address': '/sensors/3/state/flag',
                'operator': 'eq','value': 'true'
            },
            {
                'address': '/sensors/3/state/flag',
                'operator': 'dx'
            }
        ]
    }</code>

Rule for off<br>
    <code>{'conditions': 
        [
            {
                'address': '/sensors/3/state/flag',
                'operator': 'eq','value': 'true'
            },
            {
                'address': '/sensors/3/state/flag',
                'operator': 'ddx',
                'value': 'PT11:15:00A15:00'
            }
        ]
    }</code></p>
<p>What I found was that DX means the sensor transistioned. So the on rule means "sensor 3 transitions and the flag is equal to True".</p>
<p>DDX means the amount of time after transition. "11 hours and 15 minutes +/- 15 minutes after sensor 3 transitions to true".</p>
<p>Manipulating the schedule for the lights to turn on was working great. However, manipulating the rule to turn the lights off was not working.</p>
<p>I deleted the schedule in the iOS app and started from scratch. First thing to do was create a <a href="https://developers.meethue.com/develop/application-design-guidance/how-to-use-ip-sensors/">Generic State Sensor.</a></p>
<p>Then two schedules were <a href="https://developers.meethue.com/develop/hue-api/3-schedules-api/#create-schedule">created.</a></p>
<p>Schedule for On:<br><code>{
    "name": "Turn on Outside",
    "command": {
        "address": "/api/<username>/sensors/7/state/",
        "method": "PUT",
        "body": {
            "flag": true
        }
    },
    "localtime": "W127T19:45:40A10:00"
    }</code><br>
    Schedule for Off:<br>
    <code>{
    "name": "Turn off Outside",
    "command": {
        "address": "/api/<username>/sensors/7/state/",
        "method": "PUT",
        "body": {
            "flag": false
        }
    },
    "localtime": "W127T07:11:40A10:00"
        }</code></p>
<p>W127 is a bit mask for the days of the week. 0MTWRFSS = 01111111 = 127. Example, Moday only would be 01000000 = 64 and Saturday and Sunday would be 00000011 = 3</p>
<p>The idea here is that the sensor will be used as a light switch. at 7:45PM and 40 seconds +/- 10 minutes the switch will be turned on (set to true).
    Then, at 07:11AM and 40 seconds +/- 10 minutes the switch will get turned off (set to false).</p>
<p>Sensors trigger rules. Two rules were <a href="https://developers.meethue.com/develop/hue-api/6-rules-api/#create-rule">created.</a></p>
<p>Rule for lights on:<br><code>
    {  "name":"outside on",
   "conditions":[
        {"address":"/sensors/7/state/flag","operator":"eq","true"},
        {"address":"/sensors/7/state/flag","operator":"DX"}
   ],
   "actions":[    
        {"address":"/groups/0/action","method":"PUT", "body":{"on":"true"}}
    ]}</code><br>
    Rule for lights off:<br><code>
     {  "name":"outside on",
   "conditions":[
        {"address":"/sensors/7/state/flag","operator":"eq","flase"},
        {"address":"/sensors/7/state/flag","operator":"DX"}
   ],
   "actions":[    
        {"address":"/groups/0/action","method":"PUT", "body":{"on":"false"}}
    ]}
