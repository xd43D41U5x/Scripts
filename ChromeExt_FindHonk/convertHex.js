function inspectText(){
    const bodyText = document.body.innerText;
    const regex = /0?\\?[xX][0-9a-fA-FxX,\\]{10,}/g;
    let results = bodyText.match(regex);
    let count = 0;
    let output = "";
    if (results){
        results.forEach(function(item,index){
            console.log(item,index);
            if (item.includes("\\")){
                output ="";
                fixeditem = item.replace(/\\/,'0');
                fixeditem = fixeditem.replace(/\\/g,',0');
                fixeditem = fixeditem.split(",");
                fixeditem.forEach(function(item,index){
                    output += String.fromCharCode(item);
                  });
                console.log(output);
            }
            document.body.innerHTML = document.body.innerHTML.replace(item, '<mark>Convert: ' + output + '</mark>');
            count += 1;
            
        });
        
        chrome.runtime.sendMessage({type: "notification", options: { 
            type: "basic", 
            iconUrl: '/images/goose48.png',
            title: "Results",
            message: "Found " + results.length + " matches.\n Able to convert " + count + "/" + results.length,
        }});
    }
    else{
        chrome.runtime.sendMessage({type: "notification", options: { 
            type: "basic", 
            iconUrl: '/images/goose48.png',
            title: "Results",
            message: "No Matches Found"
        }});
    }
}
       
 inspectText();