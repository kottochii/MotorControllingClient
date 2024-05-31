$(document).on('click', '.keypad_key', (j) => 
{
    let value = j.target.getAttribute('data-value');
    switch(value)
    {
        case '1':case '2':case '3':case '4':case '5':case '6':case '7':case '8':case '9':case '0':
            keypadController.enterCharacter(value);
        break;
        case 'clear':
            keypadController.clear();
        break;
        case 'enter':
            keypadController.enter();
        break;
    };
});


class TimerController
{
    #current;
    #interval;
    #whole;
    #progress_bar;
    #stop = false;
    onEnd = () => {};
    constructor(initial, interval, progress_bar)
    {
        this.#current = initial;
        this.#whole = initial;
        this.#interval = interval;
        this.#progress_bar = progress_bar;
        this.#stop = false;
        setTimeout(() => {
            this.iter();
        }, this.#interval);
    }
    iter()
    {
        this.updateProgressBar();
        if(this.#stop)
            this.#current = 0;
        if(this.#current <= 0)
        {
            this.onEnd();
            return;
        }
        this.#current--;
        setTimeout(() => {
            this.iter();
        }, this.#interval);
    }
    updateProgressBar()
    {
        this.#progress_bar.value = this.#current/this.#whole;
    }
    stop()
    {
        this.#stop = true;
        this.iter();
    }
    add(amount)
    {
        this.#current = Math.min(this.#whole, this.#current + amount);
        this.updateProgressBar();
    }
};

var signedin_timer = null;
function handleState(first_argument, data = undefined)
{
    console.warn($("[data-logged-in-userdata]"));
    $("[data-logged-in-userdata]").each((x,i) =>
    {
        x.innerHTML = "";
    });
    $("[data-for-state]").hide();
    switch(first_argument)
    {
        case 'signin':
            $("[data-for-state='login']").show();
            socket.emit('get_devices');
            $("#register_card_status")[0].innerText = `To register card, put it to the reader and press "Register"`;
            let now = Math.ceil(new Date().getTime() / 1000);
            console.log(now);
            console.log(data);
            var expires_in = data.expires - now;

            console.log(expires_in);
            signedin_timer = new TimerController(expires_in * 200, 5, $("#control_panel_time_left")[0]);
            signedin_timer.onEnd = () => 
            {
                signedin_timer = null;
                console.log('times up');
                // no need for sign out here, the backend will let you know when you are signed out
            };
        break;
        case 'signout':
            $(".keypad_key").each((i, x) => {
                x.disabled = false;
            });
            $("[data-for-state='logout']").show();
            $("#login_error")[0].innerHTML = "";
            if(signedin_timer != null)
            {
                signedin_timer.stop();
                signedin_timer = null;
            }
        break;
        default:
            console.warn("State was not recognised", first_argument);
        break;
    }
}

function handleDevices(devs)
{
    let devs_container = $("#control_panel tbody[data-purpose=\"devices\"]")[0];
    devs_container.innerHTML = "";
    devs.forEach(element => {
        let table = devs_container;// ?? $("#control_panel");
        table.innerHTML += 
        `
        <tr>
        <td><code>${element.id}</code></td>
        <td>
            <button data-motor-id="${element.id}" data-action="open">open</button>
            <button data-motor-id="${element.id}" data-action="close">close</button>
        </td>
        <td>
            <span class="motor-state" data-motor-id="${element.id}">
                ONLINE: ${element.online}<br />
                OPEN_DEGREE: ${element.open_degree ?? "unknown"}<br />
                STATE: ${element.state ?? "unknown"}<br />
            </span>
        </td>
        </tr>
        `
    });
}

var keypadController;
document.addEventListener('DOMContentLoaded', () =>
{
    // make sure nothing is shown until required
    handleState({state:null});
    keypadController = new class KeypadController
    {
        #enterable = "";
        #progress_bar; #pin_appear;
        #timer = null;
        constructor(progress_bar, pin_appear)
        {
            this.#progress_bar = progress_bar;
            this.#pin_appear = pin_appear;
            this.#pin_appear.innerText = '';
        }
        enterCharacter(char)
        {
            if(this.#timer == null)
            {
                this.#timer = new TimerController(600, 10, this.#progress_bar);
                var this2 = this;
                this.#timer.onEnd = () => 
                {
                    this2.#timer = null;
                    this2.#enterable = '';
                    this2.updateEnterable();
                };
            }
            else
            {
                this.#timer.add(100);
            }
            if(this.#enterable.length >= 10)
                return;
            this.#enterable += char;
            this.updateEnterable();
        }
        updateEnterable()
        {
            let hidden_enterable = "";
            for(let i = 0; i < this.#enterable.length; i++)
            {
                hidden_enterable += '*';
            }
            this.#pin_appear.innerText = hidden_enterable;
        }
        enter()
        {
            if(this.#enterable.length == 0)
                return;
            $(".keypad_key").each((i, x) => {
                x.disabled = true;
            });
            let pin = this.#enterable;
            this.#enterable = '';
            this.updateEnterable();
            this.stopTimer();
            console.log(pin);
            socket.emit("login_attempt_pin", {pin: pin})
        }
        clear()
        {
            this.#enterable = "";
            this.updateEnterable();
            this.stopTimer();
        }
        stopTimer()
        {
            if(this.#timer != null)
            {
                this.#timer.stop();
                this.#timer = null;
            }
        }
    }($('#timer_bar')[0], $('#pin_appear')[0]);
    
}
);


$(document).on('click', '#control_panel button[data-action="open"]', (j) => 
{
    let target = (j.target)
    console.log(socket)
    socket.emit("motor_open", j.target.getAttribute('data-motor-id'))
})

$(document).on('click', '#control_panel button[data-action="close"]', (j) => 
{
    let target = (j.target)
    console.log(socket)
    socket.emit("motor_close", j.target.getAttribute('data-motor-id'))
})
$(document).on('click', '#control_panel button[data-action="signout"]', (j) => 
{
    console.log("signout")
    socket.emit("signout", {});
})
$(document).on('click', 'button#register_card_btn', (j) => 
{
    socket.emit('register_card');
    console.log(j);
    j.target.disabled = true;
})