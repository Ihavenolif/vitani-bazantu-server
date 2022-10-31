class Drawing {
    static clearCanvas(){
        ctx.fillStyle = "#FFFFFF"
        ctx.fillRect(0,0,1000,1000)
        ctx.fill()

        /*joystickCtx.fillStyle = "#FFFFFF"
        joystickCtx.fillRect(0,0,1000,1000)
        joystickCtx.fill()*/
    }

    static drawBackground(){
        ctx.drawImage(mapImageElement,0,0)
    }

    static drawJoystick(){
        console.log(touchInfo.lastYPos)
        joystickCtx.fillStyle = "#ddd"
        joystickCtx.beginPath()
        joystickCtx.arc(touchInfo.firstXPos, touchInfo.firstYPos - canvas.clientHeight, 20, 0, 2*Math.PI)
        joystickCtx.fill()

        if(touchInfo.abs > 80){
            var x = 80*Math.cos(touchInfo.angle) + touchInfo.firstXPos
            var y = 80*Math.sin(touchInfo.angle) + touchInfo.firstYPos - canvas.clientHeight
        }else{
            var x = touchInfo.lastXPos
            var y = touchInfo.lastYPos - canvas.clientHeight
        }

        joystickCtx.beginPath()
        joystickCtx.arc(x, y, 10, 0, 2*Math.PI)
        joystickCtx.fill()

        joystickCtx.strokeStyle = "#aaa"
        joystickCtx.beginPath()
        joystickCtx.moveTo(touchInfo.firstXPos, touchInfo.firstYPos - canvas.clientHeight)
        joystickCtx.lineTo(x, y)
        joystickCtx.stroke()
    }
}