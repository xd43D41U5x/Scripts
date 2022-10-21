function inspectText(){
    const bodyText = document.body.innerText;
    const regex = /\%2\)/g;
    let results = bodyText.match(regex);
    let count = 0;
    let output = "";
    if (results){
        results.forEach(function(item,index){
            console.log(item,index);
            document.body.innerHTML = document.body.innerHTML.replace(item, '<mark>Convert: ' + item + '</mark>');
            count += 1;
            
        });
        
        chrome.runtime.sendMessage({type: "notification", options: { 
            type: "basic", 
            iconUrl: '/images/goose48.png',
            title: "Results",
            message: "Found " + results.length + " matches indicating possible SocGholish.\n Review looking for %2) as indicator of string deob.",
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