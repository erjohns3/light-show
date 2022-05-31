

function socketInit() {
    console.log("socket init");

    socket = new WebSocket("ws://127.0.0.1:8765");

    socket.onopen = function () {
        console.log("socket open");

        socketAttempts = 0;

        if (!socketConnected) {
            socketConnected = true;
        }
    }

    socket.onclose = function () {
        console.log("socket close");
        if (socketConnected) {
            socketConnected = false;
        }
        let delay = 3000;
        if (socketAttempts == 0) {
            delay = 0;
        }
        setTimeout(() => {
            if (socket.readyState == WebSocket.CLOSED) {
                socketInit();
            }
        }, delay);

        socketAttempts++;
    }

    socket.onerror = function () {
        console.log("socket error");
        socket.close();
    }

    socket.onmessage = function (event) {
        console.log("socket message");
        let msg = JSON.parse(event.data);
        console.log(msg);
        
        if(msg.config){
            config = msg.config
            for(let name in config){
                modeElems[name] = new ModeItem(name);
                modeListElem.append(modeElems[name]);
            }
        }

        if(msg.status){
            setRate(msg.status.rate)
            setMode(msg.status.mode)
        }
    }
}

function setRate(rate){
    rateCurr = rate;
    rateCurrElem.textContent = rateCurr + " bpm";
}

function setMode(mode){
    if (modeCurr){
        modeElems[modeCurr].classList.remove('mode-curr');
    }
    modeCurr = mode;
    if (modeCurr){
        modeElems[modeCurr].classList.add('mode-curr');
    }
    modeCurrElem.textContent = modeCurr;
}

class ModeItem extends HTMLElement {
    constructor(name) {
        super();

        this.appendChild(templateModeItem.content.cloneNode(true));

        this.name = name;

        this.nameElem = this.querySelector(".mode-name");
        this.nameElem.textContent = this.name;

        //this.colorElem = this.querySelector(".mode-color");

        this.onclick = function () {
            //event.stopPropagation();
            if (modeNext){
                modeElems[modeNext].classList.remove('mode-next');
            }
            modeNext = this.name;
            if (modeNext){
                modeElems[modeNext].classList.add('mode-next');
            }
            modeNextElem.textContent = modeNext;
        };
    }
}
customElements.define('mode-item', ModeItem);

var socket = null;
var socketConnected = false;
var socketAttempts = 0;

var modeElems = {};
var modeListElem = document.getElementById("mode-list");

var templateModeItem = document.getElementById("template-mode-item");

var config = {};

var rateCurr = 0;
var rateNext = 0;
var modeCurr = "";
var modeNext = "";

var rateCurrElem = document.getElementById("rate-curr");
var rateNextElem = document.getElementById("rate-next");
var modeCurrElem = document.getElementById("mode-curr");
var modeNextElem = document.getElementById("mode-next");

socketInit();
