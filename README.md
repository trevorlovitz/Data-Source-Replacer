# Automated Data Source Replacer
 ---
 This script can be used to automate the replacement process for SDE feature class connections in MXDs in cases where a layer's data source can be updated with a more recent version already residing within the SDE.
 ---
### Directions
---
1. Save the script within in the same folder that contains your MXD files.
2. Open the command prompt from this location and run the script.
3. When prompted, input the feature class connection you wish to replace, then the desired version.
---
### Tips
1. Once the script has finished running, you may want to check an effected layer in one of your MXDs to verify that the connection didn't break and that the datasource matches your inputted version.
2. Should new unique feature classes be added to your database, you can simply expand the dictionary to reflect that.
