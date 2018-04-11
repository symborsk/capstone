/**
 * WeatherSet.cs
 * By: John Symborski
 * Capstone Group 2
 * Model of the weather set item
 * */

using System;
using System.Collections.Generic;
using System.Text;

namespace AIHubWeb
{
    public class WeatherSet
    {
        public WeatherSet()
        {

        }

        public DateTime RecordedTime { get; set; }

        //All of these are string as we are simply displaying them
        //This simplifies the downloading process from azure blob storage
        public string temperature { get; set; }
        public string humidity { get; set; }
        public string direction { get; set; }
        public string gust { get; set; }
        public string rain { get; set; }
        public string windSpeed { get; set; }
        public string pressure { get; set; }
        public string visibility { get; set; }

        //These are hardcoded values since 
        public string ai_one_hour_temperature { get; set; }
        public string ai_three_hour_temperature { get; set; }
        public string ai_24_hour_temperature { get; set; }

        public string ai_one_hour_humidity{ get; set; }
        public string ai_three_hour_humidity { get; set; }
        public string ai_24_hour_humidity { get; set; }

        public string ai_one_hour_wind { get; set; }
        public string ai_three_hour_wind { get; set; }
        public string ai_24_hour_wind { get; set; }

        public enum WeatherSetDateRanges
        {
            Today = 0,
            PastThreeDays = 1,
            PastWeek = 2,
            ThisMonth = 3,
            ThisYear = 4,
            AllTime = 5
        };

    }
}
