/**
 * @type {HTMLCanvasElement}
 */
const canvas = document.getElementById("canvas")
const ctx = canvas.getContext("2d")
/**
 * @type {HTMLCanvasElement}
 */
//const joystickCanvas = document.getElementById("joystick-canvas")
//const joystickCtx = joystickCanvas.getContext("2d")

canvas.height = 1000
canvas.width = 1000

//joystickCanvas.width = canvas.clientHeight
//joystickCanvas.height = canvas.clientHeight * 0.7

const player = new Player(20,20,100,100)
//const touchInfo = new TouchInfo(false, 0, 0)

/**
 * @type {number}
 */
let coinCount = 0

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
        player.moveDirection = "left"
    }else if(evt.code == "ArrowRight" || evt.code == "KeyD"){
        player.moveDirection = "right"
    }else if(evt.code == "ArrowUp" || evt.code == "KeyW"){
        player.moveDirection = "up"
    }else if(evt.code == "ArrowDown" || evt.code == "KeyS"){
        player.moveDirection = "down"
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
    if(player.moveDirection == "left"){
        player.move(-3,0)
    }
    if(player.moveDirection == "right"){
        player.move(3,0)
    }
    if(player.moveDirection == "up"){
        player.move(0,-3)
    }
    if(player.moveDirection == "down"){
        player.move(0,3)
    }

    Drawing.clearCanvas()
    /*if(touchInfo.isActive){
        Drawing.drawJoystick()
    }*/
    
    player.draw()
}

const gameLoopInterval = setInterval(gameLoop, 1000/60);