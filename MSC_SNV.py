def msc(input_data, reference=None):
    eps = np.finfo(np.float32).eps
    input_data = np.array(input_data, dtype=np.float64)
    ref = []
    ''' Perform Multiplicative scatter correction'''
    # mean centre correction
    for i in range(input_data.shape[0]):
        input_data[i,:] -= input_data[i,:].mean()
        # Get the reference spectrum. If not given, estimate it from the mean     

    # Define a new array and populate it with the corrected data    
    data_msc = np.zeros_like(input_data)
    for i in range(input_data.shape[0]):
        for j in range(0, sampleCount, 10):
            ref.append(np.mean(input_data[j:j+10], axis=0))
            # Run regression
            fit = np.polyfit(ref[i], input_data[i,:], 1, full=True)
            # Apply correction
            data_msc[i,:] = (input_data[i,:] - fit[0][1]) / fit[0][0]
    
    return data_msc
	

def snv(input_data):
  
    # Define a new array and populate it with the corrected data  
    data_snv = np.zeros_like(input_data)
    for i in range(data_snv.shape[0]):

        # Apply correction
        data_snv[i,:] = (input_data[i,:] - np.mean(input_data[i,:])) / np.std(input_data[i,:])
    
    return data_snv
	

# SNV 
x = wavelengths
# substitute individualSamples[0] to individualSamples[1],individualSamples[2]... to get individual spectra
for i in range(0,sampleCount):
    y = snv(individualSample[i])
	

    cmap = plt.get_cmap('jet')

    ys = [i for i in y]
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(np.min(ys), np.max(ys))
    line_segments = LineCollection([np.column_stack([x, y]) for y in ys],
                               linewidths=1,
                               linestyles='solid',
                               alpha = 0.4)


    ax.add_collection(line_segments)
    # axcb = fig.colorbar(line_segments)
    # axcb.set_label(target,fontsize =16)
    # ax.set_xlabel("wavelength", fontsize = 16)
    plt.title("Standard Normal Variate (SNV) of sample %i" % (i+1),  fontsize = 16)
    plt.show()
	
	
# MSC 
x = wavelengths
# substitute individualSamples[0] to individualSamples[1],individualSamples[2]... to get individual spectra
for i in range(0,sampleCount):
    y = msc(individualSample[i])
	

    cmap = plt.get_cmap('jet')

    ys = [i for i in y]
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(np.min(ys), np.max(ys))
    line_segments = LineCollection([np.column_stack([x, y]) for y in ys],
                               linewidths=1,
                               linestyles='solid',
                               alpha = 0.4)


    ax.add_collection(line_segments)
    # axcb = fig.colorbar(line_segments)
    # axcb.set_label(target,fontsize =16)
    # ax.set_xlabel("wavelength", fontsize = 16)
    plt.title("Standard Normal Variate (SNV) of sample %i" % (i+1),  fontsize = 16)
    plt.show()
	

# Apply z score on the raw data
import numpy as np
from collections import Counter
# Return the coordinates, Where the first array in each line is the row indexes of the outlier, and the second array is the column indices.
def zscorefunction(arrayMatrix, threshold=1):
    zscore = (arrayMatrix - np.median(arrayMatrix))/arrayMatrix.std()
    return np.where(np.abs(zscore) > threshold)
	
	

# A z-score is the number of standard deviations away from a mean for a data point. 
# A z-score helps point out how unusual or usual a data point is from the other values.

deleteSpectra = []

for i in range(0,sampleCount):
    # Extract the spectra numbers
    x = zscorefunction(individualSample[i])[0]
    # print sample number and spectra number with its corresponding number of outlier points
    print("\nSAMPLE",i+1)
    print(Counter(x))
    
    for j in range(0,individualSample[i].shape[0]):
        # If the sepctra contains more than 75% of points as outliers, delete the spectra
        if (Counter(x)[j] > 107):
            deleteSpectra.append(j)
            
    individualSample[i] = np.delete(individualSample[i], deleteSpectra, 0)
    print ("Delete Spectra:",deleteSpectra)
    del deleteSpectra[:]
