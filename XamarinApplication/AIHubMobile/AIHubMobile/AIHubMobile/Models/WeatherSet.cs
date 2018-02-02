using System;
using System.Collections.Generic;
using System.Text;

namespace AIHubMobile
{
    public class WeatherSet
    {
        public WeatherSet(long statId, DateTime recordedTime, int temp, int hum, int vis, int acc)
        {
            StationId = statId;
            RecordedTime = recordedTime;
            Temperature = temp;
            Humidity = hum;
            Visibility = vis;
            Acceleration = acc;
        }

        public long StationId { get; set; }
        public DateTime RecordedTime { get; set; }
        public int Temperature { get; set; }
        public int Humidity { get; set; }
        public int Visibility { get; set; }
        public int Acceleration { get; set; }
    }
}
