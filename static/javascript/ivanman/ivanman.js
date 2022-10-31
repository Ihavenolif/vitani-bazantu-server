//CANVAS SETUP

/**
 * @type {HTMLCanvasElement}
 */
const canvas = document.getElementById("canvas")
const ctx = canvas.getContext("2d")
canvas.height = 1002
canvas.width = 1002

//VARS SETUP
/**
 * @type {Array<String>}
 */
const ucitelDict = ["", "IP tě chytila", "JK tě chytil", "JM tě chytil", "JN tě chytil", "JS tě chytil", "JK tě chytila", "KK tě chytila", "LH tě chytila", "LK tě chytila", "LP tě chytila", "LZ tě chytila", "MB tě chytil", "Mistr JF tě chytil", "MK tě chytila", "OK tě chytil", "RB tě chytila", "RP tě chytil", "RP tě chytil", "SK tě chytila", "VZ tě chytil", "JJ tě chytil", "LK tě chytila", "MV tě chytil"]
/**
 * @type {Player}
 */
const player = new Player(30,30,500,20)

/**
 * @type {Array<Coin>}
 */
let coinList = []

/**
 * @type {Array<Ghost>}
 */
let ghostList = []

ghostList.push(new Ghost(20,20,0))
ghostList.push(new Ghost(20,960,1))
ghostList.push(new Ghost(980,20,2))
ghostList.push(new Ghost(980,960,3))
ghostList.push(new Ghost(640,440,4))
ghostList.push(new Ghost(360,540,5))

/**
 * @type {number}
 */
let collectedCoins = 0
/**
 * @type {number}
 */
let totalCoins = 0
/**
 * @type {number}
 */
let totalTicks = 0



//GETTING THE MAP INFO

const mapInfo = {}

/**
 * @type {XMLHttpRequest}
 */
const xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        // Typical action to be performed when the document is ready:
        /**
         * @type {Array<Array><String>}
         */
        mapInfo.parsed = JSON.parse(LZString.decompressFromUTF16(xhttp.responseText))
        startGame()
        
    }
}
xhttp.open("POST", "http://gvnqrkod.cz:6969/getMap", true)
xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8")

/**
 * @type {XMLHttpRequest}
 */
const xhttpStart = new XMLHttpRequest();
xhttpStart.open("POST", "http://gvnqrkod.cz:5000/ivanman", true)
xhttpStart.setRequestHeader("Content-Type", "application/json;charset=UTF-8")

/**
 * @type {HTMLImageElement}
 */
const mapImageElement = document.getElementById("map-img")

/**
 * @type {HTMLCanvasElement}
 */
//const joystickCanvas = document.getElementById("joystick-canvas")
//const joystickCtx = joystickCanvas.getContext("2d")



//joystickCanvas.width = canvas.clientHeight
//joystickCanvas.height = canvas.clientHeight * 0.7


//const touchInfo = new TouchInfo(false, 0, 0)

//SETTING UP KEYBOARD EVENT DETECTION

document.addEventListener("keydown", keyDown);
/*document.addEventListener("touchstart", touchStart, false)
document.addEventListener("touchmove", touchMove, {passive: false})
document.addEventListener("touchend", touchEnd, false)*/

/**
 * @param {KeyboardEvent} evt 
 */
function keyDown(evt) {
    console.log(evt.code)
    if(evt.code == "ArrowLeft" || evt.code == "KeyA"){
        player.switchDirection = "left"
    }else if(evt.code == "ArrowRight" || evt.code == "KeyD"){
        player.switchDirection = "right"
    }else if(evt.code == "ArrowUp" || evt.code == "KeyW"){
        player.switchDirection = "up"
    }else if(evt.code == "ArrowDown" || evt.code == "KeyS"){
        player.switchDirection = "down"
    }
  }

//SETTING UP TOUCH EVENT DETECTION
/**
 * @param {TouchEvent} evt 
 */
