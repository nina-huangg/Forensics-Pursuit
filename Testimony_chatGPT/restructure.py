#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 18:14:10 2025

@author: nina
"""
#### import
import os 
import numpy as np
import glob
import matplotlib.pyplot as plt
import mne
import mne_connectivity
from pymatreader import read_mat
from mne_icalabel import label_components, iclabel

# file path
# file_path = "/Users/nina/Desktop/02010002erp 20150416 1131.raw"

# Sampling frequency read from metadata
SFREQ = 250

# For power bands. Note no gamma because we'll be bandpass filtering 1-40 Hz and so gamma woul be truncated
freqs = {"theta": (4, 7), "alpha": (8, 12), "beta": (13, 25)}#, "gamma": (30, 45)}

# set montage
montage = mne.channels.make_standard_montage('GSN-HydroCel-128')
#montage_3d= mne.viz.plot_montage(montage, kind='3d', scale=0.5)
#montage_topomap = mne.viz.plot_montage(montage, kind='topomap',scale=0.5)

# variables
eeg_ch_names = []
participant_files = []

# participant group
info = {
    "02010002": "MDD",
    "02010004": "MDD",
    "02010005": "MDD",
    "02010006": "MDD",
    "02010008": "MDD",
    "02010010": "MDD",
    "02010011": "MDD",
    "02010012": "MDD",
    "02010013": "MDD",
    "02010015": "MDD",
    "02010016": "MDD",
    "02010018": "MDD",
    "02010019": "MDD",
    "02010021": "MDD",
    "02010022": "MDD",
    "02010023": "MDD",
    "02010024": "MDD",
    "02010025": "MDD",
    "02010026": "MDD",
    "02010028": "MDD",
    "02010030": "MDD",
    "02010033": "MDD",
    "02010034": "MDD",
    "02010036": "MDD",
    "02020008": "HC",
    "02020010": "HC",
    "02020013": "HC",
    "02020014": "HC",
    "02020015": "HC",
    "02020016": "HC",
    "02020018": "HC",
    "02020019": "HC",
    "02020020": "HC",
    "02020021": "HC",
    "02020022": "HC",
    "02020023": "HC",
    "02020025": "HC",
    "02020026": "HC",
    "02020027": "HC",
    "02020029": "HC",
    "02030002": "HC",
    "02030003": "HC",
    "02030004": "HC",
    "02030005": "HC",
    "02030006": "HC",
    "02030007": "HC",
    "02030009": "HC",
    "02030014": "HC",
    "02030017": "HC",
    "02030018": "HC",
    "02030019": "HC",
    "02030020": "HC",
    "02030021": "HC"
}

####################### begin pipeline ####################### 
# get subject ID
def get_subject_info(filename):
    print(filename)
    subject_id = filename[:8]
    subject_group = info[subject_id]
    
    return subject_id, subject_group

# reading data
def read_data(file_path):
    raw = mne.io.read_raw_egi(file_path)
    return raw

# drop channels
def clean_channels(raw):
    raw.drop_channels('E129') #drop value because 'zero value'
    raw.set_montage(montage)

    # pick channels
    raw_eeg = raw.copy().pick(picks=["eeg", "stim"])
    
    # plot psd
    #raw_eeg.compute_psd().plot()
    
    # set channel names
    #ch_names = raw_eeg.ch_names
    eeg_ch_names = raw.copy().pick(picks=["eeg"]).ch_names
    
    return raw_eeg

# create copy to start preprocessing
def create_copy(raw_eeg):
    raw_eeg_filter = raw_eeg.copy()
    raw_eeg_filter.load_data()
    raw_eeg_filter.set_eeg_reference('average')
    return raw_eeg_filter

# NOTCH
def notch(raw_eeg_filter):
    raw_eeg_filter.notch_filter(freqs=[50, 100])
    #raw_eeg_filter.compute_psd().plot()

# BANDSTOP
def bandstop(raw_eeg_filter):
    raw_eeg_filter.filter(l_freq=55, h_freq=45, method='iir')
    #raw_eeg_filter.compute_psd().plot()

# BANDPASS
def bandpass(raw_eeg_filter):
    raw_eeg_filter.filter(l_freq=1,h_freq=40,method = 'fir',fir_window = 'hamming')
    #raw_eeg_filter.compute_psd().plot()

# ARTIFACT DETECTION - ICA
def ICA(raw_eeg_filter):
    ica = mne.preprocessing.ICA(n_components=20)
    filt_raw = raw_eeg_filter.copy().filter(1,None, verbose=False)
    ica.fit(filt_raw, verbose=False)
    ica
    
    explained_var_ratio = ica.get_explained_variance_ratio(filt_raw)
    for channel_type, ratio in explained_var_ratio.items():
        print(f"Fraction of {channel_type} variance explained by all components: {ratio}")
    
    # plot
    raw_eeg_filter.load_data()
    #ica.plot_sources(raw_eeg_filter, show_scrollbars=True)
    #ica.plot_components()

    # automated exclusion
    ic_labels = label_components(raw_eeg_filter, ica, method="iclabel")
    y_pred = ic_labels['y_pred_proba']
    labels = ic_labels['labels']

    for i in range(len(labels)):
        print(f'channel {i}: {labels[i]}, {y_pred[i]}')

    exclude = []
    for i in range(len(labels)):
        if labels[i] == 'eye blink' or labels[i] == 'muscle artifact':
            exclude.append(i)
            
    ica.exclude = exclude
    reconstructed_raw = ica.apply(raw_eeg_filter.copy())
    
    return reconstructed_raw

    
####################### connectivity pipeline ############################
from mne_connectivity import spectral_connectivity_epochs, viz

channels = ['fcue',
 'fdot',
 'ffix',
 'fisi',
 'fwrp',
 'hcue',
 'hdot',
 'hfix',
 'hisi',
 'hwrp',
 'scue',
 'sdot',
 'sfix',
 'sisi',
 'swrp']

# copy of data
def connectivity_copy(i):
    connectivity_raw = preprocessed_raw_arrays[i]
    return connectivity_raw

# find events
def find_connectivity_events():
    all_events = mne.find_events(connectivity_raw, stim_channel=channels)
    return all_events

####### look at hcue

#hcue_events = mne.find_events(connectivity_raw, stim_channel=['hcue'])
#hcue_epochs = mne.Epochs(connectivity_raw, hcue_events, picks='eeg')
#hcue_epochs.get_data()
#hcue_epochs.plot()
#hcue_epochs.compute_psd().plot()


####### look at scue
#scue_events = mne.find_events(connectivity_raw, stim_channel=['scue'])
#scue_epochs = mne.Epochs(connectivity_raw, scue_events, picks='eeg')
#scue_epochs.get_data()
#scue_epochs.plot()
#scue_epochs.compute_psd().plot()


# get epochs 
def get_channel_epochs(connectivity_raw, channel):
    channel_events = mne.find_events(connectivity_raw, stim_channel=[channel])
    channel_epochs = mne.Epochs(connectivity_raw, channel_events, picks='eeg')
    channel_epochs.get_data()
    #channel_epochs.plot()
    #channel_epochs.compute_psd().plot()
    return channel_events, channel_epochs
    

# connectivity
def get_connectivity(title, fmin, fmax, cue_epochs, connectivity_methods):
    
    con_epochs = spectral_connectivity_epochs(
        cue_epochs, method=connectivity_methods, mode='fourier', fmin=fmin, fmax=fmax, 
        tmin=0, tmax=1,  # Time window (seconds)
        faverage=True  # Average over the frequency band
    )
    
    if len(connectivity_methods) <= 1:
        ######## plotting for 1
        conn = con_epochs.get_data(output="dense") #(128, 128, 1)
        conn.shape
        # Drop the third dimension (since it's size 1)
        con_2d = conn[:, :, 0]  # Shape will now be (128, 128)
        
        # plot
        #plt.figure(figsize=(10, 8))
        #plt.imshow(con_2d, cmap='jet', origin='lower', aspect='auto')
        #plt.colorbar(label='Coherence')
        #plt.title(f'Connectivity Matrix - {title}')
        #plt.xlabel('Channels')
        #plt.ylabel('Channels')
        return con_2d
        
    else:
        ######## plotting for 2
        for c in range(n_con_methods):
            con_epochs_array[c] = con_epochs[c].get_data(output="dense")
    
        fig, ax = plt.subplots(1, n_con_methods, figsize=(6 * n_con_methods, 6))
        for c in range(n_con_methods):
           # Plot with imshow
           con_plot = ax[c].imshow(con_epochs_array[c, :, :], cmap="binary", vmin=0, vmax=1)
           # Set title
           ax[c].set_title(connectivity_methods[c])
           # Add colorbar
           fig.colorbar(con_plot, ax=ax[c], shrink=0.7, label="Connectivity")
           # Fix labels
           ax[c].set_xticks(range(len(eeg_ch_names)))
           ax[c].set_xticklabels(eeg_ch_names)
           ax[c].set_yticks(range(len(eeg_ch_names)))
           ax[c].set_yticklabels(eeg_ch_names)
           print(
               f"Connectivity method: {connectivity_methods[c]}\n"
               + f"{con_epochs_array[c,:,:,foi]}"
           )
    return con_epochs_array

####################### connectivity pipeline ends ##########################
connectivity_methods = ["plv"] #wpli"
n_freq_bands = len(freqs)
n_con_methods = len(connectivity_methods)
n_channels = len(eeg_ch_names)


    

####################### overall pipeline ##########################
directory_path = "/Volumes/Work/EEG_128channels_ERP_lanzhou_2015"

for filename in os.listdir(directory_path):
    if filename[:2] == '._' or filename == 'External HD':
        continue
    
    file_path = os.path.join(directory_path, filename)
    
    # create numpy array to store
    dtype = [
        ('subject_id', 'U50'),   # String type, up to 50 characters
        ('subject_group', 'U50'),       # String type for stimulus
        ('pre_ICA', 'O'),              # Object type for ICA (which can be a numpy array or similar object)
        ('post_ICA', 'O'),              # Object type for ICA (which can be a numpy array or similar object)
        ('events', 'O'),             # Object type for events (timestamps or event markers)
        ('epochs', 'O'),              # Object type for epochs (e.g., a list of EEG data segments)
        ('connectivity', 'O')]
    
    # go through pipeline
    subject_id, subject_group = get_subject_info(filename)
    
    
    
    raw = read_data(file_path)
    raw_eeg = clean_channels(raw)
    raw_eeg_filter = create_copy(raw_eeg)
    notch(raw_eeg_filter)
    bandstop(raw_eeg_filter)
    bandpass(raw_eeg_filter)
    
    pre_ICA = raw_eeg_filter.copy()

    reconstructed_raw = ICA(raw_eeg_filter)
    post_ICA = reconstructed_raw.copy()
    
    # events, connectivity ....
    connectivity_raw = reconstructed_raw.copy()
    
    hcue_events, hcue_epochs = get_channel_epochs(connectivity_raw, 'hcue')
    scue_events, scue_epochs = get_channel_epochs(connectivity_raw, 'scue')
    
    events = {'hcue': hcue_events, 'scue': scue_events}
    epochs = {'hcue': hcue_epochs, 'scue': scue_epochs}
    
    hcue_connectivity = get_connectivity('title', freqs['alpha'][0], freqs['alpha'][1], hcue_epochs, connectivity_methods)
    scue_connectivity = get_connectivity('title', freqs['alpha'][0], freqs['alpha'][1], scue_epochs, connectivity_methods)
    
    connectivity = {'hcue': hcue_connectivity, 'scue': scue_connectivity}
    
    data = np.array([(subject_id, subject_group, pre_ICA, post_ICA, events, epochs, connectivity)], dtype=dtype)
    
    new_filepath = f'/Volumes/Work/modma_data/{subject_id}_{subject_group}'
    os.makedirs(os.path.dirname(new_filepath), exist_ok=True)
    np.save(new_filepath, data)

    
    

    
    
    
array = np.load('/Volumes/Work/modma_data/02010021_MDD.npy', allow_pickle=True)


print(events = (array['events']))
epochs = (array['epochs'])
connectivity = (array['connectivity'])

    
    
    
