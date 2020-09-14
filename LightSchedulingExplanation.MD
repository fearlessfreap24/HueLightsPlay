A little explanation on how the schduling worked.
<hr>
<p>I had made a schedule with the iOS app that was controlling the on/off time. At first, 
I started to try to manipulate the rules that the app created, but the off time never worked.</p>

here is a snippet from the rules:<br>
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
    }</code>

<p>What I found was that DX means the sensor transistioned. So the on rule means "sensor 3 transitions and the flag is equal to True".</p>
<p>DDX means the amount of time after transition. "11 hours and 15 minutes +/- 15 minutes after sensor 3 transitions to true".</p>
<p>I deleted the schedule in the iOS app and started from scratch. First thing to do was create a *[Generic State Sensor](https://developers.meethue.com/develop/application-design-guidance/how-to-use-ip-sensors/)*</p>
