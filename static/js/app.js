// ---- Estructura de datos ----
let data = {
    luz: 0,
    volar: 0,
    motores: [0, 0, 0, 0],
    joystick: {x: 0, y: 0},
    inerciales: {heading: 0, accel: 0},
}

let socket_connected = false;

// ---- Elementos del HTML ----
const drone = document.getElementById("drone");
const motor1 = document.querySelector("#motor1");
const motor2 = document.querySelector("#motor2");
const motor3 = document.querySelector("#motor3");
const motor4 = document.querySelector("#motor4");

const light = document.getElementById("droneLight");
light.style.opacity = 0;



// --- Funciones de ayuda ----
function updateEngineState(state) {
    if(state == true) {
        data.volar = 1;
        data.motores[0] = 1;
        data.motores[1] = 1;
        data.motores[2] = 1;
        data.motores[3] = 1;
    } else {
        data.volar = 0;
        data.motores[0] = 0;
        data.motores[1] = 0;
        data.motores[2] = 0;
        data.motores[3] = 0;
    }
}

function rotate() {
    x = data.joystick.y > 0? data.joystick.y * 60 : 0;
    y = data.joystick.x * 60 + 180;
    z = (-data.inerciales.heading);
    drone.style.webkitTransform = `rotateX(${x}deg) rotateY(${y}deg) rotateZ(${z}deg)`;
    drone.style.MozTransform = `rotateX(${x}deg) rotateY(${y}deg) rotateZ(${z}deg)`;
    drone.style.transform = `rotateX(${x}deg) rotateY(${y}deg) rotateZ(${z}deg)`;
}

function update() {
    data.motores[0] == true ? motor1.classList.add("propeller--on") : motor1.classList.remove("propeller--on");
    data.motores[1] == true ? motor2.classList.add("propeller--on") : motor2.classList.remove("propeller--on");
    data.motores[2] == true ? motor3.classList.add("propeller--on") : motor3.classList.remove("propeller--on");
    data.motores[3] == true ? motor4.classList.add("propeller--on") : motor4.classList.remove("propeller--on");
}

// ---- Web sockets contra el backend ----
let socket = io();
socket.on("connect", function() {
    socket_connected = true;
    socket.on('luz_1', function (msg) {
        const val = Number(msg);
        data.luz = val;
        light.style.opacity = val;
    });
    socket.on('volar', function (msg) {
        const val = Number(msg);
        updateEngineState(val);
        update();
    });
    socket.on('motor_1', function (msg) {
        // Si el está activado el vuelo
        // permito actualizar el estado del motor
        if(data.volar == true) {
            const val = Number(msg);
            data.motores[0] = msg;
            update();
        }
    });
    socket.on('motor_2', function (msg) {
        // Si el está activado el vuelo
        // permito actualizar el estado del motor
        if(data.volar == true) {
            const val = Number(msg);
            data.motores[1] = msg;
            update();
        }
    });
    socket.on('motor_3', function (msg) {
        // Si el está activado el vuelo
        // permito actualizar el estado del motor
        if(data.volar == true) {
            const val = Number(msg);
            data.motores[2] = msg;
            update();
        }
    });
    socket.on('motor_4', function (msg) {
        // Si el está activado el vuelo
        // permito actualizar el estado del motor
        if(data.volar == true) {
            const val = Number(msg);
            data.motores[3] = msg;
            update();
        }
    });
    socket.on('heading', function (msg) {        
        const val = Number(msg);
        data.inerciales.heading = val;
        rotate();
    });
    socket.on('joystick', function (msg) {        
        const joystick = JSON.parse(msg);
        data.joystick = joystick;
        rotate();
    });
});
