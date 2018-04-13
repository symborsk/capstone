/**
 * WeatherSet.cs
 * By: John Symborski
 * Capstone Group 2
 * Model of the weather set item
 * */

using System;

namespace AIHubWeb
{
    public class WeatherSet
    {
        public WeatherSet() { }

        public DateTime RecordedTime { get; set; }

        //All of these are string as we are simply displaying them
        //This simplifies the downloading process from azure blob storage
        private string temperature;
        public string Temperature
        {
            get
            {
                return this.temperature;
            }
            set
            {              
                if(value != null)
                {
                    string rounded = Double.Parse(value).ToString("N1");
                    this.temperature = string.Format("{0}°C", rounded);
                }
            }
        }

        private string humidity;
        public string Humidity
        {
            get
            {
                return this.humidity;
            }
            set
            {
                string rounded = Double.Parse(value).ToString("N1");
                this.humidity = string.Format("{0} %", rounded);
            }
        }


        private string direction;
        public string Direction
        {
            get
            {
                return this.direction;
            }
            set
            {
                this.direction = value;
            }
        }

        private string gust;
        public string Gust
        {
            get
            {
                return this.gust;
            }
            set
            {
                string rounded = Double.Parse(value).ToString("N1");
                this.gust = string.Format("{0} km/hr", rounded);
            }
        }

        private string rain;
        public string Rain
        {
            get
            {
                return this.rain;
            }
            set
            {
                string rounded = Double.Parse(value).ToString("N1");
                this.rain = string.Format("{0} mm", rounded);
            }
        }

        private string windSpeed;
        public string WindSpeed
        {
            get
            {
                return this.windSpeed;
            }
            set
            {
                string rounded = Double.Parse(value).ToString("N1");
                this.windSpeed = string.Format("{0} km/hr", rounded);
            }
        }

        private string pressure;
        public string Pressure
        {
            get
            {
                return this.pressure;
            }
            set
            {
                string rounded = Double.Parse(value).ToString("N1");
                this.pressure = string.Format("{0} kPa", rounded);
            }
        }

        private string visibility;
        public string Visibility
        {
            get
            {
                return this.visibility;
            }
            set
            {
                string rounded = Double.Parse(value).ToString("N2");
                this.visibility = string.Format("{0}", rounded);
            }
        }

        //These are hardcoded values since 
        public string ai_1_hour_temperature { get; set; }
        public string ai_4_hour_temperature { get; set; }
        public string ai_8_hour_temperature { get; set; }
        public string ai_12_hour_temperature { get; set; }
        public string ai_24_hour_temperature { get; set; }

        public string ai_1_hour_humidity { get; set; }
        public string ai_4_hour_humidity { get; set; }
        public string ai_8_hour_humidity { get; set; }
        public string ai_12_hour_humidity { get; set; }
        public string ai_24_hour_humidity { get; set; }

        public string ai_1_hour_wind { get; set; }
        public string ai_4_hour_wind { get; set; }
        public string ai_8_hour_wind { get; set; }
        public string ai_12_hour_wind { get; set; }
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
