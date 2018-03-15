using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace AIHubWeb

{
    public class WeatherStation
    {
        public List<WeatherSet> rgWeatherSets { get; set; }
        public StationOptions statOptions { get; set; }
        public String StationName { get; set; }
        public LatLng latlng { get; set; }

        public DateTime latestTime
        {
            get
            {
                return GetLatestDate();
            }
    
        }
        
        public WeatherStation(string name, double lat, double lng)
        {   
            StationName = name;
            latlng = new LatLng(lat, lng);
        }

        public WeatherStation(StationOptions givenStatOptions, long id, List<WeatherSet> sets)
        {    
            statOptions = givenStatOptions;
            rgWeatherSets = sets;
        }

        public void OrderListByDate()
        {
            //Sort by the Recorded time
           rgWeatherSets.Sort((x, y) => y.RecordedTime.CompareTo(x.RecordedTime));
        }

        public void AddWeatherSet(WeatherSet set)
        {
            if(rgWeatherSets == null)
            {
                rgWeatherSets = new List<WeatherSet>();
            }

            rgWeatherSets.Add(set);
            OrderListByDate();
        }

        public DateTime GetLatestDate()
        {
            if (rgWeatherSets == null || rgWeatherSets.Count == 0)
            {
                return new DateTime(1995, 1, 1);
            }

            
            return rgWeatherSets[0].RecordedTime;
        }


        public class LatLng
        {

            public LatLng(Double lat, Double lng)
            {
                Lat = lat;
                Lng = lng;
            }

            public double Lat
            {
                get;
                set;
            }
            public double Lng
            {
                get;
                set;
            }
        }
    }
}