/*function touchStart(evt){
    touchInfo.isActive = true
    touchInfo.firstXPos = evt.touches[0].pageX
    touchInfo.firstYPos = evt.touches[0].pageY
    touchInfo.lastXPos = evt.touches[0].pageX
    touchInfo.lastYPos = evt.touches[0].pageY
}*/

/**
 * @param {TouchEvent} evt 
 */
/*function touchMove(evt){
    evt.preventDefault()
    touchInfo.lastXPos = evt.touches[0].pageX
    touchInfo.lastYPos = evt.touches[0].pageY
    touchInfo.calculateAngle(evt.touches[0].pageX, evt.touches[0].pageY)
}*/

/**
 * @param {TouchEvent} evt 
 */
/*function touchEnd(evt){
    touchInfo.isActive = false
}*/

/**
 * This function will be run every frame, doing the math required for the game.
 */
function gameLoop(){
    totalTicks++
    if(player.switchDirection == "left" && player.canMoveLeft()){
        player.moveDirection = "left"
        player.switchDirection = ""
    }
    if(player.switchDirection == "right" && player.canMoveRight()){
        player.moveDirection = "right"
        player.switchDirection = ""
    }
    if(player.switchDirection == "up" && player.canMoveUp()){
        player.moveDirection = "up"
        player.switchDirection = ""
    }
    if(player.switchDirection == "down" && player.canMoveDown()){
        player.moveDirection = "down"
        player.switchDirection = ""
    }

    if(player.moveDirection == "left"){
        if(player.canMoveLeft()){
            player.move(-2,0)
        } 
    }
    if(player.moveDirection == "right"){
        if(player.canMoveRight()){
            player.move(2,0)
        } 
    }
    if(player.moveDirection == "up"){
        if(player.canMoveUp()){
            player.move(0,-2)
        } 
    }
    if(player.moveDirection == "down"){
        if(player.canMoveDown()){
            player.move(0,2)
        } 
    }
    
    draw()
}

function draw(){
    //Drawing.clearCanvas()
    Drawing.drawBackground()
    /*if(touchInfo.isActive){
        Drawing.drawJoystick()
    }*/

    for(let coin of coinList){
        coin.draw()
    }

    for(let ghost of ghostList){
        ghost.draw()
    }
    
    player.draw()
}

window.onload = () =>{
    xhttp.send(JSON.stringify({}))
    xhttpStart.send(JSON.stringify({
        request: "start_game",
        id: document.getElementById("id").value
    }))
}

/**
 * @type {interval}
 */
let gameLoopInterval = null

function startGame(){
    for(let ghost of ghostList){
        ghost.init()
    }
    player.init()
    console.log(mapInfo)
    Coin.generate()
    draw()
    setTimeout(() => {
        gameLoopInterval = setInterval(gameLoop, 1000/60)
        for(let ghost of ghostList){
            
            ghost.startMovement()
        }
    }, 1000);
    
}

/**
 * @param {boolean} win 
 */
function stopGame(win){
    clearInterval(gameLoopInterval)
    for(let ghost of ghostList){
        ghost.stopMovement()
    }

    /**
     * @type {HTMLFormElement}
     */
    const redirectForm = document.getElementById("redirect-form")
    /**
     * @type {HTMLInputElement}
     */
    const winField = document.getElementById("win")
    /**
     * @type {HTMLInputElement}
     */
    const pocetBoduField = document.getElementById("pocetBodu")
     /**
     * @type {HTMLInputElement}
     */
    const pocetCoinuField = document.getElementById("pocetCoinu")
    /**
     * @type {HTMLInputElement}
     */
    const casField = document.getElementById("cas")
    /**
     * @type {number}
     */
    const score = Math.round((Math.pow(collectedCoins,2.5)/totalTicks)*6000)/100

    if(win){
        winField.value = 1
    }else{
        winField.value = 0
        document.getElementById("bruh").play()
        
    }
    
    pocetBoduField.value = score
    pocetCoinuField.value = collectedCoins
    casField.value = Math.round((totalTicks/60)*100)/100

    setTimeout(() => {
        redirectForm.submit()
    }, 1000);

    
}