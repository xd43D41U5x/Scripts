function inspectText(){
    const bodyText = document.body.innerText;
    const regex = /[A-Za-z0-9]{10,}\={1,2}/g;
    let results = bodyText.match(regex);
    let count = 0;
    console.log("running...");
    if (results){
        results.forEach(function(item,index){ 
            if ((item.length % 4) == 0){
                console.log(item,index);
                try{
                    let decode = atob(item);
                    console.log(decode);
                    document.body.innerHTML = document.body.innerHTML.replace(item, '<mark>Convert: ' + decode + '</mark>');
                    count += 1;
                }
                catch{
                    document.body.innerHTML = document.body.innerHTML.replace(item, '<mark>FAILED Attempt: $& </mark>');
                } 
            } 
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