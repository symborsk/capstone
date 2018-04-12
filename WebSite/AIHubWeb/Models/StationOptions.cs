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

namespace AIHubWeb
{
    public class StationOptions : TableEntity
    {
        public double polling_frequency { set; get; }
        public string email_address { set; get; }
        public string cellular_backup_ro { set; get; }
        public double battery_temp_ro { set; get; }

        //We need this for TableEntity.... it how azure storage interacts with it
        public StationOptions() { }

        //This creation of the object if all is known about it
        public StationOptions(string stationName, string cellBack, int pollFreq, string email, double temp)
        {
            this.PartitionKey = stationName;
            this.RowKey = stationName;
            polling_frequency = pollFreq;
            email_address = email;
            battery_temp_ro = temp;
            cellular_backup_ro = cellBack;
        }

        //This is creation of object with the defaults 1 hour and no 3G
        public StationOptions(string stationName)
        {
            this.PartitionKey = stationName;
            this.RowKey = stationName;
            polling_frequency = 60;
            email_address = "No Entered Email";
            cellular_backup_ro = "false";
            battery_temp_ro = 20.2;
        }
    }
}
