class GameObject{
    /**
     * 
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

    draw(){
        ctx.strokeStyle = "#000000"
        ctx.beginPath()
        ctx.arc(this.xpos, this.ypos, this.height, 0, 2*Math.PI, true)
        ctx.stroke()
    }

    /**
     * @param {number} x The number of units the object should move on the X axis.
     * @param {number} y The number of units the object should move on the Y axis.
     */
    move(x, y){
        this.xpos += x
        this.ypos += y
    }
}