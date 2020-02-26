DIR = getDirectory("select the input folder");
targetFolder = getDirectory("select the output folder");
files = getFileList(DIR);
Min_IMSIZE = 512;
constrain = " ";
Channel_order = "2,3,1,4" // GRFB

setBatchMode(true);
run("Bio-Formats Macro Extensions");

for (k=0; k<5; k++) {
	print(now() + ": New Export session...");
	for (n=0; n<files.length; n++) {
		if (endsWith(files[n], ".nd2")) { 
			id = DIR + files[n];
			Ext.setId(id);
			Ext.getSeriesCount(seriesCount);
			print(seriesCount+" series in "+id);
			for (i=0; i<seriesCount; i++) {
				run("Bio-Formats Importer", "open=["+id+"] color_mode=Grayscale view=Hyperstack stack_order=XYCZT use_virtual_stack series_"+(i+1));
				
				getDimensions(width, height, channels, slices, frames);
				origTitle = getTitle();
				split_Title = split(origTitle, ".");
				Im_id = split_Title[0];
				run("Split Channels");
		
				// --- Optional: separately saving Brightfield imgage, 8-bit converted.
				selectImage("C5-" + origTitle);
				//run("Make Substack...","slices=4");
				//run("8-bit");
				//save(targetFolder + "/BF_" + Im_id + "_"+ (i+1) + ".tiff");
				close();
				//print("saved BF image for " + Im_id + "_" + (i+1));
				
				//8-bit conversion:
				//Experimented with 8-bit conversion on stack vs conversion before stacking... 
				//8-bit conversion prior to stacking appears to preserve brightness differences in individual images,
				//and hence likely preserves more information.
				selectImage("C1-" + origTitle);
				run("Z Project...", "start=1 stop="+slices+" projection=[Max Intensity]");
				run("8-bit");
				
				selectImage("C2-" + origTitle);
				run("Z Project...", "start=1 stop="+slices+" projection=[Max Intensity]");
				run("8-bit");
				
				selectImage("C3-" + origTitle);
				run("Z Project...", "start=1 stop="+slices+" projection=[Max Intensity]");
				run("8-bit");
				
				selectImage("C4-" + origTitle);
				run("Z Project...", "start=1 stop="+slices+" projection=[Max Intensity]");
				run("8-bit");
				
				selectImage("C1-" + origTitle);
				close();
				selectImage("C2-" + origTitle);
				close();
				selectImage("C3-" + origTitle);
				close();
				selectImage("C4-" + origTitle);
				close();
			
				run("Images to Stack", "name=[Stack]");
				run("Make Substack...", " slices="+Channel_order);
				run("Size...", "width=&Min_IMSIZE height=&Min_IMSIZE" +constrain+ "average interpolation=Bicubic");
	
				saveAs("tiff", targetFolder + "/" + Im_id + "_"+ (i+1) + ".tiff");
				print(now() + ": Saved Stack for" + Im_id + "_" + (i+1) + "/" + seriesCount);
		
		//		Ext.getSeries(seriesNum);
		//		print("Series# is" + seriesNum);
				run("Close All");
			}
		}
	}
}
setBatchMode(false);
print("Export : Ends at " + now() );
showMessage("Done! Processed "+n+" files and "+i+" series!");
Ext.close();

function now(){
	getDateAndTime(year, month, dayOfWeek, dayOfMonth, hour, minute, second, msec);
	nowValue = ""+IJ.pad(hour,2)+":"+IJ.pad(minute,2)+":"+IJ.pad(second,2);
	return nowValue;
}
