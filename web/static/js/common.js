;
var common_ops = {
    init:function(){
        this.eventBind()
    },
    eventBind:function(){
        console.log("common.js")
    },
    buildUrl:function(path,params){
        var url = "" + path

        return url;
    }
}

$(document).ready(function(){
    common_ops.init();
})