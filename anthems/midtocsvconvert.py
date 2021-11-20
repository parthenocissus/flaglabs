# Installing required packages.
# !pip3 install mido==1.2.9

# Importing required packages.
import os
import pandas as pd
import numpy as np
import mido
from mido import Message, MidiFile, MidiTrack

# Reading midi files from all dataset entries (all anthems) and checking arguments of different message types

dataset_path = "anthems/dataset/"

msgtypes = []
print(dataset_path)
for filename in os.listdir(dataset_path):
    mid = MidiFile(dataset_path + filename, clip=True)  # MidiFile object to manipulate with later
    # print(filename)

    dictionary = {
        "Country": [],  # country
        "Message Type": [],  # msg.type
        "Time": [],  # time - check where time means time, and where it means delta time!
        "Track Number": [],  # track number, i, the counter in the loop
        "Track Name": [],  # track_name, text
        "Channel": [], # channel, appears in channel_prefix, control change, note_on, note_off, pitchwheel, program_change; values: integer
        "Control": [],  # control_change
        "Control Value": [],  # control_change value
        "Instrument Name": [],  # instrument_name
        "Key Signature": [],  # key_signature
        "Marker Text": [],  # marker, text
        "Midi Port": [],  # midi_port
        "Note": [],  # value:
        "Velocity": [],  # note_on, note_off, value:
        "Pitch": [],  # pitchwheel, pitch
        "Program": [],  # program_change
        "Sequencer Data": [],  # sequencer_specific, data is a three value tuple? (0, 0, 65)
        "Tempo": [],  # set_tempo
        "smpte_offset": [],
        # smpte offset: make it to be a list! frame_rate, hours, minutes, seconds, frames, sub_frames,
        "Text": [],  # text
        "TS_numerator": [],  # time_signature, numerator
        "TS_denominator": [],  # time_signature, denominator
        "TS_clocks_per_click": [],  # time_signature, clocks_per_click
        "TS_32nd_notes_per_beat": [],  # time_signature, notated_32nd_notes_per_beat
        "End of Track": [],  # end_of_track, True or False
    }

    for i, track in enumerate(mid.tracks):

        print(mid)

        country = filename.split("_-_")[1].split(".")[0]

        if i == 0:
            track.name = "conductor"
        print("Track {}: {}".format(i, track.name))

        for msg in track:

            # this dictionary is a list of message types for now. change it to the list of arguments for every message type, figure out the encoding... 

            if msg.type == "channel_prefix":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(msg.channel)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)

            if msg.type == "control_change":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(None)
                dictionary["Control"].append(msg.control)
                dictionary["Control Value"].append(msg.value)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)

            if msg.type == "end_of_track":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(None)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(True)

            if msg.type == "instrument_name":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(None)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(msg.name)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(False)

            if msg.type == "key_signature":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(None)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(msg.key)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)

            if msg.type == "marker":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(None)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(msg.text)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)

            if msg.type == "note_on" or msg.type == "note_off":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(msg.channel)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(msg.note)
                dictionary["Velocity"].append(msg.velocity)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)  # this could be a problem...

            if msg.type == "pitchwheel":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(msg.channel)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(msg.pitch)
                dictionary["Program"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)

            if msg.type == "program_change":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(msg.channel)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(msg.program)
                dictionary["Sequencer Data"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)

            if msg.type == "sequencer_specific":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(None)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["Sequencer Data"].append(msg.data)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)

            if msg.type == "set_tempo":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(None)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Tempo"].append(msg.tempo)
                dictionary["Sequencer Data"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)

            if msg.type == "smpte_offset":
                smpte_offset_data = [msg.frame_rate, msg.hours, msg.minutes, msg.seconds, msg.frames, msg.sub_frames]

                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(None)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["smpte_offset"].append(smpte_offset_data)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)

            if msg.type == "text":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(None)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(msg.text)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)

            if msg.type == "time_signature":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(None)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(msg.numerator)
                dictionary["TS_denominator"].append(msg.denominator)
                dictionary["TS_clocks_per_click"].append(msg.clocks_per_click)
                dictionary["TS_32nd_notes_per_beat"].append(msg.notated_32nd_notes_per_beat)
                dictionary["End of Track"].append(None)

            if msg.type == "track_name":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(msg.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(None)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(None)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)

            if msg.type == "midi_port":
                dictionary["Country"].append(country)
                dictionary["Message Type"].append(msg.type)
                dictionary["Time"].append(msg.time)
                dictionary["Track Name"].append(track.name)
                dictionary["Track Number"].append(i)

                dictionary["Channel"].append(None)
                dictionary["Control"].append(None)
                dictionary["Control Value"].append(None)
                dictionary["Instrument Name"].append(None)
                dictionary["Key Signature"].append(None)
                dictionary["Marker Text"].append(None)
                dictionary["Midi Port"].append(msg.port)
                dictionary["Note"].append(None)
                dictionary["Velocity"].append(None)
                dictionary["Pitch"].append(None)
                dictionary["Program"].append(None)
                dictionary["Tempo"].append(None)
                dictionary["Sequencer Data"].append(None)
                dictionary["smpte_offset"].append(None)
                dictionary["Text"].append(None)
                dictionary["TS_numerator"].append(None)
                dictionary["TS_denominator"].append(None)
                dictionary["TS_clocks_per_click"].append(None)
                dictionary["TS_32nd_notes_per_beat"].append(None)
                dictionary["End of Track"].append(None)

    df = pd.DataFrame.from_dict(dictionary)
    print(df)
    # Save df to csv or json. 
    df.to_csv('D:\\flaglabs-master\\anthems\\csvdataset\\anthem_{}.csv'.format(country), index=False)
