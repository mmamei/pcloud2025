

$(document).ready(function(){
    $('#btn').click(function(){

        var data = 'sensor1, 10\nsensor2, 40\nsensor3, 70\nsensor1, 100'
        var d = {}
        
        for (var line of data.split('\n')) {
            line = line.split(', ')
            var sensor = line[0] 
            var value = line[1]
            if (!(sensor in d)) {
                d[sensor] = []
            }
            d[sensor].push(Number(value))
        }
        
        $("#d1").html(JSON.stringify(d))
        


    
    })
})
   

