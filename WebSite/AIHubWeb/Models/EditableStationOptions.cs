/**
 * AppOptions.cs
 * By: John Symborski
 * Capstone Group 2
 * Model of the various app options you can pick
 * */

using System;
using System.Collections.Generic;
using System.Text;

namespace AIHubWeb
{
    public class EditableStationOptions
    {
        public bool useWifiOnly { set; get; }
        public TimeSpan pollingFequency { set; get; }

        public EditableStationOptions( bool wifiOnly, TimeSpan pollFreq)
        {
            useWifiOnly = wifiOnly;
            pollingFequency = pollFreq;
        }
        
    }
}
