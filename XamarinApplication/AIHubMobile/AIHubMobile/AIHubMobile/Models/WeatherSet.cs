using System;
using System.Collections.Generic;
using System.Text;

namespace AIHubMobile
{
    public class WeatherSet
    {
        public long StationId { get; set; }
        public DateTime RecordedTime { get; set; }
        public int Temperature { get; set; }
        public int Humidity { get; set; }
        public int Visibility { get; set; }
        public int Acceleration { get; set; }
    }
}
