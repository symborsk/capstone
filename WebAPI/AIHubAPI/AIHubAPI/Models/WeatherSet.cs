using System;
using System.Data.Entity.Core;
using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AIHubAPI.Models
{
    public class WeatherSet
    {
        [Required, Key]
        public long StationId { get; set; }

        [Required]
        public DateTime RecordedTime { get; set; }

        public int Temperature { get; set; }

        public int Humidity { get; set; }

        public int Visibility { get; set; }

        public int Acceleration { get; set; }
    }
}
