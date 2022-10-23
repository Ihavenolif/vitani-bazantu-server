class Ghost extends GameObject{
    /**
     * @param {number} xpos 
     * @param {number} ypos 
     */
     constructor(xpos, ypos){
        super()
        this.height = 20
        this.width = 20
        this.xpos = xpos
        this.ypos = ypos
    }

    /**
     * @type {string}
     */
     moveDirection = ""
     /**
      * @type {string}
      */
     switchDirection = ""

    setFillStyle(){
        ctx.fillStyle = "#000000"
    }

    checkPlayerCollision(){
        if(Math.abs(this.xpos - player.xpos) <= 10 && Math.abs(this.ypos - player.ypos) <= 10){
            alert("game over")
        }
    }

    onMove(){
        this.checkPlayerCollision()
    }

    startMovement(){
        this.movementInterval = setInterval(() => {
            if(mapInfo.parsed[this.ypos/2][this.xpos/2] == "I"){
                let canMove = false
                do{
                    let roll = Math.random()
                    if(roll < 0.25){
                        this.moveDirection = "left"
                        canMove = this.canMoveLeft()
                    }else if(roll < 0.5){
                        this.moveDirection = "right"
                        canMove = this.canMoveRight()
                    }else if(roll < 0.75){
                        this.moveDirection = "up"
                        canMove = this.canMoveUp()
                    }else{
                        this.moveDirection = "down"
                        canMove = this.canMoveDown()
                    }
                }while(!canMove)
            }

            if(this.moveDirection == "left"){
                if(this.canMoveLeft() && Math.random() < 1 - 0.005){
                    this.move(-2,0)
                } else{
                    this.moveDirection = "right"
                }
            }
            if(this.moveDirection == "right"){
                if(this.canMoveRight() && Math.random() < 1 -0.005){
                    this.move(2,0)
                } else{
                    this.moveDirection = "left"
                }
            }
            if(this.moveDirection == "up"){
                if(this.canMoveUp() && Math.random() < 1 -0.005){
                    this.move(0,-2)
                } else{
                    this.moveDirection = "down"
                }
            }
            if(this.moveDirection == "down"){
                if(this.canMoveDown() && Math.random() < 1 -0.005){
                    this.move(0,2)
                } else{
                    this.moveDirection = "up"
                }
            }
        }, 1000/60);
    }
}