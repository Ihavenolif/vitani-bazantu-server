class Player extends GameObject{
    /**
     * @type {string}
     */
    moveDirection = "down"
    /**
     * @type {string}
     */
    switchDirection = ""
    /**
     * @type {Number}
     */
    ticksToModeSwitch = 0
    /**
     * @type {boolean}
     */
    open = false

    init(){
        this.ivani = {
            closed: {
                right: document.getElementById("ivan-closed-r"),
                left: document.getElementById("ivan-closed-l"),
                up: document.getElementById("ivan-closed-u"),
                down: document.getElementById("ivan-closed-d")
            },
            open: {
                right: document.getElementById("ivan-open-r"),
                left: document.getElementById("ivan-open-l"),
                up: document.getElementById("ivan-open-u"),
                down: document.getElementById("ivan-open-d")
            }
        }
    }

    onMove(){
        for(let coin of coinList){
            coin.checkPlayerCollision()
        }
        if(++this.ticksToModeSwitch == 20){
            this.open = !this.open
            this.ticksToModeSwitch = 0
        }
    }

    draw(){
        if(this.open){
            var status = "open"
        }else{
            var status = "closed"
        }
        console.log(this.ivani)
        ctx.drawImage(this.ivani[status][this.moveDirection], this.xpos-30, this.ypos-30, 60, 60)
    }
}