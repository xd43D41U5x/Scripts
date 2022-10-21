static function OnBeforeRequest(oSession: Session) {
        
        //The structure of the final POST with system fingerprint info before payload.
        if (oSession.uriContains("ajaxTimeout")){
            if(oSession.utilFindInRequest('0=b&1=501',true)>-1){
            
                
                //Add anti-VM here, uncomment/change the needed items
                //oSession.utilReplaceInRequest('VMware','Dell');
                //oSession.utilReplaceInRequest('VM','Dell');
                //oSession.utilReplaceInRequest('Virtual','Dell');
                //oSession.utilReplaceInRequest('Fiddler','onedrive');
                //oSession.utilReplaceInRequest('vm','d');
                //oSession.utilReplaceInRequest('Windows%20Defender','none');
                //oSession.utilReplaceInRequest('VGAuthService','none');
                //oSession.utilReplaceInRequest('IEUser','Admin');
                //oSession.utilReplaceInRequest('%25userdnsdomain%25','prod')
              
                //As an alt to above, provide cleanData below
                var cleanData = "add clean data"
                oSession.utilSetRequestBody(cleanData);
            }
            }
        //Section for the first few comms, makes sure the referer is correct in the headers when running on your own
        if (oSession.uriContains("report")){
            //append referer to header
            oSession.oRequest["Referer"] = "addreferer.com";
            
            if ( oSession.url.Length < 85){
                //do nothing to ensure we don't mess up the wrong requests.
            }else{
                try{
                    var nDate = encodeURIComponent( + (new Date()));
                    var encoded = oSession.url;
                       
                    //replay valid response here.  Can also grab calc response and edit if needed    
                    var replay = "add valid response here to edit"
                    
                    //uri decode and b64 decode to change data
                    var replay = decodeURIComponent(replay)  
                    var data = Convert.FromBase64String(replay)
                    var decodedString = System.Text.Encoding.UTF8.GetString(data);
                    //regex to find the timestamp and update with the current
                    const rex=/\d{10,}/
                    var fixedData = decodedString.replace(rex,nDate);
                     
                    //convert back to b64 and uri encode
                    var enc = System.Text.Encoding.UTF8.GetBytes(fixedData)
                    var back = Convert.ToBase64String(enc)
                    var backenc = encodeURIComponent(back)
                    backenc = '='+ backenc
                        
                    //replace new value on the end of the url    
                    var rex2 = /\=.+/
                    var updatedU = oSession.url.replace(rex2,backenc)
                    
                    //uncomment the below to add a header value for debug
                    //oSession.oRequest["test"] = updatedU
                    oSession.url = updatedU
                }catch(e){
                    //do nothing
                }
            }
