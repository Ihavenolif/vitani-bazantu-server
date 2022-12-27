class Ghost extends GameObject{
    /**
     * @param {number} xpos 
     * @param {number} ypos 
     * @param {number} id
     */
     constructor(xpos, ypos, id){
        super()
        this.height = 20
        this.width = 20
        this.xpos = xpos
        this.ypos = ypos
        this.id = id
    }

    init(){
        this.image = document.getElementById("ucitel-img-" + this.id.toString())
    }

    /**
     * @type {HTMLImageElement}
     */
    image
    /**
     * @type {number}
     */
    id
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

    draw(){
        ctx.drawImage(this.image, this.xpos-30, this.ypos-30, 60, 60)
    }

    checkPlayerCollision(){
        let deltaX = this.xpos - player.xpos
        let deltaY = this.ypos - player.ypos
        if(Math.sqrt(Math.pow(deltaX, 2) + Math.pow(deltaY, 2)) < 15){
            document.getElementById("ucitel").value = ucitelDict[ucitele[this.id]]
            stopGame(false)
        }
    }

    onMove(){
        this.checkPlayerCollision()
    }

    startMovement(){
        /**
         * @type {}
         */
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
        }, 1000/70);
    }

    stopMovement(){
        clearInterval(this.movementInterval)
    }
}