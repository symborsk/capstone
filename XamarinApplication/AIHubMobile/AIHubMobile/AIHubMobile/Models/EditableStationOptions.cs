/**
 * AppOptions.cs
 * By: John Symborski
 * Capstone Group 2
 * Model of the various app options you can pick
 * */

using System;
using System.Collections.Generic;
using System.Text;
using Microsoft.WindowsAzure.Storage.Table;

namespace AIHubMobile
{
    public class EditableStationOptions : TableEntity
    {
        public bool Use3G { set; get; }
        public int PollingFrequency { set; get; }

        //We need this for TableEntity.... it how azure storage interacts with it
        public EditableStationOptions() { }

        //This creation of the object if all is known about it
        public EditableStationOptions(string stationName, bool use3G, int pollFreq)
        {
            this.PartitionKey = "EditableStationOptions";
            this.RowKey = stationName;
            Use3G = use3G;
            PollingFrequency = pollFreq;
        }

        //This is creation of object with the defaults 1 hour and no 3G
        public EditableStationOptions(string stationName)
        {
            this.PartitionKey = "EditableStationOptions";
            this.RowKey = stationName;
            Use3G = false;
            PollingFrequency = 60;
        }
    }
}
