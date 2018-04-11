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
        public string notification_email { set; get; }
        public string cellular_backup { set; get; }
        public double  battery_temperature_ro { set; get; }

        //We need this for TableEntity.... it how azure storage interacts with it
        public StationOptions() { }

        //This creation of the object if all is known about it
        public StationOptions(string station_name, string cell_back, int pollFreq, string email, double temp)
        {
            this.PartitionKey = station_name;
            this.RowKey = station_name;
            polling_frequency = pollFreq;
            notification_email = email;
            battery_temperature_ro = temp;
            cellular_backup = cell_back;
        }
    }
}
