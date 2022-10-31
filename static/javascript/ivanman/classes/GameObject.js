class GameObject{
    /**
     * @param {number} width 
     * @param {number} height 
     * @param {number} xpos 
     * @param {number} ypos 
     */
    constructor(width, height, xpos, ypos){
        this.height = height
        this.width = width
        this.xpos = xpos
        this.ypos = ypos
    }

    setFillStyle(){
        ctx.fillStyle = "#FFAAAA"
    }

    draw(){
        this.setFillStyle()
        ctx.beginPath()
        ctx.arc(this.xpos, this.ypos, this.height, 0, 2*Math.PI, true)
        ctx.fill()
    }

    onMove(){

    }

    /**
     * @param {number} x The number of units the object should move on the X axis.
     * @param {number} y The number of units the object should move on the Y axis.
     */
    move(x, y){
        this.onMove()
        this.xpos += x
        this.ypos += y
    }

    /**
     * @returns {boolean}
     */
    canMoveLeft(){
        return mapInfo.parsed[(this.ypos)/2][((this.xpos)/2)-1] == "P" || mapInfo.parsed[(this.ypos)/2][((this.xpos)/2)-1] == "I"
    }

    /**
     * @returns {boolean}
     */
    canMoveRight(){
        return mapInfo.parsed[(this.ypos)/2][((this.xpos)/2)+1] == "P" || mapInfo.parsed[(this.ypos)/2][((this.xpos)/2)+1] == "I"
    }

    /**
     * @returns {boolean}
     */
    canMoveUp(){
        return mapInfo.parsed[((this.ypos)/2)-1][((this.xpos)/2)] == "P" || mapInfo.parsed[((this.ypos)/2)-1][((this.xpos)/2)] == "I"
    }

    /**
     * @returns {boolean}
     */
    canMoveDown(){
        return mapInfo.parsed[((this.ypos)/2)+1][((this.xpos)/2)] == "P" || mapInfo.parsed[((this.ypos)/2)+1][((this.xpos)/2)] == "I"
    }
}