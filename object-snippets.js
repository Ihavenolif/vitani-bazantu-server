/**
 * @param {string} kokot
 * @returns {string} string
 */
 function test(kokot){
    console.log(kokot)
    return kokot + kokot
}

class gameObject {
    /**
     * 
     * @param {number} xpos 
     * @param {number} ypos 
     */
    constructor(xpos, ypos){
        this.xpos = xpos
        this.ypos = ypos
    }
}

class Player extends gameObject{

}

const object = new gameObject(50,100)

console.log(object)