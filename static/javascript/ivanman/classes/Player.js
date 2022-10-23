class Player extends GameObject{
    /**
     * @type {string}
     */
    moveDirection = ""
    /**
     * @type {string}
     */
    switchDirection = ""

    onMove(){
        for(let coin of coinList){
            coin.checkPlayerCollision()
        }
    }
}