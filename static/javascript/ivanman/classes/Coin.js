class Coin extends GameObject{
    /**
     * @param {number} xpos 
     * @param {number} ypos 
     */
     constructor(xpos, ypos){
        super()
        this.height = 3
        this.width = 3
        this.xpos = xpos
        this.ypos = ypos
    }

    setFillStyle(){
        ctx.fillStyle = "#FFFF00"
    }

    checkPlayerCollision(){
        if(Math.abs(this.xpos - player.xpos) <= 4 && Math.abs(this.ypos - player.ypos) <= 4){
            coinList.splice(coinList.indexOf(this),1)
            collectedCoins++
            if(collectedCoins == totalCoins){
                stopGame(true)
                //alert("you won, total score: " + (Math.pow(collectedCoins,2)/totalTicks).toString())
            }
        }
    }

    static generate(){
        for(var y in mapInfo.parsed){
            for(var x in mapInfo.parsed[y]){
                if(mapInfo.parsed[y][x] == "P" || mapInfo.parsed[y][x] == "I"){
                    if(x%10==0 && y%10==0){
                        var temp = new Coin(x*2, y*2)
                        coinList.push(temp)
                        totalCoins++
                    }
                }
            }
        }
    }
}