using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace AIHubMobile
{
    public class WeatherStation
    {
        public List<WeatherSet> rgWeatherSets { get; set; }
        public StationOptions statOptions { get; set; }
        public long stationId { get; set; }
        
        public WeatherStation(StationOptions givenStatOptions, long id)
        {
            stationId = id;
            statOptions = givenStatOptions;
        }

        public WeatherStation(StationOptions givenStatOptions, long id, List<WeatherSet> sets)
        {
            stationId = id;
            statOptions = givenStatOptions;
            rgWeatherSets = sets;
        }

        public void OrderListByDate()
        {
            //Sort by the Recorded time
            rgWeatherSets.Sort((x, y) => x.RecordedTime.CompareTo(y.RecordedTime));
        }

        public void AddWeatherSet(WeatherSet set)
        {
            if(rgWeatherSets == null)
            {
                rgWeatherSets = new List<WeatherSet>();
            }

            rgWeatherSets.Add(set);
        }

        public DateTime GetLatestDate()
        {
            if (rgWeatherSets == null || rgWeatherSets.Count == 0)
            {
                return new DateTime(1995, 1, 1);
            }

            return rgWeatherSets[0].RecordedTime;
        }
    }
}
