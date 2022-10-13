class TouchInfo{
    /**
     * @param {number} firstXPos 
     * @param {number} firstYPos 
     */
    constructor(firstXPos, firstYPos){
        this.firstXPos = firstXPos
        this.firstYPos = firstYPos
    }

    /**
     * @type {boolean}
     */
    isActive = false
    /**
     * @type {number}
     */
    firstXPos = 0
    /**
     * @type {number}
     */
    firstYPos = 0
    /**
     * @type {number}
     */
    angle = 0
    /**
     * @type {number}
     */
    lastXPos = 0
     /**
      * @type {number}
      */
    lastYPos = 0
     /**
      * @type {number}
      */
    abs = 0

    calculateAngle(){
        let x = this.lastXPos - this.firstXPos
        let y = this.lastYPos - this.firstYPos

        this.abs = Math.sqrt((x*x)+(y*y))

        if(x >= 0 && y >= 0){
            this.angle = Math.asin(y/this.abs)
        }else if(x <= 0 && y >= 0){
            this.angle = Math.acos(x/this.abs)
        }else if(x <= 0 && y <= 0){
            this.angle = Math.asin((y*-1)/this.abs) + Math.PI
        }else if(x >= 0 && y <= 0){
            this.angle = Math.acos((x*-1)/this.abs) + Math.PI
        }
    }
}