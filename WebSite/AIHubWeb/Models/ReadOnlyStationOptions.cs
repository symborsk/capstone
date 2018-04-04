using System;
using System.Collections.Generic;
using System.Text;

namespace AIHubWeb
{
    public class ReadOnlyStationOptions
    {
        public ReadOnlyStationOptions(int battPer, int battTemp, bool on)
        {
            batteryPercentage = battPer;
            batteryTemperature = battTemp;
            isOn = on;
        }

        int batteryPercentage { set; get; }
        int batteryTemperature { set; get; }
        bool isOn { set; get; }
    }
}
