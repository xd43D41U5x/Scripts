import frida 
import sys
import argparse

def main():
        parser = argparse.ArgumentParser(description='Dump Second Stage.')
        parser.add_argument('targets', nargs='+')
        args = parser.parse_args()

        pid = frida.spawn(args.targets)
        session = frida.attach(pid)

        script = session.create_script("""

                //Load module
                try {
                        Module.load('KERNEL32.DLL');
                } catch {
                        console.log(err);

                }

                //Get function address.
                try {
                        var vaExportAddress = Module.getExportByName("KERNEL32.dll", "HeapAlloc");
                } catch(err) {
                        console.log(err);
                }

                //Array of memory regions to monitor
                var memRegions = [];

                //Pattern to search for
                const pattern = '4d 5a 90 00';

                //Variable to hold unique file name value
                var fileNum = 1;
                //Variable to hold correct memory size
                var memsize = 0;
                

                //Configure interceptor(s)
                Interceptor.attach(vaExportAddress, 
                {   
                        onEnter: function (args) {
                                //Since HeapAlloc is called a lot only look at items with large sizes.  Can be adjusted as needed.
                                if (args[2] > 0x240000){
                                    this.sizeWatch = 1;
                                    this.vaSize = args[2].toInt32();
                                    console.log("\\nHeapAlloc called => Size: " + args[2]);
                                }
                        },
                        onLeave: function (retval) { 
                            if(this.sizeWatch){  
                                console.log("HeapAlloc returned => Address: " + retval);
                                memRegions.push({memBase:ptr(retval), memSize:this.vaSize});
                            }
                            
                                for(var i = 0; i < memRegions.length; i++){
                                    fileNum++;
                                    memsize = memRegions[i].memSize
                                    Memory.scan(memRegions[i].memBase, memRegions[i].memSize, pattern, {
                                        onMatch(address, size) {
                                            try {
                                                var binContent = address.readByteArray(memsize);
                                                var filename = "dump_mz"+fileNum+".bin";
                                                var file = new File(filename, "wb");        
                                                file.write(binContent);
                                                file.flush();
                                                file.close();
                                                console.log('\\nMemory.scan() found match at', address,'with size', size);
                                                console.log("Dumped file: " + filename);  
                                                
                                            } catch(err) {
                                                    //Skip on error due to mem access issues
                                            } 
                                        }
                                    });
                                }    
                        }
                });
                """)

        script.load()
        frida.resume(pid)
        sys.stdin.read()
        session.detach()

if __name__ == '__main__':
        main()
